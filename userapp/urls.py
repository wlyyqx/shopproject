from django.urls import path,include
from . import views

urlpatterns = [
    path('register/',views.RegisterViews.as_view()),
    path('checkUname/',views.CheckUnameViews.as_view()),
    path('center/',views.CenterViews.as_view()),
    path('logout/',views.LogoutViews.as_view()),
    path('login/',views.LoginViews.as_view()),
    path('loadCode.png',views.LoadCodeViews.as_view()),
    path('checkcode/',views.CheckcodeViews.as_view()),
    path('address/',views.AddressViews.as_view()),
    path('loadArea/',views.LoadAreaViews.as_view()),

]