import logging
from telegram import Update, ReactionTypeEmoji
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageReactionHandler, MessageHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def handle_reaction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ru = update.message_reaction

    chat_id = ru.chat.id
    message_id = ru.message_id
    user = ru.user

    for r in ru.new_reaction: # 这里其实会获得一条消息上所有的reaction。
        if isinstance(r, ReactionTypeEmoji):
            text = f"{user.first_name} 点了一个 {r.emoji}"

            await context.bot.send_message(
                chat_id=chat_id,
                text=text,
                reply_to_message_id=message_id
            )

if __name__ == '__main__':
    application = ApplicationBuilder().token('8075682427:AAGlIlHOGit78OIUsgR_IHw9ySLuQN9zHF0').build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))
    application.add_handler(MessageReactionHandler(handle_reaction))
    
    # 重要提示：添加 allowed_updates 参数。
    application.run_polling(allowed_updates=["message", 'message_reaction'])