import smshandler
import tracker
import threading
import datamanager

# Used to setup the program
def main():
    lock = threading.Lock()
    datamanager.setLock(lock)

    tracker.tracking = True
    trackerThread = threading.Thread(target = tracker.track)
    trackerThread.start()

    smsThread = threading.Thread(target = smshandler.setup)
    smsThread.start()


if __name__ == "__main__":
    main()