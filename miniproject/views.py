import imp
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.conf import settings
import random
from django.http import JsonResponse
from django.db.models import Count
from dateutil.relativedelta import relativedelta
from datetime import datetime

# Create your views here.

def send_otp_email(otp, email):
    subject = "Verify your Email - {}".format(email)
    print(otp)
    message = "Your 4-digit OTP to verify your account is : " + str(otp) + ". Please don't share it with anyone else"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)

def send_psw_email(otp, email):
    subject = "Reset your Password - {}".format(email)
    print(otp)
    message = "Your 4-digit OTP to reset your password is : " + str(otp) + ". Please don't share it with anyone else"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)


def Home(request):
    return render(request, "miniproject/landing-screen.html")

def Register(request):
    if request.method == "POST":
        fnd = User.objects.filter(Email = request.POST['email'].lower())
        if len(fnd) == 0:
            request.session['fname'] = request.POST['firstname']
            request.session['lname'] = request.POST['lastname']
            request.session['tphone'] = request.POST['phone']
            request.session['email'] = request.POST['email'].lower()
            request.session['pswd'] = request.POST['password']
            cpswd = request.POST['confirm-password']

            # Register Without OTP Verification
            '''fname = request.POST['firstname']
                lname = request.POST['lastname']
                phone = request.POST['phone']
                email = request.POST['email'].lower()
                pswd = request.POST['password']
                cpswd = request.POST['confirm-password']'''
            if request.session['pswd'] == cpswd:
                request.session['pswd'] = make_password(request.POST['password'])
                request.session['otp'] = random.randint(1000,9999)
                send_otp_email(request.session['otp'], request.session['email'])
                messages.error(request, "OTP is sent to your email. Please enter it.")
                return redirect("verifyotppage")
                
                # Register Without OTP Verification
                '''if pswd == cpswd:
                    AddUser = User.objects.create(
                        FName = fname,
                        LName = lname,
                        Phone = phone,
                        Email = email,
                        Passwd = pswd
                    )
                    messages.success(request, "You have registered successfully. Please login to continue")
                    return redirect("login")'''
            else:
                messages.error(request, "Password and Confirm Password do not match. Please try again")
                return redirect("register")
        else:
            messages.error(request, "User already exists. Please login")
            return redirect("login")
    else:
        return render(request, "miniproject/register.html")
    
def Login(request):
    if request.method == "POST":
        email = request.POST['username'].lower()
        pswd = request.POST['password']
        fnd = User.objects.filter(Email = email)
        if len(fnd) > 0:
            if check_password(pswd, fnd[0].Passwd):
                request.session['id'] = fnd[0].id
                request.session['email'] = fnd[0].Email
                request.session['is_user'] = fnd[0].is_user
                
                return redirect("dashboard")
            else:
                messages.error(request, "Please enter a valid password")
                return redirect("login")
        else:
            messages.error(request, "User does not exist. Please register.")
            return redirect("register")
    else:
        return render(request, "miniproject/login.html")

def Logout(request):
    if 'email' in request.session:
        del request.session['id']
        del request.session['email']
        del request.session['is_user']
        return redirect("home-page")
    else:
        return redirect("home-page")


def VerifyOTPPage(request):
    return render(request, "miniproject/register-otp.html")

def FpEmailPage(request):
    return render(request, "miniproject/fp-email.html")

def FpOTPPage(request):
    return render(request, "miniproject/fp-otp.html")

def FpPasswordPage(request):
    return render(request, "miniproject/fp-password.html")




def Dashboard(request):
    if 'email' in request.session:
        l18 = FIR.objects.filter(S_age = "<18").count()
        b1824 = FIR.objects.filter(S_age = "18-24").count()
        b2544 = FIR.objects.filter(S_age = "25-44").count()
        b4564 = FIR.objects.filter(S_age = "45-64").count()
        p65 = FIR.objects.filter(S_age = "65+").count()
        Midwest = Wanted.objects.filter(Region = "Midwest").count()
        South = Wanted.objects.filter(Region = "South").count()
        West = Wanted.objects.filter(Region = "West").count()
        Endangered_Runaway = Missing.objects.filter(Incident_Type = "Endangered Runaway").count()
        Non_Family_Abduction = Missing.objects.filter(Incident_Type = "Non Family Abduction").count()
        Lost_Injured_Missing = Missing.objects.filter(Incident_Type = "Lost Injured Missing").count()
        return render(request, "miniproject/dashboard.html", {
            'l18': l18, 'b1824': b1824, 'b2544': b2544, 'b4564': b4564, 'p65': p65, 'midwest': Midwest, 'south': South, 
            'west': West, 'er': Endangered_Runaway, 'nfa': Non_Family_Abduction, 'lim': Lost_Injured_Missing})
    else:
        return redirect('home-page')

def EmergencyContacts(request):
    if 'email' in request.session:
        return render(request, "miniproject/emergency_contacts.html")
    else:
        return redirect('home-page')

def QuickLinks(request):
    if 'email' in request.session:
        return render(request, "miniproject/quick_links.html")
    else:
        return redirect('home-page')

def AboutUs(request):
    if 'email' in request.session:
        return render(request, "miniproject/about_us.html")
    else:
        return redirect('home-page')




def FirForm(request):
    if 'email' in request.session:
        if request.method == "POST":
            try:
                #name = request.POST['Name']
                #email = request.POST['Email']
                #phone = request.POST['Phone']
                npeople = request.POST['People']
                cat = request.POST['Category']
                sage = request.POST['S-age']
                sgen = request.POST['S-gen']
                srace = request.POST['S-race']
                vage = request.POST['V-age']
                vgen = request.POST['V-gen']
                vrace = request.POST['V-race']
                add = request.POST['Address1']
                city = request.POST['Address2']
                state = request.POST['Address3']
                #country = request.POST['Address4']
                descrip = request.POST['Describe']
                incidtype = request.POST['Incident']
                affect = request.POST['Affect']
                AddReport = FIR.objects.create(
                    #Name = name,
                    #Email = email,
                    #Phone = phone,
                    No_Of_People_Involved = npeople,
                    Category = cat,
                    S_age = sage,
                    S_race = srace,
                    S_gen = sgen,
                    V_age = vage,
                    V_race = vrace,
                    V_gen = vgen,
                    Address = add,
                    City = city,
                    State = state,
                    Describe = descrip,
                    Police_Department = incidtype,
                    Is_affected = affect
                )
                messages.success(request, "FIR filled successfully.")
                return redirect("fir-report")
            except:
                messages.error(request, "All fields are compulsory.")
                return redirect("fir-report")
        else:
            ann = None
            All = FIR.objects.all()
            if len(All) > 0:
                ann = 1
            else:
                ann = 0
            if request.session['is_user'] == "Admin":
                return render(request, "miniproject/report-fir-admin.html", {'All': All, 'n': ann})
            elif request.session['is_user'] == "Police":
                return render(request, "miniproject/report-fir-police.html", {'All': All, 'n': ann})
            else:
                return render(request, "miniproject/report-fir-other.html", {'All': All, 'n': ann})
    else:
        return redirect("home-page")

def FirUpdate(request, pk):
    if 'email' in request.session:
        if request.method == "POST":
            try:
                report = FIR.objects.get(id=pk)
                if request.session['is_user'] == "Admin":
                    print('if')
                    report.No_Of_People_Involved = request.POST['People1']
                    report.Category = request.POST['Category1']
                    report.S_age = request.POST['S-age1']
                    report.S_race = request.POST['S-race1']
                    report.S_gen = request.POST['S-gen1']
                    report.V_age = request.POST['V-age1']
                    report.V_race = request.POST['V-race1']
                    report.V_gen = request.POST['V-gen1']
                    report.Address = request.POST['Address11']
                    report.City = request.POST['Address21']
                    report.State = request.POST['Address31']
                    report.Describe = request.POST['Describe1']
                    report.Police_Department = request.POST['Incident1']
                    report.Is_affected = request.POST['Affect1']
                    if 'Status' in request.POST:
                        report.Status = request.POST['Status']
                elif request.session['is_user'] == "Police":
                    report.Status = request.POST['Status']
                # else:
                #     return redirect("dashboard")
                report.save()
                messages.success(request, "FIR updated successfully.")
                return redirect("fir-report")
            except Exception as ex:
                print(ex)
                messages.error(request, "All fields are compulsory.")
                return redirect("fir-report")
        else:
            try:
                report = FIR.objects.get(id=pk)
            except:
                messages.error(request, "Report does not exist.")
                return redirect("fir-report")
            data = {
                'people': report.No_Of_People_Involved,
                'category': report.Category,
                'sa': report.S_age,
                'sr': report.S_race,
                'sg': report.S_gen,
                'va': report.V_age,
                'vr': report.V_race,
                'vg': report.V_gen,
                'address1': report.Address,
                'address2': report.City,
                'address3': report.State,
                'describe': report.Describe,
                'dep': report.Police_Department,
                'affect': report.Is_affected,
                'status': report.Status,
            }
            return JsonResponse({'data': data})

def FirDelete(request, pk):
    if 'email' in request.session:
        try:
            report = FIR.objects.get(id=pk)
            report.delete()
            messages.success(request, "FIR deleted successfully.")
            return redirect("fir-report")
        except:
            messages.error(request, "Could not delete the report. Please try again.")
    else:
        return redirect("home-page")








def MissingForm(request):
    if 'email' in request.session:
        if request.method == "POST":
            try:
                fname = request.POST['Fname']
                lname = request.POST['Lname']
                gen = request.POST['Gen']
                race = request.POST['Race']
                hair = request.POST['Hair']
                eye = request.POST['Eye']
                dob = request.POST['DOB']
                bmark = request.POST['Birthmark']
                height = request.POST['Height']
                weight = request.POST['Weight']
                ldate = request.POST['Lastdate']
                llocc = request.POST['Lastlocc']
                llocs = request.POST['Lastlocs']
                incidtype = request.POST['Incident']
                AddReport = Missing.objects.create(
                    FName = fname,
                    LName = lname,
                    Gender = gen,
                    Race = race,
                    Hair = hair,
                    Eye = eye,
                    DOB = dob,
                    Birthmark = bmark,
                    Height = height,
                    Weight = weight,
                    Last_Date = ldate,
                    Last_City = llocc,
                    Last_State = llocs,
                    Incident_Type = incidtype
                )
                messages.success(request, "Missing report filled successfully.")
                return redirect("missing-report")
            except:
                messages.error(request, "All fields are compulsory.")
                return redirect("missing-report")
        else:
            ann = None
            All = Missing.objects.all()
            if len(All) > 0:
                ann = 1
            else:
                ann = 0
            if request.session['is_user'] == "Admin":
                return render(request, "miniproject/report-missing-admin.html", {'All': All, 'n': ann})
            elif request.session['is_user'] == "Police":
                return render(request, "miniproject/report-missing-police.html", {'All': All, 'n': ann})
            else:
                return render(request, "miniproject/report-missing-other.html", {'All': All, 'n': ann})
    else:
        return redirect("home-page")

def MissingUpdate(request, pk):
    if 'email' in request.session:
        if request.method == "POST":
            try:
                report = Missing.objects.get(id=pk)
                if request.session['is_user'] == "Admin":
                    report.FName = request.POST['Fname1']
                    report.LName = request.POST['Lname1']
                    report.Gender = request.POST['Gen1']
                    report.Race = request.POST['Race1']
                    report.Hair = request.POST['Hair1']
                    report.Eye = request.POST['Eye1']
                    report.DOB = request.POST['DOB1']
                    report.Birthmark = request.POST['Birthmark1']
                    report.Height = request.POST['Height1']
                    report.Weight = request.POST['Weight1']
                    report.Last_Date = request.POST['Lastdate1']
                    report.Last_City = request.POST['Lastlocc1']
                    report.Last_State = request.POST['Lastlocs1']
                    report.Incident_Type = request.POST['Incident1']
                    if 'Status' in request.POST:
                        report.Status = request.POST['Status']
                elif request.session['is_user'] == "Police":
                    if 'Status' in request.POST:
                        report.Status = request.POST['Status']
                else:
                    return redirect("dashboard")
                report.save()
                messages.success(request, "Missing person report updated successfully.")
                return redirect("missing-report")
            except:
                messages.error(request, "All fields are compulsory.")
                return redirect("missing-report")
        else:
            try:
                report = Missing.objects.get(id=pk)
            except:
                messages.error(request, "Report does not exist.")
                return redirect("missing-report")
            data = {
                'fname': report.FName,
                'lname': report.LName,
                'gen': report.Gender,
                'race': report.Race,
                'hair': report.Hair,
                'eye': report.Eye,
                'dob': report.DOB,
                'birthmark': report.Birthmark,
                'height': report.Height,
                'weight': report.Weight,
                'lastd': report.Last_Date,
                'lastc': report.Last_City,
                'lasts': report.Last_State,
                'type': report.Incident_Type,
                'status': report.Status,
            }
            return JsonResponse({'data': data})

def MissingDelete(request, pk):
    if 'email' in request.session:
        try:
            report = Missing.objects.get(id=pk)
            report.delete()
            messages.success(request, "Missing person report deleted successfully.")
            return redirect("missing-report")
        except:
            messages.error(request, "Could not delete the report. Please try again.")
    else:
        return redirect("home-page")




def WantedForm(request):
    if 'email' in request.session:
        if request.method == "POST":
            try:
                juvenile = "No"
                name = request.POST['FName']
                age = request.POST['Age']
                gender = request.POST['Gender']
                #crime_type = request.POST['Crime']
                race = request.POST['S-race']           
                victims = request.POST['VicCount']
                m_victims = request.POST['MaleVicCount']
                f_victims = request.POST['FemaleVicCount']
                county = request.POST['County']
                state = request.POST['State']
                region = request.POST['Region']
                m_killing = request.POST['Method']
                x = int(age)
                if x < 18 :
                    juvenile = "Yes"
                AddUser = Wanted.objects.create(
                    Name = name,
                    Age = age,
                    Gender = gender,
                    #Crime_Type = crime_type,
                    Race = race,
                    No_Of_Victims = victims,
                    Male_Victims = m_victims,
                    Female_Victims = f_victims,
                    County = county,
                    State = state,
                    Region = region,
                    MOKilling = m_killing,
                    is_juvenile = juvenile
                )
                messages.success(request, "Wanted report filled successfully.")
                return redirect("wanted-report")
            except:
                messages.error(request, "All fields are compulsory.")
                return redirect("wanted-report")
        else:
            ann = None
            All = Wanted.objects.all()
            if len(All) > 0:
                ann = 1
            else:
                ann = 0
            if request.session['is_user'] == "Admin":
                return render(request, "miniproject/report-wanted-admin.html", {'All': All, 'n': ann})
            elif request.session['is_user'] == "Police":
                return render(request, "miniproject/report-wanted-police.html", {'All': All, 'n': ann})
            else:
                return render(request, "miniproject/report-wanted-other.html", {'All': All, 'n': ann})
    else:
        return redirect("home-page")







# def WantedForm(request):
#     if 'email' in request.session:
#         try:
#             if request.method == "POST":
#                 juvenile = "No"
#                 name = request.POST['FName']
#                 age = request.POST['Age']
#                 gender = request.POST['Gender']
#                 #crime_type = request.POST['Crime']
#                 race = request.POST['S-race']           
#                 victims = request.POST['VicCount']
#                 m_victims = request.POST['MaleVicCount']
#                 f_victims = request.POST['FemaleVicCount']
#                 county = request.POST['County']
#                 state = request.POST['State']
#                 region = request.POST['Region']
#                 m_killing = request.POST['Method']
#                 x = int(age)
#                 if x < 18 :
#                     juvenile = "Yes"
#                 AddUser = Wanted.objects.create(
#                     Name = name,
#                     Age = age,
#                     Gender = gender,
#                     #Crime_Type = crime_type,
#                     Race = race,
#                     No_Of_Victims = victims,
#                     Male_Victims = m_victims,
#                     Female_Victims = f_victims,
#                     County = county,
#                     State = state,
#                     Region = region,
#                     MOKilling = m_killing,
#                     is_juvenile = juvenile
#                 )
#                 messages.success(request, "Wanted report filled successfully.")
#                 return redirect("wanted-report")
#             else:
#                 ann = None
#                 All = Wanted.objects.all()
#                 if len(All) > 0:
#                     ann = 1
#                 else:
#                     ann = 0
#                 if request.session['is_user'] == "Admin":
#                     return render(request, "miniproject/report-wanted-admin.html", {'All': All, 'n': ann})
#                 elif request.session['is_user'] == "Police":
#                     return render(request, "miniproject/report-wanted-police.html", {'All': All, 'n': ann})
#                 else:
#                     return render(request, "miniproject/report-wanted-other.html", {'All': All, 'n': ann})
#         except Exception as ex:
#             print(ex)
#             messages.error(request, "All fields are compulsory.")
#             return redirect("wanted-report")
#     else:
#         return redirect("home-page")

def WantedUpdate(request, pk):
    if 'email' in request.session:
        if request.method == "POST":
            try:
                if request.session['is_user'] == "Admin":
                    report = Wanted.objects.get(id=pk)
                    report.Name = request.POST['FName1']
                    report.Age = request.POST['Age1']
                    report.Gender = request.POST['Gender1']
                    report.Race = request.POST['S-race1']
                    report.No_Of_Victims = request.POST['VicCount1']
                    report.Male_Victims = request.POST['MaleVicCount1']
                    report.Female_Victims = request.POST['FemaleVicCount1']
                    report.County = request.POST['County1']
                    report.State = request.POST['State1']
                    report.Region = request.POST['Region1']
                    report.MOKilling = request.POST['Method1']
                    if 'Status' in request.POST:
                        report.Status = request.POST['Status']
                    x = int(request.POST['Age1'])
                    if x < 18 :
                        report.juvenile = "Yes"
                    report.save()
                elif request.session['is_user'] == "Police":
                    if 'Status' in request.POST:
                        report.Status = request.POST['Status']
                else:
                    return redirect("dashboard")
                report.save()
                messages.success(request, "Wanted person report updated successfully.")
                return redirect("wanted-report")
            except:
                messages.error(request, "All fields are compulsory.")
                return redirect("wanted-report")
        else:
            try:
                report = Wanted.objects.get(id=pk)
            except:
                messages.error(request, "Report does not exist.")
                return redirect("wanted-report")
            data = {
                'name': report.Name,
                'age': report.Age,
                'gender': report.Gender,
                'race': report.Race,
                'Tvic': report.No_Of_Victims,
                'Mvic': report.Male_Victims,
                'Fvic': report.Female_Victims,
                'county': report.County,
                'state': report.State,
                'region': report.Region,
                'mok': report.MOKilling,
                'juvenile': report.is_juvenile,
                'status': report.Status,
            }
            return JsonResponse({'data': data})

def WantedDelete(request, pk):
    if 'email' in request.session:
        try:
            report = Wanted.objects.get(id=pk)
            report.delete()
            messages.success(request, "Wanted person report deleted successfully.")
            return redirect("wanted-report")
        except:
            messages.error(request, "Could not delete the report. Please try again.")
    else:
        return redirect("home-page")












# <!-- -------------------------------------------------------------------------------------------------------------- --> #

def VerifyOTP(request):
    if request.method == "POST":
        fname = request.session['fname']
        lname = request.session['lname']
        phone = request.session['tphone']
        email = request.session['email']
        t1 = request.POST['t1']
        t2 = request.POST['t2']
        t3 = request.POST['t3']
        t4 = request.POST['t4']
        mainotp = t1+t2+t3+t4
        print(type(mainotp), type(request.session['otp']))
        if request.session['otp'] == int(mainotp):
            AddUser = User.objects.create(
                FName = request.session['fname'],
                LName = lname,
                Phone = phone,
                Email = email,
                Passwd = request.session['pswd']
            )
            del request.session['pswd']
            del request.session['email']
            del request.session['fname']
            del request.session['lname']
            del request.session['tphone']
            del request.session['otp']
            messages.success(request, "You have Registered successfully. Login to continue.")
            return redirect("login")
        else:
            messages.success(request, "Invalid OTP. Please try again")
            return redirect("verifyotppage")

def FpEmail(request):
    if request.method == "POST":
        email = request.POST['Email'].lower()
        user = User.objects.filter(Email = email)
        if user:
            request.session['email'] = email
            request.session['otp'] = random.randint(1000,9999)
            send_psw_email(request.session['otp'], request.session['email'])
            return redirect("fpotppage")
        else:
            messages.success(request, "User does not exist. Please Register")
            return redirect("register")

def FpOTP(request):
    if request.method == "POST":
        eml = request.POST['email'].lower()
        t1 = request.POST['t1']
        t2 = request.POST['t2']
        t3 = request.POST['t3']
        t4 = request.POST['t4']
        mainotp = t1+t2+t3+t4
        if request.session['otp'] == int(mainotp):
            del request.session['otp']
            return redirect("fppasswordpage")
        else:
            messages.success(request, "Invalid OTP. Please try again")
            return redirect("fpotppage")

def FpPassword(request):
    if request.method == "POST":
        fnd = User.objects.get(Email = request.session['email'])
        pswd = make_password(request.POST['Password'])
        cpswd = make_password(request.POST['CPassword'])
        if pswd == cpswd:
            fnd.Passwd = pswd
            fnd.save()
            messages.success(request, "Password changed successfully. Login to continue.")
            return redirect("login")
        else:
            messages.success(request, "Password and Confirm Password do not match. Please try again")
            return redirect("fppasswordpage")


# <!-- -------------------------------------------------------------------------------------------------------------- --> #




def FeedbackForm(request):
    if 'email' in request.session:
        if request.method == "POST":
            try:
                user = User.objects.get(id=request.session['id'])
                impression = request.POST['Impression']
                problemElaborate = request.POST['ProblemElaborate']
                improvement = request.POST['Improvement']
                ans = Feedback.objects.create(
                    Impression = impression,
                    ProblemElaborate = problemElaborate,
                    Improvement = improvement,
                )
                ans.Usr = user
                if 'ReportAdded' in request.POST:
                    ans.ReportAdded = True
                else:
                    ans.ReportAdded = False

                if 'IsUseful' in request.POST:
                    ans.IsUseful = True
                else:
                    ans.IsUseful = False

                if 'Navigation' in request.POST:
                    ans.Navigation = True
                else:
                    ans.Navigation = False
                    
                if 'ProblemFaced' in request.POST:
                    ans.ProblemFaced = True
                else:
                    ans.ProblemFaced = False
                ans.save()
                messages.success(request, 'Thank You for filling out the feedback form')
                return redirect("dashboard")
            except:
                messages.error(request, 'Could not submit the form. Please try again.')
                return redirect("feedback-form")
        else:
            if request.session['is_user'] == "Admin":
                ann = None
                All = Feedback.objects.all()
                if len(All) > 0:
                    ann = 1
                else:
                    ann = 0
                print(All)
                return render(request, "miniproject/feedback-data.html", {'All': All, 'n': ann})
            else:
                user = User.objects.get(id=request.session['id'])
                allFeedback = Feedback.objects.filter(Usr=user).order_by('-Date')
                if len(allFeedback) == 0:
                    return render(request, "miniproject/feedback-form.html")
                last = allFeedback[0].Date
                today = datetime.now()
                future = last + relativedelta(months=1)
                if future > today:
                    return render(request, "miniproject/feedback-no.html", {'date': future})
                else:
                    print('allowed')
                    return render(request, "miniproject/feedback-form.html")
    else:
        return redirect("home-page")
