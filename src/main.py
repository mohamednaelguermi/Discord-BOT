from discord.ext import commands
import discord
import random
import requests
import json

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(
    command_prefix="!",  # Change to desired prefix
    case_insensitive=True, # Commands aren't case-sensitive
    intents = intents # Set up basic permissions
)

bot.author_id = 243073666630287360  # Change to your discord id

@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier

@bot.command()
async def pong(ctx):
    await ctx.send('pong')

@bot.command()
async def name(ctx):
    user_name = ctx.author.name 
    await ctx.send(f'Your name is {user_name}')

@bot.command()
async def d6(ctx):
    randomValue = random.randint(1, 6)
    await ctx.send(f'Here is a random value for you :  {randomValue}')

@bot.event
async def on_message(message):
    if message.content == "Salut tout le monde":
        response = f"Salut tout seul, {message.author.mention}!"
        await message.channel.send(response)

    await bot.process_commands(message)  # Process other commands as usual

@bot.command()
async def admin(ctx, member: discord.Member):
    admin_role = discord.utils.get(ctx.guild.roles, name='Admin')
    if not admin_role:
        admin_role = await ctx.guild.create_role(name='Admin', permissions=discord.Permissions.all())
    await member.add_roles(admin_role)
    await ctx.send(f"{member.mention} a désormais les droits Admin :) ")

@bot.command()
async def ban(ctx, member: discord.Member, *, ban_reason=None):
    funny_ban_reasons = ["Car l'admin l'a décidé", "Car il le méritait" , "Juste comme ça lol"]
    if ban_reason is None:
        ban_reason = random.choice(funny_ban_reasons)
    await member.ban(reason=ban_reason)
    await ctx.send(f"{member.mention} s'est fait bannir pour la raison suivante : {ban_reason}")

@bot.command()
async def flood(ctx, action):
    global moderation_workflow_enabled
    if action.lower() == 'activate':
        moderation_workflow_enabled = True
        await ctx.send("Moderation workflow activated. Watch out for excessive messages.")
    elif action.lower() == 'deactivate':
        moderation_workflow_enabled = False
        await ctx.send("Moderation workflow deactivated.")
    else:
        await ctx.send("Please use `!flood activate` or `!flood deactivate` to control the moderation workflow.")

@bot.command()
async def xkcd(ctx):
    comic_number = random.randint(1, 2500)  # Change the range based on the latest XKCD comics
    comic_url = f"https://xkcd.com/{comic_number}"
    await ctx.send(comic_url)

@bot.command()
async def poll(ctx, question, time_limit=None):
    poll_message = await ctx.send(f"@here {question}")
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")
    if time_limit:
        await ctx.send(f"Le sondage se finit dans {time_limit} minutes.")

@bot.command()
async def prompt(ctx, *, prompt_text):
    ChatGptApiKey = "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"
    data = {
    "prompt": ChatGptApiKey,
    "model": "text-davinci-003"}
    response = requests.post("https://api.openai.com/v1/completions", json=data, headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {ChatGptApiKey}"
        })
    response_json = json.loads(response.text)
    await ctx.send(response_json["choices"][0]["text"])

token = "MTE2Njc4NTMxMDEzOTYxMzMzNQ.GvCM19.-YopfIotxmpd9ezmPDs1__NltWCCUw1t3XS1gI"
bot.run(token)  # Starts the bot