from pymongo import MongoClient
import os
import discord
from discord.ext import commands
import pytz
from random import randint
client = commands.Bot(command_prefix=">",intents=discord.Intents.all())

cluster = MongoClient("mongodb+srv://ekfar1:1234@cluster0.dhafo.mongodb.net/bd?retryWrites=true&w=majority")
db = cluster["bd"]
collection = db["coolname"]

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online,
        activity=discord.Game("ekfara bot")) 
@client.command()
async def create(ctx,years,floor,*,im):#создать анкету
    name = ctx.author.mention
    collection.insert_one({"_id":str(name),'years': str(years),'floor': str(floor),'im': str(im),'ava': str(ctx.author.avatar_url)})
@client.command()
async def ekfar(ctx):#help
    embed = discord.Embed(title="Это бот знакомств от экфара")
    embed.add_field(name="Бот работает через лс",value="Просто напиши ему команду",inline=False)
    embed.add_field(name="Чтобы создать анкету пропиши",value=">create возраст пол текст",inline=False)
    embed.add_field(name="Чтобы найти случайную анкету пропиши",value=">random",inline=False)
    embed.add_field(name="Чтобы найти анкету по возрасту пропиши",value=">find возраст",inline=False)
    embed.add_field(name="Чтобы вызвать это меню пропиши",value=">ekfar",inline=False)
    embed.add_field(name="Удачного пользования!",value="Создан тут https://discord.gg/sPruSKek2n",inline=False)
    await ctx.send(embed=embed)    
@client.command()
async def admindata(ctx):
    data = collection.find()
    for d in data:
        print(d)

client.run(os.environ['token'])
