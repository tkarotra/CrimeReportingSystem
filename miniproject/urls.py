from django.urls import path
from django.contrib import admin
from .views import *

urlpatterns = [
    path("", Home, name="home-page"),
    path("login/", Login, name="login"),
    path("logout/", Logout, name="logout"),
    path("register/", Register, name="register"),
    
    path("fir-report/", FirForm, name="fir-report"),
    path("fir-update/<int:pk>/", FirUpdate, name="fir-update"),
    path("fir-delete/<int:pk>/", FirDelete, name="fir-delete"),
    
    path("missing-report/", MissingForm, name="missing-report"),
    path("missing-update/<int:pk>/", MissingUpdate, name="missing-update"),
    path("missing-delete/<int:pk>/", MissingDelete, name="missing-delete"),
    
    path("wanted-report/", WantedForm, name="wanted-report"),
    path("wanted-update/<int:pk>/", WantedUpdate, name="wanted-update"),
    path("wanted-delete/<int:pk>/", WantedDelete, name="wanted-delete"),
    
    path("feedback-form/", FeedbackForm, name="feedback-form"),

    path("dashboard/", Dashboard, name="dashboard"),
    path("quick-links/", QuickLinks, name="quick-links"),
    path("emergency-contacts/", EmergencyContacts, name="emergency-contacts"),
    path("about-us/", AboutUs, name="about-us"),



    path("otp-verification/", VerifyOTPPage, name="verifyotppage"),
    path("forgot-password-email/", FpEmailPage, name="fpemailpage"),
    path("forgot-password-otp/", FpOTPPage, name="fpotppage"),
    path("forgot-password-reset/", FpPasswordPage, name="fppasswordpage"),
    # path("missing/", MissingForm, name="missing-form"),
    # path("wanted/", WantedForm, name="wanted-form"),
    
    # path("miss/", MissingF, name="miss"),

    # path("register/", Register, name="register"),
    # path("login/", Login, name="login"),
    path("verify-otp/", VerifyOTP, name="verify-otp"),
    path("fp-email/", FpEmail, name="fp-email"),
    path("fp-otp/", FpOTP, name="fp-otp"),
    path("fp-password/", FpPassword, name="fp-password"),
    # path("fir-register/", FirReport, name="fir-register"),
    # path("missing-register/", MissingReport , name="missing-register"),
    # path("wanted-register/", WantedReport, name="wanted-register"),
    # path("delete-fir/<int:pk>/", DeleteFir, name="delete-fir"),
    # path("delete-missing/<int:pk>/", DeleteMissing, name="delete-missing"),
    # path("delete-wanted/<int:pk>/", DeleteWanted, name="delete-wanted"),
    # path("update-fir/<int:pk>/", UpdateFir, name="update-fir"),
    # path("update-missing/<int:pk>/", UpdateMissing, name="update-missing"),
    # path("update-wanted/<int:pk>/", UpdateWanted, name="update-wanted"),
    # path("missing-ajax-data/<int:pk>/", MissingAjax, name="missing-ajax-data"),
    # path("fir-ajax-data/<int:pk>/", FirAjax, name="fir-ajax-data"),
    # path("wanted-ajax-data/<int:pk>/", WantedAjax, name="wanted-ajax-data"),
    # path("missing-status/<int:pk>/", MissingStatus, name="missing-status"),
    # path("fir-status/<int:pk>/", FirStatus, name="fir-status"),
    # path("wanted-status/<int:pk>/", WantedStatus, name="wanted-status"),
    # path("feedback-form-data/", FeedbackFormData, name="feedback-form-data"),
]