import json
import os.path

DEFAULT_PREFIX = '!'
PREFIXES_PATH = 'data/prefixes.json'


def get_prefix(bot, message):
    if not message.guild or not os.path.isfile(PREFIXES_PATH):
        return DEFAULT_PREFIX
    with open(PREFIXES_PATH, 'r') as file:
        prefixes = json.load(file)
    server_id = str(message.guild.id)
    return prefixes.get(server_id, DEFAULT_PREFIX)
