import os
import sys
import shutil
import pytesseract
from PIL import Image
import fitz  

def extract_text_from_image(image_path):
    try:
        image = Image.open(image_path)
        return pytesseract.image_to_string(image)
    except Exception as e:
        return f"Error processing image: {e}"

def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        return "\n".join(page.get_text() for page in doc)
    except Exception as e:
        return f"Error processing PDF: {e}"

def create_upload_folder(file_path):
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    folder_path = os.path.join("uploads", base_name)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

def save_file_and_text(original_path, text, destination_folder):
    file_name = os.path.basename(original_path)
    destination_path = os.path.join(destination_folder, file_name)
    shutil.copy(original_path, destination_path)

    txt_file_path = os.path.join(destination_folder, "transcription.txt")
    with open(txt_file_path, "w", encoding="utf-8") as f:
        f.write(text)
    
    return destination_path, txt_file_path

def extract_and_save_text(file_path):
    if not os.path.exists(file_path):
        print("❌ File does not exist.")
        return

    ext = os.path.splitext(file_path)[1].lower()
    if ext in ['.png', '.jpg', '.jpeg', '.bmp', '.tiff']:
        text = extract_text_from_image(file_path)
    elif ext == '.pdf':
        text = extract_text_from_pdf(file_path)
    else:
        print("❌ Unsupported file type. Please use an image or PDF.")
        return

    folder = create_upload_folder(file_path)
    saved_file, txt_file = save_file_and_text(file_path, text, folder)

    print(f"✅ File copied to: {saved_file}")
    print(f"📝 Text transcription saved to: {txt_file}")


if __name__ == "__main__":
    extract_and_save_text(input())
