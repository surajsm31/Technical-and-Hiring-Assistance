from django.db import models

# Create your models here.
class developer(models.Model):
    fname = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    education = models.CharField(max_length=50)
    skill = models.CharField(max_length=50)
    experience = models.CharField(max_length=50)
    github = models.CharField(max_length=50)
    portfolio = models.CharField(max_length=50)
    gender = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    graduationpy = models.IntegerField()
    contact = models.CharField(max_length=10)
    password = models.CharField(max_length=20)
    # security = models.CharField(max_length=1000,default=" ")
    # answer = models.CharField(max_length=500,default=" ")
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.email


class domain(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70)
    contact = models.IntegerField()
    domain = models.CharField(max_length=50)
    resume = models.FileField(upload_to="Resume")
    mark = models.IntegerField(default=0)
    date = models.DateTimeField()



# Domain Quiz Databases
class python(models.Model):
    Question = models.CharField(max_length=500)
    option1 = models.CharField(max_length=300)
    option2 = models.CharField(max_length=300)
    option3 = models.CharField(max_length=300)
    option4 = models.CharField(max_length=300)
    Correctoption = models.CharField(max_length=300,default=0)

class java(models.Model):
    Question = models.CharField(max_length=500)
    option1 = models.CharField(max_length=300)
    option2 = models.CharField(max_length=300)
    option3 = models.CharField(max_length=300)
    option4 = models.CharField(max_length=300)
    Correctoption = models.CharField(max_length=300,default=0)

class php(models.Model):
    Question = models.CharField(max_length=500)
    option1 = models.CharField(max_length=300)
    option2 = models.CharField(max_length=300)
    option3 = models.CharField(max_length=300)
    option4 = models.CharField(max_length=300)
    Correctoption = models.CharField(max_length=300,default=0)

class angular(models.Model):
    Question = models.CharField(max_length=500)
    option1 = models.CharField(max_length=300)
    option2 = models.CharField(max_length=300)
    option3 = models.CharField(max_length=300)
    option4 = models.CharField(max_length=300)
    Correctoption = models.CharField(max_length=300,default=0)

class cplus(models.Model):
    Question = models.CharField(max_length=500)
    option1 = models.CharField(max_length=300)
    option2 = models.CharField(max_length=300)
    option3 = models.CharField(max_length=300)
    option4 = models.CharField(max_length=300)
    Correctoption = models.CharField(max_length=300,default=0)

class aws(models.Model):
    Question = models.CharField(max_length=500)
    option1 = models.CharField(max_length=300)
    option2 = models.CharField(max_length=300)
    option3 = models.CharField(max_length=300)
    option4 = models.CharField(max_length=300)
    Correctoption = models.CharField(max_length=300,default=0)

class question(models.Model):
    Question = models.CharField(max_length=500)
    option1 = models.CharField(max_length=300)
    option2 = models.CharField(max_length=300)
    option3 = models.CharField(max_length=300)
    option4 = models.CharField(max_length=300)
    Correctoption = models.CharField(max_length=300)
    category =models.CharField(max_length=100)



class category(models.Model):
    category =models.CharField(max_length=100)
    Domain =models.CharField(max_length=100)


#Quiz Answer Table
class answer(models.Model):
    # qid = models.CharField(max_length=10000)
    qans = models.CharField(max_length=30000)



#HR Section
class hr(models.Model):
    Name = models.CharField(max_length=100)
    Email = models.CharField(max_length=100)
    Company = models.CharField(max_length=100)
    Designation = models.CharField(max_length=100)
    Password = models.CharField(max_length=100)
    Contact = models.IntegerField()
    Address = models.CharField(max_length=100)
    verified = models.BooleanField(default=False)

#Admin Section
class Admin(models.Model):
    Name = models.CharField(max_length=100)
    Email = models.CharField(max_length=100)
    Password = models.CharField(max_length=100)
    Role = models.CharField(max_length=100)
    Contact = models.IntegerField()

#Feedback section
class Feedback(models.Model):
    Name = models.CharField(max_length=100)
    Email = models.CharField(max_length=100)
    Message = models.CharField(max_length=10000)