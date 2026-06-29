from django import forms

#reg form
from .models import Reg  # Tumhara model
class RegForm(forms.ModelForm):
    class Meta:
        model = Reg
        fields = ['name', 'rollno', 'email', 'mobile', 'course','branch', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

#student login
from .models import StudentLogin
class StudentLoginForm(forms.ModelForm):
    class Meta:
        model = StudentLogin
        fields = ['rollno', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': 'Enter Password'}),
        }



#forget password
class ForgetPasswordForm(forms.ModelForm):
    class Meta:
        model = StudentLogin
        fields = ['rollno', 'email']

        

#admin login
from .models import AdminLogin
class AdminLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

#lor submission
from .models import LORSubmission
class LORForm(forms.ModelForm):
    class Meta:
        model = LORSubmission
        fields = ['mobile', 'address', 'image']
        

#fees challan
from .models import FeesChallan
class FeesChallanForm(forms.ModelForm):
    class Meta:
        model = FeesChallan
        fields = ['email', 'uid', 'date', 'name', 'clg', 'mobile']

#batch allotment
from .models import BatchAllotment
class BatchAllotmentForm(forms.ModelForm):
    class Meta:
        model = BatchAllotment
        fields = '__all__'
 
        
#contact form
from .models import ContactMessage
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'mobile', 'subject', 'message']
        
        
#certificate
