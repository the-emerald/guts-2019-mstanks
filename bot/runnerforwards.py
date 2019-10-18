from bot.forwards import ForwardsBot
from bot.common.servercomms import ServerComms

gs = ServerComms('127.0.0.1', 8052)
bot = ForwardsBot(gs, "TeamA:Bot1")
while True:
    bot.rx()
    bot.move()
