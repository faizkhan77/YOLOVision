# YOLOv8 Object Detection App

This repository contains a Flask-based web application for object detection using the YOLOv8 model, combined with FastAPI and OpenCV. The application supports object detection in images, videos, and live webcam streams.

## Overview

The YOLOv8 Object Detection App allows users to perform real-time object detection through a user-friendly interface. Whether uploading images/videos or utilizing live webcam detection, users can view and analyze object detection results directly in their web browser. This project leverages the powerful YOLOv8 model to provide accurate and efficient object detection capabilities.

## Project Structure

- **`app.py`**: Contains the main Flask backend code that handles all server-side logic, including routing and processing.
- **`requirements.txt`**: Lists all the Python dependencies required for the application.
- **`yolov8n.pt`**: The pre-trained YOLOv8 model used for object detection.
- **`templates/`**: Contains HTML files for the user interface of the application.
- **`static/`**: Includes static files such as CSS and output folders.
  - **`css/style.css`**: Styling for the application's UI.
  - **`output/`**: Stores detected images and videos.
  - **`uploads/`**: Directory for storing uploaded images and videos.
- **`take_pic.py`**: A Python script to capture images directly from a webcam, if needed.

## Installation

To run this project locally, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/faizkhan77/object-detection-yolov8.git
   ```

2. **Install dependencies:**
   Ensure you have Python 3.12.4 installed. Then, install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install FFmpeg:**
   Download and install FFmpeg from [FFmpeg.org](https://ffmpeg.org/download.html). Make sure to add FFmpeg to your system's environment variables.

4. **Run the application:**
   ```bash
   python app.py
   ```
   Access the web application at `http://127.0.0.1:5000`.

## How It Works

- **Image/Video Upload**: Users can upload images or videos through the web interface. The backend processes these files and applies YOLOv8 object detection. Detected results are stored in the `output/` folder.
- **Live Webcam Detection**: Users can start live detection by clicking the "Live Camera Detection" button. The live feed is processed in real-time using the YOLOv8 model.
- **Webcam Picture Capture**: The `take_pic.py` script allows capturing pictures directly from the webcam if required.

## Development & Deployment

The project is containerized using Docker to ensure consistent environments across different systems. 

### Pulling the Docker Image

To pull the Docker image, use:
```bash
docker pull faizkhan7/object-detector-yolov8:latest
```

### Running the Docker Container

Run the Docker container with:
```bash
docker run -p 5000:5000 faizkhan7/object-detector-yolov8:latest
```

## Contribution

Feel free to contribute to this project by submitting pull requests or opening issues. 

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

**Inspiration for the Project:**

I was inspired to develop this application because of the technical complexity involved in using state-of-the-art object detection models like YOLOv8. While working with YOLOv5 and YOLOv8, I realized the need for a user-friendly interface that abstracts away the complexities of model setup and dependencies. Thus, I created this Flask-based application to make object detection accessible to users who may not have a technical background.

---
