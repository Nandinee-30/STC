# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login , logout
from django.contrib import messages

#index.html
def index(request):
    return render(request, 'index.html')

#adminlogin
from .forms import AdminLoginForm 
def admin_login_view(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_staff:
                login(request, user)
                return redirect('admin_panel')  # Your dashboard URL name
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AdminLoginForm()
    return render(request, 'admin_login.html', {'form': form})
from django.contrib.auth.decorators import login_required
@login_required

#adminpanel
def admin_panel_view(request):
    return render(request, 'admin_panel.html')  # make sure this template exists

def admin_logout_view(request):
    logout(request)
    return redirect('admin_login')  # ya jahan aap login page rakhna chahti ho

#about.html
def about(request):
    return render(request,'about.html')

#contact.html
def contact(request):
    return render(request,'contact.html')

# contact form
from .forms import ContactForm
from .models import ContactMessage
# Contact form view
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'contact.html', {'form': ContactForm(), 'success': True})
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

# Contact table view
def contact_table(request):
    contacts = ContactMessage.objects.all()
    return render(request, 'contact_table.html', {'contacts': contacts})

#delete contact
def delete_contact(request, id):
    contact = get_object_or_404(ContactMessage, id=id)
    contact.delete()
    return redirect('contact_table')

#thanku.html
def thanku(request):
    return render(request, 'thanku.html')

#regform
from .forms import RegForm
def reg(request):
    if request.method == 'POST':
        form = RegForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'reg.html', {'form': RegForm(), 'success': True})
    else:
        form = RegForm()
    return render(request, 'reg.html', {'form': form})

#create password student_login
from django.contrib.auth.hashers import make_password
def reg(request):
    if request.method == 'POST':
        form = RegForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.password = make_password(form.cleaned_data['password'])  # ✅ Good!
            student.save()
            return render(request, 'reg.html', {'form': RegForm(), 'success': True})
    else:
        form = RegForm()
    return render(request, 'reg.html', {'form': form})

#student dashboard
from .models import StudentLogin  # apne model ka import
def student_dashboard(request):
    rollno = request.session.get('student_rollno')
    if not rollno:
        return redirect('student_login')  # Agar login nahi hua
    try:
        student = Reg.objects.get(rollno=rollno)
        approved = BatchAllotment.objects.filter(name=student.name, is_approved=True).first()       
        idcard_approved = BatchAllotment.objects.filter(mobile=student.mobile, is_idcard_approved=True).first()
        return render(request, 'student_dashboard.html', {
            'student': student,
            'approved': approved,
            'idcard_approved':idcard_approved
        })
    except StudentLogin.DoesNotExist:
        return redirect('student_login')

#student_login create password
from django.contrib.auth.hashers import check_password
from .models import Reg
def student_login(request):
    if request.method == "POST":
        rollno=request.POST['rollno']
        print("Roll No. ", rollno)
        password=request.POST['password']
        print("password", password)
        try:
            student = Reg.objects.get(rollno=rollno)
            print("Student Data:",student)
            if check_password(password,student.password):
                request.session['student_rollno']=student.rollno
                    #login successfull
                return redirect('student_dashboard')
            else:
                return render(request,'student_login.html',{'error':'Invalid password'})
        except Reg.DoesNotExist:
            return render(request,'student_login.html',{'error':'Roll number not found'})
    return render(request,'student_login.html')           
  
            
#forget password
from django.contrib.auth.hashers import make_password
def forget_password_view(request):
    if request.method == 'POST':
        rollno = request.POST.get('rollno')
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        try:
            student = StudentLogin.objects.get(rollno=rollno, email=email)
            student.password = make_password(new_password)  # hash the new password
            student.save()
            return render(request, 'forget_password.html', {'message': 'Password updated successfully!'})
        except StudentLogin.DoesNotExist:
            return render(request, 'forget_password.html', {'error': 'Invalid Roll Number or Email'})
    return render(request, 'forget_password.html')


def view_registered_students(request):
    students = Reg.objects.all()
    return render(request, 'reg_table.html', {'students': students})

#regdelete
from django.shortcuts import render, get_object_or_404, redirect
from .models import Reg
def delete_student_login(request, id):
    student = get_object_or_404(Reg, id=id)
    student.delete()
    return redirect('registered_students')



#lorform
from .forms import LORForm
def lor_submission(request):
    if request.method == 'POST':
        form = LORForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lor')  # or a success page
    else:
        form = LORForm()
    return render(request, 'lor.html', {'form': form})

#lor table submission
from .models import LORSubmission
def lor_table_view(request):
    lors = LORSubmission.objects.all()
    return render(request, 'lor_table.html', {'lors': lors})

#lor delete
from .models import LORSubmission
def delete_lor(request, id):
    LORSubmission.objects.filter(id=id).delete()
    return redirect('lor_table')  # or your table view name



#adminlogin
from .models import AdminLogin
def admin_login(request):
    error = ""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username == "" and password == "":
            request.session["admin"] = True
            return redirect('admin_panel')
        else:
            error = "Invalid credentials"

    return render(request, "admin_login.html", {"error": error})

#adminpanel
def admin_panel(request):
    if not request.session.get("admin_login"):
        return redirect("admin_login")
    students = StudentLogin.objects.all()
    return render(request, "admin_panel.html", {"students": students})


#feeschallan
def fees_challan(request):
    return render(request, 'fees_challan.html')
from .forms import FeesChallanForm
def fees_challan_view(request):
    if request.method == 'POST':
        form = FeesChallanForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'challan.html', {'form': FeesChallanForm(), 'submitted': True})
    else:
        form = FeesChallanForm()
    return render(request, 'fees_challan.html', {'form': form})

#fees table
from .models import FeesChallan
def fees_challan_table(request):
    challans = FeesChallan.objects.all()
    return render(request, 'fees_challan_table.html', {'challans': challans})

#delete feeschallan
from .models import FeesChallan  # use your actual model name
def delete_fees_challan(request, id):
    challan = get_object_or_404(FeesChallan, id=id)
    challan.delete()
    return redirect('fees_challan_table')  # this should match the name of your table view



#forget password
def forgot_password_view(request):
    return render(request, 'forgot_password.html')

#profile
from .models import Reg, BatchAllotment
def view_profile(request):
    rollno = request.session.get('student_rollno')
    if not rollno:
        return redirect('student_login')
    try:
        student = Reg.objects.get(rollno=rollno)
        mobile = student.mobile  # use student.mobile once
        entry = BatchAllotment.objects.filter(mobile=mobile).first()
    except Reg.DoesNotExist:
        return render(request, 'student_login.html', {'error': 'Student not found.'})
    return render(request, 'profile.html', {
        'student': student,
        'entry': entry,
    })

    
#id card
import re
from datetime import timedelta
from .models import Reg, BatchAllotment, FeesChallan
def id_card(request):
    rollno = request.session.get('student_rollno')
    if not rollno:
        return redirect('student_login')
    try:
        student = Reg.objects.get(rollno=rollno)
        mobile = student.mobile  # use student.mobile once
        entry = BatchAllotment.objects.filter(mobile=mobile).first()
        challan = FeesChallan.objects.filter(mobile=mobile).first()
        duration_weeks = int(re.findall(r'\d+', entry.duration)[0])
        start_date = entry.date
        # Calculate start weekday (0=Monday, 6=Sunday)
        start_weekday = start_date.weekday()
        # To get to Saturday of N-th week
        days_to_saturday = 5 - start_weekday  # 5 = Saturday
        days_total = (duration_weeks - 1) * 7 + days_to_saturday
        end_date = start_date + timedelta(days=days_total)
    except Reg.DoesNotExist:
        return render(request, 'id_card.html', {'error': 'Student not found.'})
    return render(request, 'id_card.html', {
        'student': student,
        'entry': entry,
        'challan': challan,
        'end_date': end_date,
    })


#id card approval
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .models import BatchAllotment
@csrf_exempt
def update_idcard_approval(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            entry_id = data.get('id')
            is_idcard_approved = data.get('is_idcard_approved', False)
            # Update only that entry
            entry = BatchAllotment.objects.get(id=entry_id)
            entry.is_idcard_approved = is_idcard_approved
            entry.save()
            return JsonResponse({'message': 'Approval updated successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)



#batch allotment
from .models import BatchAllotment
def batch_allotment_view(request):
    if request.method == 'POST':
        # Get data from form
        email = request.POST.get('email')
        uid = request.POST.get('uid')
        receipt = request.POST.get('receipt')
        name = request.POST.get('name')
        father = request.POST.get('father')
        college = request.POST.get('college')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')

        # Save to DB
        BatchAllotment.objects.create(
            email=email,
            uid=uid,
            receipt=receipt,
            name=name,
            father=father,
            college=college,
            mobile=mobile,
            address=address
        )
        return redirect('batch_allot1')  # Redirect to thank you page after submission
    return render(request, 'batch_allot.html')


# Step 2
def batch_allot1_view(request):
    if request.method == 'POST':
        # Hidden data from batch_allot.html
        data = {
            'id': request.POST.get('id'),
            'email': request.POST.get('email'),
            'uid': request.POST.get('uid'),
            'receipt': request.POST.get('receipt'),
            'name': request.POST.get('name'),
            'father': request.POST.get('father'),
            'college': request.POST.get('college'),
            'mobile': request.POST.get('mobile'),
            'address': request.POST.get('address'),
            'course': request.POST.get('course'),
            'year': request.POST.get('year'),
            'duration': request.POST.get('duration'),
            'eng_branch': request.POST.get('eng_branch')
        }
        return render(request, 'batch_allot1.html', {'entry': data})   
    return redirect('batch_allot2')  # Agar direct aaye to redirect kar do back


# Step 3
def batch_allot2_view(request):
    if request.method == 'POST':
        # Combine all data (hidden + new)
        data = {
            'id': request.POST.get('id'),
            'email': request.POST.get('email'),
            'uid': request.POST.get('uid'),
            'receipt': request.POST.get('receipt'),
            'name': request.POST.get('name'),
            'father': request.POST.get('father'),
            'college': request.POST.get('college'),
            'mobile': request.POST.get('mobile'),
            'address': request.POST.get('address'),
            'course': request.POST.get('course'),
            'year': request.POST.get('year'),
            'duration': request.POST.get('duration'),
            'eng_branch': request.POST.get('eng_branch'),
            'date': request.POST.get('date'),
            'batch_code':request.POST.get('batch_code'),
        }
        return render(request, 'batch_allot2.html', {'entry': data})
    return redirect('batch_allot3')  # if someone accesses directly


# Step 4
from collections import defaultdict
def batch_allot3_view(request):
    if request.method == 'POST':
       # Combine all data (hidden + new)
        data = {
            'id': request.POST.get('id'),
            'email': request.POST.get('email'),
            'uid': request.POST.get('uid'),
            'receipt': request.POST.get('receipt'),
            'name': request.POST.get('name'),
            'father': request.POST.get('father'),
            'college': request.POST.get('college'),
            'mobile': request.POST.get('mobile'),
            'address': request.POST.get('address'),
            'course': request.POST.get('course'),
            'year': request.POST.get('year'),
            'duration': request.POST.get('duration'),
            'eng_branch': request.POST.get('eng_branch'),
            'date': request.POST.get('date'),
            'batch_code':request.POST.get('batch_code'),
            'project_code': request.POST.get('project_code'),
            'project': request.POST.get('project'),
            'report_to':request.POST.get('report_to'),
        }
        return render(request, 'batch_allot3.html', {'entry': data})
    return redirect('batch_allot4')  # if someone accesses directly


def batch_allot4_view(request):
    if request.method == 'POST':
        # Combine all data (hidden + new)
        data = {
            'id': request.POST.get('id'),
            'email': request.POST.get('email'),
            'uid': request.POST.get('uid'),
            'receipt': request.POST.get('receipt'),
            'name': request.POST.get('name'),
            'father': request.POST.get('father'),
            'college': request.POST.get('college'),
            'mobile': request.POST.get('mobile'),
            'address': request.POST.get('address'),
            'course': request.POST.get('course'),
            'year': request.POST.get('year'),
            'duration': request.POST.get('duration'),
            'eng_branch': request.POST.get('eng_branch'),
            'date': request.POST.get('date'), 
            'batch_code':request.POST.get('batch_code'),        
            'project_code': request.POST.get('project_code'),
            'project': request.POST.get('project'),
            'report_to':request.POST.get('report_to'),
            'photo': request.FILES.get('photo'),
        }
        return render(request, 'batch_allot4.html', {'entry': data})
    return redirect('thanku')  # if someone accesses directly



# Final Submission Step
from django.http import HttpResponse
from datetime import datetime
from .models import BatchAllotment  # <-- apne model ka import karo
def thanku(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        uid = request.POST.get('uid')
        receipt = request.POST.get('receipt')
        name = request.POST.get('name')
        father = request.POST.get('father')
        college = request.POST.get('college')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        course = request.POST.get('course')
        year = request.POST.get('year')
        duration = request.POST.get('duration')
        eng_branch = request.POST.get('eng_branch')
        date_str = request.POST.get("date")  # 👈 Raw string
        date = None
        if date_str:
            try:
                date = datetime.strptime(date_str, "%d-%m-%Y").date()
            except ValueError:
                date = None  # or set default like datetime.today().date()  
        batch_code=request.POST.get('batch_code')     
        project_code = request.POST.get('project_code')
        project = request.POST.get('project')
        report_to =request.POST.get('report_to')
        count = BatchAllotment.objects.filter(date=date, project=project).count()
        if count >= 15:
            return HttpResponse("This project is already full for selected date. Please go back and choose another project.")
        photo = request.FILES.get('photo')        
        # Save to model
        entry=BatchAllotment.objects.create(
            email=email,
            uid=uid,
            receipt=receipt,
            name=name,
            father=father,
            college=college,
            mobile=mobile,
            address=address,
            course=course,
            year=year,
            duration=duration,
            eng_branch=eng_branch,
            date=date,
            batch_code=batch_code,
            project_code=project_code,
            project=project,
            report_to=report_to,
            photo=photo
        )
        return render(request, 'thanku.html')
    else:
        return render(request, 'index.html')  

#limit project  
from django.http import JsonResponse
from .models import BatchAllotment
def get_project_counts(request):
    try:
        date = request.GET.get('date')
        counts = {}
        if date:
            entries = BatchAllotment.objects.filter(date=date)
            for entry in entries:
                code = entry.project_code
                counts[code] = counts.get(code, 0) + 1
        return JsonResponse(counts)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# Table to view all entries
def batch_allot_table(request):
    data = BatchAllotment.objects.all()
    return render(request, 'batch_allot_table.html', {'data': data})


#delete batch_allot
def delete_entry(request, id):
    BatchAllotment.objects.filter(id=id).delete()
    return redirect('batch_allot_table')
    


def batch_allotment_table(request):
    data = BatchAllotment.objects.all()
    return render(request, 'batch_allot_table.html', {'data': data})


#certificate
from datetime import datetime, timedelta
import re
from django.shortcuts import render, redirect
from .models import Reg, BatchAllotment, FeesChallan, Certificate
def certificate_view(request):
    rollno = request.session.get('student_rollno')
    if not rollno:
        return redirect('student_login')
    try:
        student = Reg.objects.get(rollno=rollno)
        mobile = student.mobile
        entry = BatchAllotment.objects.filter(mobile=mobile).first()
        challan = FeesChallan.objects.filter(mobile=mobile).first()
        if not entry:
            return render(request, 'certificate.html', {'error': 'No batch allotment data found.'})
        if not entry.duration:
            return render(request, 'certificate.html', {'error': 'Duration not filled for this entry.'})
        duration_weeks = int(re.findall(r'\d+', entry.duration)[0])
        start_date = entry.date
        start_weekday = start_date.weekday()
        days_to_saturday = 5 - start_weekday
        days_total = (duration_weeks - 1) * 7 + days_to_saturday
        end_date = start_date + timedelta(days=days_total)
        current_date = datetime.now().strftime('%d/%m/%Y')        
        return render(request, 'certificate.html', {
            'student': student,
            'entry': entry,
            'challan': challan,
            'end_date': end_date,
            'current_date': current_date,
        })
    except Reg.DoesNotExist:
        return render(request, 'certificate.html', {'error': 'Student not found.'})



#challan download
from django.utils import timezone
from .models import FeesChallan
from .forms import FeesChallanForm
def fees_challan_view(request):
    if request.method == 'POST':
        form = FeesChallanForm(request.POST)
        if form.is_valid():
            challan = form.save()
            return redirect('challan', challan_id=challan.id)
    else:
        form = FeesChallanForm()
    return render(request, 'fees_challan.html', {'form': form})

def challan_pdf_view(request, challan_id):
    from django.shortcuts import get_object_or_404
    challan = get_object_or_404(FeesChallan, id=challan_id)   
    context = {
        'challan': challan,
        'current_date': timezone.now().strftime("%d-%m-%Y"),
    }
    return render(request, 'challan.html', context)


from .models import Reg, BatchAllotment,Certificate
# Training  # if available
def admin_panel(request):
    total_students =Reg.objects.count()
    total_batches = BatchAllotment.objects.count()
    return render(request, 'admin_panel.html', {
        'total_students': total_students,
        'total_batches': total_batches,
    })


#approved student when download certificate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import BatchAllotment
@csrf_exempt
def update_is_active(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            entry_id = data.get('id')
            is_approved = data.get('is_approved', False)
            # Update only that entry
            entry = BatchAllotment.objects.get(id=entry_id)
            entry.is_approved = is_approved
            entry.save()
            return JsonResponse({'message': 'Approval updated successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)


#approved student when download certificate admin
import io,os,zipfile,re
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from stvt.models import BatchAllotment
from datetime import date, timedelta, datetime
def fetch_resources(uri, rel):
    if uri.startswith('/static/'):
        return os.path.join(settings.BASE_DIR, uri.replace('/static/', 'static/'))
    return uri
def download_approved_certificates(request):
    approved_entries = BatchAllotment.objects.filter(is_approved=True)
    zip_buffer = io.BytesIO()
    today = date.today()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for entry in approved_entries:
            template = get_template("certificate_table.html")
            # Ensure entry.date is a date object
            if isinstance(entry.date, str):
                try:
                    start_date = datetime.strptime(entry.date, "%Y-%m-%d").date()
                except:
                    continue
            else:
                start_date = entry.date
            # Extract weeks from "4 Weeks" or "6 Weeks"
            try:
                duration_weeks = int(re.findall(r'\d+', entry.duration)[0])
            except:
                duration_weeks = 0
            # Calculate end date (last Saturday of N-th week)
            start_weekday = start_date.weekday()  # 0=Monday, ..., 5=Saturday
            days_to_saturday = 5 - start_weekday  # 5=Saturday
            days_total = (duration_weeks - 1) * 7 + days_to_saturday
            end_date = start_date + timedelta(days=days_total)
            context = {
                "entry": entry,
                "student": entry,
                "challan": entry,
                "certificate": entry,
                "start_date": start_date,
                "end_date": end_date,
                "current_date": today,
            }
            html = template.render(context)
            pdf_buffer = io.BytesIO()
            pisa_status = pisa.CreatePDF(html, dest=pdf_buffer, link_callback=fetch_resources)
            if pisa_status.err:
                continue
            filename = f"{entry.uid}_certificate.pdf"
            zip_file.writestr(filename, pdf_buffer.getvalue())
    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer.read(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="approved_certificates.zip"'
    return response


#training_letter
from datetime import datetime, timedelta, date
from django.shortcuts import render, redirect
from .models import BatchAllotment
def training_letter_view(request):
    if request.method == 'POST':
        date_str = request.POST.get('date')         # Format: DD-MM-YYYY
        duration = request.POST.get('duration')     # e.g., "4 weeks"
        project = request.POST.get('project')       # selected project
        try:
            start_date = datetime.strptime(date_str, "%d-%m-%Y").date()
        except ValueError:
            return render(request, 'training_letter.html', {
                'error': 'Invalid date format',
            })
        # Save start_date in session
        request.session['selected_date'] = start_date.strftime('%Y-%m-%d')  # store as ISO format
        # Optionally store other data
        request.session['selected_duration'] = duration
        request.session['selected_project'] = project
        return redirect('training_pdf')  # Redirect to PDF page
    return render(request, 'training_letter.html')


#training letter data trainin_pdf
def training_pdf_view(request):
    date_str = request.session.get('selected_date')      # e.g. "2025-07-31"
    duration = request.session.get('selected_duration')  # e.g. "4 weeks"
    project = request.session.get('selected_project')    # e.g. "06-D/M-1"
    if not date_str or not duration or not project:
        return redirect('training_letter')
    start_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    # 🔹 Filter with all 3: date, duration, project
    data = BatchAllotment.objects.filter(
        date=start_date,
        duration=duration,
        project=project,
        is_approved=True
    )
    if not data.exists():
        return render(request, 'training_pdf.html', {'error': 'No approved data found for selected criteria.'})
    entry = data.first()  # individual trainee
    # 🔹 End Date Calculation
    duration_weeks = int(re.findall(r'\d+', entry.duration)[0])
    start_weekday = start_date.weekday()
    days_to_saturday = 5 - start_weekday
    days_total = (duration_weeks - 1) * 7 + days_to_saturday
    end_date = start_date + timedelta(days=days_total)
    context = {
        'entry': entry,
        'data': data,
        'end_date': end_date,
        'current_date': datetime.now().strftime('%d/%m/%Y'),
    }
    return render(request, 'training_pdf.html', context)