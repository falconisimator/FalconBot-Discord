import random
import os
import re
import csv
import time
import math
import asyncio
import aiohttp
import json
import discord
import requests
import pandas as pd
import simpy as sp
import numpy as np
import scipy as scp
import scipy.signal as sig
from discord import Game
from discord.ext.commands import Bot
import matplotlib
from matplotlib import rcParams
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab


BOT_PREFIX = ("?","^","~")
TOKEN = "Token"  # Get at discordapp.com/developers/applications/me

client = Bot(command_prefix=BOT_PREFIX)


#rcParams['text.usetex'] = True

path = os.getcwd()
print(path)



#################################################################################
##Commands

@client.command(name='8ball',
                description="Answers a yes/no question.",
                brief="Answers from the beyond.",
                aliases=['eight_ball', 'eightball', '8-ball'],
                pass_context=True)
async def eight_ball(context):
    possible_responses = [
        'That is a resounding no',
        'It is not looking likely',
        'Too hard to tell',
        'It is quite possible',
        'Definitely',
    ]
    await client.say(random.choice(possible_responses) + ", " + context.message.author.mention)


@client.command(pass_context=True)
async def ping(ctx):
    channel = ctx.message.channel
    t1 = time.perf_counter()
    await client.send_typing(channel)
    t2 = time.perf_counter()
    embed=discord.Embed(title=None, description='Ping: {}'.format(round((t2-t1)*1000)), color=0x2874A6)
    await client.say(embed=embed)


@client.command(pass_context=True)
async def bitcoin():
    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    async with aiohttp.ClientSession() as session:  # Async HTTP request
        raw_response = await session.get(url)
        response = await raw_response.text()
        response = json.loads(response)
        await client.say("Bitcoin price is: $" + response['bpi']['USD']['rate'])


@client.command()
async def square(number):
    squared_value = int(number) * int(number)
    await client.say(str(number) + " squared is not " + str(squared_value))

@client.command(pass_context=True)
async def annoy(context):
    for i in range(0,5):
        await client.say(context.message.author.mention + " Wanted me to annoy you " + context.message.mentions[0].mention)
        time.sleep(5)

@client.command(pass_context=True,
                description="Further Help",
                brief="Further help and bot details")
async def morehelp():
	await client.say("http://mrfalcon.net/falconbot-commands/")


@client.command()
async def step(num,den):
    try:
        num=tuple(map(int,num.split(',')))
        den=tuple(map(int,den.split(',')))
        
        tf= sig.lti(num,den)
        t, s = sig.step(tf)
        plt.plot(t, s)
        plt.xlabel('Time / s')
        plt.ylabel('Displacement / m')
        plt.savefig(path+'/step.png')
        plt.clf()
        await client.upload(path+"/step.png")
    except:
        await client.say("You dun :truck:'d up")

@client.command(pass_context=True)
async def decompose(context):
	print(context.message.edited_timestamp)
	print(context.message.timestamp)
	print(context.message.tts)
	print(context.message.content)
	print(context.message.embeds)
	print(context.message.channel)
	print(context.message.server)
	print(context.message.mentions)
	print(context.message.channel_mentions)
	print(context.message.role_mentions)
	print(context.message.id)
	print(context.message.attachments)
	print(context.message.pinned)
	print(context.message.reactions)
	print(context.message.system_content)
	await client.say('```context.message.edited_timestamp: '+str(context.message.edited_timestamp)+
		'\n context.message.timestamp: '+str(context.message.timestamp)+
		'\n context.message.tts: '+str(context.message.tts)+
		'\n context.message.content: '+str(context.message.content)+
		'\n context.message.embeds: '+str(context.message.embeds)+
		'\n context.message.channel: '+str(context.message.channel)+
		'\n context.message.server: '+str(context.message.server)+
		'\n context.message.mentions: '+str(context.message.mentions)+
		'\n context.message.channel_mentions: '+str(context.message.channel_mentions)+
		'\n context.message.role_mentions: '+str(context.message.role_mentions)+
		'\n context.message.id: '+str(context.message.id)+
		'\n context.message.attachments: '+str(context.message.attachments)+
		'\n context.message.pinned: '+str(context.message.pinned)+
		'\n context.message.reactions: '+str(context.message.reactions)+
		'\n context.message.system_content: '+str(context.message.system_content)+'```') 

@client.command(pass_context=True)
async def steal(context, emo, title):
	try:
		emoID=re.findall(r'\d+',emo)[0]
		try:
			url='https://cdn.discordapp.com/emojis/'+emoID
		except:
			await client.say("you broke something")
		print(url)
		image=requests.get(url).content
		await client.create_custom_emoji(context.message.server, name=title, image=image)
		await client.say('Emoji stolen :spy:')
	except:
		await client.say("You dun :truck:'d up")

@client.command(pass_context=True)
async def stealu(context, url, title):
	
	image=requests.get(url).content
	await client.create_custom_emoji(context.message.server, name=title, image=image)
	await client.say('Emoji stolen :spy:')

@client.command(pass_context=True)
async def kill(context):
	if(context.message.mentions[0]!='Falcon#6280'):
		await client.change_nickname(context.message.mentions[0],'Ded '+ context.message.mentions[0].display_name)
		await client.say(context.message.mentions[0].mention + 'Killed')
	else:
		await client.say('Nice Try')

global data

@client.command(pass_context=True,
				aliases=['ld', 'load'])
async def load_data(context,name):
	global data
	if not os.path.isfile(name+'.csv'):
		url=context.message.attachments[0]['url']
		if url.endswith('.csv'):
			r = requests.get(url, allow_redirects=True)
			open(name +'.csv', 'wb').write(r.content)
			data = pd.read_csv(name+'.csv')
			
			await client.say("`"+url+"` saved to: "+name+'.csv as:\n```'+str(data[0:5])+'\n...\n...\n'+str(data[len(data)-5:len(data)])+'```')
		else:
			await client.say('File is not a .csv')
	else:
		await client.say(name+'.csv already exists')
		data = pd.read_csv(name+'.csv')
			
		await client.say(name+'.csv loaded as:\n```'+str(data[0:5])+'\n...\n...\n'+str(data[len(data)-5:len(data)])+'```')

@client.command(pass_context=True,
				aliases=['pd', 'plot'])
async def plot_data(context,y,*x):
	global data
	if x:
		plt.plot(data[x[0]],data[y],linewidth=1)
	else:
		plt.plot(data[y],linewidth=1)
	plt.savefig(path+'/data.png',dpi=600)
	plt.clf()
	await client.upload(path+"/data.png")

@client.command()
async def restart():
	await client.say("Restarting...")
	os.system("python3 FalconBot.py")
	time.sleep(0.5) # 200ms to CTR+C twice
	quit()


#################################################################################
#D&D functions

@client.command(pass_context=True,
                description="Balance of Characters Money",
                brief="Returns The balance of a characters money")
async def bank(context,*character,**action):
	try:
		with open('bank.csv') as csvfile:
			reader = csv.DictReader(csvfile)
			flag=0
			for row in reader:
				if row['Character'].find(''.join(character).title())!=-1 and str(context.message.author)==row['Id'] :
					flag=1
					await client.say(row['Character'] + ' has: ' + row['Platinum']+' Platinum, '+ row['Gold']+' Gold, '+ row['Silver']+' Silver, and '+ row['Copper']+' Copper')
			if (flag==0):
				await client.say('Character: "'+''.join(character)+'" not found under your user: '+ str(context.message.author))
	except:
		await client.say("You dun :truck:'d up")

global rolls
rolls=[]

@client.command(description="Records rolls on d20s",
                brief="Records rolls on d20s")
async def roll(comm,*roll):
	global rolls
	if comm=='add':
		for num in roll[0].split(','):
			if (int(num)<21 and int(num)>0):
				rolls.append(int(num))	
			else:
				await client.say('Please add a d20 roll')
		await client.say('Roll(s) added')
	elif comm=='plot':
		x=[1,2,3,4,5,6,7,8,9,10,11,12, 13, 14, 15, 16, 17, 18, 19, 20];
		count=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0, 0, 0, 0]

		for i in range(0,len(rolls)):
			for r in range(0,len(x)):
				if rolls[i]==x[r]:
					count[r]=count[r]+1

		m=np.mean(rolls)
		n=len(rolls)

		sum=0
		for num in rolls:
			sum=sum+(num-m)**2

		sd=np.sqrt(1/n*sum)

		
		gauss=(sd/0.4)*max(count)*(1/(sd*np.sqrt(2*3.14)))*2.71**(-(1/2)*((np.linspace(0,20,200)-m)/sd)**2)

		plt.bar(x,count)
		plt.plot(np.linspace(0,20,200),gauss,'r')
		plt.xlabel('Rolls')
		plt.ylabel('Count')
		plt.savefig(path+'/rolls.png')
		plt.clf()
		await client.upload(path+"/rolls.png")
	elif comm=='clear':
		rolls=[]
		await client.say('cleared')
	elif comm=='list':
		await client.say(rolls)
	print(str(comm)+' '+str(roll))


#################################################################################
#Utilities

@client.event
async def on_ready():
    await client.change_presence(game=Game(name="with humans"))
    print("Logged in as " + client.user.name)

async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)
	

client.loop.create_task(list_servers())
client.run(TOKEN)
