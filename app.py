from flask import Flask, request, send_file, render_template_string
from openai import OpenAI
from fpdf import FPDF
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENAI_API_KEY"),
    default_headers={
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
        "HTTP-Referer": "https://render.com/",
        "X-Title": "TextbookGenerator"
    }
)

HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
  <title>Textbook Generator</title>
</head>
<body>
  <h2>Enter a topic to generate your textbook:</h2>
  <form method="get" action="/generate">
    <input type="text" name="topic" required>
    <button type="submit">Generate PDF</button>
  </form>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_FORM)

@app.route("/generate")
def generate():
    topic = request.args.get("topic", "Artificial Intelligence")

    tot_content = f"""
    Generate structured textbook material for the topic "{topic}".

    Include the following:
    1. Chapter-wise breakdown (at least 5 chapters)
    2. Summary at the end of each chapter
    3. 3 MCQs at the end with 4 options each
    4. Clearly mark the correct answer for each MCQ

    Make the tone educational, clear, and concise.
    """

    completion = client.chat.completions.create(
        model="tngtech/deepseek-r1t2-chimera:free",
        messages=[{"role": "user", "content": tot_content}],
    )

    output = completion.choices[0].message.content

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.add_font("DejaVu", "", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", uni=True)
    pdf.set_font("DejaVu", size=12)

    for line in output.split("\n"):
        pdf.multi_cell(0, 10, line)

    filename = f"/tmp/{topic}.pdf"
    pdf.output(filename)

    return send_file(filename, as_attachment=True, download_name=f"{topic}.pdf")

