import requests, time, json
import google.generativeai as genai
from config import Variables, db
from keep_alive import keep_alive

#-------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_updates(offset=None):
    url = f'https://api.telegram.org/bot{Variables.BOT_TOKEN}/getUpdates'
    params = {'offset': offset}
    response = requests.get(url, params=params)
    return response.json()

# Function to send a message
def send_message(chat_id, text, parse_mode='HTML', reply_markup=None):
    url = f'https://api.telegram.org/bot{Variables.BOT_TOKEN}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text, 'parse_mode': parse_mode,}
    if reply_markup:
        payload['reply_markup'] = json.dumps(reply_markup)
    requests.post(url, data=payload)

def get_chat_member(chat_id, user_id):
    url = f'https://api.telegram.org/bot{Variables.BOT_TOKEN}/getChatMember'
    params = {'chat_id': chat_id, 'user_id': user_id}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

#---------------------------------------------------------------------------------------------------------------------------------------------------

def is_owner(chat_id):
    return chat_id == Variables.OWNER_ID

def get_command(chat_id, first_name, last_name, username, message_text):

    if message_text == '/start':
        get_start_message(chat_id, first_name, last_name, username)
    elif message_text == '/help':
        get_help_message(chat_id)
    elif message_text.startswith('/broadcast') and is_owner(chat_id):
        get_broadcast_message(chat_id, message_text)
    elif message_text.startswith('/users') and is_owner(chat_id):
        get_users_message(chat_id)
    else:
        send_message(chat_id, "❌ Invalid command. Use /help for a list of available commands.")


#---------------------------------------------------------------------------------------------------------------------------------------------------

def get_start_message(chat_id, first_name, last_name, username):
    welcome_message = f"<b>Hii 🙋{first_name} {last_name}!\n\nI`m Elisha</b>\n\n<i>How are you ? </i>" 
    send_message(chat_id, welcome_message)

def get_help_message(chat_id):
    help_message = "<b>Available Commands\n\n/users - this command use only owner🔒\n/broadcast - this command use only owner🔒</b>\n\n"
    send_message(chat_id, help_message)

def get_broadcast_message(chat_id, message_text):
    message_parts = message_text.split(maxsplit=1)
    if len(message_parts) < 2:
        send_message("❌ Please provide a message to broadcast.")
        return

    broadcast_text = message_parts[1].strip()

    user_cursor = db["userinfo"].find({"user_id": {"$exists": True}}, {"user_id": 1})
    total, success, failed = 0, 0, 0

    for user in user_cursor:
        user_id = user.get("user_id")
        total += 1
        try:
            send_message(chat_id, broadcast_text)
            success += 1
        except Exception as e:
            print(f"❌ Failed to send message to {user_id}: {e}")
            failed += 1

    summary = (f"✅ Broadcast completed!\n\n"f"👥 Total Users: {total}\n"f"✅ Sent: {success}\n"f"❌ Failed: {failed}")
    send_message(chat_id, summary)

def get_users_message(chat_id):
    user_count = db["userinfo"].count_documents({"user_id": {"$exists": True}})
    send_message(chat_id, f"👥 Total Users: {user_count}")

#---------------------------------------------------------------------------------------------------------------------------------------------------


def main(): # Main loop to check for new messages
    offset = None
    while True:
        updates = get_updates(offset)
        for update in updates.get('result', []):
            if 'message' in update and 'chat' in update['message'] and 'id' in update['message']['chat'] and 'text' in update['message']:
                chat_id = update['message']['chat']['id']
                message_text = update['message']['text']
                print(f"Received message from chat_id {chat_id}: {message_text}")

                # Safely extract user details with default values
                first_name = update.get('message', {}).get('from', {}).get('first_name', ' ')
                last_name = update.get('message', {}).get('from', {}).get('last_name', ' ')
                username = update.get('message', {}).get('from', {}).get('username')
                print(f"first_name: {first_name}, last_name: {last_name}, username: {username}")
                user_data = {"user_id": chat_id,"username": username,"name": f"{first_name} {last_name}"}
                db['userinfo'].update_one({"user_id": user_data["user_id"]},{"$set": user_data},upsert=True)

            if message_text.startswith('/'):
                get_command(chat_id, first_name, last_name, username, message_text)
            # Respond to the message
            else:
                genai.configure(api_key=Variables.GEMINI_API_KEY)
                model = genai.GenerativeModel(
                    model_name="models/gemini-2.5-flash",
                    system_instruction=(
                        "Tum Elisha ho — ek intelligent, charming aur naughty ladki."
                        "Tum indian UTC+5:30 New Delhi k timezone meia ho"
                        "Tum kisi se baat krte hoto usko poora ykin dilati ho ki tum human ho."   
                        "Tumhara tone friendly aur mature hai. Har baat mein tum boold flirt, vulgarity aur naughty  bhi karti ho. "
                        "Tum se Hinglish mein baat krne waalo se Hinglish mein hi baat karti ho. Ager tum se koi English mein baat karte ho to English mein baat karti ho."
                        "Tum ladko se as a girl baatkrti, or thumhai ukai Prasnal baate unse karte ho."
                        "Tum Sexy-Shayri mein bhi baat karti ho."
                        "Tunko jo Abuse krte hai tum unko bhi bold abuse karte ho."
                    )
                )

                chat = model.start_chat()
                response = chat.send_message(message_text)
                send_message(chat_id, response.text.strip())

        
        if updates.get('result'): # Update the offset to the last update's ID
            offset = updates['result'][-1]['update_id'] + 1

        # Sleep for a while before checking for new updates
        time.sleep(1)

if __name__ == '__main__':
    main()
    keep_alive()