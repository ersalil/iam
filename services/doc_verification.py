import re
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
        aadhaar_info = extract_aadhaar_info(extracted_text)
        if aadhaar_info:
                # Insert extracted data into the database
                db.execute("INSERT INTO DocumentValue (document_type, document_data) VALUES (?, ?)",
                               ("aadhaar", str(aadhaar_info)))
                db.commit()
                return aadhaar_info
        return extracted_text
    
    elif document_type == "passport":
        passport_info = extract_passport_info(extracted_text)
        if passport_info:
                # Insert extracted data into the database
                db.execute("INSERT INTO DocumentValue (document_type, document_data) VALUES (?, ?)",
                               ("passport", str(passport_info)))
                db.commit()
                return passport_info
        # Use regex or other techniques to extract passport specific information
        # For demonstration, let's just return the extracted text
        return extracted_text
    # Similarly, handle other document types...
    else:
            return None
        
def extract_aadhaar_info(text):
    aadhaar_info = {}

    # Extract Aadhaar Number
    aadhaar_number_match = re.search(r'\d{12}', text)
    if aadhaar_number_match:
        aadhaar_info["aadhaar_number"] = aadhaar_number_match.group()
    
    # Extract Name
    name_match = re.search(r'Name:\s*(.*)', text, re.I)
    if name_match:
        aadhaar_info["aadhaar_name"] = name_match.group(1).strip()

    # Extract Gender
    gender_match = re.search(r'Gender:\s*(.*)', text, re.I)
    if gender_match:
        aadhaar_info["aadhaar_gender"] = gender_match.group(1).strip()
    
    # Extract Date of Birth
    dob_match = re.search(r'DOB:\s*(.*)', text, re.I)
    if dob_match:
        aadhaar_info["aadhaar_dob"] = dob_match.group(1).strip()
    
    # Extract Address (assuming address is multiline)
    address_match = re.search(r'Address:(.*?)(?=\n|$)', text, re.I | re.S)
    if address_match:
        aadhaar_info["aadhaar_address"] = address_match.group(1).strip()

    return aadhaar_info

def extract_passport_info(text):
    passport_info = {}

    # Extract Passport Number
    passport_number_match = re.search(r'Passport Number:\s*(.*)', text, re.I)
    if passport_number_match:
        passport_info["Passport Number"] = passport_number_match.group(1).strip()

    # Extract Name
    name_match = re.search(r'Name:\s*(.*)', text, re.I)
    if name_match:
        passport_info["Name"] = name_match.group(1).strip()
    
    # Extract Gender
    gender_match = re.search(r'Gender:\s*(.*)', text, re.I)
    if gender_match:
        passport_info["passport_gender"] = gender_match.group(1).strip()
    
    # Extract Date of Birth
    dob_match = re.search(r'DOB:\s*(.*)', text, re.I)
    if dob_match:
        passport_info["passport_dob"] = dob_match.group(1).strip()
    
    # Extract Nationality
    nationality_match = re.search(r'Nationality:\s*(.*)', text, re.I)
    if nationality_match:
        passport_info["passport_nationality"] = nationality_match.group(1).strip()
    
    # Extract Expiry Date
    expiry_date_match = re.search(r'Expiry Date:\s*(\d{2}/\d{2}/\d{4})', text)
    if expiry_date_match:
        passport_info["Expiry Date"] = expiry_date_match.group(1)

    # Add more patterns and logic to extract other Passport information as needed
    # Example: Date of Birth, Nationality, etc.

    return passport_info