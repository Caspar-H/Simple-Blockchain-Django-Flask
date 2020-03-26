from django.urls import path

from . import views

app_name = 'blockchainapp'
urlpatterns = [
    path('test/', views.test, name='test'),
    path('mine/', views.mine, name='mine'),
    path('fullchain/', views.full_chain, name='full_chain'),
    path('newtransaction/', views.new_transaction, name='new_transaction'),
    path('registernodes/', views.register_nodes, name='register_nodes'),
    path('consensus/', views.consensus, name='consensus'),
]
