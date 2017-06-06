import schedule
import time
import datetime
def job():
    print "I'm working...", str(datetime.datetime.now())[:19]

schedule.every(1).minutes.do(job)
schedule.every().hour.do(job)
schedule.every().day.at("10:30").do(job)
schedule.every().monday.do(job)
schedule.every().wednesday.at("13:15").do(job)

while True:
    schedule.run_pending()
    print str(datetime.datetime.now())[:19]
    time.sleep(1)
