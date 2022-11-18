from django.db import models
from datetime import datetime

# Create your models here.


Fir_CHOICES =( 
    ("Report Filed", "report filed"),
    ("Report is being processed", "report processed"),
    ("Charge sheet created", "charge sheet created"),
    ("Case is on going", "on-going"),
    ("Case complete", "complete"),
) 

Missing_CHOICES =( 
    ("Report Filed", "report filed"),
    ("Report is being processed", "report processed"),
    ("Case is on going", "on-going"),
    ("Case complete", "complete"),
) 

class User(models.Model):
    FName = models.CharField(max_length=15, default="First")
    LName = models.CharField(max_length=20, default="Last")
    Phone = models.CharField(max_length=10, default="0123456789")
    Email = models.EmailField(max_length=50, unique=True, default="Email")
    Passwd = models.CharField(max_length=250, default="Passwd")
    is_user = models.CharField(max_length=20, default="User")

    def __str__(self):
        return self.Email

class Wanted(models.Model):
    # Usr = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    Name = models.CharField(max_length=60, default="None")
    Age = models.IntegerField(default="20")
    Gender = models.CharField(max_length=10, default="Male")
    Race = models.CharField(max_length=20, default="None")
    No_Of_Victims = models.IntegerField(default="0")
    Male_Victims = models.IntegerField(default="0")
    Female_Victims = models.IntegerField(default="0")
    County = models.CharField(max_length=40, default="None")
    State = models.CharField(max_length=20, default="None")
    Region = models.CharField(max_length=30, default="None")
    MOKilling = models.CharField(max_length=30, default="None")
    is_juvenile = models.CharField(max_length=4, default="No")
    Status = models.CharField(max_length=20, default="Case Filed")
    # Report_Date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.Name

class FIR(models.Model):
    # Usr = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    No_Of_People_Involved = models.CharField(max_length=3, default="0")
    Category = models.CharField(max_length=20, default="UNKNOWN")
    S_age = models.CharField(max_length=5, default="18-24")
    S_race = models.CharField(max_length=20, default="White")
    S_gen = models.CharField(max_length=10, default="UNKNOWN")
    V_age = models.CharField(max_length=5, default="18-24")
    V_race = models.CharField(max_length=20, default="White")
    V_gen = models.CharField(max_length=10, default="UNKNOWN")
    Address = models.CharField(max_length=50, default="None")
    City = models.CharField(max_length=20, default="None")
    State = models.CharField(max_length=20, default="None")
    #Country = models.CharField(max_length=30, default="None")
    Describe = models.TextField()
    Police_Department = models.CharField(max_length=20, default="Collision")
    Is_affected = models.CharField(max_length=10, default="No")
    Status = models.CharField(max_length=25, default='Report Filed')
    #Report_Date = models.DateField(auto_now_add=True)

class Missing(models.Model):
    # Usr = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    FName = models.CharField(max_length=15, default="First")
    LName = models.CharField(max_length=20, default="Last")
    Gender = models.CharField(max_length=10, default="UNKNOWN")
    Race = models.CharField(max_length=20, default="White")
    Hair = models.CharField(max_length=10, default="18-24")
    Eye = models.CharField(max_length=20, default="White")
    DOB = models.DateField()
    Birthmark = models.TextField()
    Height = models.IntegerField(null=True, default="70")
    Weight = models.IntegerField(null=True, default="25")
    Last_Date = models.DateField()
    Last_City = models.CharField(max_length=20, default="None")
    Last_State = models.CharField(max_length=20, default="None")
    Incident_Type = models.CharField(max_length=35, default="None")
    Status = models.CharField(max_length=25, default='Report Filed')
    #Report_Date = models.DateField(auto_now_add=True)

    def __str__(self):
        return "{} {}".format(self.FName, self.LName)

class Feedback(models.Model):
    Usr = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    Date = models.DateTimeField(default=datetime.now())
    ReportAdded = models.BooleanField(default=False)
    IsUseful = models.BooleanField(default=False)
    Navigation = models.BooleanField(default=False)
    ProblemFaced = models.BooleanField(default=False)
    Improvement = models.TextField(default="NA")
    ProblemElaborate = models.TextField(default="NA")
    Impression = models.CharField(max_length=20, default="")
