import io
import requests
from pypdf import PdfReader

# Paste your PDF link here
url = "https://www.alexandergilmore.com/wp-content/uploads/2022/08/14_Nation_-10000Headwords.pdf"

print("Downloading PDF from link...")
response = requests.get(url)
pdf_file = io.BytesIO(response.content)

print("Extracting text...")
reader = PdfReader(pdf_file)
text = ""
for i, page in enumerate(reader.pages):
  extracted = page.extract_text()
  if extracted:
    text += extracted + "\n"

# Save the extracted text to a local txt file
with open("words.txt", "w", encoding="utf-8") as f:
  f.write(text)

print("Done! Saved as words.txt")