🧠 Gesture-Based Calculator
A contactless calculator powered by Computer Vision and Hand Gesture Recognition using Python, OpenCV, and MediaPipe.

📌 Overview
This project implements a real-time, touch-free calculator that interprets hand gestures to input digits and perform arithmetic operations. By tracking your hand and finger movements using your webcam, the system recognizes numbers (0–5) and allows you to hover over virtual calculator buttons to build and evaluate expressions.

✨ Key Features
🎥 Real-Time Hand Detection using MediaPipe

✋ Finger Gesture Recognition for digits 0–5

➕ Hover-Based Operator Input (+, -, *, /, =, C)

🧮 Live Expression Building and Evaluation

🧠 Debounce Logic to prevent accidental multiple selections

🧼 Idle Timeout Reset after 3 seconds of inactivity

🖼️ Intuitive UI with on-screen button feedback via OpenCV


🛠️ Technologies Used
Python 3.7+

OpenCV – Computer Vision library

MediaPipe – Google’s ML pipeline for hand detection

🔄 How It Works
Hand Tracking: MediaPipe locates and tracks 21 hand landmarks.

Finger Counting: Logic compares fingertip and lower joint positions to determine which fingers are up.

Hover Detection: A bounding box detects whether your index finger hovers over a virtual button for ~1.2 seconds.

Expression Handling: Detected digits and operators are appended to an expression. Upon hovering over =, the result is calculated and displayed.

Visual Feedback: Buttons highlight when hovered and selected.

🖥️ System Requirements
Python 3.7 or above

Webcam-enabled laptop or PC

Decent lighting conditions

📦 Installation
Clone the Repository

bash
Copy
Edit
git clone https://github.com/your-username/gesture-calculator.git
cd gesture-calculator
Install Required Packages

bash
Copy
Edit
pip install opencv-python mediapipe
▶️ Running the Application
bash
Copy
Edit
python gesture_calculator.py
Position your dominant hand in front of the webcam.

Show digits using fingers (0–5).

Hover your index finger over a button to select it.

Wait for the hover indicator (~1.2s) to register the input.

✋ Gesture Mapping
Finger Gesture	Interpreted As
✊ (Fist)	0
☝️ (Index)	1
✌️ (Index + Middle)	2
🤟 (Index + Middle + Ring)	3
🖖 (Four fingers)	4
🖐️ (Open Palm)	5

💡 Example Workflow
text
Copy
Edit
Show "2" ➝ Expression: 2  
Hover on "+" ➝ Expression: 2+  
Show "3" ➝ Expression: 2+3  
Hover on "=" ➝ Result: 5  
📂 Project Structure
bash
Copy
Edit
gesture-calculator/
├── gesture_calculator.py   # Main script
├── README.md               # Project documentation
⚠️ Notes
Best used in well-lit environments with a plain background.

Works best with one hand centered in the camera frame.

Avoid quick gestures; use deliberate and steady movements.

🧾 License
This project is released under the MIT License.
Feel free to use and modify it for academic or personal purposes.

🙌 Acknowledgements
MediaPipe Hands

OpenCV Python Docs
