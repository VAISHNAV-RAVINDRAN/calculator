from flask import Flask, render_template, request
import datetime
import multiprocessing
from instabot import Bot
import os
import time

app = Flask(__name__)
message_queue = multiprocessing.Queue()

def send_message(receiver_name, message):
    check = os.path.isfile('./config/lawefel233_uuid_and_cookie.json')
    print(check)
    if(check == True):
        os.remove('./config/lawefel233_uuid_and_cookie.json')
        bot = Bot()
        bot.login(username="lawefel233", password="Zeta23@2003")
        bot.send_message(message, [receiver_name])
    elif(check == False):
        bot = Bot()
        bot.login(username="lawefel233", password="Zeta23@2003")
        bot.send_message("Hello", ["code_console"])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send():
    receiver_name = request.form['receiver-name']
    message = request.form['message']
    date_time_str = request.form['date-time']

    # Convert the date and time string to a datetime object
    date_time = datetime.datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M')

    # Calculate the number of seconds until the scheduled time
    time_diff = (date_time - datetime.datetime.now()).total_seconds()

    # Schedule the message to be sent at the scheduled time
    message_queue.put({'receiver_name': receiver_name, 'message': message, 'time_diff': time_diff})

    return 'Message scheduled successfully!'

def message_sender(queue):
    while True:
        message = queue.get()
        time_diff = message['time_diff']
        receiver_name = message['receiver_name']
        message_text = message['message']
        if time_diff > 0:
            # Wait until the scheduled time
            time.sleep(time_diff)
        # Send the message
        send_message(receiver_name, message_text)

if __name__ == '__main__':
    # Start the message sender process
    message_sender_process = multiprocessing.Process(target=message_sender, args=(message_queue,))
    message_sender_process.start()

    app.run(debug=True)
