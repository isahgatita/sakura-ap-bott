discord
from discord.ext import commands
import json
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

def load_data():
    try:
        with open("dados.json","r") as f:
            return json.load(f)
    except:
        return {"saldo":{}}

def save_data(data):
    with open("dados.json","w") as f:
        json.dump(data,f)

data = load_data()

aposta = {
    "ativa":False,
    "valor":0,
    "jogadores":[]
}

@bot.event
async def on_ready():
    print(f"Sakura AP online: {bot.user}")

@bot.command()
async def registrar(ctx):

    user = str(ctx.author.id)

    if user not in data["saldo"]:
        data["saldo"][user] = 100
        save_data(data)

        await ctx.send(f"🌸 {ctx.author.mention} recebeu 100 coins!")
    else:
        await ctx.send("Você já está registrado.")

@bot.command()
async def saldo(ctx):

    user = str(ctx.author.id)

    if user not in data["saldo"]:
        await ctx.send("Use !registrar primeiro")
        return

    await ctx.send(f"💰 Saldo: {data['saldo'][user]}")

@bot.command()
async def criar_ap(ctx, valor:int):

    aposta["ativa"] = True
    aposta["valor"] = valor
    aposta["jogadores"] = []

    await ctx.send(f"🔥 Apostado criado ({valor})\nDigite !entrar")

@bot.command()
async def entrar(ctx):

    user = str(ctx.author.id)

    if not aposta["ativa"]:
        await ctx.send("Nenhum AP ativo")
        return

    if data["saldo"][user] < aposta["valor"]:
        await ctx.send("Saldo insuficiente")
        return

    data["saldo"][user] -= aposta["valor"]
    aposta["jogadores"].append(user)

    save_data(data)

    await ctx.send(f"{ctx.author.mention} entrou no AP")

@bot.command()
async def vencedor(ctx, membro:discord.Member):

    if not aposta["ativa"]:
        await ctx.send("Nenhum AP ativo")
        return

    premio = aposta["valor"] * len(aposta["jogadores"])

    user = str(membro.id)

    if user not in data["saldo"]:
        data["saldo"][user] = 0

    data["saldo"][user] += premio
    save_data(data)

    await ctx.send(f"🏆 {membro.mention} ganhou {premio} coins")

    aposta["ativa"] = False
    aposta["jogadores"] = []


bot.run(os.getenv("TOKEN"))
