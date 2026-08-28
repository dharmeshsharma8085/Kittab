from pdf_loader import extract_text_from_pdf

text = extract_text_from_pdf(
    r"C:\Users\DHARMESH SHARMA\Downloads\DSA_for_AI_Engineers.pdf"
)

print(text[:3000])