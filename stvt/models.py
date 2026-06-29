from django.db import models
#reg form
class Reg(models.Model):
    name = models.CharField(max_length=100)
    rollno = models.CharField(max_length=20)
    email = models.EmailField(null=True, blank=True)
    mobile = models.IntegerField()
    course = models.CharField(max_length=100)
    branch = models.CharField(max_length=100,default='Unknown')
    password = models.CharField(max_length=100)  # In real apps, use hashed passwords

    def __str__(self):
        return self.name
    
        
#student login
class StudentLogin(models.Model):
    name = models.CharField(max_length=100)
    rollno = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=100)  # for simplicity, no encryption
    email = models.EmailField(unique=True)  # <-- Add this line


    def __str__(self):
        return self.rollno

#adminlogin
class AdminLogin(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)  # Note: This is plain text; use hashed passwords in production

    def __str__(self):
        return self.username
    
#lor submitation
class LORSubmission(models.Model):
    mobile = models.IntegerField()
    address = models.TextField()
    image = models.ImageField(upload_to='lor_images/')

    def __str__(self):
        return self.mobile


#feeschallan
class FeesChallan(models.Model):
    email = models.EmailField()
    uid = models.CharField(max_length=20)
    date = models.DateField()
    name = models.CharField(max_length=100)
    clg = models.CharField(max_length=200)
    mobile = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.uid})"
    
class Challan(models.Model):
    name = models.CharField(max_length=100)


#batch allotment
class BatchAllotment(models.Model):
    id=models.AutoField(primary_key=True) 
    email = models.EmailField()
    uid = models.CharField(max_length=20)
    receipt = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    father = models.CharField(max_length=100)
    college = models.CharField(max_length=150)
    mobile = models.IntegerField(blank=True, null=True)
    address = models.TextField()
    course = models.CharField(max_length=50)
    year = models.CharField(max_length=10)
    duration = models.CharField(max_length=10)
    eng_branch = models.CharField(max_length=50)
    date = models.DateField()
    batch_code=models.CharField(max_length=5,null=True,blank=True)
    project_code=models.CharField(max_length=5,null=True,blank=True)
    project = models.CharField(max_length=250)
    report_to=models.CharField(max_length=20,null=True,blank=True)
    photo = models.ImageField(upload_to='photos/',null=True, blank=True)
    is_approved = models.BooleanField(default=False) #for certificate approval
    is_idcard_approved = models.BooleanField(default=False) 
    
    def __str__(self):
        return self.name

    
    

    
#contact form
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.IntegerField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    
    def __str__(self):
        return self.name
    
    


class Certificate(models.Model):
    certificate_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    rollno = models.IntegerField()

    def __str__(self):
        return self.certificate_number
