def burnout_check(hours):
    if hours > 10:
        return "⚠️ High burnout risk. Reduce workload."
    elif hours > 7:
        return "⚠️ Moderate stress. Take breaks."
    else:
        return "✅ Balanced routine."

def create_timetable(tasks, hours):
    schedule = f"Tasks: {tasks}\nPlanned study hours: {hours}"
    return schedule, burnout_check(hours)
