import smshandler
import hikari_lightbulb_bot.bot as bot
import tracker
import threading
import datamanager

# Used to setup the program
def main():
    #lock = threading.Lock()
    #datamanager.setLock(lock)

    tracker.tracking = True
    #trackerThread = threading.Thread(target = tracker.track)
    #trackerThread.start()

    #smsThread = threading.Thread(target = bot.setup)
    #smsThread.start()

    #await tracker.track()

    #await bot.setup()

    bot.setup()


if __name__ == "__main__":
    main()