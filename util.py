import discord

async def execute_command(bot, msg, txt, ctx):
    cmd, *args = txt.split(" ")
    chan = msg.channel
    match cmd:
        case "!!on":
            ctx["online"] = True
            await bot.alert_change(bot.get_active_chan())
        case "!!off":
            ctx["online"] = False
            await bot.alert_change(bot.get_active_chan())
        case "!check":
            ctx["online"] = bot.is_online()
            com = "Com" if ctx["online"] else "Sem"
            await chan.send(f"{com} Energia")
        case "!on?":
            com = "Com" if ctx["online"] else "Sem"
            await chan.send(f"{com} Energia")
        case "!here":
            ctx["active_chan_id"] = chan.id
            await chan.send("Ok!")
        case "!pong":
            if args:
                for person in args:
                    ctx["pings"].remove(person)
                await chan.send(f"Removed: {' '.join(args)} from future mentions")
        case "!ping":
            if args:
                for person in args:
                    ctx["pings"].append(person)
                await chan.send(f"Added: {' '.join(args)} to future mentions")
            else:
                await chan.send("pong")
        case default:
            await chan.send("""wtf?

Lista de comandos:
```
!on?        | pergunta se, na última vez que o teste foi feito, o site da FATEC estava funcionando
!check      | testa agora se o site da FATEC está funcionando
!here       | define o canal em que atualizações sobre o status da FATEC devem ser enviadas
!ping @nome | adiciona @nome na próxima vez que o status do site da FATEC mudar
!pong @nome | remove @nome na próxima vez que o status do site da FATEC mudar
```
""")

