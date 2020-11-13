import json

import data

content = {"goals": data.goals, "goals_items": data.goals_items, "teachers": data.teachers, "days": dict(
    zip(data.teachers[0].get("free").keys(),
        ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]))}

with open("data.json", 'w', encoding="utf-8") as file:
    json.dump(content, file, ensure_ascii=False)
