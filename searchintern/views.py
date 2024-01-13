from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render 
from userinfo.models import User_details
from submit_std.models import Student
from rec_details.models import RecruiterForm
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import re

#----------------------------------------------
# this is for authentication
def homepage(request):
        contents = {"title":"Home"}
        return render(request, 'index.html', contents)

@login_required(login_url='login')
def aboutUs(request):
        contents = {"title":"aboutus"}
        return render (request, 'about_us.html', contents)


def recform(request):
    return render(request,'rec_form.html')
def register(request):
    contents = {"title":"Registration"}
    return render(request,"register_form.html",contents)

@login_required(login_url='login')
def userprofile(request):
    contents = {"title":"profile"}
    return render(request,"user_profile.html",contents)

def signup(request):
    print("signup")
    error = False
    
    try:
        if request.method == 'POST':
            print("Inside POST method")
            # Accessing form data
            name = (request.POST.get('name'))
            email = request.POST.get('email')
            pw = request.POST.get('pass')
            vpw = request.POST.get('v-pass')

            category= request.POST.get('category')
            if pw != vpw:
                contents = {'title': "signup",
                                   'error':True,
                                   'error_message':"password mismatch",
                                   }
                return render(request, "signup.html", contents)

            print("Email:", email)
            print("Password:", pw)
            
            if is_valid_email(email):
               print("in valid email")
               if is_valid_password(pw):
                   print("in valid pass")
                   if is_valid_name(name):
                       print("in valid name")
                       
                       en1=User_details(name=name,email=email,password=pw,category=category)
                       en2 = User.objects.create_user(name,email,pw)
                       try:
                            en2.save()
                            en1.save()
                           
                            print("save to both")
                            contents = {'title': "login",
                                   'error':True,
                                   'error_message':"congratulations now login",
                                   }

                            return render(request,"login.html")
                        
                       except Exception as e:
                           contents = {'title': "signup",
                                   'error':True,
                                   'error_message':"didnt submit on user",
                                   }
                           print("Error:", str(e))
                           return render(request, 'signup.html',contents)

                       return HttpResponse("welcome")
                   else:
                        contents = {'title': "signup",
                                   'error':True,
                                   'error_message':"invalid name",
                                   }
                        return render(request, "signup.html", contents)
               else:
                   
                   contents = {'title': "signup",
                                   'error':True,
                                   'error_message':"invalid password",
            
                                } 
                   return render(request, "signup.html", contents)
            else:    
                             
                 contents = {'title': "signup",
                                   'error':True,
                                   'error_message':"invalid email",
                                   }
                 return render(request, "signup.html", contents)
        else:
            contents={"title":"signup",
                      'error':False}
            print("Inside else")
            return render(request, "signup.html", contents)

    except Exception as e:
        print("Error:", str(e))

    


#rex match function
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    match = re.match(pattern, email)
    return bool(match)
def is_valid_password(password):
    # At least 8 characters, containing both letters and numbers
    pattern = r'^(?=.*[a-zA-Z])(?=.*\d).{8,}$'

   
    match = re.match(pattern, password)

    # Return True if the password is valid, False otherwise
    return bool(match)


def is_valid_name(name):
    # Define the regex pattern for name validation
    # Allows letters and optional spaces
    pattern = r'^[a-zA-Z]*$'


    # Use re.match to check if the name matches the pattern
    match = re.match(pattern, name)

    # Return True if the name is valid, False otherwise
    return bool(match)

# def login(request):
#     error = False
    
#     try:
#         if request.method == 'POST':
#             print("Inside POST method")
#             # Accessing form data
#             email =str(request.POST.get('email'))
#             pw = str(request.POST.get('pass'))
#             print("Email:", email)
#             print("Password:", pw)
#             if is_valid_email(email):
#                login_data = User_details.objects.all()
#                for a in login_data:
#                    print(a.email)
#                    print(a.password)
#                    if a.email == email and a.password == pw:
#                       return render(request, 'index.html') 
                   
#                contents = {"title": "Login", 'error': True,"error_message":"credential mismatch"}
#                return render(request, "login.html", contents)
              
#             else:
            
                
#                 contents = {"title": "Login", 'error': True,'error_message':"Enter proper value"}
#                 return render(request, "login.html", contents)

#             return render(request, "login.html", contents)
#         else:
#             print("Inside else")
#             contents = {"title": "Login", 'error': error}
#             return render(request, "login.html", contents)

#     except Exception as e:
#         print("Error:", str(e))  # Print or log the exception message
#         contents = {"title": "Login", 'error': error, 'exception_message': str(e)}
#         return render(request, "login.html", contents)

def login(request):
    error = False
    
    try:
        if request.method == 'POST':
            print("Inside POST method")
            # Accessing form data
            name =str(request.POST.get('name'))
            pw = str(request.POST.get('pass'))
            print("name:", name)
            print("Password:", pw)
            if is_valid_name(name):
               
               user = authenticate(request,username=name,password=pw)
               

               if user is not None:
                   auth_login(request,user,pw)
                   return render(request,'index.html')
               else:
                   contents = {"title": "Login", 'error': True,"error_message":"credential mismatch"}
                   return render(request, "login.html", contents)
              
            else:
            
                
                contents = {"title": "Login", 'error': True,'error_message':"Enter proper value"}
                return render(request, "login.html", contents)

            return render(request, "login.html", contents)
        else:
            print("Inside else")
            contents = {"title": "Login", 'error': error}
            return render(request, "login.html", contents)

    except Exception as e:
        print("Error:", str(e))  # Print or log the exception message
        contents = {"title": "Login", 'error': error, 'exception_message': str(e)}
        return render(request, "login.html", contents)

def logoutPage(request):
    logout(request)
    return render(request,'index.html')

#to save the data from recuiter
def recdata(request):
    if request.method == 'POST':
        internship_title = request.POST.get('internshipTitle')
        address = request.POST.get('address')
        description = request.POST.get('description')
        #duration = request.POST.get('duration')
        category = request.POST.get('category')
        timing = request.POST.get('timing')
        formDueDate = (request.POST.get('formDueDate'))
        en1= RecruiterForm(internship_title=internship_title,address=address,description=description,category=category,timing=timing,deadline=formDueDate)
        en1.save()

        return HttpResponse("submitted")
    

def submitStudent(request):
    print(f"Submit student : {request}")
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        #duration = request.POST.get('duration')
        address = request.POST.get('address')
        skills = request.POST.get('skills')
        sskill = request.POST.get('sskill')
        college = request.POST.get('college')
        course = request.POST.get('course')
        github=request.POST.get('github')
        linkedin=request.POST.get('linkedin')
        
        en= Student(name=name,email=email,phone=phone,address=address,skills=skills,sskill=sskill,college=college,course=course,github=github,linkedin=linkedin)
        en.save()
        # en1= RecruiterForm(internship_title=internship_title,address=address,description=description,category=category,timing=timing,deadline=formDueDate)
        # en1.save()

        return HttpResponse("submitted")    
