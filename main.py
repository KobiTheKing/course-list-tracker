import smshandler
import tracker
import threading

# Used to setup the program
def main():
    #smsThread = threading.Thread(target = smshandler.setup)
    tracker.tracking = True
    trackerThread = threading.Thread(target = tracker.track)
    trackerThread.start()
    smshandler.setup()


if __name__ == "__main__":
    main()