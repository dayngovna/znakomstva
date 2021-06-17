from pymongo import MongoClient
import os
import discord
from discord.ext import commands
import pytz
from random import randint
client = commands.Bot(command_prefix=">",intents=discord.Intents.all())

cluster = MongoClient("mongodb+srv://ekfar1:1234@cluster0.dhafo.mongodb.net/bd?retryWrites=true&w=majority")
bd = cluster["bd"]
collection = bd["coolname"]

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online,
        activity=discord.Game("ekfara bot")) 
@client.command()
async def create(ctx,years,floor,*,im):#создать анкету
    if collection.count_documents({"_id":ctx.author.mention}) == 1:
        collection.delete_one({"_id":ctx.author.mention})
    collection.insert_one({"_id":ctx.author.mention,'years': years,'floor': floor,'im': im,'ava': str(ctx.author.avatar_url)})

    for x in bd:
        if x['_id'] == ctx.author.mention:
            embed = discord.Embed(title=f'Анкета '+x['_id'])
            embed.set_thumbnail(url=x['ava'])
            embed.add_field(name="Возраст",value=x['years'])
            embed.add_field(name="Пол",value=x['floor'])
            embed.add_field(name="О себе",value=x['im'],inline=False)
            await ctx.author.send(embed=embed)
@client.command()
async def find(ctx,years):#поиск анкеты
        for xx in bd:
            print(xx)
            if xx['years'] == str(years):
                print("finded!")
                embed = discord.Embed(title=f'Анкета '+xx['_id'])
                embed.set_thumbnail(url=xx['ava'])
                embed.add_field(name="Возраст",value=xx['years'])
                embed.add_field(name="Пол",value=xx['floor'])
                embed.add_field(name="О себе",value=xx['im'],inline=False)
                await ctx.author.send(embed=embed)
            else:
                await ctx.author.send("Мы не нашли анкету,измените запрос")            
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
        await ctx.author.send(d)

client.run(os.environ['token'])
