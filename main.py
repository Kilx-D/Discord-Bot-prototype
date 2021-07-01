import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

#connects to discord
client = discord.Client()
sad_words = [
    "sad", "depressed", "depression", "unhappy", "miserable", "depressing",
    "fuck", "sussy", "bruh", "nigger", "pussy", "penis", "hype", "memes",
    "bitch", "idc", "wtf", "gay", "piss", "dank", "rad", "scp", "lol", "lmao",
    "magik", "no", "false", "fun", "bdsm", "poop"
]
starter_encouragements = ["stfu", "idc", "did i ask?"]

if "responding" not in db.keys():
    db["responding"] = True


def get_quote():
    #returns a random quote, while making a http request
    response = requests.get("https://zenquotes.io/api/random")
    #converts the response to json
    json_data = json.loads(response.text)
    #retrieves the quote from the response text and the author
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return quote


def update_happi(text):
    #if the list exist in the database
    if "le_happi" in db.keys():
        happi = db["le_happi"]
        happi.append(text)  #adds the new text into the list
        db["le_happi"] = happi  #saves the new list
    else:
        #if the list doesnt exist, create it with the text inside it
        db["le_happi"] = [text]


def delete_happi(index):
    happi = db["le_happi"]
    #checks if the inserted index is valid
    if len(happi) > index:
        #deletes the item inthe list wiht the index
        del happi[index]
        db["le_happi"] = happi


#creates an event
@client.event
#once the bot is loaded up and ready, it will automatically send a message
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Game("Going to rule the world"))



##client.event
#async def on_typing(channel, user, when):
#  await message.channel.send('I see you typing there {username}'.format(username = user.name))


@client.event
#checks if the sender of the message is not the bot itself, makes a command
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content.lower()

    if msg.startswith('$inspire'):
        quote = get_quote()
        await message.channel.send(quote)

    if db["responding"]:
        options = starter_encouragements
        if "le_happi" in db.keys():
            options += db["le_happi"]

        #checks to see if the word in the message is in the sad words list
        if any(word.lower() in msg for word in sad_words):
            #it then sends a random message from the starter encouragements list
            await message.channel.send(random.choice(options))

    if msg.startswith("$new"):
        #takes the new message
        happi = msg.split("$new ", 1)[1]
        #puts the new message intot he list in to the database
        update_happi(happi)
        #lets user know the message was added
        await message.channel.send("Message added")

    if msg.startswith("$del"):
        happi = []
        if "le_happi" in db.keys():
            #takes the index the user has specified
            index = int(msg.split("$del", 1)[1])
            delete_happi(index)
            happi = db["le_happi"]
            #tells user the items left in the list
        await message.channel.send(happi)

    if msg.startswith("$list"):
        le_happi = []
        if "le_happi" in db.keys():
            le_happi = db["le_happi"]
            
            
        await message.channel.send(le_happi)

    if msg.startswith("$spam"):
        value = msg.replace("$spam ", "")
        itere = value.split(" ", 1)[0]
        spam_message = value.split(" ", 1)[1]

        for i in range(int(itere)):
          if msg.startswith("$stop"):
            await message.channel.send("Execution has been terminated")
            break
          await message.channel.send(spam_message)

    if msg.startswith("$responding"):
        value = msg.split("$responding ", 1)[1]
        if value.lower() == "true":
            db["responding"] = True
            await message.channel.send("Responding is on.")
        else:
            db["responding"] = False
            await message.channel.send("Responding is off.")

      
    if msg.startswith("$commands"):
      await message.channel.send('''
      ```
      $inspire: generates an inspiring quote
      $responding [true or false]: sets if the bot is allow to respond or not
      $list: returns the possible responses
      $new [response to add]: gives the bot a new response
      $del [index number]: deletes a response based on it's index
      $spam [amount of times to spam] [what to spam]: spams a text a certain amount of times
      ```''')





#the bot token
access_token = os.environ['token1']

#runs the bot using the access token
keep_alive()
client.run(access_token)
