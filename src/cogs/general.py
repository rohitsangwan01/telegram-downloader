import logging
import os
import shutil
import socket    
from telegram import Update
from telegram.ext import ContextTypes
from ..middlewares.auth import auth_required
from ..middlewares.handlers import command_handler

logger = logging.getLogger(__name__)

DOWNLOAD_TO_DIR = os.getenv("DOWNLOAD_TO_DIR")

# List of available commands
commands = {
    "/start": "Start the bot",
    "/help": "Get help",
    "/info": "Get user and chat info",
    "/storage": "Get available storage information",
    "/status": "Get downloading files status",
    "/ip": "Get ip address"
}


@command_handler("help")
async def help_command(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a list of available commands to the user."""
    commands_list = "The following commands are available:\n" + "\n".join(
        [f"{key} - {value}" for key, value in commands.items()]
    )
    await update.message.reply_text(
        f"{commands_list}\n\nSend me a file and I'll download it to `{DOWNLOAD_TO_DIR}`.",
        parse_mode="markdown",
    )


@command_handler("start")
async def start(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a start message to the user."""
    user = update.effective_user
    await update.message.reply_html(
        f"Hi {user.mention_html()}! I'm a bot that can download files for you. "
        "Send me a file and I'll download it for you.\n\n"
        "Use /help to see available commands."
    )


@command_handler("info")
async def info(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Send user and chat IDs to the user."""
    user = update.effective_user
    await update.message.reply_text(
        f"*User ID*: {user.id}\n*Chat ID*: {update.effective_chat.id}",
        parse_mode="markdown",
    )


@command_handler("storage")
async def storage(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Send available storage information of the specified folder."""
    if os.path.exists(DOWNLOAD_TO_DIR):
        total, used, free = shutil.disk_usage(DOWNLOAD_TO_DIR)
        await update.message.reply_text(
            f"📂 *Folder*:   `{DOWNLOAD_TO_DIR}`\n"
            f"🟣 *Total Space*:   `{total // (2**30)} GB`\n"
            f"🟠 *Used Space*:   `{used // (2**30)} GB`\n"
            f"🟢 *Free Space*:    `{free // (2**30)} GB`",
            parse_mode="markdown",
        )
    else:
        await update.message.reply_text("The specified folder does not exist.")

@command_handler("ip")
@auth_required
async def get_ip(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Get ip address of your device"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80)) # Attempt to connect to Google DNS server
        ip = s.getsockname()[0]
        await update.message.reply_text(f"Your IP address is: {ip}")
        s.close()
    except:
        update.message.reply_text("Failed to get IP address.")
