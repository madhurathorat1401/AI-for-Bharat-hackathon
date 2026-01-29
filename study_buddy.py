from pypdf import PdfReader
import openai

def extract_text(pdf):
    reader = PdfReader(pdf)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text

def study_ai(content, question, lang):
    lang_line = "Explain in simple Hindi." if lang == "hindi" else "Explain in simple Hinglish."

    prompt = f"""
    You are an AI study buddy for Indian students.
    {lang_line}

    Notes:
    {content}

    Question:
    {question}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
