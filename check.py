from openai import OpenAI

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)

completion = client.chat.completions.create(
  extra_headers={
    "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
    "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
  },
  extra_body={},
  model="tngtech/deepseek-r1t2-chimera:free",
  messages=[
    {
      "role": "user",
      "content": "the topic is about the sport volleyball. i the description a the volleyball aas a chapter and first it should ahave Chapter-wise content ,Summaries, MCQs with options + correct answer"
    }
  ]
)
from fpdf import FPDF

# Assume this is your response content from the API
output = completion.choices[0].message.content

# Function to clean text by replacing unsupported characters
def clean_text(text):
    return text.encode('latin-1', 'replace').decode('latin-1')

# Clean the output string
output_clean = clean_text(output)

# Create a PDF class instance
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font("Arial", size=12)

# Write each line to the PDF safely
for line in output_clean.split('\n'):
    pdf.multi_cell(0, 10, line)

# Save the PDF
pdf.output("volleyball_content.pdf")