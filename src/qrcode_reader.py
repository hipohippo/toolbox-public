import cv2
from qreader import QReader

# Create a QReader instance


def read_qr_code(image_path: str) -> str:
    # Get the image that contains the QR code
    image = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)
    qreader = QReader()
    # Use the detect_and_decode function to get the decoded QR data
    decoded_text = qreader.detect_and_decode(image=image)
    return decoded_text


if __name__ == "__main__":
    print(read_qr_code(r"../data/qrcode_test.png"))
