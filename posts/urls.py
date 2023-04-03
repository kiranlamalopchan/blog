
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import HomeView, BlogView, MyPostView, PostCreateView, PostDeleteView, PostDetailView, ContactView, MobilePriceView, PostUpdateView, RegisterView, MyProfileView, ProfilePictureView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("blog/", BlogView.as_view(), name="blog"),
    path("mypost/<id>/", MyPostView.as_view(), name="mypost"),
    path("myprofile/<id>/", MyProfileView.as_view(), name="myprofile"),
    path("myprofile-picture/<id>/", ProfilePictureView.as_view(),
         name="myprofilepicture"),
    path("create/", PostCreateView.as_view(), name="post-create"),
    path("mypost/<id>/update/", PostUpdateView.as_view(), name="post-update"),
    path("mypost/<id>/delete/", PostDeleteView.as_view(), name="post-delete"),
    path("post-detail/<id>/", PostDetailView.as_view(), name="post-detail"),
    path("mobile-price/", MobilePriceView.as_view(), name="mobile-price"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("login/", auth_views.LoginView.as_view(template_name='login.html'), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name='logout.html'), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path('tinymce/', include('tinymce.urls')),
]
