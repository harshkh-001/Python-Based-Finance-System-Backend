from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.decorators import api_view
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from Accounts.models import User
from django.contrib import messages
from .serializer import UserSerializer
from Users.models import Transaction
from .serializer import TransactionSerializer
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from rest_framework import status

@login_required
@api_view(['POST'])
def create_user(request):
    if request.method != 'POST':
        return Response({"success": False, "error": "Method not allowed"}, status=405)

    if request.user.role != 'admin':
        return Response({"success": False, "error": "Unauthorized"}, status=403)
    
    try:
        print(request.POST)
        name = request.POST['name']
        email = request.POST['email']
        mobile = request.POST['mobile_number']
        role = request.POST['role']
        username = request.POST['username']
        password = request.POST['password']
        
        if not all([name, email, username, password]):
            messages.error(request, "Missing required fields")
            return redirect('create_user_page')
        
        user = User.objects.create_user(
            name=name,
            email=email,
            mobile=mobile,
            username=username,
            role=role
        )
        user.set_password(password)
        user.save()
        return Response({
            "success": True,
            "data": "User created successfully"
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            "success": False,
            "error": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
@login_required
@api_view(['GET'])
def get_users(request):
    if(request.method == "GET" and request.user.role == 'admin'):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    else:
        return HttpResponse("You are not authorized for this page")
    
@login_required
@api_view(['GET'])
def get_transactions(request):
    if(request.user.role == 'admin'):
        transaction = Transaction.objects.all()
        serializer = TransactionSerializer(transaction, many=True)
        return Response(serializer.data)
    else:
        transaction = Transaction.objects.filter(user=request.user)
        serializer = TransactionSerializer(transaction, many=True)
        return Response(serializer.data)
    
    
@login_required
@api_view(['POST'])
def create_transaction(request):
    if request.method != 'POST':
        return Response({"success": False, "error": "Method not allowed"}, status=405)

    if request.user.role != 'admin':
        return Response({"success": False, "error": "Unauthorized"}, status=403)
    
    try:
        id = request.POST.get('id')
        user = User.objects.get(id=id)
        amount = request.POST.get('amount')
        transaction_type = request.POST.get('transaction_type')
        category = request.POST.get('category')
        description = request.POST.get('description', '')
        
        if not all([id, amount, transaction_type, category]):
            return Response({"success": False, "error": "Missing required fields"}, status=400)
        
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({"success": False, "error": "User not found"}, status=404)
        
        transaction = Transaction.objects.create(
            user=user,
            amount=amount,
            transaction_type=transaction_type,
            category=category.lower(),
            description=description
        )
        transaction.save()
        return Response({
            "success": True,
            "data": "Transaction created successfully"
        }, status=201)
    
    except Exception as e:
        return Response({
            "success": False,
            "error": str(e)
        }, status=500)
    
    
@login_required
@api_view(['POST'])
def update_transaction(request):
    if request.method != 'POST':
        return Response({"success": False, "error": "Method not allowed"}, status=405)
    
    if request.user.role != 'admin':
        return Response({"success": False, "error": "Unauthorized"}, status=403)
        
    try:
        id = request.POST.get('id')
        amount = request.POST.get('amount')
        transaction_type = request.POST.get('transaction_type')
        category = request.POST.get('category')
        description = request.POST.get('description', '')
        
        transaction = Transaction.objects.filter(id=id)
    
        if not transaction.exists():
            return Response({
                "success": False,
                "error": "Transaction not found"
            }, status=404)
            
            
        transaction.update(
            amount=amount,
            transaction_type=transaction_type,
            category=category,
            description=description
        )
        return Response({
            "success": True,
            "data": "Transaction updated successfully"
        })

    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=500)
    
    
@login_required
@api_view(['POST'])
def delete_transaction(request):
    if request.method != 'POST':
        return Response({"success": False, "error": "Method not allowed"}, status=405)

    if request.user.role != 'admin':
        return Response({"success": False, "error": "Unauthorized"}, status=403)
    
    try:
        id = request.POST.get('id')
        
        transaction = Transaction.objects.filter(id=id)
        
        if not transaction.exists():
            return Response({
                "success": False,
                "error": "Transaction not found"
            }, status=404)

        transaction.delete()
        return Response({
            "success": True,
            "data": "Transaction deleted successfully"
        })
     
    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=500)
    
    
@login_required
@api_view(['GET'])
def financial_summary(request):
    if(request.user.role == 'admin'):
        income = Transaction.objects.filter(transaction_type='income').aggregate(Sum('amount'))['amount__sum'] or 0
        expense = Transaction.objects.filter(transaction_type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
        balance = income - expense
        return Response({
            "total_income": income,
            "total_expense": expense,
            "current_balance": balance
        })
    
    else:
        user = request.user
        income = Transaction.objects.filter(user=user, transaction_type='income').aggregate(Sum('amount'))['amount__sum'] or 0
        expense = Transaction.objects.filter(user=user, transaction_type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
        balance = income - expense
        return Response({
            "total_income": income,
            "total_expense": expense,
            "current_balance": balance
        })
    
    
@login_required
@api_view(['GET'])
def category_breakdown(request):
    if(request.user.role == 'admin'):
        data = ([
        {
            'Income' : 
            Transaction.objects
            .filter(transaction_type='income')
            .values('category')
            .annotate(total=Sum('amount'))
            .order_by('-total')
        }, 
        {
            'Expense' : 
            Transaction.objects
            .filter(transaction_type='expense')
            .values('category')
            .annotate(total=Sum('amount'))
            .order_by('-total')
        }
        ])
        return Response(data)
    
    else:
        user = request.user
        data = ([
        {
            'Income' : 
            Transaction.objects
            .filter(user=user, transaction_type='income')
            .values('category')
            .annotate(total=Sum('amount'))
            .order_by('-total')
        }, 
        {
            'Expense' : 
            Transaction.objects
            .filter(user=user, transaction_type='expense')
            .values('category')
            .annotate(total=Sum('amount'))
            .order_by('-total')
        }
        ])
        return Response(data)



@login_required
@api_view(['GET'])
def monthly_summary(request):
    if(request.user.role == 'admin'):
        data = (
            Transaction.objects
            .filter()
            .annotate(month=TruncMonth('created_at'))
            .values('month', 'transaction_type')
            .annotate(total=Sum('amount'))
            .order_by('month')
        )
        return Response(data)
    
    else: 
        user = request.user
        data = (
            Transaction.objects
            .filter(user=user)
            .annotate(month=TruncMonth('created_at'))
            .values('month', 'transaction_type')
            .annotate(total=Sum('amount'))
            .order_by('month')
        )
        return Response(data)


@api_view(['GET'])
def recent_activity(request):
    if(request.user.role == 'admin'):
        transactions = Transaction.objects.all().order_by('-created_at')[:5]
        data = [
            {
                "amount": t.amount,
                "transaction_type": t.transaction_type,
                "category": t.category,
                "date": t.created_at
            }
            for t in transactions
        ]
        return Response(data)
    
    else:
        user = request.user
        transactions = Transaction.objects.filter(user=user).order_by('-created_at')[:5]
        data = [
            {
                "amount": t.amount,
                "transaction_type": t.transaction_type,
                "category": t.category,
                "date": t.created_at
            }
            for t in transactions
        ]
        return Response(data)

@login_required
@api_view(['GET'])
def filter_transactions(request):
    try:
        date = request.GET.get('date')
        category = request.GET.get('category')
        transaction_type = request.GET.get('transaction_type')

        if request.user.role == 'admin':
            transaction = Transaction.objects.all()
        else:
            transaction = Transaction.objects.filter(user=request.user)

        if date:
            transaction = transaction.filter(date__date=date)

        if category:
            transaction = transaction.filter(category=category)

        if transaction_type:
            transaction = transaction.filter(transaction_type=transaction_type)

        serializer = TransactionSerializer(transaction, many=True)
        
        return Response({
            "success": True,
            "data": serializer.data
        }, status=200)
        
    except Exception as e:
        return Response({
            "success": False,
            "error": str(e)
        }, status=500)