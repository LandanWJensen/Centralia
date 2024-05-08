import discord
from discord.ext import commands

class Roles:
    def __init__(self):
        emoji_role = {
            self.crypto_emoji : '\U0001F4BB',
            self.stocks_emoji : '\U0001F4C8',
            self.deals_emoji : '\U0001F911',
        }

        self.role_message = 1215357531702951946
        self.added_roles_channel = 1215402119423598665

    async def setup_roles(self, ctx):

        # Create a message and add reactions to it
        message = await ctx.send('Choose your roles')
        reactions = [self.crypto_emoji, self.stocks_emoji, self.deals_emoji]
        for emoji in reactions:
            await message.add_reaction(emoji)

    async def add_role(self, payload):
        # Check if the reaction is added to the correct message and by a non-bot user
        if payload.message_id == self.role_message:
            channel = payload.channel_id
            message = payload.message_id
            # Check which reaction was added
            emoji = payload.emoji.name  # For custom emojis, use payload.emoji.id

            if emoji == self.crypto_emoji:
                role_name = 'Crypto'
                print("Crypto")
            elif emoji == self.stocks_emoji:
                role_name = 'Stocks'
                print("Stocks")
            elif emoji == self.deals_emoji:
                role_name = 'Deals'
                print("Deals")
            return role_name


    async def remove_role(self, payload):
        # Check if the reaction is added to the correct message and by a non-bot user
        if payload.message_id == self.role_message:
            channel = payload.channel_id
            message = payload.message_id
            # Check which reaction was added
            emoji = payload.emoji.name  # For custom emojis, use payload.emoji.id

            if emoji == self.crypto_emoji:
                role_name = 'Crypto'
                print("Crypto")
            elif emoji == self.stocks_emoji:
                role_name = 'Stocks'
                print("Stocks")
            elif emoji == self.deals_emoji:
                role_name = 'Deals'
                print("Deals")
            return role_name

    async def assign_role(self, ctx, member, role_name):
        # Get the role object based on the provided role name
        role = discord.utils.get(member.guild.roles, name=role_name)
        if role:
            # Assign the role to the user who invoked the command
            await member.add_roles(role)
            await ctx.send(f'Role "{role_name}" assigned to {member.display_name}')
        else:
            await ctx.send(f'Role "{role_name}" not found.')

    async def unassign_role(self, ctx, member, role_name):
        role = discord.utils.get(member.guild.roles, name=role_name)
        if role:
            # Assign the role to the user who invoked the command
            await member.remove_roles(role)
            await ctx.send(f'Role "{role_name}" removed from {member.display_name}')
        else:
            await ctx.send(f'Role "{role_name}" not found.')