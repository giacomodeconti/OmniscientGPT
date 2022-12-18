import openai
import telegram
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

# Set up a flag to track whether the chat command has been called
chat_active = False
api_key_active = False

# -- START CONFIGURATION --

# Setup Engine
engine_ai = "text-davinci-003"

# Set up with user input the OpenAI API client
openai.api_key = ""

# Set up the Telegram bot, static
TELEGRAM_TOKEN = "5881071670:AAHqOHdpYnBa2oQCKjsrex7KlgyGfEvDVQQ"
bot = telegram.Bot(token=TELEGRAM_TOKEN)

# -- END CONFIGURATION --

def start(update, context):
  update.message.reply_text("""
    This is an AI interface.

Use Menu button for all commands and description

Follw these steps to configure your AI:

1- Clik here https://beta.openai.com/account/api-keys

2- Create your API key and save it

Creator: @james_sec
Contact me if you want to add features to this bot
or support me to get online this bot

Before start, set your API key with /set_api_key

Warning !!:
The usage of this tool is only your responsability
  
  """)

def set_api_key(update, context):
  global api_key_active
  # Set the api_key_active flag to True
  api_key_active = True
  # Prompt the user to enter their API key
  update.message.reply_text("Please enter your API key:")

def display_api_key(update, context):
  update.message.reply_text(f"Your API Key is:\n{openai.api_key}")

def chat(update, context):
  global chat_active
  # Set the chat_active flag to True
  chat_active = True
  update.message.reply_text("Ask me something")

def stop_chat(update, context):
  global chat_active
  # Set the chat_active flag to False
  chat_active = False
  update.message.reply_text("Stopping chat")

def handle_message(update, context):
  global chat_active, api_key_active
  # If the chat or API key input commands have not been called, return without doing anything
  if not chat_active and not api_key_active:
    return
  # If the API key input command has been called, set the API key and return
  if api_key_active:
    api_key = update.message.text
    openai.api_key = api_key
    update.message.reply_text(f"API key set successfully!\n{api_key}")
    api_key_active = False
    return
  # If the chat command has been called, process the message as before
  testo = update.message.text.lower()
  # Use the actual message text as the prompt in the OpenAI API call
  response = openai.Completion.create(engine=engine_ai,prompt=(f'{testo}\n'),temperature=1,max_tokens=2048,top_p=1,frequency_penalty=0.0,)
  # Send the response to the user
  response_def = response['choices'][0]['text']
  update.message.reply_text(response_def)
  
# Set up the message handler
updater = Updater(TELEGRAM_TOKEN)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('set_api_key', set_api_key))
updater.dispatcher.add_handler(CommandHandler('display_api_key', display_api_key))
updater.dispatcher.add_handler(CommandHandler('chat', chat))
updater.dispatcher.add_handler(CommandHandler('stop_chat', stop_chat))

updater.dispatcher.add_handler(MessageHandler(Filters.text, handle_message))

# Start the bot and listen for incoming messages
print('Bot is running ...')
updater.start_polling()