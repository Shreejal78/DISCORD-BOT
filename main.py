
import os
import discord
from flask import Flask
from threading import Thread
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise ValueError("DISCORD_TOKEN is missing!")

# --- 1. Flask Web Server ---
app = Flask(__name__)

@app.route("/")
def home():
    return "PASA ESPORTS Bot is active and running!"

def run_web():
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

def keep_alive():
    t = Thread(target=run_web, daemon=True)
    t.start()

# --- 2. Ordinal Suffix ---
def get_ordinal_suffix(n):
    if 11 <= n % 100 <= 13:
        return "th"
    return {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")

# --- 3. Discord Bot ---
intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in successfully as {client.user}")

WELCOME_CHANNEL_ID = 1559107368292458537  # Replace with your channel ID

@client.event
async def on_member_join(member):
    welcome_channel = member.guild.get_channel(WELCOME_CHANNEL_ID)

    if welcome_channel:
        position = member.guild.member_count
        position_str = f"{position}{get_ordinal_suffix(position)}"

        message = (
            f"Hello, {member.mention}. Welcome to PASA ESPORTS "
            f"Discord channel. You're the {position_str} member "
            "to join. Be respectful to all other members."
        )

        await welcome_channel.send(message)
    else:
        print("Welcome channel not found. Check the channel ID.")

# --- 4. Main Execution ---
if __name__ == "__main__":
    keep_alive()
    client.run(TOKEN)
