import logging
import datetime
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telethon import TelegramClient
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError

# API 配置
load_dotenv()
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
    )


async def get_user_join_date(update, context):
    message = update.effective_message
    chat = update.effective_chat
    user = update.effective_user

    # 如果是在私聊中使用，直接跳过
    if chat.type == "private":
        await message.reply_text("请在群组中使用此命令。")
        return

    # 启动 Telethon 客户端 (建议在全局初始化，这里为了演示放在函数内)
    # 注意：'bot_session' 是 session 文件名
    client = TelegramClient("bot_session", API_ID, API_HASH)

    try:
        await client.start(bot_token=BOT_TOKEN)

        # 获取当前用户在该群组的参与信息
        # Telethon 的 channel 参数接受 PeerID 或 Username
        participant_data = await client(
            GetParticipantRequest(channel=chat.id, participant=user.id)
        )

        # 提取入群日期 (datetime 对象)
        join_date = participant_data.participant.date

        # 格式化时间（转换为北京时间或本地时间）
        local_join_date = join_date.astimezone(
            datetime.timezone(datetime.timedelta(hours=8))
        )
        date_str = local_join_date.strftime("%Y-%m-%d %H:%M:%S")

        await message.reply_text(
            f"👤 用户的入群时间为：\n`{date_str}` (UTC+8)", parse_mode="Markdown"
        )

    except UserNotParticipantError:
        await message.reply_text("未能在成员列表中找到该用户。")
    except Exception as e:
        await message.reply_text(f"查询失败: {str(e)}")
    finally:
        # 记得断开连接，除非你是在全局维护这个 client
        await client.disconnect()


if __name__ == "__main__":
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("get_join_date", get_user_join_date))

    application.run_polling(allowed_updates=["message"])
