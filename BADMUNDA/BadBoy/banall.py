import asyncio
import logging
from pyrogram import Client, filters

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

@Client.on_message(filters.command("banall") & filters.group)
async def start_banall(Badmunda, message):
    chat = message.chat
    a = await Badmunda.get_chat_member(chat.id, 'me')  # Check if the bot has admin rights
    if a.status != "administrator":
        # If the bot doesn't have admin privileges, send a message and exit
        return await Badmunda.send_message(chat.id, "Promote me to admin😭")

    # Send an initial message to notify that the banning process is starting
    x = await Badmunda.send_message(chat.id, "Hey, it's Pb Bot Spam... Starting the ban process.")

    done = 0
    failed = 0
    try:
        # Iterating over all chat members
        async for u in Badmunda.get_chat_members(chat.id):
            user = u.user
            try:
                # Ban each user
                if user.is_bot or user.id == Badmunda.id:  # Skip the bot itself
                    continue
                await Badmunda.ban_chat_member(chat.id, user.id)
                done += 1
            except Exception as err:
                logging.error(f"Pb Bot Spam - [INFO]: Failed to ban {user.id} - {str(err)}")
                failed += 1
    except Exception as e:
        logging.error(f"Pb Bot Spam - [ERROR]: {str(e)}")
        await Badmunda.send_message(chat.id, "There was an error during the banning process.")

    # Delete the initial message after the process is complete
    await x.delete()

    # Send a completion message with statistics
    await Badmunda.send_message(chat.id, f"Members Banned ✓ \n\n Banned {done} users\n Failed {failed} users")

