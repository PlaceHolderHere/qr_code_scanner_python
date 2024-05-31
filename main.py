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


def get_qr_data(given_frame):
    # Convert frame to grayscale
    gray = cv2.cvtColor(given_frame, cv2.COLOR_BGR2GRAY)

    # Use the pyzbar library to decode the QR code
    qr_codes = decode(gray)
    decrypted_text = None

    # Loop over all detected QR codes
    if len(qr_codes) > 0:
        # Decode QR code
        qr_data = qr_codes[0].data.decode("utf-8")

        # Decryption
        decrypted_text = ''
        for char in qr_data:
            i = key.index(char)
            decrypted_text += chars[i]

            # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        return decrypted_text, qr_codes[0].rect

    else:
        return None, None

# Decryption
chars = [' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?',
         '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a',
         'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w',
         'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
         'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
key = ['^', '(', 's', 'P', '?', "'", 'F', '0', '6', 'G', '#', '-', 'H', 'm', '`', 'R', 'K', 'T', '>', 'E', '[', 'W',
       '/', 'y', 'J', 'D', '_', 'n', 'h', 'I', 'S', '{', 'o', 'B', '2', 'V', '\\', ' ', '|', 'A', 'f', 'Y', 'i', '"',
       'M', 'a', 'd', '8', 'l', 'r', ']', '<', '}', '.', 'C', ',', 'v', 't', '4', 'j', 'w', 'x', 'q', ':', '7', 'z',
       '=', ';', 'U', 'b', '$', 'X', '&', 'Z', '*', 'O', 'g', '!', 'e', '9', '1', 'L', '~', '+', 'N', 'u', 'c', '3',
       'Q', '%', 'p', ')', '@', '5', 'k']
# Set the desired screen size
width, height = 1200, 1080

# Initialize the webcam with the desired screen size
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

output = None
running = True

while running:
    ret, frame = cap.read()

    # Reading Qr Code
    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    output = get_qr_data(frame)

    qr_is_scanned = False
    if output[0] is not None:
        my_cursor.execute(f'SELECT * FROM students WHERE student_id={output[0]}')
        result = my_cursor.fetchone()
        if result is not None:
            is_logged_in = result[5]
            qr_is_scanned = True
            
            if is_logged_in == 1:
                my_cursor.execute(f"UPDATE students SET logged_in = False WHERE student_id = {output[0]};")
                cv2.putText(frame, 'Scanned!', (250, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                            2)
                cv2.putText(frame, f"Logging In:", (150, 170), cv2.FONT_HERSHEY_SIMPLEX,
                            2, (0, 255, 0), 3)
                cv2.putText(frame, f"{result[1]} {result[2]}", (150, 290), cv2.FONT_HERSHEY_SIMPLEX,
                            3, (0, 255, 0), 5)

            else:
                my_cursor.execute(f"UPDATE students SET logged_in = True WHERE student_id = {output[0]};")
                cv2.putText(frame, 'Scanned!', (250, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                            2)
                cv2.putText(frame, f"Logging Out:", (150, 170), cv2.FONT_HERSHEY_SIMPLEX,
                            2, (0, 255, 0), 3)
                cv2.putText(frame, f"{result[1]} {result[2]}", (150, 290), cv2.FONT_HERSHEY_SIMPLEX,
                            3, (0, 255, 0), 5)
            my_database.commit()

        else:
            cv2.putText(frame, 'ERROR!', (250, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0),
                        5)
            cv2.putText(frame, 'Please Scan Again!', (250, 170), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255),
                        5)

    # Show Window
    cv2.imshow("QR Code Scanner", frame)

    # Quit
    if cv2.waitKey(1) & 0xFF == 27 or cv2.getWindowProperty("QR Code Scanner", cv2.WND_PROP_VISIBLE) < 1:
        running = False
        break

    if qr_is_scanned:
        time.sleep(1)

# Release the capture
cap.release()
cv2.destroyAllWindows()
