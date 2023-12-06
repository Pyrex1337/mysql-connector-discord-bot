import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio
import aiofiles
import mysql.connector

def is_allowed_role(role_id):
    async def predicate(ctx):
        role = ctx.guild.get_role(role_id)
        if role is None:
            return False
        return role in ctx.author.roles
    return commands.check(predicate)

load_dotenv()

TOKEN = "x"
DB_HOST = "x"
DB_USER = "x"           #doldur buraları
DB_PASSWORD = ""
DB_NAME = "x"

intents = discord.Intents.all()
intents.members = True
intents.guilds = True
intents.messages = True
intents.reactions = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot olarak giriş yapıldı: {bot.user.name} - {bot.user.id}')

@bot.command()
@is_allowed_role(1116438403215523931)
async def merhabapyrex28(ctx):
    await ctx.send("Merhaba.")

@bot.command()
async def pyrexhelp(ctx):
    author_name = ctx.author.name
    ad_soyad = f"{author_name}"

    embed = discord.Embed(title="PYR3XHELP", description="Kullanım:", color=discord.Color.red())
    embed.add_field(name="Ad Soyad Help)", value="!adsoyadhelp", inline=False)
    embed.add_field(name="Bilinmeyenli Sorgu Help", value="!bilinmeyen", inline=False)
    embed.add_field(name="Sms Bomber Help", value="!smshelp", inline=False)
    embed.add_field(name="Sherlock Tool Help", value="!sherlockhelp", inline=False)
    embed.add_field(name="Web sitemiz", value="pyrexbot.xyz", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def adsoyadsorgu(ctx):
    if ctx.guild is not None:
        await ctx.send("Bu komutu özel mesaj yoluyla kullanmalısınız.")
        return

    await ctx.send("Sorgulamak istediğiniz kişinin adını giriniz.")

    def check(msg):
        return msg.author == ctx.author and isinstance(msg.channel, discord.DMChannel)

    try:
        ad_msg = await bot.wait_for('message', check=check, timeout=60)
        ad = ad_msg.content

        await ctx.send("Sorgulamak istediğiniz kişinin soyadını giriniz.")
        soyad_msg = await bot.wait_for('message', check=check, timeout=60)
        soyad = soyad_msg.content

        await ctx.send("Sorgulamak istediğiniz kişinin ilini giriniz. (Bilmiyorsanız - yazın)")
        il_msg = await bot.wait_for('message', check=check, timeout=60)
        il = il_msg.content

        await ctx.send("Sorgulamak istediğiniz kişinin ilçesini giriniz. (Bilmiyorsanız - yazın)")
        ilce_msg = await bot.wait_for('message', check=check, timeout=60)
        ilce = ilce_msg.content

        embed = discord.Embed(title="Pyrexbot", description="Sorgu başlatılıyor.", color=discord.Color.red())
        embed.add_field(name=f"{ad}", value="{ad}", inline=False)
        embed.add_field(name=f"{soyad}", value="{soyad}", inline=False)
        embed.add_field(name=f"{il}", value="{il}", inline=False)
        embed.add_field(name=f"{ilce}", value="! PYR3X TH3 SANTA MUERTE#1337", inline=False)
        await ctx.send(embed=embed)

        cnx = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = cnx.cursor()

        if ilce == "-":
            if il == "-":
                query = f"SELECT * FROM `101m` WHERE ADI LIKE '{ad}' AND SOYADI LIKE '{soyad}'"
            else:
                query = f"SELECT * FROM `101m` WHERE ADI LIKE '{ad}' AND SOYADI LIKE '{soyad}' AND NUFUSIL LIKE '{il}'"
        else:
            if il == "-":
                query = f"SELECT * FROM `101m` WHERE ADI LIKE '{ad}' AND SOYADI LIKE '{soyad}' AND NUFUSILCE LIKE '{ilce}'"
            else:
                query = f"SELECT * FROM `101m` WHERE ADI LIKE '{ad}' AND SOYADI LIKE '{soyad}' AND NUFUSIL LIKE '{il}' AND NUFUSILCE LIKE '{ilce}'"

        cursor.execute(query)
        result = cursor.fetchall()

        filename = f"text/pyrexbot_{ad}_{soyad}.txt"

        async with aiofiles.open(filename, mode='w', encoding='utf-8') as file:
            column_names = [i[0] for i in cursor.description]
            column_names.remove("id")  
            column_names_line = "\t".join(column_names)
            await file.write(column_names_line + '\n')

            for row in result:
                row_values = [str(item) for item in row]
                row_values.remove(str(row[0]))  
                row_line = "\t".join(row_values)
                await file.write(row_line + '\n')

        file_message = f"Sorgu sonuçları"
        await ctx.author.send(file=discord.File(filename), content=file_message)

        cursor.close()
        cnx.close()

    except asyncio.TimeoutError:
        await ctx.author.send("Uzun süre yanıt vermediğiniz için zaman aşımına uğradı.")
        return

bot.run(TOKEN)