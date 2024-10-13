import subprocess
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes,InlineQueryHandler

# Function to ping the camera or any IP address
async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Check if the user provided an IP address
    if len(context.args) > 0:
        ip_address = context.args[0]  # Get the first argument (IP address)
        command = ['ping', '-c', '4', ip_address]  # Use '-c' for Linux/macOS
        response = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if response.returncode == 0:
            await update.message.reply_text(f"PING УСПЕШНЫЙ!\n{response.stdout.decode()}")
        else:
            await update.message.reply_text(f"PING НЕ УДАЛСЯ!\n{response.stderr.decode()}")
    else:
        await update.message.reply_text("Пожалуйста напишите IP address чтобы пинговать. Например: /ping 192.168.1.100")

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Добро пожаловать в PingBot! Введи /ping <IP_ADDRESS> чтобы пинговать либой IP adress который тебе нужен.\nНапример /ping 192.168.0.100")

async def inline_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.inline_query.query

    # Create a list of possible commands to suggest
    results = []
    if query.startswith('/'):
        results.append(
            InlineQueryResultArticle(
                id='1',
                title='Ping Command',
                input_message_content=InputTextMessageContent('/ping '),
                description='Ping an IP address',
            )
        )
        results.append(
            InlineQueryResultArticle(
                id='2',
                title='Start Command',
                input_message_content=InputTextMessageContent('/start'),
                description='Start the bot'
            )
        )

    await update.inline_query.answer(results)


def main():
    # Add your token here
    token = "7640527279:AAE--i9N1HsIDNSiVEzRNDUafxTVFkbkv8c"  # Replace with your actual bot token

    # Set up the application
    application = ApplicationBuilder().token(token).build()

    # Define commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ping", ping))
    application.add_handler(InlineQueryHandler(inline_query_handler))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()  
    
