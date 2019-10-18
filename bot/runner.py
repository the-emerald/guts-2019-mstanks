from bot.emerald import EmeraldBot
from bot.servercomms import ServerComms

gs = ServerComms('127.0.0.1', 8052)

bot_1 = EmeraldBot(gs, "TeamA:Bot1")
while True:
    message = bot_1.game_server.readMessage()
    bot_1.forward_thing()
