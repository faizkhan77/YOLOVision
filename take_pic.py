# This is a Python code to take picture using OpenCV


# 1. Import Dependencies
"""need to import the OpenCV library (cv2) and optionally the os library to handle file paths.
uuid to give unique name to each images"""
import cv2
import os
import uuid
import time


# 2. Access the webcam (0 is usually the default camera)
"""use the VideoCapture method to access your webcam and capture an image."""
cap = cv2.VideoCapture(1)

# Give the camera some time to warm up
"""This gives the camera a couple of seconds to initialize properly before capturing the image."""
time.sleep(3)

# 3. Read a frame from the webcam
ret, frame = cap.read()

# 4. Release the webcam
cap.release()

# 5. Check if the frame was captured successfully
if ret:
    # 6. Display the captured frame in a window
    cv2.imshow("Captured Image", frame)

    # Wait for 2 seconds before closing the window automatically
    cv2.waitKey(2000)
    cv2.destroyAllWindows()

    # 7. Define the folder where you want to save the image
    save_folder = "captured_images"

    # Create the folder if it doesn't exist
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    # 8. Define the file name and full path
    image_name = "captured_image_" + str(uuid.uuid1()) + ".jpg"
    image_path = os.path.join(save_folder, image_name)

    # 9. Save the captured image to the specified folder
    cv2.imwrite(image_path, frame)
    print(f"Image saved at {image_path}")

else:
    print("Failed to capture image")
