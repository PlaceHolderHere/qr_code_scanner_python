import mysql.connector
import time
import cv2
from pyzbar.pyzbar import decode

my_database = mysql.connector.connect(
    host='localhost',
    user='root',
    password='password',
    database='students'
)
# CURSOR, MUST HAVE
my_cursor = my_database.cursor()


def read_qr_code(given_frame):
    # Convert frame to grayscale
    gray = cv2.cvtColor(given_frame, cv2.COLOR_BGR2GRAY)

    # Use the pyzbar library to decode the QR code
    qr_codes = decode(gray)
    decrypted_text = None

    # Loop over all detected QR codes
    for qr_code in qr_codes:
        # Decode the QR code
        qr_data = qr_code.data.decode("utf-8")

        # Decrypting
        decrypted_text = ''
        for char in qr_data:
            i = key.index(char)
            decrypted_text += chars[i]

        # Extract the bounding box location of the QR code
        (x, y, w, h) = qr_code.rect

        # Draw a rectangle around the QR code
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Return Qr_data
        cv2.putText(frame, 'Scanned!', (250, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 5)
        cv2.putText(frame, f"Student id:{decrypted_text}", (150, 170), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 0), 5)

    # Show the frame
    cv2.imshow("QR Code Scanner", given_frame)
    return decrypted_text


# Decryption
chars = [' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
key = ['^', '(', 's', 'P', '?', "'", 'F', '0', '6', 'G', '#', '-', 'H', 'm', '`', 'R', 'K', 'T', '>', 'E', '[', 'W', '/', 'y', 'J', 'D', '_', 'n', 'h', 'I', 'S', '{', 'o', 'B', '2', 'V', '\\', ' ', '|', 'A', 'f', 'Y', 'i', '"', 'M', 'a', 'd', '8', 'l', 'r', ']', '<', '}', '.', 'C', ',', 'v', 't', '4', 'j', 'w', 'x', 'q', ':', '7', 'z', '=', ';', 'U', 'b', '$', 'X', '&', 'Z', '*', 'O', 'g', '!', 'e', '9', '1', 'L', '~', '+', 'N', 'u', 'c', '3', 'Q', '%', 'p', ')', '@', '5', 'k']

# Set the desired screen size
width, height = 1200, 1080

# Initialize the webcam with the desired screen size
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

output = None
running = True

while running:
    # Capture frame-by-frame
    ret, frame = cap.read()

    output = read_qr_code(frame)

    if cv2.waitKey(1) & 0xFF == 27 or cv2.getWindowProperty("QR Code Scanner", cv2.WND_PROP_VISIBLE) < 1:
        running = False
        break

    if output is not None:
        my_cursor.execute(f'SELECT * FROM students WHERE student_id={output}')
        result = my_cursor.fetchone()
        logged_in = result[-1]

        if logged_in == 1:
            my_cursor.execute(f"UPDATE students SET logged_in = False WHERE student_id = {output};")

        else:
            my_cursor.execute(f"UPDATE students SET logged_in = True WHERE student_id = {output};")

        my_cursor.execute(f'SELECT * FROM students WHERE student_id={output}')
        result = my_cursor.fetchone()
        print(result)
        my_database.commit()

        time.sleep(1)

    cv2.putText(frame, 'hallo', (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# Release the capture
cap.release()
cv2.destroyAllWindows()
