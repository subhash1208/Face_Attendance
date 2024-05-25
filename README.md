   # Face Attendance System

## Overview
The Face Attendance System is a facial recognition-based attendance logging application. Utilizing a webcam, it identifies individuals in real-time and records their attendance, capturing both check-in and check-out times. This system leverages OpenCV for image processing, the face_recognition library for facial recognition, and numpy for numerical operations.

## Features
- **Real-Time Face Detection and Recognition:** Detects and recognizes faces using the `face_recognition` library.
- **Attendance Logging:** Automatically logs attendance in a CSV file with the current date, including check-in and check-out times.
- **Anti-Spoofing Mechanism:** Uses a pre-trained model to prevent spoofing attacks.

## Installation
### Prerequisites
Ensure you have the following installed:
- Python 3.x
- OpenCV
- face_recognition
- numpy

### Steps
1. **Clone the repository:**
   ```bash
   git clone https://github.com/subhash1208/Face_Attendance.git
   ```
2. **Navigate to the project directory:**
   ```bash
   cd Face_Attendance
   ```
3. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```
## Usage

1. **Prepare the Images**

   Place images of known individuals in the `images` directory. The filename should be the name of the person.

2. **Run the Main Script**

   Execute the main script to start the attendance system:

   ```bash
   python attendance.py
   ```
3. **Attendance Logging**

   The system will log check-in and check-out times in a CSV file named with the current date in the attendanceSheet directory.
## Code Explanation

1. **Image Loading and Encoding**

    The code loads images from the `images` directory, converts them to RGB format, and encodes them using the `face_recognition.face_encodings` function.

2. **Real-Time Face Recognition**

    The code captures webcam feed using OpenCV. Each frame is processed to detect and encode faces, which are then compared against the known encodings.

3. **Attendance Posting**

    The code logs attendance by writing the individual's name and current time to a CSV file. If the individual is already logged in, it updates the check-out time.

4. **Anti-Spoofing**

    The code calls an external anti-spoofing test function from the `Silent.test` module to verify if the detected face is real or a spoof.
## Notes

**Important Configuration**

Ensure the Silent-Face-Anti-Spoofing model is properly configured and the path to the model is correctly set in the script.

**Environmental Requirements**

A clear and well-lit environment is required for accurate facial recognition.

## Contribution

**Get Involved!**

Contributions are welcome! Feel free to open issues or submit pull requests for any improvements or bug fixes.