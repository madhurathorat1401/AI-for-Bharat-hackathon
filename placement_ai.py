import openai

def placement_path(college, branch, skills, lang):
    lang_line = "Answer in simple Hindi." if lang == "hindi" else "Answer in Hinglish."

    prompt = f"""
    You are a career mentor for Indian students.
    {lang_line}

    College: {college}
    Branch: {branch}
    Skills: {skills}

    Create:
    - Skill gap analysis
    - 3 month roadmap
    - Free learning resources
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
