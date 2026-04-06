from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required,permission_required,user_passes_test
from Accounts.models import User
from Users.models import Transaction

def unauthorized():
    return HttpResponse("Unauthorized", status=403)

def server_error(e):
    return HttpResponse(f"Internal Server Error: {str(e)}", status=500)

def home(request):
    try:
        return render(request, 'Users/home.html')
    
    except Exception as e:
        return server_error(e)


@login_required
def dashboard(request):
    try: 
        return render(request, "users/dashboard.html", {
            "role" : request.user.role,
            "user" : request.user
        })
        
    except Exception as e:
        return server_error(e)
        
    
@login_required
def create_user(request):
    if(request.user.role == 'admin'):
        try:
            return render(request, 'Users/create_user.html')
        
        except Exception as e:
            return server_error(e)
    
    else:
        return unauthorized()
    
    
@login_required
def user_list(request):
    if(request.user.role == 'admin'):
        try:
            return redirect('/api/get-users')
        
        except Exception as e:
            return server_error(e)
    
    else:
        return unauthorized()
    
    
@login_required
def transaction_services(request):
    try:   
        return render(request, 'Users/transaction_services.html',{
            "role" : request.user.role,
            "user" : request.user       
        })
        
    except Exception as e:
        return server_error(e)
    
    
@login_required
def create_transaction(request):
    if(request.user.role == 'admin'):
        try:
            user = User.objects.values('id')
            return render(request, 'Users/create_transaction.html', {
                'data' : user 
            })
            
        except Exception as e:
            return server_error(e)
    
    else:
        return unauthorized()

@login_required
def update_transaction(request):
    if(request.user.role == 'admin'):
        try:
            transaction = Transaction.objects.values('id','amount', 'transaction_type', 'category', 'description')
            return render(request, 'Users/update_transaction.html', {
                'data': transaction,
            })
            
        except Exception as e:
            return server_error(e)
    
    else:
        return unauthorized()
    
    
@login_required
def delete_transaction(request):
    if(request.user.role == 'admin'):
        try:
            transaction = Transaction.objects.values('id','amount', 'transaction_type', 'category', 'description')
            return render(request, 'Users/delete_transaction.html', {
                'data': transaction,
            })
        
        except Exception as e:
            return server_error(e)
    
    else:
        return unauthorized()
    

@login_required
def user_analysis(request):
    if(request.user.role == 'admin'):
        try:
            admin_count = len(User.objects.filter(role='admin'))
            analyst_count = len(User.objects.filter(role='analyst'))
            viewer_count = len(User.objects.filter(role='viewer'))
            total = admin_count+analyst_count+viewer_count
            return render(request, "Users/user_analysis.html",{
                'total' : total,
                'admin' : admin_count,
                'analyst' : analyst_count,
                'viewer' : viewer_count
            })
            
        except Exception as e:
            return server_error(e)
        
    else:
        unauthorized()
    
@login_required
def transaction_analysis(request):
    try:
        return render(request, "Users/transaction_summary.html")
    
    except Exception as e:
        return server_error(e)


@login_required
def filter_transaction(request):
    try:
        if(request.user.role == 'admin'):
            data = Transaction.objects.all()
            
        elif(request.user.role == 'analyst'):
            data = Transaction.objects.filter(user=request.user)
            
        else:
            return unauthorized()

        date = data.values_list('date__date', flat=True).distinct()
        category = data.values_list('category', flat=True).distinct()
        transaction_type = data.values_list('transaction_type', flat=True).distinct()
        return render(request, 'Users/filter_search.html', {
            'date' : date,
            'category' : category,
            'transaction_type' : transaction_type,
        })
        
    except Exception as e:
        return server_error(e)