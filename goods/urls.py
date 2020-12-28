from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.IndexViews.as_view()),
    path('category/<int:cid>',views.IndexViews.as_view()),
    path('category/<int:cid>/page/<int:num>',views.IndexViews.as_view()),
    path('goodsdetails/<int:goodsid>',views.DetailViews.as_view()),
]