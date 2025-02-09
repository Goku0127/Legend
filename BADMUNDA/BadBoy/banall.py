import asyncio
from pyrogram import Client, filters
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, FloodWait
from os import getenv
from sample_config import SUDO_USERS
@Client.on_message(filters.command("banall") & filters.group)
async def banall(bot, message):
    # Check if the user is a sudo user
    if str(message.from_user.id) not in SUDO_USERS:
        await message.reply("Sorry, only sudo users can use this command.")
        return
    
    try:
        # Use async for to iterate over the async generator
        async for i in bot.get_chat_members(message.chat.id):
            try:
                # Try banning the user
                await bot.ban_chat_member(chat_id=message.chat.id, user_id=i.user.id)
                await asyncio.sleep(0.1)  # Add a small delay to avoid rate limiting
            except ChatAdminRequired:
                await bot.send_message(message.chat.id, "Make me admin to ban all members.")
                return  # Stop further execution if the bot is not an admin
            except UserNotParticipant:
                # Skip users who are not participants or already banned
                pass
            except FloodWait as e:
                await asyncio.sleep(e.x)  # Wait for the flood time before trying again
            except Exception as e:
                pass  # Ignore other exceptions

        await bot.send_message(message.chat.id, "Ban all process completed!")
    except Exception as e:
        await bot.send_message(message.chat.id, "There was an error while banning members.")
