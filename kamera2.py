import telebot
import requests
import cv2
import numpy as np
import time

# Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your bot token
bot = telebot.TeleBot('6038856046:AAHFYptTYuVdUyapymwCKO435eK6f5ClxMP51c')
chat_id = '14969299157'  # Замените на ваш Chat ID

# URL for accessing the video stream from the camera
camera_url = 'http://192.161.38.54:8692/video'

# Flag to track motion detection
motion_detected = False

# Handler for the /start command
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Hello! I'm a motion detection bot. Use the /motion command to start motion tracking.")

# Handler for the /motion command
@bot.message_handler(commands=['motion'])
def motion(message):
    global motion_detected
    if motion_detected:
        bot.reply_to(message, "Motion detection is already running.")
    else:
        motion_detected = True
        bot.reply_to(message, "Motion detection started.")
        start_motion_tracking()

# Function for motion tracking
def start_motion_tracking():
    while motion_detected:
        stream = requests.get(camera_url, stream=True)
        if stream.status_code == 200:
            bytes_data = bytes()
            for chunk in stream.iter_content(chunk_size=1024):
                bytes_data += chunk
                a = bytes_data.find(b'\xff\xd8')
                b = bytes_data.find(b'\xff\xd9')
                if a != -1 and b != -1:
                    jpg = bytes_data[a:b + 2]
                    bytes_data = bytes_data[b + 2:]
                    try:
                        image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    except cv2.error:kamera3
                        continue

                    # Process the image as needed
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    # ...

                    if motion_detected:
                        cv2.imwrite("motion_detected.jpg", image)
                        with open("motion_detected.jpg", "rb") as photo:
                            bot.send_photo(chat_id, photo)

        time.sleep(0.1)

# Handler for the /stop command
@bot.message_handler(commands=['stop'])
def stop(message):
    global motion_detected
    motion_detected = False
    bot.reply_to(message, "Motion detection stopped.")

# Run the bot
bot.polling()
