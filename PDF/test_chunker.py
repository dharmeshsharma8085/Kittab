from pdf_loader import extract_text_from_pdf
from chunker import chunk_text


pdf_path = r"C:\Users\DHARMESH SHARMA\Downloads\DSA_for_AI_Engineers.pdf"

text = extract_text_from_pdf(pdf_path)

chunks = chunk_text(text)

print(f"Total characters: {len(text)}")
print(f"Total chunks: {len(chunks)}")

for i, chunk in enumerate(chunks[:3], start=1):
    print(f"\n{'=' * 50}")
    print(f"CHUNK {i}")
    print(f"{'=' * 50}")
    print(chunk)