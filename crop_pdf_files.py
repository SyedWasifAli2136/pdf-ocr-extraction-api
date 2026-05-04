import os
from crop_pdf import crop_pdf

def crop_multiple_pdfs(input_dir, output_dir):
    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            input_pdf = os.path.join(input_dir, filename)
            output_pdf = os.path.join(output_dir, f"cropped_{filename}")
            
            # Determine the crop area based on the file name prefix
            if filename.startswith("sample"):
                crop_area = (0, 0, 500, 600)  # Crop box for sample files
            elif filename.startswith("dual"):
                crop_area = (0, 270, 600, 750)  # Crop box for dual files
            else:
                print(f"Skipping file {filename}: No matching prefix.")
                continue  # Skip files without matching prefix
            
            # Apply cropping
            crop_pdf(input_pdf, output_pdf, crop_area)

# Example usage
input_dir = "sample_pdfs"  # Directory containing input PDFs
output_dir = "output_pdfs"  # Directory to save cropped PDFs

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

crop_multiple_pdfs(input_dir, output_dir)
