from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler
from telegram import Update
from telegram.ext import CallbackContext
from flask import Flask, request
from threading import Thread

app = Flask('')

# Define states for the conversation
CONFIRMATION = 1
PASSWORD_LIST = 2
REFERRAL_LINK = 3
ACCOUNT_DETAILS = 4
CHANNEL = 5
CHANNEL_USERNAME = '@Darking_down'
TELEGRAM_PORT = 8080


# User data dictionary to store points and account details
user_data = {}
referral_link_data = {}  # Dictionary to store referral link information

def check_subscription(user_id):
    try:
        user_status = updater.bot.get_chat_member(CHANNEL_USERNAME, user_id).status
        return user_status == 'member' or user_status == 'administrator'
    except Exception as e:
        print(f"Error checking channel subscription: {e}")
        return False

def start(update, context):
    user_id = update.message.from_user.id
    try:
        user_status = context.bot.get_chat_member(CHANNEL_USERNAME, user_id).status
        if user_status != 'member' and user_status != 'administrator':
            # User is not subscribed, prompt them to subscribe first
            subscribe_message = f"🚸| عذرا عزيزي\n🔰| عليك الاشتراك بقناة البوت لتتمكن من استخدامه\n\n‼| اشترك في {CHANNEL_USERNAME} ثم ارسل \start"  
            update.message.reply_text(subscribe_message)
            return
    except Exception as e:
        print(f"Error checking channel subscription: {e}")
        # Handle the exception as needed
        return
        
    # Create a keyboard with the buttons
    keyboard = [[
        KeyboardButton('🔓حساب الكراك'),
        KeyboardButton('👤تفاصيل الحساب'),
    ], [
        KeyboardButton('🌀 احصل على الرابط لزيادة النقاط'),
        KeyboardButton('📖 الدليل'),
        KeyboardButton('🔐 قائمة كلمات المرور'),
        KeyboardButton('🔊قناتنا'),
    ]]

    # Send the customized welcome message with the keyboard
    welcome_message = (
        "مرحبا بك في Cracker Facebook bot\n\n"
        "🔺 كسر سهل لصفحات الأقسام اختر الكراك للفيسبوك"
    )
    update.message.reply_text(welcome_message, reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))

def handle_crack_request(update, context):
    # Send the terms and conditions message
    terms_message = (
        "🔖 قوانین\n\n"
        "🔺 أنت تؤكد أن مسؤوليات الكراك تقع عليك ولا يتحمل هذا الروبوت أي مسؤولية\n\n"
        "☑ في حالة التأكيد، ارسل كلمه تأكيد وانتقل إلى الخطوة التالية"
    )
    update.message.reply_text(terms_message)

    # Set the state to CONFIRMATION
    return CONFIRMATION

def handle_confirmation(update, context):
    user_id = update.message.from_user.id

    # Check if the user confirmed
    if update.message.text.lower() == 'تأكيد':
        # Process the confirmation and proceed to the next step
        # For example, you can deduct points from the user's balance here
        update.message.reply_text("تم التأكيد بنجاح! يمكنك الآن استخدام البوت.")
        return ConversationHandler.END  # End the conversation

    # User didn't confirm, ask them to confirm again
    update.message.reply_text("لم يتم التأكيد. يرجى إرسال 'تأكيد' للمتابعة.")

    # Stay in the CONFIRMATION state
    return CONFIRMATION

def handle_password_list(update, context):
    # Send the message about the default password list
    password_list_message = "حاليا، يتم تعيين كلمة المرور الخاصة بالقائمة الافتراضية في الروبوت"
    update.message.reply_text(password_list_message)

    # You can add further logic or actions related to password list handling here

    return ConversationHandler.END  # End the conversation

def handle_referral_link(update, context):
    # Generate a referral link based on the user's ID
    user_id = update.message.from_user.id
    referral_link = f"http://t.me/Haaacking_bot?start={user_id}"

    # Update user data with the referral link
    user_data[user_id] = {
        'name': update.message.from_user.first_name,
        'username': user_id,
        'points': 15,
        'referral_link': referral_link,
    }

    # Store referral link information
    referral_link_data[referral_link] = user_id

    # Send the referral link to the user
    referral_message = f"🔝 هذا الرابط هو الرابط الموجود أسفل مجموعتك\n\n👤 تحصل على نقطة واحدة عن طريق دعوة كل مستخدم من خلال رابط الفئة الفرعية الخاصة بك\n\n{referral_link}"
    update.message.reply_text(referral_message)

    return ConversationHandler.END  # End the conversation

def handle_account_details(update, context):
    user_id = update.message.from_user.id

    # Check if the user data exists for the current user_id
    if user_id not in user_data:
        # User data is not available, handle this case as needed
        update.message.reply_text("لا يوجد بيانات مستخدم لعرضها.")
        return ConversationHandler.END  # End the conversation

    # Access user data safely
    user_name = user_data[user_id].get('name', 'N/A')

    # Send the account details message
    account_details_message = (
        f"😊 اسمك: {user_name}\n"
        f"🔵 المعرف الرقمي المعرف الرقمي: {user_id}\n"
        f"😁 عدد الماس الخاص بك : {user_data[user_id]['points']}\n"
        f"لكسب المزيد من العملات اضغط على زر (🌀 احصل على الرابط لزيادة النقاط)"
    )
    update.message.reply_text(account_details_message)

    return ConversationHandler.END  

def handle_channel(update, context):
    # Send the message about the channel
    channel_message = "📌قناتنا..👨💻\n@Darking_down"
    update.message.reply_text(channel_message)

    return ConversationHandler.END  # End the conversation

# Handle regular text messages as well
def handle_text(update, context):
    text = update.message.text
    if text == '🔓حساب الكراك':
        # Start the crack request process
        return handle_crack_request(update, context)
    elif text == '🔐 قائمة كلمات المرور':
        # Start the password list handling process
        return handle_password_list(update, context)
    elif text == '🌀 احصل على الرابط لزيادة النقاط':
        # Start the referral link handling process
        return handle_referral_link(update, context)
    elif text == '👤تفاصيل الحساب':
        # Start the account details handling process
        return handle_account_details(update, context)
    elif text == '🔊قناتنا':
        # Start the channel handling process
        return handle_channel(update, context)

# Handle callback queries (for referral link sharing)
def handle_referral_link_callback(update: Update, context: CallbackContext):
    user_id = update.callback_query.from_user.id

    # Check if the user data exists for the current user_id
    if user_id not in user_data:
        # User data is not available, handle this case as needed
        update.callback_query.answer("لا يوجد بيانات مستخدم لعرضها.")
        return

    # Access user data safely
    user_name = user_data[user_id].get('name', 'N/A')

    # Check if the user shared the referral link
    if update.callback_query.data.startswith("referral_link"):
        # Increment points for the user who shared the link
        shared_user_id = int(update.callback_query.data.split("_")[1])
        if shared_user_id in user_data:
            user_data[shared_user_id]['points'] += 1
            # Send a message to the shared user about the earned point
            context.bot.send_message(shared_user_id, "لقد تمت مشاركة الرابط وحصولك على نقطة إضافية!")

    # Send the referral points message to the user who shared the link
    update.callback_query.answer("لقد تم توفير نقطة لحسابك لمشاركة الرابط.")
    update.callback_query.bot.send_message(user_id, f"لقد تم توفير نقطة لحسابك لمشاركة الرابط. شكراً!")

updater = Updater(token='6184145071:AAGk-c7IIrDb7nVhZO1lgZwdqdupJH52EQ0', use_context=True)
dispatcher = updater.dispatcher

# Create conversation handlers
crack_conversation_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.text & ~Filters.command, handle_text)],
    states={
        CONFIRMATION: [MessageHandler(Filters.text & ~Filters.command, handle_confirmation)],
    },
    fallbacks=[],
)

password_list_conversation_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.text & ~Filters.command, handle_text)],
    states={
        PASSWORD_LIST: [MessageHandler(Filters.text & ~Filters.command, handle_password_list)],
    },
    fallbacks=[],
)

referral_link_conversation_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.text & ~Filters.command, handle_referral_link)],
    states={
        REFERRAL_LINK: [MessageHandler(Filters.text & ~Filters.command, handle_referral_link)],
    },
    fallbacks=[],
)

account_details_conversation_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.text & ~Filters.command, handle_text)],
    states={
        ACCOUNT_DETAILS: [MessageHandler(Filters.text & ~Filters.command, handle_account_details)],
    },
    fallbacks=[],
)

channel_conversation_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.text & ~Filters.command, handle_text)],
    states={
        CHANNEL: [MessageHandler(Filters.text & ~Filters.command, handle_channel)],
    },
    fallbacks=[],
)

# Add the callback query handler
dispatcher.add_handler(CallbackQueryHandler(handle_referral_link_callback))

# Add all conversation handlers to the dispatcher
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(crack_conversation_handler)
dispatcher.add_handler(password_list_conversation_handler)
dispatcher.add_handler(referral_link_conversation_handler)
dispatcher.add_handler(account_details_conversation_handler)
dispatcher.add_handler(channel_conversation_handler)

def run():
    app.run(host='0.0.0.0', port=8080)

# Start polling for updates
updater.start_polling()

updater.idle()

 keep_alive()  # Start the web server
    bot.infinity_polling(skip_pending=True)

