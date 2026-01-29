from flask import Flask, render_template, request
from study_buddy import extract_text, study_ai
from placement_ai import placement_path
from timetable_ai import create_timetable
import openai

app = Flask(__name__)

# default language
selected_lang = "hinglish"

@app.route("/", methods=["GET", "POST"])
def home():
    global selected_lang

    study_answer = ""
    placement_result = ""
    timetable = ""
    burnout = ""
    wellness_result = ""

    stress_level = ""
    stress_percent = 0
    stress_color = "green"

    if request.method == "POST":
        action = request.form.get("action")

        if action == "language":
            selected_lang = request.form["lang"]

        elif action == "study":
            pdf = request.files["pdf"]
            question = request.form["question"]
            text = extract_text(pdf)
            study_answer = study_ai(text, question, selected_lang)

        elif action == "placement":
            college = request.form["college"]
            branch = request.form["branch"]
            skills = request.form["skills"]
            placement_result = placement_path(college, branch, skills, selected_lang)

        elif action == "timetable":
            tasks = request.form["tasks"]
            hours = int(request.form["hours"])
            timetable, burnout = create_timetable(tasks, hours)

        elif action == "wellness":
            feeling = request.form["feeling"].lower()

            high = ["anxious", "panic", "burnout", "depressed", "overwhelmed", "hopeless"]
            medium = ["stress", "tired", "worried", "pressure", "confused"]

            score = 0
            for w in high:
                if w in feeling:
                    score += 2
            for w in medium:
                if w in feeling:
                    score += 1

            if score >= 4:
                stress_level = "High Stress"
                stress_percent = 90
                stress_color = "red"
            elif score >= 2:
                stress_level = "Moderate Stress"
                stress_percent = 60
                stress_color = "yellow"
            else:
                stress_level = "Low Stress"
                stress_percent = 30
                stress_color = "green"

            lang_line = "Reply in simple Hindi." if selected_lang == "hindi" else "Reply in calm Hinglish."

            prompt = f"""
            You are a supportive wellness assistant for Indian students.
            {lang_line}
            Give gentle advice for {stress_level}.
            """

            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )

            wellness_result = response.choices[0].message.content

    return render_template(
        "index.html",
        study_answer=study_answer,
        placement_result=placement_result,
        timetable=timetable,
        burnout=burnout,
        wellness_result=wellness_result,
        stress_level=stress_level,
        stress_percent=stress_percent,
        stress_color=stress_color,
        selected_lang=selected_lang
    )

if __name__ == "__main__":
    app.run(debug=True)
