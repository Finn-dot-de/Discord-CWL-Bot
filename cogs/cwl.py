import discord
from discord.ext import commands
from discord import app_commands
from tabulate import tabulate
import logging

from views.cwl_views import CWLAnmeldungView
from utils.validation import validate_townhall, validate_username
from utils.storage import init_db, add_entry, remove_entry, get_all_entries, get_db_connection, get_cwl_list_from_db

logger = logging.getLogger('discord')

class CWLCog(commands.Cog):
    ADMIN_ROLE_NAME = "CWL-Leiter"

    def __init__(self, bot):
        self.bot = bot
        init_db()
        logger.info('CWLCog initialisiert.')

    @app_commands.command(name='cwl_loeschen', description='Löscht einen CWL-Eintrag. (Nur für CWL-Leiter)')
    @app_commands.describe(username='Benutzername des Eintrags, der gelöscht werden soll')
    async def cwl_loeschen(self, interaction: discord.Interaction, username: str):
        logger.info(f'/cwl_loeschen Befehl aufgerufen von {interaction.user} für Benutzer: {username}')
        if self.ADMIN_ROLE_NAME in [role.name for role in interaction.user.roles]:
            remove_entry(username)
            await interaction.response.send_message(
                f'{username} wurde erfolgreich aus der CWL-Liste gelöscht.', 
                ephemeral=True
            )
            logger.info(f'{username} aus der CWL-Liste entfernt.')
        else:
            await interaction.response.send_message(
                "Du hast keine Berechtigung, diesen Befehl zu verwenden.", 
                ephemeral=True
            )
            logger.warning(f'{interaction.user} hat versucht, /cwl_loeschen ohne Berechtigung zu verwenden.')

    @app_commands.command(name='cwl_loeschen_all', description='Löscht alle CWL-Einträge. (Nur für CWL-Leiter)')
    async def cwl_loeschen_all(self, interaction: discord.Interaction):
        logger.info(f'/cwl_loeschen_all Befehl aufgerufen von {interaction.user}')
        if self.ADMIN_ROLE_NAME in [role.name for role in interaction.user.roles]:
            conn = None
            try:
                conn = get_db_connection()
                if conn:
                    with conn.cursor() as cur:
                        cur.execute('DELETE FROM cwl')
                        conn.commit()
                        await interaction.response.send_message(
                            "Alle CWL-Einträge wurden erfolgreich gelöscht.", 
                            ephemeral=True
                        )
                        logger.info('Alle CWL-Einträge wurden gelöscht.')
            except Exception as e:
                logger.error("Fehler beim Löschen aller Einträge:", exc_info=e)
                await interaction.response.send_message(
                    "Es ist ein Fehler aufgetreten. Bitte versuche es später erneut.",
                    ephemeral=True
                )
            finally:
                if conn:
                    conn.close()
        else:
            await interaction.response.send_message(
                "Du hast keine Berechtigung, diesen Befehl zu verwenden.", 
                ephemeral=True
            )
            logger.warning(f'{interaction.user} hat versucht, /cwl_loeschen_all ohne Berechtigung zu verwenden.')

    @app_commands.command(name='cwl_liste', description='Zeigt die aktuelle CWL-Liste an.')
    async def cwl_liste(self, interaction: discord.Interaction):
        logger.info(f'/cwl_liste Befehl aufgerufen von {interaction.user}')
        entries = get_all_entries()
        if entries:
            table_data = []
            for index, (username, townhall) in enumerate(entries, start=1):
                table_data.append([index, username, townhall])

            table = tabulate(table_data, headers=["Nr.", "Benutzername", "Rathaus-Level"], tablefmt="grid")

            await interaction.response.send_message(
                f"**Aktuelle CWL-Anmeldungen:**\n```\n{table}\n```", 
                ephemeral=False
            )
            logger.info('CWL-Liste angezeigt.')
        else:
            await interaction.response.send_message(
                "Noch niemand hat sich für die CWL eingetragen.", 
                ephemeral=True
            )
            logger.info('CWL-Liste ist leer.')

    async def get_cwl_list_from_db(self):
        return await get_cwl_list_from_db()

    @app_commands.command(name='cwl_anmeldung', description='Startet die CWL-Anmeldung.')
    async def cwl_anmeldung(self, interaction: discord.Interaction):
        logger.info(f'/cwl_anmeldung Befehl aufgerufen von {interaction.user}')
        try:
            view = CWLAnmeldungView()
            await interaction.response.send_message(
                "Klicke auf den Button, um dich für die CWL anzumelden:", 
                view=view, 
                ephemeral=False
            )
            logger.info('CWL-Anmeldung View gesendet.')
        except Exception as e:
            logger.error("Fehler beim Senden der CWL-Anmeldung View:", exc_info=e)
            try:
                await interaction.response.send_message(
                    "Es ist ein Fehler aufgetreten. Bitte versuche es später erneut.",
                    ephemeral=True
                )
            except Exception as send_error:
                logger.error("Fehler beim Senden der Fehlermeldung:", exc_info=send_error)


    @app_commands.command(name='help', description='Zeigt diese Hilfsnachricht an.')
    async def help_command(self, interaction: discord.Interaction):
        logger.info(f'/help Befehl aufgerufen von {interaction.user}')
        help_text = """
**Verfügbare Befehle:**

**/cwl_anmeldung**
Startet den CWL-Anmeldeprozess. Klicke auf den angezeigten Button, um dich anzumelden.

**/cwl_liste**
Zeigt die aktuelle Liste der CWL-Anmeldungen in Tabellenform an.

**/cwl_loeschen <Benutzername>**
Löscht den CWL-Eintrag des angegebenen Benutzers. *Nur für Benutzer mit der Rolle 'CWL-Leiter' verfügbar.*

**/cwl_loeschen_all**
Löscht alle CWL-Anmeldungen. *Nur für Benutzer mit der Rolle 'CWL-Leiter' verfügbar.*

**/help**
Zeigt diese Hilfsnachricht an.

**Hinweis:**
Alle Befehle sind jetzt Slash-Commands und einige Befehle erfordern spezielle Berechtigungen.
        """
        await interaction.response.send_message(help_text, ephemeral=True)
        logger.info('Hilfsnachricht gesendet.')

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f'{self.bot.user} ist jetzt online!')
        try:
            synced = await self.bot.tree.sync()
            logger.info(f'{len(synced)} Befehle synchronisiert.')
        except Exception as e:
            logger.error('Fehler beim Synchronisieren der Befehle:', exc_info=e)

async def setup(bot):
    await bot.add_cog(CWLCog(bot))
    logger.info('CWLCog geladen.')
