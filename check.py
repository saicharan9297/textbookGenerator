from openai import OpenAI
from fpdf import FPDF
import os

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",  # Replace with your real one
)

topic = input("Enter topic: ")
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
    extra_headers={
        "HTTP-Referer": "http://localhost/",
        "X-Title": "TextbookGenerator"
    }
)

# Extract output
try:
    output = completion.choices[0].message.content
    print("🔎 Output Preview:\n", output[:300])  # Print first few lines
except Exception as e:
    print("❌ Failed to get output:", e)
    exit()

# Save to PDF
def clean_text(text):
    return text.encode('latin-1', 'replace').decode('latin-1')

output_clean = clean_text(output)
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font("Arial", size=12)

for line in output_clean.split('\n'):
    pdf.multi_cell(0, 10, line)

filename = f"{topic}.pdf"
pdf.output(filename)
print(f"✅ PDF generated: {filename}")
