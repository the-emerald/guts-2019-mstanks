from bot.emerald import EmeraldBot
from bot.servercomms import ServerComms

gs = ServerComms('127.0.0.1', 8052)
bot = EmeraldBot(gs, "TeamA:Bot1")
while True:
    bot.rx()
    bot.forward_thing()
