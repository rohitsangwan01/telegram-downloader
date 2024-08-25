from .downloader import button, default_handler, download, status
from .error_handler import error_handler
from .general import help_command, info, start, storage

# Specify the commands for the bot
general_commands: list = [
    help_command,
    info,
    start,
    storage
]

downloader_commands: list = [
    button,
    download,
    status,
    default_handler,
]
