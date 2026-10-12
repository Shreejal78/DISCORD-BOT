import discord
from flask import Flask
from threading import Thread

# --- 1. Flask Web Server (Keeps Render Free Tier Alive) ---
app = Flask('')

@app.route('/')
def home():
    return "PASA ESPORTS Bot is active and running!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

# --- 2. Helper Function for Ordinal Suffix (e.g., 8th, 21st) ---
def get_ordinal_suffix(n):
    if 11 <= n <= 13:
        return 'th'
    return {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')

# --- 3. Discord Bot Logic ---
intents = discord.Intents.default()
intents.members = True  # Required to detect when members join

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in successfully as {client.user}')

@client.event
async def on_member_join(member):
    # Looks for a channel named 'welcome', falls back to system channel
    welcome_channel = discord.utils.get(member.guild.text_channels, name='welcome')
    if not welcome_channel:
        welcome_channel = member.guild.system_channel
        
    if welcome_channel:
        position = member.guild.member_count
        position_str = f"{position}{get_ordinal_suffix(position)}"
        
        message = (
            f"Hello, {member.mention}. Welcome to PASA ESPORTS discord channel. "
            f"You're the {position_str} member to join. Be respectful to all other members."
        )
        await welcome_channel.send(message)

# --- 4. Main Execution ---
if __name__ == '__main__':
    keep_alive()
    # Your token is placed directly here
    client.run('MTU1OTEzOTg5OTY2MjI3MDU3NA.Ge9H2H.l2ajOl5YxalCQTRJgomu9pQUVfNYesfJh705is')