from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime

def calculate_priority(task):
    today = datetime.today().date()
    due = datetime.strptime(task['due_date'], "%Y-%m-%d").date()
    days_left = (due - today).days

    urgency = 10 if days_left <= 0 else max(1, 10 - days_left)
    importance = task.get('importance', 5)
    effort = task.get('estimated_hours', 5)

    score = (urgency * 0.4) + (importance * 0.4) + (10 - effort) * 0.2
    return round(score, 1)

@api_view(['POST'])
def prioritize_tasks_api(request):
    try:
        tasks = request.data

        for task in tasks:
            task["priority_score"] = calculate_priority(task)

        sorted_tasks = sorted(tasks, key=lambda x: x["priority_score"], reverse=True)

        return Response({"tasks": sorted_tasks})
    except Exception as e:
        return Response({"error": str(e)}, status=500)
