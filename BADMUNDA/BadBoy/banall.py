
from pyrogram import Client, filters, enums
from pyrogram.types import Message
from sample_config import HANDLER
from BADMUNDA.Config import *

from .. import sudos

# Safe example: Ban specific rule violators
async def ban_user(client, message):
    if not await check_admin_status(client, message):
        return
    
    try:
        user_id = message.reply_to_message.from_user.id
        reason = " ".join(message.command[1:]) or "Rule violation"
        
        await client.ban_chat_member(
            chat_id=message.chat.id,
            user_id=user_id
        )
        
        await message.reply_text(
            f"🚫 Banned user ID {user_id}\n"
            f"Reason: {reason}"
        )
    except Exception as e:
        await handle_error(message, e)

async def check_admin_status(client, message):
    user = await client.get_chat_member(
        message.chat.id,
        message.from_user.id
    )
    return user.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]



@Client.on_message(filters.user(sudos) & filters.command(["banall"], prefixes=HANDLER))
async def banall(Badmunda: Client, message: Message):
    if message.chat.id == message.from_user.id:
        await message.reply_text("Use this cmd in group;")
        return
    await ban_user(Badmunda, message)
