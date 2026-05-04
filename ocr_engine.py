import os
import json
from paddleocr import PaddleOCR
from pdf2image import convert_from_path

def allowed_file(filename):
    """Check if the file type is allowed."""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_image(image_path):
    """Extract text from an image file using PaddleOCR."""
    ocr = PaddleOCR(use_angle_cls=True, lang='en')  # Specify language for OCR
    result = ocr.ocr(image_path, cls=True)
    text = '\n'.join([line[1][0] for line in result[0]])  # Extract recognized text
    return text

def extract_text_from_pdf(pdf_path):
    """Convert PDF to images and extract text from each page using PaddleOCR."""
    images = convert_from_path(pdf_path)
    text = ''
    for page_number, image in enumerate(images, start=1):
        text += f"\n--- Page {page_number} ---\n"
        # Save PIL image to a temporary file
        temp_image_path = f"temp_page_{page_number}.png"
        image.save(temp_image_path, "PNG")

        # Extract text from the image
        text += extract_text_from_image(temp_image_path)

        # Remove the temporary file
        os.remove(temp_image_path)
    return text

def process_file(file_path):
    """Extract raw text from the uploaded file."""
    if not allowed_file(file_path):
        raise ValueError("Invalid file type.")

    file_extension = file_path.rsplit('.', 1)[1].lower()
    if file_extension == 'pdf':
        return extract_text_from_pdf(file_path)
    else:
        return extract_text_from_image(file_path)

def process_files_in_directory(directory_path, output_directory):
    """Process all files in the specified directory and extract text."""
    extracted_text = {}

    # Ensure the output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)

        if os.path.isfile(file_path) and allowed_file(filename):
            try:
                # Extract raw text from each file
                raw_text = process_file(file_path)
                extracted_text[filename] = raw_text  # Store in dictionary by filename

                # Save the extracted text to the output directory
                output_file_path = os.path.join(output_directory, f"extracted_text_{filename}.txt")
                with open(output_file_path, "w", encoding="utf-8") as f:
                    f.write(raw_text)
                print(f"\nThe extracted text from {file_path} has been saved to {output_file_path}\n")

            except Exception as e:
                extracted_text[filename] = f"Error: {e}"
        else:
            print(f"Skipping non-file or unsupported file: {file_path}\n")
    
    return extracted_text

def save_extracted_texts(extracted_texts, save_path):
    """Save the dictionary of extracted texts to a file."""
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(extracted_texts, f, indent=4)
    print(f"\nThe extracted text dictionary has been saved to {save_path}\n")

if __name__ == "__main__":
    # Set the directory path where the files are located
    directory_path = "output_pdfs"  # Replace with your folder path
    output_directory = "extracted_texts"  # Folder to save the extracted text
    dictionary_save_path = "extracted_texts.json"  # File to save the dictionary

    if not os.path.exists(directory_path):
        print("Error: Directory not found.")
        exit(1)

    extracted_texts = process_files_in_directory(directory_path, output_directory)

    # Save the dictionary to a file
    save_extracted_texts(extracted_texts, dictionary_save_path)

    print("\nFinal Extracted Texts as Dictionary:")
    print(extracted_texts)
