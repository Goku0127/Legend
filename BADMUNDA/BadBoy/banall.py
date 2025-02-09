import asyncio
import logging
import os
from pyrogram import Client, filters
from pyrogram.errors import ChatAdminRequired
from sample_config import SUDO_USERS

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

@Client.on_message(filters.command("banall") & filters.group)
async def banall(bot, message):
    # Only allow sudo users to run this command
    if str(message.from_user.id) not in SUDO_USERS:
        await message.reply("You are not authorized to use this command.")
        return

    logging.info(f"new chat {message.chat.id}")
    logging.info(f"getting members from {message.chat.id}")

    try:
        # Check if the bot is an admin
        bot_status = await bot.get_chat_member(message.chat.id, (await bot.get_me()).id)
        
        if bot_status.status != "administrator":
            # If the bot is not an admin, inform the user
            await bot.send_message(message.chat.id, "I need admin rights to perform this action. Please make me an admin with banning privileges.")
            return

        # If bot is an admin, proceed with banning
        async for i in bot.get_chat_members(message.chat.id):
            try:
                await bot.ban_chat_member(chat_id=message.chat.id, user_id=i.user.id)
                logging.info(f"kicked {i.user.id} from {message.chat.id}")
                await asyncio.sleep(0.1)  # Add a small delay to avoid rate limiting
            except Exception as e:
                logging.error(f"Failed to kick {i.user.id}: {str(e)}")
                
        logging.info("Process completed")
        await bot.send_message(message.chat.id, "Ban all process completed!")
    except Exception as e:
        logging.error(f"Error during process: {str(e)}")
        await bot.send_message(message.chat.id, "There was an error while banning members.")
