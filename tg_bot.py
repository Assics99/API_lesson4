import telegram

BOT_TOKEN = os.environ['TG_KEY']
CHAT_ID = "@space_photos88"
PHOTO_PATH = "photo.jpg"

def send_photo():
    bot = telegram.Bot(token=BOT_TOKEN)
    
    with open(PHOTO_PATH, "rb") as photo:
        bot.send_photo(chat_id=CHAT_ID, photo=photo)

if __name__ == "__main__":
    send_photo()
