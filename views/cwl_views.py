# cwl_views.py

import discord
from discord.ui import View, Button
from modals.cwl_modal import CWLAnmeldungModal
import logging

logger = logging.getLogger('discord')

class CWLAnmeldungView(View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Für CWL eintragen", style=discord.ButtonStyle.green)
    async def button_callback(self, interaction: discord.Interaction, button: Button):
        logger.info(f'Button "Für CWL eintragen" geklickt von {interaction.user}')
        try:
            modal = CWLAnmeldungModal()
            await interaction.response.send_modal(modal)
            logger.info('Modal erfolgreich gesendet.')
        except Exception as e:
            logger.error("Fehler beim Senden des Modals:", exc_info=e)
            try:
                await interaction.response.send_message(
                    "Es ist ein Fehler aufgetreten. Bitte versuche es später erneut.",
                    ephemeral=True
                )
            except Exception as send_error:
                logger.error("Fehler beim Senden der Fehlermeldung:", exc_info=send_error)
