from django.urls import path
from Users import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard', views.dashboard, name="dashboard"),
    path('create-user', views.create_user, name='create_user_page'),
    path('user-list', views.user_list, name='user_list'),
    path('transaction-services', views.transaction_services, name='transaction_services'),
    path('create-transaction', views.create_transaction, name='create_transaction_page'),
    path('update-transaction', views.update_transaction, name='update_transaction_page'),
    path('delete-transaction', views.delete_transaction, name='delete_transaction_page'),
    path('user-analysis', views.user_analysis, name='user_analysis'),
    path('transaction-analysis', views.transaction_analysis, name='transaction_analysis'),
    path('filter-transaction', views.filter_transaction, name='filter_transaction')
]
