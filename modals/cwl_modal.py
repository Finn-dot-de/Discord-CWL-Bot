# modals/cwl_modal.py

import discord
from discord.ui import Modal, TextInput
from utils.validation import validate_townhall, validate_username
import logging

from utils.storage import add_entry, test_entry_exists

logger = logging.getLogger('discord')

class CWLAnmeldungModal(Modal):
    def __init__(self):
        super().__init__(title="CWL Anmeldung")

        # Definieren der Textfelder innerhalb der __init__
        self.username = TextInput(
            label="Benutzername",
            placeholder="Dein Benutzername",
            required=True
        )
        self.townhall = TextInput(
            label="Rathaus-Level",
            placeholder="Dein Rathaus-Level (10-16)",
            required=True
        )

        self.add_item(self.username)
        self.add_item(self.townhall)

    async def on_submit(self, interaction: discord.Interaction):
        logger.info(f'Modal von {interaction.user} abgesendet.')
        username = self.username.value
        townhall = self.townhall.value

        # Validierung der Eingaben
        if not validate_townhall(townhall):
            await interaction.response.send_message(
                "Ungültiger Rathaus-Level. Bitte gib eine Zahl zwischen 10 und 16 ein.", 
                ephemeral=True
            )
            logger.warning(f'Ungültiger Rathaus-Level von {interaction.user}: {townhall}')
            return

        if not validate_username(username):
            await interaction.response.send_message(
                "Ungültiger Benutzername. Der Name muss mindestens 3 Zeichen lang sein und darf nur Buchstaben und Zahlen enthalten.", 
                ephemeral=True
            )
            logger.warning(f'Ungültiger Benutzername von {interaction.user}: {username}')
            return

        # Benutzer in die CWL-Liste eintragen
        user_entry = f"{username} (Rathaus: {townhall})"
        self.cwl_list = test_entry_exists(username)
        logger.info(f"Eintrag bereits vorhanden: {self.cwl_list}")

        if not self.cwl_list:
            try:
                add_entry(username, townhall)  # Kein await, da die Funktion synchron ist
                await interaction.response.send_message(
                    f'{username} mit Rathaus-Level {townhall} wurde erfolgreich für die CWL eingetragen!', 
                    ephemeral=True
                )
                logger.info(f'{user_entry} zur CWL-Liste hinzugefügt.')
            except Exception as e:
                logger.error(f'Fehler beim Eintragen: {e}')
                await interaction.response.send_message(
                    f'Beim Eintragen von {username} in die CWL-Liste ist ein Fehler aufgetreten. Bitte versuche es erneut.', 
                    ephemeral=True
                )
        else:
            await interaction.response.send_message(
                f'{username} ist bereits in der CWL-Liste eingetragen.', 
                ephemeral=True
            )
            logger.info(f'{user_entry} war bereits in der CWL-Liste.')
