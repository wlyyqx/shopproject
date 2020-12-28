from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.AddCartViews.as_view()),
    path('queryAll/',views.CartListViews.as_view()),

]