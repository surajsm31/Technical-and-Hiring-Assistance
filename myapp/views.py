from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from .models import *   #for access of database tables

import random #for otp
import sib_api_v3_sdk #for email Api
from django.core.cache import cache #store temp data

 #for Ats Score
import os
import docx2txt
from django.core.files.storage import FileSystemStorage
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.conf import settings

from datetime import *  #for date and time
from django.contrib import messages  #for messages

BREVO_API_KEY = "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"

# Create your views here.
def send_otp_email(email, otp, msg):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = BREVO_API_KEY
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    sender = {"name": "TAHAS", "email": "ssmtest31@gmail.com"}
    to = [{"email": email}]

    subject = "Your OTP Code"
    html_content = f"<h3>Your OTP code for {msg} is: {otp}</h3>"

    email_data = sib_api_v3_sdk.SendSmtpEmail(
        sender=sender, to=to, subject=subject, html_content=html_content
    )

    try:
        api_instance.send_transac_email(email_data)
        return True
    except Exception as e:
        print("Error sending email:", e)
        return False

#to send emails
def send_email(email, msg):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = BREVO_API_KEY
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    sender = {"name": "TAHAS", "email": "ssmtest31@gmail.com"}
    to = [{"email": email}]

    subject = "Recruiter Viewd your profile"
    html_content = f"<h3> {msg} </h3>"

    email_data = sib_api_v3_sdk.SendSmtpEmail(
        sender=sender, to=to, subject=subject, html_content=html_content
    )

    try:
        api_instance.send_transac_email(email_data)
        return True
    except Exception as e:
        print("Error sending email:", e)
        return False



def index(request):
    return render(request,"index.html")

def submit_feedback(request):
    if request.method == "POST":
        n = request.POST["name"]
        e = request.POST["email"]
        m = request.POST["msg"]
        feedback = Feedback(Name=n,Email=e,Message=m)
        feedback.save()
        messages.success(request, "Feedback Sent Successfully")
        return redirect("/")

#Developer Section
def developerlogin(request):
    return render(request,"Developer/developerlogin.html")

def dregister(request):
    return render(request,"Developer/dregister.html")

# def register(request):
#     if request.method == "POST":
#         n = request.POST["name"]
#         # dob = request.POST["dob"]
#         contact = request.POST["contact"]
#         edu = request.POST["education"]
#         email = request.POST["email"]
#         pw = request.POST["password"]
#         g = request.POST["r1"]
#         add = request.POST["address"]
#         py = request.POST["pyear"]
#         sq = request.POST["sque"]
#         ans = request.POST["ans"]
#         # r = request.FILES["resume"]
#
#         if developer.objects.all().filter(email=email):
#             messages.warning(request, "Entered Email is already exists,Please use another email for registration.....")
#             return redirect("/dregister")
#         else:
#             d = developer(fname=n,contact=contact,education=edu,email=email,password=pw,gender=g,address=add,
#                       pyear=py,security=sq,answer=ans)
#             # ,resume=r)
#             d.save()
#             messages.success(request, "Registration Successfully completed")
#             return redirect("/developerlogin")
#     else:
#         return redirect("/dregister")



def send_otp(request):
        if request.method == "POST":
           full_name = request.POST['full_name']
           email = request.POST['email']
           education = request.POST['education']
           skill = request.POST['skills']
           experience = request.POST['experience']
           github = request.POST['github']
           portfolio = request.POST['portfolio']
           gender = request.POST['gender']
           address = request.POST['address']
           graduationpy = request.POST['passout_year']
           contact = request.POST['contact_number']
           password = request.POST['password']
           confirm_password = request.POST['confirm_password']

           if password != confirm_password:
              messages.error(request, "Passwords do not match!")
              return render(request, 'Developer/dregister.html')

           if developer.objects.filter(email=email).exists():
              return HttpResponse("Email already registered. Please log in.")

            # Generate 6-digit OTP
           otp = random.randint(100000, 999999)
           print(otp)
        # Store user data temporarily
           cache.set(f"user_{email}",
                      {"name": full_name, "email": email, "education": education,"skill": skill, "experience": experience, "github": github,
                       "portfolio": portfolio,"gender": gender, "address": address,"graduationpy": graduationpy,"contact": contact,
                       "password": password, "otp": otp}, timeout=100000)

        # Send OTP via email
           msg = " Registration "
           if send_otp_email(email, otp, msg):
              return render(request, "Developer/verify_otp1.html", {"email": email})
           else:
              return HttpResponse("Error sending OTP. Try again.")

        return render(request, "Developer/dregister.html")


def verify_otp(request):
    if request.method == "POST":
        email = request.POST.get("email")
        entered_otp = request.POST.get("otp")

        # Retrieve stored user data
        user_data = cache.get(f"user_{email}")

        if user_data and str(user_data["otp"]) == entered_otp:
            # Save user in the database
            developer.objects.create(fname=user_data["name"], email=user_data["email"], education=user_data["education"],skill=user_data["skill"],
                                     experience=user_data["experience"], github=user_data["github"], portfolio=user_data["portfolio"],
                                     gender=user_data["gender"],address=user_data["address"],graduationpy=user_data["graduationpy"],
                                     contact=user_data["contact"],password=user_data["password"],verified=True)

            # Clear cached data
            cache.delete(f"user_{email}")
            messages.success(request, "Registration of Developer OnSite Successfully completed!.")

            return redirect("/developerlogin")
            # return HttpResponse("OTP Verified! Registration Successful.")
        else:
            return HttpResponse("Invalid OTP. Please try again.")

    return render(request, "Developer/verify_otp1.html")



def login_validate(request):
    if request.method == "POST":
        u = request.POST["uname"]
        pw = request.POST["psw"]

        data =  developer.objects.all().filter(email=u,password=pw)
        if data:
            messages.success(request, "Login Successfully completed")
            request.session['username'] = u
            return redirect("/ddashboard")
        else:
            messages.warning(request, "Invalid username and password,Please try again...")
            return redirect("/developerlogin")

def ddashboard(request):
    if request.session.get('username') is not None:
        email = request.session.get('username')
        data = developer.objects.all().filter(email=email)
        data1 = category.objects.all()
        return render(request,"Developer/ddashboard.html",{'data':data,'data1':data1})
    else:
        return redirect("/developerlogin")

def home(request):
    del request.session['category']  # session end
    answer.objects.all().delete()
    return redirect("/ddashboard")

def analyze_resume(request):
    if request.session.get('username') is not None:
       result = None

       if request.method == 'POST':
           uploaded_resume = request.FILES['resume']
           job_role = request.POST['job_role']
           job_description = request.POST['job_description']

           fs = FileSystemStorage()
           filename = fs.save(uploaded_resume.name, uploaded_resume)
           file_path = fs.path(filename)

           try:
               if filename.endswith('.pdf'):
                   import PyPDF2
                   with open(file_path, 'rb') as f:
                       reader = PyPDF2.PdfReader(f)
                       resume_text = ''
                       for page in reader.pages:
                           resume_text += page.extract_text()
               elif filename.endswith('.docx'):
                   resume_text = docx2txt.process(file_path)
               else:
                   resume_text = uploaded_resume.read().decode('utf-8')

               text_corpus = [resume_text, job_description]
               vectorizer = TfidfVectorizer()
               vectors = vectorizer.fit_transform(text_corpus)
               similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0] * 100

               result = {
                   'job_role': job_role,
                   'similarity': round(similarity, 2),
                   'match_status': 'Good Match' if similarity >= 60 else 'Needs Improvement'
               }

           finally:
              if os.path.exists(file_path):
                  os.remove(file_path)

       return render(request, 'Developer/analyze.html', {'result': result})



def quiz(request):
    if request.session.get('username') is not None:
        uemail = request.session.get('username')
        if request.method == "POST":
            name = request.POST["name"]
            email = request.POST["email"]
            cn = request.POST["contact"]
            qd = request.POST["quizDomain"]
            resume = request.FILES["resume"]
            print(resume)
            date = datetime.now()

            if email == uemail:
                if domain.objects.all().filter(email=email, domain=qd):
                    domain.objects.all().filter(email=email, domain=qd).delete()
                    do = domain(name=name, email=email, contact=cn, domain=qd, resume=resume, date=date)
                    do.save()
                    # domain.objects.all().filter(email=email, domain=qd).update(name=name, email=email, contact=cn, domain=qd, resume=resume, date=date)#update
                else:
                    do = domain(name=name, email=email, contact=cn, domain=qd, resume=resume, date=date)
                    do.save()

                if question.objects.filter(category=qd):
                    request.session['category'] = qd
                    if request.session.get('category') is not None:
                        cate = request.session.get('category')
                        questions = list(question.objects.filter(category=cate))
                        random.shuffle(questions)
                        data = questions[:25]
                        if request.session.get('username') is not None:
                            uemail = request.session.get('username')
                            data1 = developer.objects.all().filter(email=uemail)
                            messages.success(request, "Welcome to ultimate quiz experience! Start your test to begin testing your wits")
                            return render(request, "Developer/quiz.html", {'data': data,'data1':data1})

                else:
                    messages.warning(request, "Invalid inputs... plz enter correct inputs")
                    return redirect("/ddashboard")
            else:
                return redirect("/ddashboard")
        else:
            return redirect("/ddashboard")
    else:
        return redirect("/")

# After quiz submit
def submit(request):
    if request.method == "POST":
        ans = request.POST
        print(request.POST)
        a = []
        # b = []
        # for j in ans.keys():
        #     b.append(j)
        #     print(b)
        # c = b.pop(0)
        # for j in b:
        #     an = answer(qid=j)
        #     an.save()

        for i in ans.values():
            print(i)
            a.append(i)
        r = a.pop(0)
            # a,b = i.split("-")
        print(a)
            # l = list(a)
        for i in a:
            b,c = i.split("-")
            an = answer(qans=c)
            an.save()

        return redirect("/score")

def score(request):
    if request.session.get('category') is not None:
        cate = request.session.get('category')
        data= question.objects.values_list('Correctoption',flat=True).filter(category=cate)
        data1 = answer.objects.values_list('qans',flat=True)
        count = 0
        print(data)
        print(data1)
        temp = count
        for i in data:
            for j in data1:
                if i == j:
                    count +=1
                else:
                    temp
    if request.session.get('username') is not None:
        uemail = request.session.get('username')
    if request.session.get('category') is not None:
        cate = request.session.get('category')

        do = domain.objects.all().filter(email=uemail,domain=cate).update(mark=count)

        entry_count = question.objects.filter(category=cate).count()
        print(entry_count)
        return render(request, "Developer/Result.html",{'data':entry_count,'data1':count})
        # return HttpResponse(f"Your Test Score is {count}")

def certificate(request):
    if request.session.get('username') is not None:
        uemail = request.session.get('username')
        # data = domain.objects.all().filter(email=uemail)
        developers = domain.objects.all().filter(email=uemail)
        data = []
        for dev in developers:
            total_questions = question.objects.filter(category=dev.domain).count()
            if total_questions == 0:
                continue  # Avoid division by zero

        percentage = (dev.mark / total_questions) * 100

        if percentage >= 50:
            data.append({
                "name": dev.name,
                "domain": dev.domain,
                "date": dev.date,
                "percentage": round(percentage, 2)
            })
            return render(request,"Developer/certificate.html",{'data':data})
            # else:
            #     return HttpResponse("Failed")

def profile(request):
    if request.session.get('username') is not None:
        uemail = request.session.get('username')
        data = developer.objects.all().filter(email=uemail)
        return render(request,"Developer/profile.html",{'data':data})
    else:
        return redirect("/")

def update_dprofile(request):
    if request.session.get('username') is not None:
        uemail = request.session.get('username')
        data = developer.objects.all().filter(email=uemail)
        return render(request,"Developer/updateprofile.html",{'data':data})

def dprofile_update(request):
    if request.session.get('username') is not None:
        uemail = request.session.get('username')
        if request.method =="POST":
            full_name = request.POST['name']
            email = request.POST['email']
            education = request.POST['education']
            skill = request.POST['skills']
            experience = request.POST['experience']
            github = request.POST['github']
            portfolio = request.POST['portfolio']
            contact = request.POST['contact']

            developer.objects.all().filter(email=uemail).update(fname=full_name, email=email, education=education,
                                                            skill=skill, experience=experience, github=github, portfolio=portfolio,contact=contact)#update
            messages.success(request, "Profile Updated Successfully..")
            return redirect("/profile")
        else:
            return redirect("/update_profile")

def dpass_change(request):
    if request.session.get('username') is not None:
        uemail = request.session.get('username')
        data = developer.objects.all().filter(email=uemail)
        return render(request,"Developer/dpass_change.html",{'data':data})

def change_dpass(request):
    if request.session.get('username') is not None:
        uemail = request.session.get('username')
        if request.method == "POST":
            em = request.POST["email"]
            op = request.POST["old_password"]
            np = request.POST["new_password"]
            cp = request.POST["confirm_password"]

            if np !=cp:
                messages.warning(request, "New Password And Confirm Password Dosen't Match!!!. Try Again...")
                return redirect("/dpass_change")
            else:
                if developer.objects.all().filter(email=em,password=op).exists():
                   developer.objects.all().filter(email=em).update(password=np)
                   messages.success(request, " Password Updated Successfully !!!.")
                   return redirect("/profile")
                else:
                    messages.success(request, "The Old Password Cannot Match !!!. Try Again ...")
                    return redirect("/dpass_change")


def dlogout(request):
    del request.session['username']  # session end
    answer.objects.all().delete()
    messages.success(request, "Logout Successfully completed")
    return redirect("/")

#forget password
def forget(request):
    return render(request,"Developer/forget.html")

def reset_password(request):
    if request.method == "POST":
        email = request.POST["email"]
        np = request.POST["new_pass"]
        cp = request.POST["confirm_pass"]
        # Generate 6-digit OTP
        otp = random.randint(100000, 999999)
        print(otp)
        # Store user data temporarily
        cache.set(f"user_{email}",
                  {"email": email,"new_pass":np,"confirm_pass":cp, "otp": otp}, timeout=100000)

        # Send OTP via email
        msg = " Reset your Password "
        if send_otp_email(email, otp, msg):
            return render(request, "Developer/verify_fpass.html", {"email": email})
        else:
            return HttpResponse("Error sending OTP. Try again.")

    return redirect("/forget_dev_password")

def verify_dev_fpass(request):
        if request.method == "POST":
            email = request.POST.get("email")
            entered_otp = request.POST.get("otp")

            # Retrieve stored user data
            user_data = cache.get(f"user_{email}")
            if user_data and str(user_data["otp"]) == entered_otp:
                developer.objects.all().filter(email=user_data["email"]).update(password=user_data["confirm_pass"])  # update
                # Clear cached data
                cache.delete(f"user_{email}")
                messages.success(request, "Password Updated OnSite Successfully completed!.")
                return redirect("/developerlogin")
            else:
                return HttpResponse("Invalid OTP. Please try again.")


def hrlogin(request):
    return render(request, "HR/hrlogin.html")

def hrregister(request):
    return render(request, "HR/hrregister.html")

def otp_to_hr(request):
    if request.method == "POST":
        full_name = request.POST['full_name']
        email = request.POST['email']
        company = request.POST['company_name']
        job_position = request.POST['job_position']
        contact_number = request.POST['contact_number']
        company_address = request.POST['company_address']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, 'HR/hrregister.html')

        if hr.objects.filter(Email=email).exists():
            return HttpResponse("Email already registered. Please log in.")

        # Generate 6-digit OTP
        otp = random.randint(100000, 999999)
        print(otp)
        # Store user data temporarily
        cache.set(f"user_{email}",
                  {"name": full_name, "email": email, "company": company, "job_position": job_position,
                   "contact_number": contact_number,
                   "company_address": company_address, "password": password, "otp": otp}, timeout=100000)

        # Send OTP via email
        msg = " Registration "
        if send_otp_email(email, otp, msg):
            return render(request, "Hr/verify_hr.html", {"email": email})
        else:
            return HttpResponse("Error sending OTP. Try again.")

    return render(request, "HR/hrregister.html")

def verify_hr(request):
    if request.method == "POST":
        email = request.POST.get("email")
        entered_otp = request.POST.get("otp")

        # Retrieve stored user data
        user_data = cache.get(f"user_{email}")

        if user_data and str(user_data["otp"]) == entered_otp:
            # Save user in the database
            hr.objects.create(Name=user_data["name"], Email=user_data["email"], Company=user_data["company"],
                                     Designation=user_data["job_position"], Password=user_data["password"], Contact=user_data["contact_number"],
                              Address=user_data["company_address"],verified=True)

            # Clear cached data
            cache.delete(f"user_{email}")
            messages.success(request, "Registration of Hiring Recruiter OnSite Successfully completed!.")

            return redirect("/hrlogin")
            # return HttpResponse("OTP Verified! Registration Successful.")
        else:
            return HttpResponse("Invalid OTP. Please try again.")

    return render(request, "HR/verify_hr.html")


def hr_validate(request):
    if request.method == "POST":
        e = request.POST["uname"]
        p = request.POST["psw"]

        data = hr.objects.all().filter(Email=e, Password=p)
        if data:
            messages.success(request, "Login Successfully completed")
            request.session['username1'] = e
            return redirect("/hrdashboard")
        else:
            messages.warning(request, "Invalid username and password,Please try again...")
            return redirect("/hrlogin")

def hrdashboard(request):
    if request.session.get('username1') is not None:
        email = request.session.get('username1')
        data = hr.objects.all().filter(Email=email)
        return render(request,"HR/hrdash.html",{'data':data})

def hrprofile(request):
    if request.session.get('username1') is not None:
        email = request.session.get('username1')
        data = hr.objects.all().filter(Email=email)
        return render(request,"HR/profile.html",{'data':data})

def update_hrprofile(request):
    if request.session.get('username1') is not None:
        email = request.session.get('username1')
        data = hr.objects.all().filter(Email=email)
        return render(request, "HR/updateprofile.html", {'data': data})

def updatehrprofile(request):
    if request.session.get('username1') is not None:
        email = request.session.get('username1')
        if request.method == "POST":
            n = request.POST["name"]
            e = request.POST["email"]
            cm = request.POST["company"]
            d = request.POST["designation"]
            cn = request.POST["contact"]
            ad = request.POST["address"]

            hr.objects.all().filter(Email=e).update(Name=n, Email=e, Company=cm, Designation=d, Contact=cn, Address=ad)
            messages.success(request, "Profile Updated Successfully.. ")
            return redirect("/hr_profile")
        else:
            messages.success(request, "Due to Invalid Input Profile Updatation Cannot be done..., Please try again")
            return redirect("/hr_profile")

def hrpass_change(request):
    if request.session.get('username1') is not None:
        email = request.session.get('username1')
        data = hr.objects.all().filter(Email=email)
        return render(request,"HR/pass_change.html",{'data':data})

def change_hrpass(request):
    if request.session.get('username1') is not None:
        uemail = request.session.get('username1')
        if request.method == "POST":
            em = request.POST["email"]
            op = request.POST["old_password"]
            np = request.POST["new_password"]
            cp = request.POST["confirm_password"]

            if np !=cp:
                messages.warning(request, "New Password And Confirm Password Dosen't Match!!!. Try Again...")
                return redirect("/hrpass_change")
            else:
                if hr.objects.all().filter(Email=em,Password=op).exists():
                   hr.objects.all().filter(Email=em).update(Password=np)
                   messages.success(request, " Password Updated Successfully !!!.")
                   return redirect("/hr_profile")
                else:
                    messages.success(request, "The Old Password Cannot Match !!!. Try Again ...")
                    return redirect("/hrpass_change")

def search(request):
    if request.session.get('username1') is not None:
        email = request.session.get('username1')
        data1 = hr.objects.all().filter(Email=email)

        if request.method == "POST":
            s = request.POST["search"]

            if s and s[0].islower():
                entered_word = s[0].upper() + s[1:]
                res = entered_word

                matched_domains = domain.objects.filter(domain=res)

                # Extract emails from domain table
                emails = matched_domains.values_list('email', flat=True)

                # Get all matching developers at once
                developers = developer.objects.filter(email__in=emails)

                # Build a map for quick lookup
                dev_map = {dev.email: dev for dev in developers}

                # Create combined data (domain + matched developer)
                combined_data = [(dom, dev_map.get(dom.email)) for dom in matched_domains]
                # c=data.count()

                return render(request, "HR/hrdash.html", {'data':data1,'combined_data':combined_data})
            else:
                data = domain.objects.all().filter(domain= s)
                for i in data:
                    user = i.email
                data2 = developer.objects.all().filter(email=user)
                combined_data = zip(data,data2)
                return render(request, "HR/hrdash.html", {'data1': data, 'data':data1, 'combined_data':combined_data})

def view(request,id):
    if request.session.get('username1') is not None:
        dev = get_object_or_404(developer, id=id)
        domain_data = domain.objects.filter(email=dev.email)

        msg = "Recruiter(s) expressed interest in your Profile. Stay connected and Updated"
        send_email(dev.email,msg)
        return render(request, 'Hr/view.html', {
            'developer': dev,
            'domain_data': domain_data
        })


def hrlogout(request):
    del request.session['username1']  # session end
    messages.success(request, "Logout Successfully completed")
    return redirect("/")

def forgetpass(request):
    return render(request,"HR/forget.html")

def reset_hr_password(request):
    if request.method == "POST":
        email = request.POST["email"]
        np = request.POST["new_pass"]
        cp = request.POST["confirm_pass"]
        # Generate 6-digit OTP
        otp = random.randint(100000, 999999)
        print(otp)
        # Store user data temporarily
        cache.set(f"user_{email}",
                  {"email": email,"new_pass":np,"confirm_pass":cp, "otp": otp}, timeout=100000)

        # Send OTP via email
        msg = " Reset your Password "
        if send_otp_email(email, otp, msg):
            return render(request, "HR/verify_fpass.html", {"email": email})
        else:
            return HttpResponse("Error sending OTP. Try again.")

    return redirect("/forget_hr_password")

def verify_hr_fpass(request):
        if request.method == "POST":
            email = request.POST.get("email")
            entered_otp = request.POST.get("otp")

            # Retrieve stored user data
            user_data = cache.get(f"user_{email}")
            if user_data and str(user_data["otp"]) == entered_otp:
                hr.objects.all().filter(Email=user_data["email"]).update(Password=user_data["confirm_pass"])  # update
                # Clear cached data
                cache.delete(f"user_{email}")
                messages.success(request, "Password Updated OnSite Successfully completed!.")
                return redirect("/hrlogin")
            else:
                return HttpResponse("Invalid OTP. Please try again.")


#Admin Section
def admin_login(request):
    #registration logic for Admin
    name = "Suraj Suryabhan More"
    em = "ssmtest31@gmail.com"
    pw = "SurajTest@315"
    role = "Admin"
    cn = "9370909318"
    count = Admin.objects.count()
    if count == 0:
        ad = Admin(Name=name,Email=em, Password=pw, Role=role, Contact=cn)
        ad.save()
    return render(request,"Admin/admin_login.html")

def admin_loginvalidate(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        if Admin.objects.all().filter(Email=email,Password=password):
            request.session['username2'] = email
            messages.success(request, "Login Successfully completed. Welcome to the admin panel!.")
            return redirect("/Admin1")
        else:
            messages.warning(request, "Due to invalid inputs login failed...., Try Again....")
            return redirect("/admin_login")

def admin(request):
    if request.session.get('username2') is not None:
        email = request.session.get('username2')
        admin = Admin.objects.values_list('Name', flat=True).first()
        data = domain.objects.all()
        count1 = developer.objects.count()
        count2 = hr.objects.count()
        count3 = question.objects.count()
        count4 = category.objects.count()
        return render(request,"Admin/admin.html",{'admin':admin,'data':data,'data1':count1,'data2':count2,
                                                  'data3':count3,'data4':count4})
    else:
        return redirect("/admin_login")

def admin_profile(request):
    if request.session.get('username2') is not None:
        email = request.session.get('username2')
        data = Admin.objects.all().filter(Email=email)
        admin = Admin.objects.values_list('Name', flat=True).first()
        return render(request,"Admin/admin_profile.html",{'admin':admin,'data':data})

def change_pass(request):
    if request.session.get('username2') is not None:
        email = request.session.get('username2')
        data = Admin.objects.all().filter(Email=email)
        admin = Admin.objects.values_list('Name', flat=True).first()
        return render(request,"Admin/change_pass.html",{'admin':admin,'data':data})

def pass_change(request):
    if request.session.get('username2') is not None:
        email = request.session.get('username2')
        if request.method == "POST":
            em = request.POST["email"]
            op = request.POST["old_password"]
            np = request.POST["new_password"]
            cp = request.POST["confirm_password"]

            if np !=cp:
                messages.warning(request, "New Password And Confirm Password Dosen't Match!!!. Try Again...")
                return redirect("/change_pass")
            else:
                if Admin.objects.all().filter(Email=em,Password=op).exists():
                   Admin.objects.all().filter(Email=em).update(Password=np)
                   messages.success(request, " Password Updated Successfully !!!.")
                   return redirect("/admin_profile")
                else:
                    messages.success(request, "The Old Password Cannot Match !!!. Try Again ...")
                    return redirect("/change_pass")

def update_profile(request):
    if request.session.get('username2') is not None:
        email = request.session.get('username2')
        data = Admin.objects.all().filter(Email=email)
        admin = Admin.objects.values_list('Name', flat=True).first()
        return render(request,"Admin/update_profile.html",{'admin':admin,'data':data})

def profile_update(request):
    if request.session.get('username2') is not None:
        email = request.session.get('username2')
        if request.method == "POST":
            name = request.POST["name"]
            email1 = request.POST["email"]
            contact = request.POST["contact"]

            Admin.objects.all().filter(Email=email1).update(Name=name, Contact=contact)#update
            return redirect("/admin_profile")


# Developer Management Section Of Admin
def dev_info(request):
    if request.session.get('username2') is not None:
        email = request.session.get('username2')
        data = developer.objects.all()
        admin = Admin.objects.values_list('Name', flat=True).first()
        return render(request,"Admin/developer_info.html",{'admin':admin,'data':data})

def dev_register(request):
    if request.session.get('username2') is not None:
        email = request.session.get('username2')
        admin = Admin.objects.values_list('Name', flat=True).first()
        return render(request,"Admin/dev_register.html",{'admin':admin})

def send_otp_to_dev(request):
    if request.session.get('username2') is not None:
        email = request.session.get('username2')
        if request.method == "POST":
           full_name = request.POST['full_name']
           email = request.POST['email']
           education = request.POST['education']
           skill = request.POST['skills']
           experience = request.POST['experience']
           github = request.POST['github']
           portfolio = request.POST['portfolio']
           gender = request.POST['gender']
           address = request.POST['address']
           graduationpy = request.POST['passout_year']
           contact = request.POST['contact_number']
           password = request.POST['password']
           confirm_password = request.POST['confirm_password']

           if password != confirm_password:
              messages.error(request, "Passwords do not match!")
              return render(request, 'Admin/dev_register.html')

           if developer.objects.filter(email=email).exists():
              return HttpResponse("Email already registered. Please log in.")

            # Generate 6-digit OTP
           otp = random.randint(100000, 999999)
           print(otp)
        # Store user data temporarily
           cache.set(f"user_{email}",
                      {"name": full_name, "email": email, "education": education,"skill": skill, "experience": experience, "github": github,
                       "portfolio": portfolio,"gender": gender, "address": address,"graduationpy": graduationpy,"contact": contact,
                       "password": password, "otp": otp}, timeout=100000)

        # Send OTP via email
           msg = " Registration "
           if send_otp_email(email, otp, msg):
              return render(request, "Admin/verify_dev_otp.html", {"email": email})
           else:
              return HttpResponse("Error sending OTP. Try again.")

        return render(request, "Admin/dev_register.html")

def verify_dev_otp(request):
    if request.method == "POST":
        email = request.POST.get("email")
        entered_otp = request.POST.get("otp")

        # Retrieve stored user data
        user_data = cache.get(f"user_{email}")

        if user_data and str(user_data["otp"]) == entered_otp:
            # Save user in the database
            developer.objects.create(fname=user_data["name"], email=user_data["email"], education=user_data["education"],skill=user_data["skill"],
                                     experience=user_data["experience"], github=user_data["github"], portfolio=user_data["portfolio"],
                                     gender=user_data["gender"],address=user_data["address"],graduationpy=user_data["graduationpy"],
                                     contact=user_data["contact"],password=user_data["password"],verified=True)

            # Clear cached data
            cache.delete(f"user_{email}")
            messages.success(request, "Registration of Developer OnSite Successfully completed!.")
            return redirect("/dev")
            # return HttpResponse("OTP Verified! Registration Successful.")
        else:
            return HttpResponse("Invalid OTP. Please try again.")

    return render(request, "Admin/verify_dev_otp.html")

def delete_dev(request,id):
    if request.session.get('username2') is not None:
        email = request.session.get('username2')
        dev = developer.objects.get(id=id)
        dev.delete()
        return redirect("/dev")

def dtest_info(request):
    if request.session.get('username2') is not None:
        email = request.session.get('username2')
        data = domain.objects.all()
        admin = Admin.objects.values_list('Name', flat=True).first()
        return render(request,"Admin/dtest_info.html",{'admin':admin,'data':data})



# HR Management section of Admin
def hr_info(request):
    if request.session.get('username2') is not None:
        email = request.session.get('username2')
        data = hr.objects.all()
        admin = Admin.objects.values_list('Name', flat=True).first()
        return render(request,"Admin/hr_info.html",{'admin':admin,'data':data})
    else:
        return redirect("/admin_login")

def hr_register(request):
    if request.session.get('username2') is not None:
        email = request.session.get('username2')
        admin = Admin.objects.values_list('Name', flat=True).first()
        return render(request,"Admin/hr_register.html",{'admin':admin})

def send_otp_to_hr(request):
    if request.session.get('username2') is not None:
        email = request.session.get('username2')
        if request.method == "POST":
           full_name = request.POST['full_name']
           email = request.POST['email']
           company = request.POST['company']
           job_position = request.POST['job_position']
           contact_number = request.POST['contact_number']
           company_address = request.POST['company_address']
           password = request.POST['password']
           confirm_password = request.POST['confirm_password']

           if password != confirm_password:
              messages.error(request, "Passwords do not match!")
              return render(request, 'Admin/hr_register.html')

           if hr.objects.filter(Email=email).exists():
              return HttpResponse("Email already registered. Please log in.")

            # Generate 6-digit OTP
           otp = random.randint(100000, 999999)
           print(otp)
        # Store user data temporarily
           cache.set(f"user_{email}",
                      {"name": full_name, "email": email, "company": company, "job_position": job_position, "contact_number": contact_number,
                       "company_address": company_address,"password": password, "otp": otp}, timeout=100000)

        # Send OTP via email
           msg = " Registration "
           if send_otp_email(email, otp, msg):
              return render(request, "Admin/verify_hr_otp.html", {"email": email})
           else:
              return HttpResponse("Error sending OTP. Try again.")

        return render(request, "Admin/hr_register.html")

def verify_hr_otp(request):
    if request.method == "POST":
        email = request.POST.get("email")
        entered_otp = request.POST.get("otp")

        # Retrieve stored user data
        user_data = cache.get(f"user_{email}")

        if user_data and str(user_data["otp"]) == entered_otp:
            # Save user in the database
            hr.objects.create(Name=user_data["name"], Email=user_data["email"], Company=user_data["company"],
                                     Designation=user_data["job_position"], Password=user_data["password"],
                              Contact=user_data["contact_number"],Address=user_data["company_address"],verified=True)

            # Clear cached data
            cache.delete(f"user_{email}")
            messages.success(request, "Registration of Hiring Recruiter OnSite Successfully completed!.")

            return redirect("/hr")
            # return HttpResponse("OTP Verified! Registration Successful.")
        else:
            return HttpResponse("Invalid OTP. Please try again.")

    return render(request, "Admin/verify_hr_otp.html")

def delete_hr(request,id):
    if request.session.get('username2') is not None:
        email = request.session.get('username2')
        recruiter = hr.objects.get(id=id)
        recruiter.delete()
        return redirect("/hr")


# Test Question Management by Admin
def test_que(request):
    if request.session.get('username2') is not None:
        email = request.session.get('username2')
        data = question.objects.all()
        admin = Admin.objects.values_list('Name', flat=True).first()
        return render(request,"Admin/test_que.html",{'admin':admin,'data':data})

def add_test_que(request):
    if request.session.get('username2') is not None:
        email = request.session.get('username2')
        admin = Admin.objects.values_list('Name', flat=True).first()
        data = category.objects.all()
        return render(request,"Admin/add_test.html",{'admin':admin,'data':data})

def add_question(request):
    if request.session.get('username2') is not None:
        email = request.session.get('username2')
        if request.method == "POST":
            que = request.POST["question"]
            op1 = request.POST["option1"]
            op2 = request.POST["option2"]
            op3 = request.POST["option3"]
            op4 = request.POST["option4"]
            cop = request.POST["correct_option"]
            cate = request.POST["category"]

            ad = question(Question=que, option1=op1, option2=op2, option3=op3, option4=op4, Correctoption=cop, category=cate)
            ad.save()
            messages.success(request, "Test Question Added Successfully !!!.")
            return redirect("/test")
        else:
            return redirect("/add_test")

def delete_que(request,id):
    if request.session.get('username2') is not None:
        email = request.session.get('username2')
        que = question.objects.get(id=id)
        que.delete()
        return redirect("/test")


# Test Category Management by Admin
def test_cate(request):
    if request.session.get('username2') is not None:
        email = request.session.get('username2')
        data = category.objects.all()
        admin = Admin.objects.values_list('Name', flat=True).first()
        return render(request,"Admin/test_category.html",{'admin':admin,'data':data})

def add_test_cate(request):
    if request.session.get('username2') is not None:
        email = request.session.get('username2')
        admin = Admin.objects.values_list('Name', flat=True).first()
        return render(request,"Admin/add_test_cate.html",{'admin':admin})

def add_cate(request):
    if request.session.get('username2') is not None:
        email = request.session.get('username2')
        if request.method == "POST":
            cate = request.POST["category_name"]
            domain = request.POST["domain_name"]

            if category.objects.all().filter(Domain=domain).exists():
                messages.warning(request, "Test Category already exists !!!.")
                return redirect("/add_test_cate")
            else:
                c = category(category=cate,Domain=domain)
                c.save()
            messages.success(request, "Test Category Added Successfully !!!.")
            return redirect("/test_cate")

def delete_cate(request,id):
    if request.session.get('username2') is not None:
        email = request.session.get('username2')
        cate = category.objects.get(id=id)
        cate.delete()
        return redirect("/test_cate")

def feedback(request):
    if request.session.get('username2') is not None:
        email = request.session.get('username2')
        fb = Feedback.objects.all()
        admin = Admin.objects.values_list('Name', flat=True).first()
        return render(request,"Admin/feedback.html",{'admin':admin,'data':fb})

def admin_logout(request):
    del request.session['username2']
    messages.success(request, "Logout Successfull..")
    return redirect("/admin_login")

def admin_clear(request):
    Admin.objects.all().delete()
    return redirect("/admin_login")


# Alert on Test Page
from django.shortcuts import render
def alert_on_tab_change(request):
    return render(request, 'quiz.html')

def next_page(request):
    return redirect("/ddashboard")

