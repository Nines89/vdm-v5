
import os
import discord

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ["DISCORD_TOKEN"]
GUILD = discord.Object(id=int(os.environ["GUILD_ID"]))


class Bot(commands.Bot):

    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=discord.Intents.default()
        )

    async def setup_hook(self):

        # Caricamento dei moduli
        await self.load_extension("commands.dice")

        # Sincronizzazione comandi
        self.tree.copy_global_to(guild=GUILD)
        await self.tree.sync(guild=GUILD)

        print("Comandi sincronizzati!")


client = Bot()


@client.tree.command(
    name="ping",
    description="Test di connessione"
)
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("pong")


client.run(TOKEN)
