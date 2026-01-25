from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),  # Default route
    path("index.html", views.index, name="index"),
    path("UserLogin.html", views.UserLogin, name="UserLogin"),
    path("UserLoginAction", views.UserLoginAction, name="UserLoginAction"),
    path("Register.html", views.Register, name="Register"),
    path("RegisterAction", views.RegisterAction, name="RegisterAction"),
    path("UploadFile.html", views.UploadFile, name="UploadFile"),
    path("UploadFileAction", views.UploadFileAction, name="UploadFileAction"),
    path("DownloadFile", views.DownloadFile, name="DownloadFile"),
    path("VerifyIntegrity", views.VerifyIntegrity, name="VerifyIntegrity"),
    path("VerifyIntegrityAction", views.VerifyIntegrityAction, name="VerifyIntegrityAction"),
    path("DownloadFileAction", views.DownloadFileAction, name="DownloadFileAction"),
    path("Graph", views.Graph, name="Graph"),
]
