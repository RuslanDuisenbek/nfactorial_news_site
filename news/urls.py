from django.urls import path, register_converter
from news import views
from . import convertors

register_converter(convertors.FourDigitYearConvertor, 'year4')
urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('addpage/', views.AddPage.as_view(), name='addpage'),
    path('about/', views.about, name='about'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', views.Categories.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.TagPostLists.as_view(), name='tag'),
    path('edit/<slug:slug>/', views.UpdatePage.as_view(), name='edit_page'),
    path('delete/<slug:slug>/', views.DeletePage.as_view(), name='delete_page'),
    path('content/', views.contacts, name='contacts'),

]
