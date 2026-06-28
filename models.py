from dataclasses import dataclass

from pydantic import BaseModel


@dataclass
class RestaurantCustomerContext:
    name: str
    tier: str = "basic"
    phone: str = "010-0000-0000"


class InputGuardRailOutput(BaseModel):
    is_off_topic: bool
    contains_inappropriate_language: bool
    reason: str


class RestaurantOutputGuardRailOutput(BaseModel):
    contains_unprofessional_tone: bool
    contains_internal_information: bool
    reason: str


class HandoffData(BaseModel):
    reason: str
    issue_type: str
    issue_description: str


MENU_CATEGORIES = [
    {
        "title": "박스",
        "subtitle": "Box",
        "items": [
            {"name": "징거더블다운통다리 박스", "price": "12,900원"},
            {"name": "칠리모짜징거통다리 박스", "price": "12,600원"},
            {"name": "업그레이비타워 박스", "price": "11,500원"},
            {"name": "치즈징거통다리 박스", "price": "11,000원"},
            {"name": "징거BLT 박스", "price": "11,000원"},
            {"name": "징거타워 박스", "price": "10,800원"},
            {"name": "칠리징거통다리 박스", "price": "10,600원"},
            {"name": "클래식징거통다리 박스", "price": "10,300원"},
            {"name": "징거 박스", "price": "9,800원"},
        ],
    },
    {
        "title": "세트",
        "subtitle": "Meal",
        "items": [
            {"name": "징거더블다운통다리 세트", "price": "11,000원 / 9,000원"},
            {"name": "칠리모짜징거통다리 세트", "price": "10,700원 / 8,700원"},
            {"name": "업그레이비타워 세트", "price": "9,600원 / 7,600원"},
            {"name": "치즈징거통다리 세트", "price": "9,100원 / 7,100원"},
            {"name": "징거타워 세트", "price": "8,900원 / 6,900원"},
            {"name": "칠리징거통다리 세트", "price": "8,700원 / 6,700원"},
            {"name": "클래식징거통다리 세트", "price": "8,400원 / 6,400원"},
            {"name": "징거 세트", "price": "7,900원 / 5,900원"},
            {"name": "갓양념치밥 세트", "price": "6,900원 / 4,900원"},
            {"name": "데리야끼켄치밥 세트", "price": "6,900원 / 4,900원"},
            {"name": "트위스터세트", "price": "6,200원 / 4,200원"},
            {"name": "커넬오리지널세트", "price": "5,900원 / 3,900원"},
        ],
    },
    {
        "title": "치킨",
        "subtitle": "Chicken",
        "items": [
            {
                "name": "핫크리스피치킨 / 오리지널치킨",
                "price": "8조각 23,800원 · 5조각 15,700원 · 3조각 9,600원 · 1조각 3,300원",
            },
            {
                "name": "핫크리스피통다리",
                "price": "8조각 24,600원 · 5조각 16,200원 · 3조각 9,900원 · 1조각 3,400원",
            },
            {"name": "핫크리스피통다리세트", "price": "3조각 12,100원"},
            {
                "name": "갓양념치킨",
                "price": "8조각 25,400원 · 5조각 16,700원 · 3조각 10,200원 · 1조각 3,500원",
            },
            {
                "name": "갓양념통다리",
                "price": "8조각 26,200원 · 5조각 17,200원 · 3조각 10,500원 · 1조각 3,600원",
            },
            {"name": "갓양념통다리세트", "price": "3조각 12,700원"},
        ],
    },
    {
        "title": "사이드",
        "subtitle": "Side",
        "items": [
            {"name": "텐더 4조각", "price": "5,900원"},
            {"name": "닭껍질튀김", "price": "3,500원"},
            {"name": "버터비스켓", "price": "2,600원"},
            {"name": "너겟 4조각", "price": "2,600원"},
            {"name": "매쉬포테이토 & 그레이비", "price": "2,900원"},
            {"name": "에그타르트", "price": "2,300원"},
            {"name": "코울슬로", "price": "2,100원"},
            {"name": "콘샐러드", "price": "2,100원"},
        ],
    },
    {
        "title": "소스",
        "subtitle": "Sauce",
        "items": [
            {"name": "그레이비 소스", "price": "700원"},
            {"name": "갓양념 소스", "price": "700원"},
            {"name": "스위트칠리소스", "price": "700원"},
            {"name": "스모키머스타드소스", "price": "700원"},
        ],
    },
    {
        "title": "음료",
        "subtitle": "Beverage",
        "items": [
            {"name": "탄산음료(M)", "price": "2,200원"},
            {"name": "아메리카노(M)", "price": "1,900원"},
            {"name": "초코", "price": "2,500원"},
            {"name": "오렌지주스", "price": "2,300원"},
        ],
    },
]


RESTAURANT_INFO = """
Restaurant Name: kfchat

Menu:
- Box:
  - Zinger Double Down Tong-dari Box: 12,900 KRW
  - Chili Mozza Zinger Tong-dari Box: 12,600 KRW
  - Upgravy Tower Box: 11,500 KRW
  - Cheese Zinger Tong-dari Box: 11,000 KRW
  - Zinger BLT Box: 11,000 KRW
  - Zinger Tower Box: 10,800 KRW
  - Chili Zinger Tong-dari Box: 10,600 KRW
  - Classic Zinger Tong-dari Box: 10,300 KRW
  - Zinger Box: 9,800 KRW
- Meal:
  - Zinger Double Down Tong-dari Meal: 11,000 / 9,000 KRW
  - Chili Mozza Zinger Tong-dari Meal: 10,700 / 8,700 KRW
  - Upgravy Tower Meal: 9,600 / 7,600 KRW
  - Cheese Zinger Tong-dari Meal: 9,100 / 7,100 KRW
  - Zinger Tower Meal: 8,900 / 6,900 KRW
  - Chili Zinger Tong-dari Meal: 8,700 / 6,700 KRW
  - Classic Zinger Tong-dari Meal: 8,400 / 6,400 KRW
  - Zinger Meal: 7,900 / 5,900 KRW
  - Sweet and Spicy Rice Bowl Meal: 6,900 / 4,900 KRW
  - Teriyaki Rice Bowl Meal: 6,900 / 4,900 KRW
  - Twister Meal: 6,200 / 4,200 KRW
  - Colonel Original Meal: 5,900 / 3,900 KRW
- Chicken:
  - Hot & Crispy Chicken / Original Recipe Chicken: 8 pcs 23,800 KRW, 5 pcs 15,700 KRW, 3 pcs 9,600 KRW, 1 pc 3,300 KRW
  - Hot & Crispy Tong-dari: 8 pcs 24,600 KRW, 5 pcs 16,200 KRW, 3 pcs 9,900 KRW, 1 pc 3,400 KRW
  - Hot & Crispy Tong-dari Meal: 3 pcs 12,100 KRW
  - Sweet & Spicy Chicken: 8 pcs 25,400 KRW, 5 pcs 16,700 KRW, 3 pcs 10,200 KRW, 1 pc 3,500 KRW
  - Sweet & Spicy Tong-dari: 8 pcs 26,200 KRW, 5 pcs 17,200 KRW, 3 pcs 10,500 KRW, 1 pc 3,600 KRW
  - Sweet & Spicy Tong-dari Meal: 3 pcs 12,700 KRW
- Side:
  - Tender 4 pcs: 5,900 KRW
  - Fried Chicken Skin: 3,500 KRW
  - Butter Biscuit: 2,600 KRW
  - Nugget 4 pcs: 2,600 KRW
  - Mashed Potato & Gravy: 2,900 KRW
  - Egg Tart: 2,300 KRW
  - Coleslaw: 2,100 KRW
  - Corn Salad: 2,100 KRW
- Sauce:
  - Gravy Sauce: 700 KRW
  - Sweet & Spicy Sauce: 700 KRW
  - Sweet Chili Sauce: 700 KRW
  - Smoky Mustard Sauce: 700 KRW
- Beverage:
  - Soda (M): 2,200 KRW
  - Americano (M): 1,900 KRW
  - Chocolate: 2,500 KRW
  - Orange Juice: 2,300 KRW

Allergy notes:
- Biscuit, burger, twister, and many box or set items may contain gluten.
- Cheese-based items may contain milk.
- Coleslaw and some sauces may contain egg.
- Fried products may share fryers.

Reservation policy:
- Reservations are accepted for 1 to 6 guests.
- Collect name, party size, date, time, and phone number.

Order policy:
- Orders can be dine-in or takeout.
- Confirm items, quantities, and special requests before finalizing.
"""
