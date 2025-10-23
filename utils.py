# utils.py
import random

# Main meals dataset (used by recommend_diet)
MEALS = [
    # Breakfast
    {"name": "Oats meal with Fruits", "calories": 300, "type": "breakfast"},
    {"name": "Eggs and Toast", "calories": 350, "type": "breakfast"},
    {"name": "Smoothie Bowl", "calories": 280, "type": "breakfast"},
    {"name": "Idli with Sambar", "calories": 320, "type": "breakfast"},
    {"name": "Poha with Vegetables", "calories": 330, "type": "breakfast"},
    {"name": "Upma with Coconut Chutney", "calories": 340, "type": "breakfast"},
    {"name": "Paneer Sandwich", "calories": 360, "type": "breakfast"},
    {"name": "Banana Pancakes", "calories": 380, "type": "breakfast"},
    {"name": "Paratha with Curd", "calories": 400, "type": "breakfast"},

    # Lunch
    {"name": "Grilled Chicken Salad", "calories": 400, "type": "lunch"},
    {"name": "Brown Rice with Vegetables", "calories": 450, "type": "lunch"},
    {"name": "Paneer Wrap", "calories": 420, "type": "lunch"},
    {"name": "Rajma Chawal", "calories": 500, "type": "lunch"},
    {"name": "Dal Tadka with Jeera Rice", "calories": 480, "type": "lunch"},
    {"name": "Veg Biryani with Raita", "calories": 520, "type": "lunch"},
    {"name": "Grilled Fish with Brown Rice", "calories": 530, "type": "lunch"},
    {"name": "Chicken Curry with Chapati", "calories": 550, "type": "lunch"},
    {"name": "Tofu Stir Fry with Noodles", "calories": 490, "type": "lunch"},

    # Snacks (common)
    {"name": "Fruit & Nuts Mix", "calories": 200, "type": "snack"},
    {"name": "Greek Yogurt", "calories": 180, "type": "snack"},
    {"name": "Protein Bar", "calories": 220, "type": "snack"},
    {"name": "Sprouts Salad", "calories": 150, "type": "snack"},
    {"name": "Peanut Butter Toast", "calories": 230, "type": "snack"},
    {"name": "Roasted Chana", "calories": 160, "type": "snack"},
    {"name": "Apple with Almonds", "calories": 190, "type": "snack"},
    {"name": "Boiled Eggs", "calories": 140, "type": "snack"},
    {"name": "Vegetable Sandwich", "calories": 210, "type": "snack"},

    # Dinner
    {"name": "Grilled Fish with Veggies", "calories": 500, "type": "dinner"},
    {"name": "Dal with Chapati", "calories": 480, "type": "dinner"},
    {"name": "Vegetable Soup with Bread", "calories": 450, "type": "dinner"},
    {"name": "Paneer Curry with Rice", "calories": 520, "type": "dinner"},
    {"name": "Mixed Veg Curry with Roti", "calories": 490, "type": "dinner"},
    {"name": "Chicken Stir Fry with Veggies", "calories": 530, "type": "dinner"},
    {"name": "Tofu Curry with Brown Rice", "calories": 510, "type": "dinner"},
    {"name": "Khichdi with Curd", "calories": 460, "type": "dinner"},
]

# Extra snacks list (same as we show on snacks page)
EXTRA_SNACKS = [
    {"name": "Chocolate Protein Bar", "calories": 250},
    {"name": "Almond Butter on Rice Cake", "calories": 200},
    {"name": "Cottage Cheese Cubes", "calories": 150},
    {"name": "Trail Mix with Seeds", "calories": 220},
    {"name": "Banana with Peanut Butter", "calories": 210},
    {"name": "Yogurt with Granola", "calories": 180},
    {"name": "Roasted Chana", "calories": 160},
    {"name": "Protein Shake (250ml)", "calories": 260}
]

def calculate_bmr(weight, height, age, gender):
    """
    Mifflin-St Jeor formula for BMR (returns kcal/day)
    weight: kg, height: cm, age: years
    """
    if gender.lower() == "male":
        return 10 * weight + 6.25 * height - 5 * age + 5
    else:
        return 10 * weight + 6.25 * height - 5 * age - 161

def safe_choice(meals, meal_type, max_cal):
    """Pick a meal of type with calorie constraint; fallback to any of that type."""
    options = [m for m in meals if m["type"] == meal_type and m["calories"] <= max_cal]
    if not options:
        options = [m for m in meals if m["type"] == meal_type]
    return random.choice(options)

def recommend_diet(goal, daily_calories):
    """
    Return a diet plan dict:
    - target: desired daily calories (based on goal)
    - breakfast/lunch/snack/dinner : chosen items
    - total: sum of chosen meals' calories
    """
    if goal.lower() == "weight loss":
        target_calories = max(1200, daily_calories - 500)
    elif goal.lower() == "weight gain":
        target_calories = daily_calories + 500
    else:
        target_calories = daily_calories

    breakfast = safe_choice(MEALS, "breakfast", target_calories * 0.30)
    lunch     = safe_choice(MEALS, "lunch",     target_calories * 0.35)
    snack     = safe_choice(MEALS, "snack",     target_calories * 0.10)
    dinner    = safe_choice(MEALS, "dinner",    target_calories * 0.25)

    total = breakfast["calories"] + lunch["calories"] + snack["calories"] + dinner["calories"]

    return {
        "target": round(target_calories),
        "total": total,
        "breakfast": breakfast,
        "lunch": lunch,
        "snack": snack,
        "dinner": dinner
    }
