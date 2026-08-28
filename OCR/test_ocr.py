from ocr_reader import OCRReader


IMAGE_PATH = (
    r"C:\Users\DHARMESH SHARMA\OneDrive\Pictures\Camera Roll\WhatsApp Image 2026-08-27 at 3.14.04 PM.jpeg"
)


print(
    "\nHANDWRITTEN NOTES OCR TEST"
)

print(
    "=" * 60
)


reader = OCRReader()


text = reader.read_image(
    IMAGE_PATH
)


print(
    "\nEXTRACTED TEXT"
)

print(
    "=" * 60
)

print(
    text
)