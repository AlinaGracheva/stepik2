import json


def add_goal(goal_id, goal, goal_pic, *teachers_id):
    with open("data.json", encoding="utf-8") as file:
        data = json.load(file)
    data.get("goals")[goal_id] = goal
    data.get("goals_items")[goal] = goal_pic
    teachers_id = set(teachers_id)
    for teacher in data.get("teachers"):
        if teacher["id"] in teachers_id:
            teacher["goals"].append(goal_id)
    with open("data.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False)


add_goal("programming", "Для программирования", "🏢", 8, 9, 10, 11)
