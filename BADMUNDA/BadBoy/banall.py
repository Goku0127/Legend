import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.errors import ChatAdminRequired, UserNotParticipant

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

@Client.on_message(filters.command("banall") & filters.group)
async def banall(bot, message):
    logging.info(f"new chat {message.chat.id}")
    logging.info(f"getting members from {message.chat.id}")
    try:
        # Use async for to iterate over the async generator
        async for i in bot.get_chat_members(message.chat.id):
            try:
                await bot.ban_chat_member(chat_id=message.chat.id, user_id=i.user.id)
                logging.info(f"kicked {i.user.id} from {message.chat.id}")
                await asyncio.sleep(0.1)  # Add a small delay to avoid rate limiting
            except ChatAdminRequired:
                logging.error("Bot is not an admin. Please make me an admin to ban members.")
                await bot.send_message(message.chat.id, "Make me admin to ban all members.")
                return  # Stop further execution if the bot is not an admin
            except UserNotParticipant:
                logging.warning(f"{i.user.id} is not a participant or is already banned.")
            except Exception as e:
                logging.error(f"Failed to kick {i.user.id}: {str(e)}")
                
        logging.info("Process completed")
        await bot.send_message(message.chat.id, "Ban all process completed!")
    except Exception as e:
        logging.error(f"Error during process: {str(e)}")
        await bot.send_message(message.chat.id, "There was an error while banning members.")
