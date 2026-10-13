import os
import discord
from discord import app_commands
from flask import Flask
from threading import Thread

# Securely load credentials from environment variables
TOKEN = os.getenv('BOT_TOKEN')

# Read numeric ID safely as an integer
try:
    MY_USER_ID = int(os.getenv('MY_USER_ID', 0))
except ValueError:
    MY_USER_ID = 0

class UltimateBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.all() 
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        await self.tree.sync()
        print(f'Logged in as {self.user}!')

client = UltimateBot()

@client.tree.command(name="ping", description="Ping the tech support administrator for help.")
async def ping_support(interaction: discord.Interaction):
    support_mention = f"<@{MY_USER_ID}>" if MY_USER_ID else "Admin"
    await interaction.response.send_message(
        f"🔔 {interaction.user.mention} has requested tech support! {support_mention} has been notified.",
        allowed_mentions=discord.AllowedMentions(users=True)
    )

app = Flask('')
@app.route('/')
def home(): 
    return "Bot is online!"

def run(): 
    app.run(host='0.0.0.0', port=8080)

Thread(target=run).start()

if TOKEN:
    client.run(TOKEN)
else:
    print("Error: BOT_TOKEN environment variable is missing!")
