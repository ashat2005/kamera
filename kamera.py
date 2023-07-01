import cv2
import telebot

# Замените 'YOUR_TELEGRAM_BOT_TOKEN' на ваш токен бота
bot = telebot.TeleBot('6038856046:AAHFYptTYuVdUvgtgsre6343yapymwCKOeK6f5ClxMP51c')
chat_id = '119925245432599157'  # Замените на ваш Chat ID
# Флаг для отслеживания движения
motion_tracking = False

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я бот для отслеживания движения. Используй команду /motion для запуска отслеживания.")

# Обработчик команды /motion
@bot.message_handler(commands=['motion'])
def motion(message):
    global motion_tracking
    if motion_tracking:
        bot.reply_to(message, "Отслеживание движения уже запущено.")
    else:
        motion_tracking = True
        bot.reply_to(message, "Отслеживание движения запущено.")
        start_motion_tracking()

# Функция для отслеживания движения
def start_motion_tracking():
    cap = cv2.VideoCapture(0)
    previous_frame = None
    motion_detected = False

    while motion_tracking:
        _, frame = cap.read()
        current_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if previous_frame is not None:
            frame_diff = cv2.absdiff(previous_frame, current_frame)
            _, threshold = cv2.threshold(frame_diff, 30, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if len(contours) > 0:
                motion_detected = True

        previous_frame = current_frame

        if motion_detected:
            # Если обнаружено движение, отправляем фотографию
            cv2.imwrite("motion_detected.jpg", frame)
            with open("motion_detected.jpg", "rb") as photo:
                bot.send_photo(chat_id, photo)
            motion_detected = False

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Обработчик команды /stop
@bot.message_handler(commands=['stop'])
def stop(message):
    global motion_tracking
    motion_tracking = False
    bot.reply_to(message, "Отслеживание движения остановлено.")
# Запуск бота
bot.polling()
