from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from wscubetech.views import (
    index, about, contact_view, cab, cab_search, insurance_view,
    hotel, travel_guides, weather, add_history, package, profile,
    Help, auth_view, messages_list_view, Course, courseDetails
)

urlpatterns = [
    path("", index, name="home"),

    path("admin/", admin.site.urls),

    path("about/", about, name="about"),
    path("contact/", contact_view, name="contact"),
    path("cab/", cab, name="cab"),
    path("cab-search/", cab_search, name="cab_search"),
    path("insurance/", insurance_view, name='insurance'),
    path("hotel/", hotel, name="hotel"),
    path("travel-guides/", travel_guides, name='travel_guides'),
    path("weather/", weather, name="weather"),
    path("add-history/", add_history, name="add_history"),
    path("package/", package, name="package"),
    path("profile/", profile, name="profile"),
    path("Help/", Help, name="Help"),

    # ✅ LOGIN / LOGOUT
    path("signin/", auth_views.LoginView.as_view(template_name="signin.html"), name="signin"),
    path("logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"),

    path("auth/", auth_view, name="auth"),
    path("messages/", messages_list_view, name="messages_list"),
    path("course/", Course, name="course_list"),
    path("course/<int:courseid>/", courseDetails, name="course_details"),
]
