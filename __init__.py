import discord
from discord.ext import commands
from slotMachine import SlotMachine
import os
from discord.ext.commands.errors import *
import requests

#from roles import Roles
from finance import Stocks
from finance import Crypto

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

slot_machine = SlotMachine()
#roles_class = Roles()
stocks_class = Stocks()
crypto_class = Crypto()

@bot.command(name='stock')
async def stock(ctx, tick):
    await stocks_class.check_stock(ctx, tick)

@bot.command(name='crypto')
async def crypto(ctx, *coins):
    await crypto_class.check_coin(ctx, coins)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        if ctx.command and ctx.command.name == 'spin':
            await ctx.reply("Use the following format: !spin [bet]")

@bot.event
async def on_ready():
    target_channel = bot.get_channel(1215470440298840164)
    cwd = os.getcwd()
    print("Current working directory:", cwd)
    #if target_channel:
    #    await target_channel.send('Bot locked in')

@bot.command(name='leaderboard')
async def leaderboard(ctx):
    await ctx.reply (await slot_machine.leaderboard(ctx), allowed_mentions = discord.AllowedMentions.none())


@bot.command(name='spin')
async def spin(ctx, bet, no_of_spins = None):
    if no_of_spins == None:
        no_of_spins = 1
    try:
        no_of_spins = int(no_of_spins)
    except ValueError:
        no_of_spins = 1
    if no_of_spins < 1:
        no_of_spins = 1
    if no_of_spins > 5:
        await ctx.reply("Maximum of 5 spins")
        return
    check = await slot_machine.check_funds(ctx, bet, int(no_of_spins))
    if check == 0: 
        return
    for x in range(no_of_spins):
        outcome = await slot_machine.spin(ctx, bet)
        await ctx.reply(f'{outcome[0]} \n {outcome[1]}')

@bot.command(name='bank')
async def check_bank(ctx):
    await slot_machine.check_bank(ctx)
    await ctx.reply(f'Balance: {await slot_machine.check_bank(ctx)}')

@bot.command(name='reload')
async def reload(ctx):
    await slot_machine.reload_bank()

@bot.command(name='hello')
async def hello(ctx):
    await ctx.send('Hello!')

@bot.command(name='list_symbols')
async def list_symbols(ctx):
    await ctx.send(slot_machine.symbols)

"""@bot.command(name='setup_roles')
async def setup_roles(ctx):
    await roles_class.setup_roles(ctx)

@bot.event
async def on_raw_reaction_add(payload):
    role_name = await roles_class.add_role(payload)
    guild_id = payload.guild_id
    guild = bot.get_guild(guild_id)
    role = discord.utils.get(guild.roles, name=role_name)
    added_roles_channel = bot.get_channel(1215402119423598665)

    if role:
        # Assign the role to the user
        await guild.get_member(payload.user_id).add_roles(role)
        target_channel = added_roles_channel
        username = bot.get_user(payload.user_id).name
        message = await target_channel.send(f'role {role} added to {username}')

@bot.event
async def on_raw_reaction_remove(payload):
    role_name = await roles_class.remove_role(payload)
    guild_id = payload.guild_id
    guild = bot.get_guild(guild_id)
    role = discord.utils.get(guild.roles, name=role_name)
    added_roles_channel = bot.get_channel(1215402119423598665)

    if role:
        # Assign the role to the user
        await guild.get_member(payload.user_id).remove_roles(role)
        target_channel = added_roles_channel
        username = bot.get_user(payload.user_id).name
        message = await target_channel.send(f'role {role} removed {username}')

@bot.command(name='assign')
async def assign_role(ctx, member: discord.Member, role_name):
    await roles_class.assign_role(ctx, member, role_name)

@bot.command(name='unassign')
async def unassign_role(ctx, member: discord.Member, role_name):
    await roles_class.unassign_role(ctx, member, role_name)
    """

@bot.event
async def on_member_join(member):
    # Replace 'YourRoleName' with the actual name of the role you want to assign
    role = discord.utils.get(member.guild.roles, name='Viewer')

    if role:
        await member.add_roles(role)
        print(f"Assigned role '{role.name}' to {member.display_name}")

bot.run('MTIxNTA4MzE0NDIwMjY4MjQxOA.Gy4WGd._LB0Zslb1FzDDQ5tFF1Q6v3Lx0e5kzHMp28H9o')