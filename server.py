from flask import Flask, render_template, jsonify
import pyautogui
import csv

app = Flask(__name__)

# Load keypoints from the CSV file
keypoints = {}

with open('keypoints.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        slide_number = int(row['slide'])
        keypoints[slide_number] = row['content']

current_slide = 1  # Initialize the current slide number

@app.route('/')
def index():
    return render_template('index.html', current_slide=current_slide, keypoints=keypoints.get(current_slide, ''))

@app.route('/control/<action>')
def control(action):
    global current_slide

    if action == 'next':
        current_slide += 1
        pyautogui.press('right')  # Simulate right arrow key press
    elif action == 'previous':
        current_slide -= 1
        pyautogui.press('left')   # Simulate left arrow key press

    # Ensure current_slide is within the bounds of the keypoints
    current_slide = max(1, min(current_slide, len(keypoints)))

    return jsonify({'current_slide': current_slide, 'keypoints': keypoints.get(current_slide, '')})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
