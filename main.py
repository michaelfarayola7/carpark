import cv2
import numpy as np
import cvzone
import pickle

# Load the video and parking positions
cap = cv2.VideoCapture('carPark.mp4')

with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)

# Corrected width and height for parking spots
width, height = 108, 48  # Example dimensions, adjust as needed


# Function to check each parking space
def checkParkingSpace(imgPro):
    spaceCounter = 0

    for pos in posList:
        x, y = pos

        imgCrop = imgPro[y:y + height, x:x + width]
        count = cv2.countNonZero(imgCrop)

        # Display count on the original image
        cvzone.putTextRect(img, str(count), (x, y + height - 2), scale=1, thickness=2, offset=0, colorR=(0, 0, 255))

        # Determine if space is free based on the count of non-zero pixels
        if count < 500:  # Threshold, adjust based on your analysis
            color = (0, 255, 0)  # Green for available
            thickness = 5
            spaceCounter += 1
        else:
            color = (0, 0, 255)  # Red for occupied
            thickness = 2

        cv2.rectangle(img, (x, y), (x + width, y + height), color, thickness)

    # Display the total number of free spaces
    cvzone.putTextRect(img, f'FREE {spaceCounter}/{len(posList)}', (450, 50), scale=2, thickness=5, offset=20,
                       colorR=(0, 200, 0))


while True:
    # Reset video to start if at the end
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, img = cap.read()
    if not success:
        break  # Break the loop if video ends or there's an error

    # Image preprocessing
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    # Check parking spaces
    checkParkingSpace(imgDilate)

    cv2.imshow('Image', img)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(6) & 0xFF == ord('q'):
        break

# Release resources and close windows
cap.release()
cv2.destroyAllWindows()
