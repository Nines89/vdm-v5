
import discord
from discord.ext import commands
from discord import app_commands

from core.dice_engine import roll_v5


class Dice(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="roll",
        description="Esegue un tiro di dado V5"
    )
    @app_commands.describe(
        pool="Numero totale di dadi",
        hunger="Livello di Fame del personaggio",
        difficulty="Successi richiesti",
        private="Rendere privato il risultato?"
    )
    async def roll(
        self,
        interaction: discord.Interaction,
        pool: int,
        hunger: int,
        difficulty: int,
        private: bool = False
    ):

        try:
            result = roll_v5(
                pool=pool,
                hunger=hunger,
                difficulty=difficulty
            )

        except ValueError as error:
            await interaction.response.send_message(
                str(error),
                ephemeral=True
            )
            return

        # Visualizzazione dei dadi
        dice_display = []

        for die in result["dice"]:
            prefix = "F" if die["is_hunger"] else "N"
            dice_display.append(
                f"`{prefix}:{die['value']}`"
            )

        # Descrizione dell'esito
        outcomes = {
            "success": "SUCCESSO",
            "critical": "CRITICAL SUCCESS",
            "messy_critical": "MESSY CRITICAL",
            "failure": "FALLIMENTO",
            "bestial_failure": "BESTIAL FAILURE"
        }

        colors = {
            "success": discord.Color.green(),
            "critical": discord.Color.gold(),
            "messy_critical": discord.Color.dark_red(),
            "failure": discord.Color.light_grey(),
            "bestial_failure": discord.Color.red()
        }

        outcome = result["outcome"]

        embed = discord.Embed(
            title=f"🎲 Tiro V5 - {outcomes[outcome]}",
            color=colors[outcome]
        )

        embed.add_field(
            name="Pool",
            value=f"{pool} dadi",
            inline=True
        )

        embed.add_field(
            name="Fame",
            value=f"{hunger}",
            inline=True
        )

        embed.add_field(
            name="Difficoltà",
            value=f"{difficulty}",
            inline=True
        )

        embed.add_field(
            name="Risultati",
            value=" ".join(dice_display),
            inline=False
        )

        embed.add_field(
            name="Successi",
            value=(
                f"{result['successes']} "
                f"/ {difficulty}"
            ),
            inline=True
        )

        embed.add_field(
            name="Critici",
            value=f"{result['critical_pairs']}",
            inline=True
        )

        embed.set_footer(
            text="N = Dado normale | F = Dado Fame"
        )

        await interaction.response.send_message(
            embed=embed,
            ephemeral=private
        )


async def setup(bot):
    await bot.add_cog(Dice(bot))
