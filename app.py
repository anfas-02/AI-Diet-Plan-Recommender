# app.py
from flask import Flask, render_template, request, redirect, url_for, session
from utils import calculate_bmr, recommend_diet, EXTRA_SNACKS
import os

app = Flask(__name__)
# Use a constant secret key for dev; in production set via env var
app.secret_key = os.environ.get("FLASK_SECRET", "dev-secret-key-please-change")

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/diet', methods=['POST'])
def diet():
    name = request.form.get('name', 'User')
    age = int(request.form.get('age', 25))
    gender = request.form.get('gender', 'Male')
    weight = float(request.form.get('weight', 60.0))
    height = float(request.form.get('height', 170.0))
    goal = request.form.get('goal', 'Maintain')

    bmr = calculate_bmr(weight, height, age, gender)
    plan = recommend_diet(goal, bmr)

    # store plan and user data in session for later pages
    session['name'] = name
    session['plan'] = plan
    session['bmr'] = round(bmr)
    session['goal'] = goal
    # reset selected snacks
    session.pop('selected_snacks', None)

    return render_template('result.html', name=name, plan=plan, bmr=round(bmr), goal=goal)

@app.route('/snacks', methods=['GET', 'POST'])
def snacks():
    """
    Show extra snack options and accept selections.
    """
    snacks = EXTRA_SNACKS
    if request.method == 'POST':
        selected = request.form.getlist('snack')  # names of selected snacks
        # compute calories for selected
        selected_items = []
        for s in snacks:
            if s['name'] in selected:
                selected_items.append(s)
        # store selected snack names in session
        session['selected_snacks'] = [s['name'] for s in selected_items]
        session['selected_snacks_cal'] = sum(s['calories'] for s in selected_items)
        return redirect(url_for('summary'))
    return render_template('snacks.html', snacks=snacks)

@app.route('/summary', methods=['GET'])
def summary():
    plan = session.get('plan')
    if not plan:
        return redirect(url_for('index'))

    name = session.get('name', 'User')
    selected_names = session.get('selected_snacks', [])
    selected_cal = session.get('selected_snacks_cal', 0)

    # total = meals total (from plan) + extras
    base_meal_total = plan.get('total', 0)
    adjusted_total = base_meal_total + selected_cal

    # pass everything to template
    return render_template(
        'summary.html',
        name=name,
        plan=plan,
        total=adjusted_total,
        selected_snacks=selected_names
    )

if __name__ == '__main__':
    app.run(debug=True)
