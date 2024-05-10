from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from messenger.models import Messages
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
            messages.success(request, "Registration successful. You can now log in.")
            return redirect('/home/')
        
    return render(request,"register.html")




def chat_interface(request):
    user=User.objects.exclude(username=request.user.username)
    chatuser=User.objects.filter(username="dryrdyer")
    if not chatuser:
     chatuser.id=user[0].id
    chatusers=chat_user(request.user.id)
    return render(request, "chatting interface null.html",context={'users':user,'chatuser':chatuser,'chatusers':chatusers})
   



def chat_interface_user(request,id):
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
    if not chatuser:
        chatuser.id=user[0].id
    chatusers=chat_user(request.user.id)
    return render(request, "chatting interface null.html",context={'users':user,'chatuser':chatuser,'chatusers':chatusers})


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