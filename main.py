import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging

# Konfiguriere das Logging
logging.basicConfig(
    level=logging.INFO,  # Setze auf DEBUG für detailliertere Logs
    format='%(asctime)s:%(levelname)s:%(name)s: %(message)s'
)

logger = logging.getLogger('discord')

# Lade Umgebungsvariablen aus der .env Datei
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

if not TOKEN:
    logger.error("DISCORD_TOKEN ist nicht gesetzt. Bitte überprüfe deine .env Datei.")
    exit(1)

# Setze die Intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True  # Stelle sicher, dass die Gilden-Intents aktiviert sind

# Initialisiere den Bot
bot = commands.Bot(command_prefix="/", intents=intents, help_command=None)

# Funktion zum Laden der Cogs
async def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                logger.info(f'Erweiterung {filename} geladen.')
            except Exception as e:
                logger.error(f'Fehler beim Laden der Erweiterung {filename}:', exc_info=e)

# Starte den Bot
async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

if __name__ == "__main__":
    import asyncio
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot wurde manuell beendet.")
    except Exception as e:
        logger.error("Ein unerwarteter Fehler ist aufgetreten:", exc_info=e)
