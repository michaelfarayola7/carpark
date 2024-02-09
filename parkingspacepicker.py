# import cv2
# import pickle
#
# width, height = (158-50), (240-192)
#
# try:
#     with open('CarParkPos', 'rb') as f:
#         posList = pickle.load(f)
# except:
#     posList = []
#
# def mouseClick(events, x, y, flags, params):
#     if events == cv2.EVENT_LBUTTONDOWN:
#         posList.append((x,y))
#     if events == cv2.EVENT_RBUTTONDOWN:
#         for i, pos in enumerate(posList):
#             x1,y1 = pos
#             if x1<x<x1+width and y1<y<y1+height:
#                 posList.pop(i)
#     with open('CarParkPos','wb') as f:
#         pickle.dump(posList,f)
#
# while True:
#     img = cv2.imread('carParkImg.png')
#     cv2.rectangle(img, (50,192), (158,240),(255,0,255),1)
#
#     for pos in posList:
#         cv2.rectangle(img, pos, (pos[0]+width, pos[1]+height), (255,0,255),2)
#     cv2.imshow('Image', img)
#
#     cv2.setMouseCallback('Image', mouseClick)
#
#     cv2.waitKey(1)
#
#
# img = cv2.imread('carParkImg.png')
# cv2.imshow('image',img)
# cv2.waitKey(0)

import cv2
import pickle

# Define the dimensions for the parking spot rectangles
width, height = (158-50), (240-192)  # Width and height calculated from specific points

# Attempt to load existing parking spot positions from a file
try:
    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []  # Initialize to an empty list if file doesn't exist or error occurs

# Function to handle mouse clicks
def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:  # Left click to add a parking spot
        posList.append((x, y))
    elif events == cv2.EVENT_RBUTTONDOWN:  # Right click to remove a parking spot
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)
                break
    with open('CarParkPos', 'wb') as f:  # Save the updated positions to a file
        pickle.dump(posList, f)

# Main loop to display the image and handle interactions
while True:
    img = cv2.imread('carParkImg.png')  # Load the image

    for pos in posList:  # Draw all parking spots
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)

    cv2.imshow('Image', img)  # Show the image with marked spots
    cv2.setMouseCallback('Image', mouseClick)  # Set the mouse click callback

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup: Release resources and close windows
cv2.destroyAllWindows()
