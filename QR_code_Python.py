# QR code using Python
#install pip install qrcode
from PIL import Image
import qrcode

# Create a QR code object with a larger size and higher error correction
qr = qrcode.QRCode(version=3, box_size=20, border=10, error_correction=qrcode.constants.ERROR_CORRECT_H)

# The data you want to encode in the QR code
# Define the vCard data
vcard = """BEGIN:VCARD
VERSION:4.0
FN:John Smith
ORG:Example Company
TITLE:CEO
TEL;TYPE=WORK,VOICE:(555) 555-5555
EMAIL;TYPE=PREF,INTERNET:john.smith@example.com
URL:https://www.example.com
END:VCARD"""


# Add the data to the QR code object
qr.add_data(data)

# Make the QR code
qr.make(fit=True)

# Create an image from the QR code with a black fill color and white background
img = qr.make_image(fill_color="black", back_color="white")

# Save the QR code image
img.save("qr_code_vcard.png")

img.open("qr_code_vcard.png")

# Open the logo or image file
logo = Image.open("logo.png")

# Resize the logo or image if needed
logo = logo.resize((50, 50))

# Position the logo or image in the center of the QR code
img_w, img_h = img.size
logo_w, logo_h = logo.size
pos = ((img_w - logo_w) // 2, (img_h - logo_h) // 2)

# Paste the logo or image onto the QR code
img.paste(logo, pos)

# Save the QR code image with logo or image
img.save("qr_code_with_logo.png")
