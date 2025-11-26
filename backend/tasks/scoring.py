from datetime import date, datetime

# Weight profiles used for scoring
WEIGHT_PROFILES = {
    "balanced":        {"urgency": 0.30, "importance": 0.30, "effort": 0.20, "dependencies": 0.20},
    "fastest_wins":    {"urgency": 0.15, "importance": 0.15, "effort": 0.50, "dependencies": 0.20},
    "high_impact":     {"urgency": 0.20, "importance": 0.50, "effort": 0.10, "dependencies": 0.20},
    "deadline_driven": {"urgency": 0.60, "importance": 0.20, "effort": 0.10, "dependencies": 0.10},
}


def _parse_due_date(value):
    """
    Convert string (e.g. '2025-01-05') or date -> datetime.date.
    Falls back to today if parsing fails.
    """
    if isinstance(value, date):
        return value

    if isinstance(value, str):
        for fmt in ("%Y-%m-%d", "%d-%m-%Y"):
            try:
                return datetime.strptime(value, fmt).date()
            except ValueError:
                continue

    return date.today()


def calculate_urgency(due_date_raw):
    """
    Higher when deadline is close or overdue.
    Returns value >= 0 (typically around 0–2+).
    """
    today = date.today()
    due = _parse_due_date(due_date_raw)
    delta_days = (due - today).days

    if delta_days < 0:
        # overdue => extra urgency
        return 1 + abs(delta_days) * 0.1

    return 1 / (1 + delta_days)


def calculate_effort_score(hours_raw):
    """
    Lower effort => higher score. Max hours capped at 40.
    """
    max_hours = 40.0
    try:
        hours = float(hours_raw)
    except (TypeError, ValueError):
        hours = 1.0

    return 1.0 - min(hours / max_hours, 1.0)


def calculate_dependency_score(task, all_tasks):
    """
    How many tasks are blocked by this one?
    Returns a fraction between 0 and 1.
    """
    task_id = task.get("id")
    if not task_id:
        return 0.0

    blocked_count = sum(
        1 for t in all_tasks
        if task_id in (t.get("dependencies") or [])
    )
    max_blocking = 5.0
    return min(blocked_count / max_blocking, 1.0)


def has_circular_dependency(task, all_tasks, visited=None, path=None):
    """
    Detect circular dependencies via DFS.
    """
    if visited is None:
        visited = set()
    if path is None:
        path = set()

    task_id = task.get("id")
    if not task_id:
        return False

    if task_id in path:
        return True
    if task_id in visited:
        return False

    visited.add(task_id)
    path.add(task_id)

    for dep_id in task.get("dependencies") or []:
        dep_task = next((t for t in all_tasks if t.get("id") == dep_id), None)
        if dep_task and has_circular_dependency(dep_task, all_tasks, visited, path):
            return True

    path.remove(task_id)
    return False


def calculate_priority(task, all_tasks, profile="balanced"):
    """
    Main priority score used by the API.
    Returns a numeric score in ~0–100 range.
    """
    weights = WEIGHT_PROFILES.get(profile, WEIGHT_PROFILES["balanced"])

    urgency = calculate_urgency(task.get("due_date"))
    importance = float(task.get("importance", 5)) / 10.0
    effort = calculate_effort_score(task.get("estimated_hours"))

    if has_circular_dependency(task, all_tasks):
        dep_frac = 0.0
    else:
        dep_frac = calculate_dependency_score(task, all_tasks)

    score = (
        weights["urgency"] * urgency +
        weights["importance"] * importance +
        weights["effort"] * effort +
        weights["dependencies"] * dep_frac
    )

    return round(score * 100.0, 1)


def calculate_scores(tasks, profile="balanced"):
    """
    Helper used by tests:
    - Accepts list of tasks
    - Returns NEW list sorted by priority_score (desc)
    - Includes priority_score and dependency_contribution
    """
    scored = []
    weights = WEIGHT_PROFILES.get(profile, WEIGHT_PROFILES["balanced"])

    for task in tasks:
        t = dict(task)  # copy to not mutate original

        urgency = calculate_urgency(t.get("due_date"))
        importance = float(t.get("importance", 5)) / 10.0
        effort = calculate_effort_score(t.get("estimated_hours"))

        if has_circular_dependency(t, tasks):
            dep_frac = 0.0
        else:
            dep_frac = calculate_dependency_score(t, tasks)

        raw_score = (
            weights["urgency"] * urgency +
            weights["importance"] * importance +
            weights["effort"] * effort +
            weights["dependencies"] * dep_frac
        )

        t["priority_score"] = round(raw_score * 100.0, 1)
        t["dependency_contribution"] = round(weights["dependencies"] * dep_frac * 100.0, 1)

        scored.append(t)

    scored.sort(key=lambda x: x["priority_score"], reverse=True)
    return scored
