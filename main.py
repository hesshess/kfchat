import asyncio
import json
import os
import re
from pathlib import Path

import streamlit as st
from agents import (
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered,
    Runner,
)

from models import RestaurantCustomerContext
from my_agents.triage_agent import triage_agent


def configure_openai_api_key():
    api_key = st.secrets.get("OPENAI_API_KEY")
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
        return

    st.error("`.streamlit/secrets.toml`에 `OPENAI_API_KEY`를 설정해 주세요.")
    st.stop()

customer_context = RestaurantCustomerContext(
    name="Guest",
    tier="basic",
    phone="010-1234-5678",
)


def ensure_ui_state():
    if "restaurant_bot_chat_history" not in st.session_state:
        st.session_state["restaurant_bot_chat_history"] = []
    if "restaurant_bot_pending_handoffs" not in st.session_state:
        st.session_state["restaurant_bot_pending_handoffs"] = []


def inject_brand_styles():
    css_path = Path(__file__).parent / "styles" / "app.css"
    css = css_path.read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def render_brand_hero():
    st.markdown(
        """
        <section class="brand-hero">
            <h1 class="brand-title">KFChat</h1>
            <div class="stat-grid">
                <div class="stat-card">
                    <div class="stat-label">Today Pick</div>
                    <div class="stat-value">징거더블다운통다리 박스</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Order Style</div>
                    <div class="stat-value">박스 · 세트 · 치킨</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Reservation</div>
                    <div class="stat-value">1 to 6 Guests</div>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

def build_runner_input():
    runner_input = []
    for entry in st.session_state["restaurant_bot_chat_history"]:
        text = entry.get("text", "").strip()
        if not text:
            continue
        runner_input.append({"role": entry["role"], "content": text})
    return runner_input


def render_history():
    for entry in st.session_state["restaurant_bot_chat_history"]:
        with st.chat_message(entry["role"]):
            agent_label = entry.get("agent_label")
            if agent_label:
                st.caption(f"응답 에이전트: {agent_label}")
            if entry.get("text"):
                st.write(entry["text"])



def sanitize_assistant_text(text: str) -> str:
    cleaned = text.strip()

    if not cleaned:
        return cleaned

    json_prefix_pattern = re.compile(r"^\s*(\{.*?\})\s*", re.DOTALL)
    match = json_prefix_pattern.match(cleaned)
    if not match:
        return cleaned

    candidate = match.group(1)
    try:
        parsed = json.loads(candidate)
    except json.JSONDecodeError:
        return cleaned

    if not isinstance(parsed, dict):
        return cleaned

    known_keys = {"reason", "issue_type", "issue_description"}
    if not known_keys.intersection(parsed.keys()):
        return cleaned

    return cleaned[match.end():].lstrip()


def get_current_agent_status():
    pending_handoffs = st.session_state["restaurant_bot_pending_handoffs"]
    if pending_handoffs:
        current_agent = pending_handoffs[-1].get("agent_label", "Triage Agent")
        return f"{current_agent}가 현재 응대하고 있습니다."

    for entry in reversed(st.session_state["restaurant_bot_chat_history"]):
        if entry.get("role") == "assistant" and entry.get("agent_label"):
            current_agent = entry["agent_label"]
            return f"최근 응답은 {current_agent}가 담당했습니다."

    return "Triage Agent가 새로운 요청을 기다리고 있습니다."


async def run_restaurant_bot():
    with st.chat_message("assistant"):
        status_container = st.status("요청을 파악하는 중...", expanded=True)
        agent_placeholder = st.empty()
        text_placeholder = st.empty()
        response_text = ""
        responding_agent = "Triage Agent"
        st.session_state["restaurant_bot_pending_handoffs"] = []
        agent_placeholder.caption(f"응답 에이전트: {responding_agent}")

        try:
            stream = Runner.run_streamed(
                triage_agent,
                build_runner_input(),
                context=customer_context,
            )

            async for event in stream.stream_events():
                pending_handoffs = st.session_state["restaurant_bot_pending_handoffs"]
                if pending_handoffs:
                    visible_labels = [item["label"] for item in pending_handoffs]
                    responding_agent = pending_handoffs[-1].get(
                        "agent_label", responding_agent
                    )
                    agent_placeholder.caption(f"응답 에이전트: {responding_agent}")
                    status_container.update(label=visible_labels[-1], state="running")

                if event.type != "raw_response_event":
                    continue

                if event.data.type == "response.output_text.delta":
                    response_text += event.data.delta
                    text_placeholder.write(sanitize_assistant_text(response_text))
                elif event.data.type == "response.completed":
                    status_container.update(label="응답 완료", state="complete")
                    if response_text:
                        response_text = sanitize_assistant_text(response_text)
                        text_placeholder.write(response_text)
        except InputGuardrailTripwireTriggered as exc:
            info = exc.guardrail_result.output.output_info
            responding_agent = "Input Guardrail"
            response_text = (
                "저는 레스토랑 관련 질문에 대해서만 도와드리고 있어요. "
                "메뉴를 확인하거나, 예약하거나, 음식을 주문할 수 있어요."
                if getattr(info, "is_off_topic", False)
                else "불편한 표현은 도와드리기 어려워요. 메뉴, 주문, 예약, 불만 접수처럼 레스토랑 관련 내용으로 말씀해 주세요."
            )
            status_container.update(label="입력 가드레일 작동", state="complete")
            agent_placeholder.caption(f"응답 에이전트: {responding_agent}")
            response_text = sanitize_assistant_text(response_text)
            text_placeholder.write(response_text)
        except OutputGuardrailTripwireTriggered as exc:
            responding_agent = "Output Guardrail"
            response_text = (
                "죄송합니다. 더 정중하고 안전한 방식으로만 안내드릴 수 있어요. "
                "메뉴, 주문, 예약, 불만 해결과 관련된 내용으로 다시 말씀해 주세요."
            )
            status_container.update(label="출력 가드레일 작동", state="complete")
            agent_placeholder.caption(f"응답 에이전트: {responding_agent}")
            response_text = sanitize_assistant_text(response_text)
            text_placeholder.write(response_text)

        st.session_state["restaurant_bot_chat_history"].append(
            {
                "agent_label": responding_agent,
                "role": "assistant",
                "text": response_text,
                "handoffs": [],
            }
        )


st.set_page_config(page_title="kfchat", page_icon="🍗", layout="wide")
configure_openai_api_key()
ensure_ui_state()
inject_brand_styles()

render_brand_hero()
render_history()

prompt = st.chat_input("kfchat에 메뉴, 주문, 예약, 불만 접수를 요청해 보세요")

if prompt:
    st.session_state["restaurant_bot_chat_history"].append(
        {
            "role": "user",
            "text": prompt,
            "handoffs": [],
        }
    )
    with st.chat_message("user"):
        st.write(prompt)
    asyncio.run(run_restaurant_bot())

with st.sidebar:
    st.markdown("## kfchat")
    st.caption("현재 응대 상태")
    st.markdown("### Agent Status")
    st.write(get_current_agent_status())

    reset = st.button("대화 초기화")
    if reset:
        st.session_state["restaurant_bot_chat_history"] = []
        st.session_state["restaurant_bot_pending_handoffs"] = []
        st.rerun()
