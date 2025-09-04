
from ncatbot.core import BotClient, GroupMessage, PrivateMessage
from ncatbot.utils.config import config
from ncatbot.utils.logger import get_log

import jmcomic
import os
import shutil

from ncatbot.core.element import (
    MessageChain,
    Text,
    Reply,
    At,
    AtAll,
    Dice,
    Face,
    Image,
    Json,
    Music,
    CustomMusic,
    Record,
    Rps,
    Video,
    File,
)

_log = get_log()

config.set_bot_uin("1412633232")
config.set_root("1224403167")
config.set_ws_uri("ws://localhost:3001")
config.set_token("napcat")

bot = BotClient()

config = "config.yml"
loadConfig = jmcomic.JmOption.from_file(config)
manhua = []

def clean_up_files(file_path):
    # 删除 pdf 文件
    try:
        os.remove(file_path)
        _log.info(f"已删除文件: {file_path}")
    except Exception as e:
        _log.error(f"删除文件失败: {file_path}, 原因: {e}")

    # 清空 stock 文件夹
    stock_dir = "stock"
    if os.path.exists(stock_dir):
        try:
            shutil.rmtree(stock_dir)
            _log.info(f"已清空文件夹: {stock_dir}")
        except Exception as e:
            _log.error(f"清空文件夹失败: {stock_dir}, 原因: {e}")

@bot.group_event()
async def on_group_message(msg: GroupMessage):
    _log.info(msg)
    manhua.clear()
    if msg.raw_message.startswith("/jm "):
        album_id = msg.raw_message.split("/jm ", 1)[1].strip()
        manhua.append(album_id)

        loadConfig.download_album(manhua)
        file_path = f"pdf/{album_id}.pdf"

        msg_chain = MessageChain([
            File(file_path).to_dict()
        ])

        await msg.reply(rtf=msg_chain)
        clean_up_files(file_path)

@bot.private_event()
async def on_private_message(msg: PrivateMessage):
    _log.info(msg)
    manhua.clear()
    if msg.raw_message.startswith("/jm "):
        album_id = msg.raw_message.split("/jm ", 1)[1].strip()
        manhua.append(album_id)

        loadConfig.download_album(manhua)
        file_path = f"pdf/{album_id}.pdf"

        msg_chain = MessageChain([
            File(file_path).to_dict()
        ])

        await bot.api.post_private_msg(msg.user_id, rtf=msg_chain)
        clean_up_files(file_path)

if __name__ == "__main__":
    bot.run(reload=False)
