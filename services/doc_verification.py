import cv2
import pytesseract

def scan_document(image_path, document_type):
    # Load the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to enhance text visibility
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Use pytesseract to extract text
    extracted_text = pytesseract.image_to_string(thresh)

    # Depending on the document_type, extract relevant information
    if document_type == "aadhaar":
        # Use regex or other techniques to extract Aadhaar specific information
        # For demonstration, let's just return the extracted text
        return extracted_text
    elif document_type == "passport":
        # Use regex or other techniques to extract passport specific information
        # For demonstration, let's just return the extracted text
        return extracted_text
    # Similarly, handle other document types...

    # If document_type is not recognized
    return None
