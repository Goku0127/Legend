from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from sample_config import HANDLER
from BADMUNDA.Config import *
from .. import sudos

async def handle_error(message, error):
    """Proper error handling function"""
    await message.reply_text(f"❌ Error: {str(error)}")

async def check_admin_status(client, message):
    """Verify user is admin/owner"""
    try:
        user = await client.get_chat_member(
            message.chat.id,
            message.from_user.id
        )
        return user.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]
    except Exception as e:
        await handle_error(message, e)
        return False

async def ban_user(client, message):
    """Safely ban a single user"""
    try:
        # Check if message is a reply
        if not message.reply_to_message:
            await message.reply_text("❗ Reply to a user's message to ban them!")
            return

        # Get target user
        target = message.reply_to_message.from_user
        reason = " ".join(message.command[1:]) or "Rule violation"

        # Confirm ban
        confirm_buttons = InlineKeyboardMarkup(
            [[
                InlineKeyboardButton("✅ Confirm Ban", callback_data=f"ban_confirm_{target.id}"),
                InlineKeyboardButton("❌ Cancel", callback_data="ban_cancel")
            ]]
        )
        
        await message.reply_text(
            f"⚠️ Confirm banning {target.mention}?\nReason: {reason}",
            reply_markup=confirm_buttons
        )

    except Exception as e:
        await handle_error(message, e)

@Client.on_callback_query(filters.regex(r"^ban_confirm_"))
async def confirm_ban(client, callback_query):
    """Handle ban confirmation"""
    try:
        target_id = int(callback_query.data.split("_")[2])
        user = await client.get_chat_member(
            callback_query.message.chat.id,
            callback_query.from_user.id
        )

        if user.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
            await callback_query.answer("You're not authorized!", show_alert=True)
            return

        await client.ban_chat_member(
            chat_id=callback_query.message.chat.id,
            user_id=target_id
        )
        
        await callback_query.message.edit_text(
            f"🚫 Successfully banned user ID: {target_id}",
            reply_markup=None
        )
        
    except Exception as e:
        await handle_error(callback_query.message, e)

@Client.on_callback_query(filters.regex("^ban_cancel$"))
async def cancel_ban(client, callback_query):
    """Handle ban cancellation"""
    await callback_query.message.edit_text("✅ Ban request cancelled!", reply_markup=None)

@Client.on_message(filters.user(sudos) & filters.command(["ban"], prefixes=HANDLER) & filters.group)
async def safe_ban_command(client: Client, message: Message):
    """Safer ban command handler"""
    try:
        # Check admin status first
        if not await check_admin_status(client, message):
            await message.reply_text("❌ You need to be an admin to use this command!")
            return

        await ban_user(client, message)
        
    except Exception as e:
        await handle_error(message, e)
