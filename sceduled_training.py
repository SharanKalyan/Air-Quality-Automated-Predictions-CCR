import schedule
import time
from historical_training import *


#schedule.every(2).hours.do(main)
#schedule.every().day.at("10:30").do(main) ## everyday
#schedule.every(30).seconds.do(main)
#schedule.every(90).minutes.do(main)
#schedule.every().hour.do(job)
schedule.every(30).days.at("13:45").do(main)
# schedule.every(5).to(10).minutes.do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)
# schedule.every().minute.at(":17").do(job)



while True:
    schedule.run_pending()
    time.sleep(1)
