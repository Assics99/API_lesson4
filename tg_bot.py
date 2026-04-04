import telegram


from dotenv import load_dotenv
load_dotenv()


bot = telegram.Bot(token = os.environ['TG_KEY'])
bot.send_message(chat_id='@space_photos88', text="Здесь будут фотографии космоса!")