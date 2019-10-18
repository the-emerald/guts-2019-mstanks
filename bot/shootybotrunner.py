from bot.shootybot import ShootyBot
from bot.common.servercomms import ServerComms

gs = ServerComms('127.0.0.1', 8052)
bot = ShootyBot(gs, "TeamA:Bot1")
while True:
    bot.rx()
    bot.action()
