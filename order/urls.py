from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.ToOrderViews.as_view()),
    path('order.html/',views.OrderListViews.as_view()),


]