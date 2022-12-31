from django.urls import path
from . import views
urlpatterns =[
    path('',views.main, name="main"),
    path('menu-list',views.menuList, name="menu-list"),
    path('login',views.loginpage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerpage, name="register"),
    path("about/", views.about, name="about"),


    path('check-out', views.checkOut, name="check-out"),
    path('delivery', views.delivery, name="delivery"),
    path('menu-view/<str:pk>/', views.menuView, name="menu-view"),
    path('update_item/', views.updateItem, name="update_item"),
    path('delivery_text', views.orders, name="delivery_text"),
    path('process_order/', views.processOrder, name="process_order"),
    path('cart_num/', views.cartNumber, name="cart_num"),
    path("data/", views.ajaxUpdate, name="data"),
    path("history/", views.historyPage, name="history"),
    path('product_form', views.createProduct, name="product_form"),
    path('transaction_page/<str:pk>/', views.TransactionPage, name="transaction_page"),

]