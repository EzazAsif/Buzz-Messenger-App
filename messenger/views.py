from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from messenger.models import *
import string
from django.http import JsonResponse

def home(request):
    if request.method=="POST":
        data=request.POST
        Email=data.get('first')
        password=data.get('password')

        user=User.objects.filter(email=Email)

        if not user.exists() :
            messages.error(request,"User doesn't Exists")
            return redirect('/home/')
        
        else:
            user=User.objects.get(email=Email)
            username=user.username
            user=authenticate(request,username=username,password=password)

            if user is not None:
                login(request,user)
                return redirect('/chat/')
             
            else:
                messages.error(request,"Invalid Password")
                return redirect('/home/')
                
        
    return render(request,"index.html") 





def register(request):
    
    if request.method=="POST":
        data=request.POST
        Firstname=data.get('FirstName')
        Lastname=data.get('LastName')
        Email=data.get('email')
        password=data.get('psw')
        rpassword=data.get('psw-repeat')

        if checkvalidity(request,password,rpassword,Email):
            username=f"{Firstname} {Lastname}"
            user = User.objects.create(username=username, email=Email, first_name=Firstname, last_name=Lastname)
            user.set_password(password) 
            user.save()
            user2=UserProfile.objects.create(profileid =user.id)
            user2.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect('/home/')
        
    return render(request,"register.html")




def chat_interface(request):
    mainuserpicture=UserProfile.objects.get(profileid=request.user.id)
    user=User.objects.exclude(username=request.user.username)
    userpictures=UserProfile.objects.exclude(profileid=request.user.id)
    chatuser=User.objects.filter(username="dryrdyer")
    if not chatuser:
     chatuser=user[0]
    chatusers=chat_user(request.user.id)
    chatuserpictur=UserProfile.objects.get(profileid=chatuser.id)
    users_and_pictures = list(zip(user, userpictures))
    chatuserpicture=chatuserpictures(chatusers)
    chatusers_and_pictures = list(zip(chatusers, chatuserpicture))
    return render(request, "chatting interface null.html",context={'chatusers_and_pictures':chatusers_and_pictures,'users_and_pictures':users_and_pictures,'users':user,'chatuser':chatuser,'chatusers':chatusers,'mainuserpicture':mainuserpicture,'chatuserpicture':chatuserpictur})
   




def chat_interface_user(request,id):
    mainuserpicture=UserProfile.objects.get(profileid=request.user.id)
    if request.method == "POST" :
        message = request.POST.get('message')
        picture = request.FILES.get('picturefile')
        if message or picture:
            if message:
                Messages.objects.create(sender=request.user.id, message=message, receiver=id)
                return redirect(f"/chat/{id}/")
            if picture:
                Messages.objects.create(sender=request.user.id, attachment=picture, receiver=id)
                return redirect(f"/chat/{id}/")
    user = User.objects.exclude(username=request.user.username)
    chatuser = User.objects.get(id=id)
    chatuserpictur=UserProfile.objects.get(profileid=id)
    userpictures=UserProfile.objects.exclude(profileid=request.user.id)
    if not chatuser:
        chatuser.id=user[0].id
    chatusers=chat_user(request.user.id)
    users_and_pictures = list(zip(user, userpictures))
    chatuserpicture=chatuserpictures(chatusers)
    chatusers_and_pictures = list(zip(chatusers, chatuserpicture))
    return render(request, "chatting interface null.html",context={'chatusers_and_pictures':chatusers_and_pictures,'users_and_pictures':users_and_pictures,'users':user,'chatuser':chatuser,'chatusers':chatusers,'mainuserpicture':mainuserpicture,'chatuserpicture':chatuserpictur})


def get_chat(request,id):
    messages = Messages.objects.filter(sender=request.user.id,receiver=id)|Messages.objects.filter(sender=id,receiver=request.user.id)
    messages_html = list(messages.values())
          
    return JsonResponse({'messages': messages_html,'id':id})


def chat_user(uid):
    messages = Messages.objects.filter(receiver=uid)|Messages.objects.filter(sender=uid)
    id_array = [message.sender for message in messages] + [message.receiver for message in messages]
    id_array = list(set(id_array))
    if uid in id_array:
      id_array.remove(uid)
    users = User.objects.filter(id__in=id_array)
    return(users)


def checkvalidity(request, passw, rpassw,Email):
    if len(passw) < 8:
        messages.error(request, "Passwords must be at least 8 characters")
        return False
    elif passw != rpassw:
        messages.error(request, "Passwords don't match")
        return False
    elif User.objects.filter(username=Email).exists():
        messages.error(request, "User Exists")
        return False
    
    return True

def contains_any(string, char_list):
    for char in string:
        if char in char_list:
            return True
    return False

def edit_profile(request):
    user=User.objects.get(id=request.user.id)
    if request.method=="POST":
        data=request.POST
        Firstname=data.get('FirstName')
        Lastname=data.get('LastName')
        Email=data.get('email')
        password=data.get('psw')
        rpassword=data.get('psw-repeat')
        picture = request.FILES.get('editpp')
        if(password and rpassword ):
            if( password==rpassword):
                user.set_password(password)
            else:
                messages.error(request,"Passwords don't match")  
        if Firstname:
            user.first_name=Firstname
        if Lastname:
            user.last_name=Lastname
        if Email:
            user.email=Email
        if picture:
            userp=UserProfile.objects.get(profileid=request.user.id)
            userp.picture=picture
            userp.save()
            messages.success(request, "Changes Succesful")
        return redirect('/editprofile/')
    
    return render(request,"editprofile.html",context={'users':user})

def chatuserpictures(chatuser):
    chatuserpictures=[]
    for i in chatuser:
        chatuserpicture=UserProfile.objects.get(profileid=i.id)
        chatuserpictures.append(chatuserpicture)
    return(chatuserpictures)