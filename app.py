import json
import random

from flask import Flask, render_template, abort, redirect

import Forms

app = Flask(__name__)
app.config["SECRET_KEY"] = str(random.randint(1, 10000))


@app.route('/')
def main_view():
    with open("data.json", encoding="utf-8") as file:
        data_from_file = json.load(file)
    goals_items = data_from_file.get("goals_items")
    goals = data_from_file.get("goals")
    all_teachers = data_from_file.get("teachers")
    random.shuffle(all_teachers)
    teachers_for_main = all_teachers[0:6]
    return render_template("index.html", goals=goals, goals_items=goals_items, teachers=teachers_for_main)


@app.route('/goals/<goal>/')
def goals_view(goal):
    with open("data.json", encoding="utf-8") as file:
        data_from_file = json.load(file)
    if goal not in data_from_file.get("goals"):
        abort(404)
    teachers_for_goal = []
    for teacher in data_from_file.get('teachers'):
        if goal in set(teacher["goals"]):
            teachers_for_goal.append(teacher)
    its_goal = data_from_file.get("goals")[goal]
    item_for_goal = data_from_file.get("goals_items")[its_goal]
    return render_template("goal.html", teachers=teachers_for_goal, its_goal=its_goal, item_for_goal=item_for_goal)


@app.route('/profiles/<int:teacher_id>/')
def teachers_profile_view(teacher_id):
    with open("data.json", encoding="utf-8") as file:
        data_from_file = json.load(file)
    day_of_the_week = data_from_file.get("days")
    teacher = None
    for item in data_from_file.get('teachers'):
        if item.get("id") == teacher_id:
            teacher = item.copy()
            break
    if teacher is None:
        abort(404)
    return render_template("profile.html", teacher=teacher, day_of_the_week=day_of_the_week)


@app.route('/request/', methods=["POST", "GET"])
def request_view():
    form = Forms.RequestForm()
    if form.validate_on_submit():
        return redirect('/request_done/')
    return render_template("request.html", form=form)


@app.route('/request_done/', methods=["POST"])
def request_done_view():
    form = Forms.RequestForm()
    goal = form.goal.data
    time = form.time.data
    name = form.clientName.data
    phone = form.clientPhone.data
    with open("request.json", encoding="utf-8") as file:
        request_data = json.load(file)
    request_data.append({"goal": goal, "study_hours": time, "phone": phone, "name": name})
    with open("request.json", "w", encoding="utf-8") as file:
        json.dump(request_data, file, ensure_ascii=False)
    return render_template("request_done.html", form=form, goal=goal, time=time, name=name, phone=phone)


@app.route('/booking/<int:teacher_id>/<day>/<time>/', methods=["POST", "GET"])
def booking_view(teacher_id, day, time):
    form = Forms.BookingForm()
    if form.validate_on_submit():
        return redirect('/booking_done/')
    with open("data.json", encoding="utf-8") as file:
        data_from_file = json.load(file)
    teacher = None
    for item in data_from_file.get('teachers'):
        if item.get("id") == teacher_id:
            teacher = item.copy()
            break
    if teacher is None:
        abort(404)
    day_of_the_week = data_from_file.get("days")
    time = time.replace("&", ":")
    return render_template("booking.html", form=form, teacher_id=teacher_id, day=day, teacher=teacher, day_of_the_week=day_of_the_week, time=time)


@app.route('/booking_done/', methods=['POST'])
def booking_done_view():
    with open("data.json", encoding="utf-8") as file:
        data_from_file = json.load(file)
    form = Forms.BookingForm()
    client_name = form.clientName.data
    client_phone = form.clientPhone.data
    client_weekday = form.clientWeekday.data
    client_time = form.clientTime.data
    client_teacher = form.clientTeacher.data
    day = data_from_file.get("days")[client_weekday]
    with open("booking.json", encoding="utf-8") as file:
        booking_data = json.load(file)
    booking_data.append({"teacher_id": client_teacher, "day": client_weekday, "time": client_time, "phone": client_phone, "name": client_name})
    with open("booking.json", "w", encoding="utf-8") as file:
        json.dump(booking_data, file, ensure_ascii=False)
    return render_template("booking_done.html", day=day, time=client_time, clientName=client_name, clientPhone=client_phone)


@app.route('/profiles/')
def all_profiles_view():
    with open("data.json", encoding="utf-8") as file:
        data_from_file = json.load(file)
    all_teachers = data_from_file.get("teachers")
    goals_items = data_from_file.get("goals_items")
    goals = data_from_file.get("goals")
    return render_template("all_profiles.html", goals=goals, goals_items=goals_items, teachers=all_teachers)

@app.errorhandler(404)
def render_not_found(error):
    return render_template('404_page.html')


if __name__ == '__main__':
    app.run()
