import scrapingLogic as SL
import schedule
import time
import json
import sys
import math

# Data is passed in from runner.py
data = sys.argv[1]
locations = json.loads(data)
show_similar_result = locations.pop(0) == "ON"
rate = float(locations.pop(0))
# Recognizes if search is based on rpm or offer. rpm doesn't go very high while offer does
if rate <= 7.00:
    minRPM = rate
    minOffer = math.inf
else:
    minRPM = math.inf
    minOffer = rate
maxWeight = float(locations.pop(0))
origin = locations.pop(0)
start_date = locations.pop(0)
end_date = locations.pop(0)

# Define a job wrapper to pass parameters to the job function
def job_wrapper():
    SL.job(show_similar_result, minRPM, minOffer, maxWeight, origin, end_date, start_date, locations)

# Run job once before scheduling
job_wrapper()
# Schedule the job to run every hour
schedule.every().hour.do(job_wrapper())  # Change This Line Based On Desired Time For The Job

while True:
    schedule.run_pending()
    time.sleep(1)