from django.shortcuts import render,redirect
from django.http import HttpResponse
from Accounts.models import User
from django.contrib.auth import authenticate,login,logout

def bad_request(msg="Bad Request"):
    return HttpResponse(msg, status=400)

def unauthorized(msg="Invalid credentials"):
    return HttpResponse(msg, status=401)

def server_error(e):
    return HttpResponse(f"Internal Server Error", status=500)


def login_user(request):
    try:
        if(request.method == 'POST'):
            username = request.POST['username']
            password = request.POST['password']
            
            if not username or not password:
                return bad_request("Username and password are required")
            
            user = authenticate(username=username, password=password)
            
            if user is None:
                return unauthorized()
            
            login(request, user)
            return redirect('dashboard') 
                    
        return render(request, "Accounts/login.html")
    
    except Exception as e:
        return server_error(e)


def signup(request):
    try:
        return render(request, "Accounts/signup.html")
    
    except Exception as e:
        return server_error(e)
    
    
def save_user(request):
    try:
        if request.method != 'POST':
            return bad_request("Method not allowed")
        
        name = request.POST['name']
        email = request.POST['email']
        mobile = request.POST['mobile_number']
        role = request.POST['role']
        username = request.POST['username']
        password = request.POST['password']
        
        if not all([name, email, username, password]):
            return bad_request("Missing required fields")

        if User.objects.filter(username=username).exists():
            return HttpResponse("Username already exists", status=409)
        
        user = User.objects.create_user(
            name=name,
            email=email,
            mobile=mobile,
            username=username,
            role=role
        )
        user.set_password(password)
        user.save()
        return redirect('login')
    
    except Exception as e:
        return server_error(e)
    
def logout_user(request):
    try:
        logout(request)
        return redirect('login')
    
    except Exception as e:
        return server_error(e)