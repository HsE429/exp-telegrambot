import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    PollAnswerHandler,
    TypeHandler,
)


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
    )


# 发起投票的函数
async def start_poll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    questions = ["Python", "JavaScript", "C++", "Java"]
    chat_id = update.effective_chat.id

    message = await context.bot.send_poll(
        chat_id=chat_id,
        question="你最喜欢的编程语言是？",
        options=questions,
        is_anonymous=False,  # 是否匿名，False 则可以看到谁投了票
        allows_multiple_answers=True,  # 是否允许多选
    )

    # 关键点：将 poll_id 与当前群组 ID 绑定存入 context.bot_data
    # 这样在任何 Handler 里都能通过 poll_id 查到该发往哪个群
    context.bot_data[message.poll.id] = update.effective_chat.id


# 注意：poll_answer 更新（用户点击选项时发出的事件）不包含聊天上下文信息。
# Telegram 的 API 设计逻辑是：投票答案是与“投票 ID”（poll_id）绑定的，而不是直接与某个特定的聊天窗口绑定。
async def receive_poll_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer = update.poll_answer
    poll_id = answer.poll_id

    # 从存储中找回对应的 chat_id
    chat_id = context.bot_data.get(poll_id)

    if chat_id:
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"用户 {answer.user.full_name} (ID: {answer.user.id}) 选择了索引: {answer.option_ids}",
        )


# async def debug_all_updates(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     # 这会打印收到的所有原始更新对象
#     print(f"收到更新: {update.to_dict()}")


if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # app.add_handler(TypeHandler(Update, debug_all_updates), group=-1)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("poll", start_poll))
    app.add_handler(PollAnswerHandler(receive_poll_answer))

    # 需要显式添加 allowed_updates 参数。
    app.run_polling(allowed_updates=["message", "poll", "poll_answer"])
