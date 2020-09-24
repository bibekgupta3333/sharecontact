from django.urls import path
from . import views

app_name = 'blogposts'

urlpatterns = [
    path('create/', views.CreateContactView.as_view(), name='create'),
    path('', views.ListContactView.as_view(), name='list'),
    path('list/<str:author>/<int:author_id>/<slug:slug>/',
         views.DetailContactView.as_view(), name='detail'),
    path('<str:author>/<int:author_id>/',
         views.UserDetailListContactView.as_view(), name='user_post_list'),
    path('update/<str:author>/<int:author_id>/<slug:slug>/',
         views.UpdateContactView.as_view(), name='update'),
    path('delete/<int:author_id>/<slug:slug>/',
         views.DeleteContactView.as_view(), name='delete'),
]
