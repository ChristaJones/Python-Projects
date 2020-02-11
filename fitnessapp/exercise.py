import datetime
from datetime import timedelta

class Exercise:

  def __init__(self, calories,starttime,endtime,date,name):
      self.calories = calories
      self.start = starttime
      self.end = endtime
      self.date = date
      self.name = name
      t1 = timedelta(hours=starttime.hour, minutes=starttime.minute, seconds=0)
      t2 = timedelta(hours=endtime.hour, minutes=endtime.minute, seconds=0)
      delta = t2 - t1
      duration = delta.seconds/60
      self.duration = duration

  def __str__(self):
      return ({'{self.name}\n{self.date}\nDuration:{self.duration} {self.calories} calories'}.format(self = self))

  def duration(self):
      return self.duration

  def updatetime(self, num, time):
      #0 start time
      #1 end time
      if num==0:
          self.start = time
      elif num==1:
          self.end = time

  def updatecalories(self, newcal):
        self.calories = newcal;

  def updatedate(self, newdate):
        self.date = newdate

  def changename(self, name):
        self.name = name


#date_entry = input('Enter a date in YYYY-MM-DD format')
#year, month, day = map(int, date_entry.split('-'))
#date1 = datetime.date(year, month, day)

#time_entry1 = input('Enter a start timee in HH-MM format')
#hour, minute= map(int, date_entry.split('-'))
#starttime = datetime.date()
