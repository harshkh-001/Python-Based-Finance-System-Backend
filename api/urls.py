from django.urls import path
from api import views

urlpatterns = [
    path('create-user', views.create_user, name="create_user"),
    path('get-users', views.get_users, name = "get_users"),
    path('get-transactions', views.get_transactions, name='get_transactions'),
    path('create-transaction', views.create_transaction, name='create_transaction'),
    path('update-transaction', views.update_transaction, name='update_transaction'),
    path('delete-transaction', views.delete_transaction, name='delete_transaction'),
    path('summary', views.financial_summary, name='financial_summary'),
    path('category-breakdown', views.category_breakdown, name='category_breakdown'),
    path('monthly-summary', views.monthly_summary, name='monthly_summary'),
    path('recent-transactions', views.recent_activity, name='recent_activity'),
    path('get-filter-transactions', views.filter_transactions, name='filter_transactions')
    
]
