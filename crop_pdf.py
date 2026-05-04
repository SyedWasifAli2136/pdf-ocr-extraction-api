import fitz  # PyMuPDF

def crop_pdf(input_pdf, output_pdf, crop_area):
    # Open the PDF
    document = fitz.open(input_pdf)

    # Define the area you want to crop (x0, y0, x1, y1)
    # For example, cropping a box from coordinates (50, 50) to (500, 500)
    rect = fitz.Rect(crop_area)

    # Loop through all pages and crop the area
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        page.set_cropbox(rect)  # Set crop box

    # Save the cropped PDF
    document.save(output_pdf)

# # Example usage
# input_pdf = "sample 3 COI (1).pdf"
# output_pdf = "cropped_output_15.pdf"
# crop_area = (0, 270, 600, 750)  # Crop box coordinates

# crop_pdf(input_pdf, output_pdf, crop_area)
