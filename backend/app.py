import cv2
import numpy as np
from fer import FER
import pyttsx3
from threading import Thread
from flask import Flask, Response, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Initialize the emotion detector
emotion_detector = FER(mtcnn=True)

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speaking rate
engine.setProperty('volume', 0.9)  # Volume level

# Compliments database
compliments = {
    "happy": [
        "Your smile brightens everyone's day!",
        "That joy looks amazing on you!",
        "Your positive energy is contagious!"
    ],
    "neutral": [
        "Your presence brings calm and stability.",
        "You carry yourself with natural grace.",
        "Your quiet confidence is admirable."
    ],
    "sad": [
        "You're stronger than you know.",
        "Every storm passes - you've got this!",
        "Your resilience is truly inspiring."
    ]
}

# Fashion recommendations based on emotion
fashion_recommendations = {
    "happy": "Bright summer dresses and colorful accessories.",
    "neutral": "Elegant minimal outfits and formal wear.",
    "sad": "Comfortable cozy wear like hoodies and jeans.",
    "angry": "Bold statement outfits with edgy designs."
}

def get_compliment(emotion):
    if emotion in compliments:
        return np.random.choice(compliments[emotion])
    return np.random.choice(compliments["neutral"])

def get_fashion_tip(emotion):
    return fashion_recommendations.get(emotion, "Try versatile fashion today!")

def speak_compliment_async(compliment):
    """Run TTS in a separate thread to avoid blocking Flask."""
    def tts_task():
        engine.say(compliment)
        engine.runAndWait()
    
    Thread(target=tts_task).start()

def process_frame(frame):
    """Process a single frame for emotion detection"""
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = emotion_detector.detect_emotions(rgb_frame)
    
    if result:
        emotions = result[0]["emotions"]
        dominant_emotion = max(emotions.items(), key=lambda x: x[1])[0]
        box = result[0]["box"]

        # Draw rectangle around the face
        cv2.rectangle(frame, (box[0], box[1]), (box[0] + box[2], box[1] + box[3]), (0, 255, 0), 2)
        cv2.putText(frame, dominant_emotion, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        
        return frame, dominant_emotion
    
    return frame, "neutral"

def generate_frames():
    """Generate frames from webcam with emotion detection"""
    camera = cv2.VideoCapture(0)
    
    while True:
        success, frame = camera.read()
        if not success:
            break
            
        processed_frame, emotion = process_frame(frame)
        ret, buffer = cv2.imencode('.jpg', processed_frame)
        frame = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_emotion')
def get_emotion():
    emotions = ["happy", "neutral", "sad", "angry"]
    current_emotion = np.random.choice(emotions)
    compliment = get_compliment(current_emotion)
    fashion_tip = get_fashion_tip(current_emotion)
    
    return jsonify({
        "emotion": current_emotion,
        "compliment": compliment,
        "fashion_tip": fashion_tip
    })

@app.route('/speak/<emotion>')
def speak(emotion):
    compliment = get_compliment(emotion)
    speak_compliment_async(compliment)
    return jsonify({"success": True, "compliment": compliment})

@app.route('/fashion_overlay', methods=['POST'])
def fashion_overlay():
    """Apply fashion AR overlay based on emotion"""
    emotion = request.json.get("emotion", "neutral")
    fashion_tip = get_fashion_tip(emotion)
    return jsonify({
        "message": f"{fashion_tip}",
        "emotion": emotion
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)