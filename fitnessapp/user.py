
class User:

  def __init__(self, fname = None, lname = None, uname = None, password = None, startweight = None, currentweight = None, goalweight = None, age = None, height = None,  metrics = None, gender = None, watergoal = None):
    self.fname = fname
    self.lname = lname
    self.username = uname
    self.password = password
    self.currentweight = currentweight
    self.goalweight = goalweight
    self.age = age
    self.height = height
    self.startweight = startweight
    self.metrics = metrics
    self.gender = gender
    self.watergoal = watergoal

  def __str__(self):
      return ('Name: {self.fname} {self.lname} \nAge: {self.age} \nCurrent Weight: {self.currentweight} \nGoal Weight: {self.goalweight}'.format(self=self))

  def updateweight(self, delta):
      self.currentweight +=delta

  def checkweight(self):
      return abs(self.goalweight - self.currentweight)

  def updateage(self, age):
      self.age = age

  def updateheight(self, height):
      self.height = height

  def updatename(self, first, last):
      self.fname = first
      self.lname = last

  def updatepassword(self, newpassword):
      self.password = newpassword

  def updatemetrics(self, metrics):
      self.metrics = metrics

  def updategoalweight(self, goal):
      self.goalweight = goal

  def updatewatergoal(self, watergoal):
      self.watergoal = watergoal
