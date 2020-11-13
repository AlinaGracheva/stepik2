import json

import phonenumbers
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, RadioField
from wtforms.fields.html5 import TelField
from wtforms.validators import InputRequired, ValidationError

goal_choices = []
with open("data.json", encoding="utf-8") as file:
    data_from_file = json.load(file)
goals = data_from_file.get("goals")
for goal in goals.values():
    goal_choices.append((goal, goal))


class IsPhone:
    """Не понимаю, почему не работает"""
    def __init__(self):
        self.message = "Invalid number"

    def __call__(self, form, field):
        try:
            phone = phonenumbers.parse(field.data)
            if not phonenumbers.is_valid_number(phone):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError(self.message)


class BookingForm(FlaskForm):
    clientName = StringField("Вас зовут", [InputRequired(message="Имя должно быть заполнено")])
    clientPhone = TelField("Ваш телефон", [InputRequired(message="Введите ваш номер телефона"), IsPhone()])
    clientWeekday = HiddenField()
    clientTime = HiddenField()
    clientTeacher = HiddenField()
    submit = SubmitField("Записаться на пробный урок")


class RequestForm(FlaskForm):
    goal = RadioField('Какая цель занятий?', choices=goal_choices, default="Для путешествий")
    time = RadioField('Сколько времени есть?', choices=[("1-2 часа в неделю", "1-2 часа в неделю"), ("3-5 часов в неделю", "3-5 часов в неделю"), ("5-7 часов в неделю", "5-7 часов в неделю"), ("7-10 часов в неделю", "7-10 часов в неделю")], default="1-2 часа в неделю")
    clientName = StringField("Вас зовут", [InputRequired(message="Имя должно быть заполнено")])
    clientPhone = TelField("Ваш телефон", [InputRequired(message="Введите ваш номер телефона")])
    submit = SubmitField("Найдите мне преподавателя")
