# Using Python 3.6, this script will not work with 3.7 at the current moment
import random
import asyncio
import aiohttp
import json
from discord import Game
from discord.ext.commands import Bot

BOT_PREFIX = ("$")
file = open('token.txt', 'r')
TOKEN = file.readline().strip()  #Go get a token at discordapp.com/developers/applications.  Place the token in a file called "token.txt" in the same directory as this script

client = Bot(command_prefix=BOT_PREFIX)

@client.command() #link the github page for this bot
async def github():
    await client.say("Learn more about this bot at https://github.com/amring777/DiscordBot9000")

@client.command(name='dice',
                aliases=['roll'],
                pass_context=True)
async def dice(context, *rolled): #roll some dice
    results = ' rolled '
    sum = 0
    for x in range(0, len(rolled)):
        currentDie = rolled[x].replace('D', 'd').split('d')
        if len(currentDie) != 2:
            await client.say("That format is incorrect")
            return
        for y in range(0, int(currentDie[0])):
            if y != 0 or x != 0:
                results += ' + '
            rollNumber = random.randint(1, int(currentDie[1]))
            sum += rollNumber
            results += str(rollNumber)
    await client.say(context.message.author.mention + results + ' = ' + str(sum))

@client.command(name='8ball',
                description="Answers a yes/no question.",
                brief="Answers from the beyond.",
                aliases=['eight_ball', 'eightball', '8-ball'],
                pass_context=True)
async def eight_ball(context): #get a random fortune for the user
    possible_responses = [
        'That is a resounding no',
        'It is not looking likely',
        'Too hard to tell',
        'It is quite possible',
        'Definitely',
    ]
    await client.say(random.choice(possible_responses) + ", " + context.message.author.mention)


@client.command()
async def square(number): #find the square of the given number
    squared_value = int(number) * int(number)
    await client.say(str(number) + " squared is " + str(squared_value))


@client.event
async def on_ready(): #set the name of what the bot is "Playing"
    await client.change_presence(game=Game(name="with Bjorn the Fell Handed"))
    print("Logged in as " + client.user.name)


@client.command()
async def bitcoin(): #find the current price of bitcoin
    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    async with aiohttp.ClientSession() as session:  # Async HTTP request
        raw_response = await session.get(url)
        response = await raw_response.text()
        response = json.loads(response)
        await client.say("Bitcoin price is: $" + response['bpi']['USD']['rate'])


async def list_servers(): #list all servers currently in
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)


client.loop.create_task(list_servers()) #print servers currently in
client.run(TOKEN)