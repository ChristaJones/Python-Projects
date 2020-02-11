
class Water:

  def __init__(self, amount, goal, date, metrics):
      self.amount = amount
      self.goal = goal
      self.date = date
      self.metrics = metrics

  def __str__(self):
     measurement = {1: 'oz', 0:'ml'}
     return ({'{self.date}\n{self.amount}/{self.goal} {m}'}.format(self = self, m = measurement[self.metrics] ))

  def addwater(self, wateramount):
      self.amount+=wateramount

  def checkgoal(self):
      measurement = {1: 'oz', 0:'ml'}
      if(self.amount>self.goal):
          print("You have exceeded your goal")
      elif(self.amount == self.goal):
          print("You have met your goal")
      else:
           print("You need %d more oz to reach your goal" % (self.goal-self.amount))

  def updatewateramount(self,  wateramount):
      self.amount = wateramount
