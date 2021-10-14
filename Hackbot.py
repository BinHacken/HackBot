# Invite Link:
# discord.com/oauth2/authorize?client_id=894589289323692124&scope=bot

import discord
import os
import subprocess
import sys
from random import randint

from discord import message


class RoleReactClient(discord.Client):
    # stolen from https://github.com/Rapptz/discord.py/blob/master/examples/reaction_roles.py
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ID of message that can be reacted to to add role
        self.role_message_id = 760650447727624263
        self.emoji_to_role = {
            # [ID emoji]: [ID role]
            # ID of role associated with partial emoji object 'greenaxe' -> Hacker
            894607266794336286: 731897726392074351,
            # ID of role associated with partial emoji object 'bingener' -> Studi
            895695507547107329: 537243714205122560
        }

    async def on_raw_reaction_add(self, payload):
        """Gives a role based on a reaction emoji."""
        # Make sure that the message the user is reacting to is the one we care about
        if payload.message_id != self.role_message_id:
            return

        try:
            # print(payload.emoji.id)
            role_id = self.emoji_to_role[payload.emoji.id]
        except KeyError:
            # If the emoji isn't the one we care about then exit as well.
            return

        guild = self.get_guild(payload.guild_id)
        if guild is None:
            # Check if we're still in the guild and it's cached.
            return

        role = guild.get_role(role_id)
        if role is None:
            # Make sure the role still exists and is valid.
            return

        try:
            # Finally add the role
            await payload.member.add_roles(role)
            print(str(role) + " given to " + str(payload.member.name))
        except discord.HTTPException:
            # If we want to do something in case of errors we'd do it here.
            pass

    async def on_raw_reaction_remove(self, payload):
        """Removes a role based on a reaction emoji."""
        # Make sure that the message the user is reacting to is the one we care about
        if payload.message_id != self.role_message_id:
            return

        try:
            role_id = self.emoji_to_role[payload.emoji.id]
        except KeyError:
            # If the emoji isn't the one we care about then exit as well.
            return

        guild = self.get_guild(payload.guild_id)
        if guild is None:
            # Check if we're still in the guild and it's cached.
            return

        role = guild.get_role(role_id)
        if role is None:
            # Make sure the role still exists and is valid.
            return

        member = guild.get_member(payload.user_id)
        if member is None:
            # Makes sure the member still exists and is valid
            return

        try:
            # Finally, remove the role
            await member.remove_roles(role)
            print(str(role) + " removed from " + str(member.name))
        except discord.HTTPException:
            # If we want to do something in case of errors we'd do it here.
            pass


# This bot requires the members and reactions intents.
intents = discord.Intents.default()
intents.members = True
client = RoleReactClient(intents=intents)
lastMessage = None

@client.event
async def on_message(message):
    # make sure to not get triggered by own messages
    if message.author == client.user:
        return
    # put cntent of message in variable m for following comparisons
    m =message.content.lower()
    output = ""

    if m.startswith("help") or m.startswith("/help"):
        output ="If you need help please contact a Member from the **Support-team** or **Orga-team**"
    elif m.startswith("hilfe") or m.startswith("/hilfe"):
        output ="Wenn du Hilfe braucht, kontaktiere bitte ein Mitgleid aus dem **Support-team** oder **Orga-team**"
    elif m.startswith("easteregg") or m.startswith("/easteregg"):
        output ="Glückwunsch, du hast ein schlecht verstecktes **Easteregg** gefunden"
    else:   # no matching keywords
        return 

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

token_path = 'token.txt'

if os.path.exists(token_path):
    with open(token_path, 'r') as file:
        token = file.read().replace('\n', '')
else:
    #token = input("Discord Token:")
    #with open(token_path, 'w') as file:
    #    file.write(token)
    token = 'WKsoYQCoAM7Q3Gl6vn1RUy0yVi7K9zvr' #here for test purposes. will be changed and removed later.

client.run(token)
