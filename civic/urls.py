from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("user-login/", views.user_login, name="user_login"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_view, name="login"),
    path("dashboard/", views.front, name="front"),
    path("logout/", views.logout_view, name="logout"),
    path("issue/", views.issue, name="issue"),
    path("profile/", views.profile, name="profile"),
    path("feedback/", views.feedback, name="feedback"),
    path("my-city/", views.my_city, name="my_city"),
    path("help/", views.help_page, name="help"),
    path("privacy/", views.privacy, name="privacy"),
    path("about/", views.about, name="about"),

    path("admin-login/", views.admin_login, name="admin_login"),
    path("admin-logout/", views.admin_logout, name="admin_logout"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("admin/users/", views.admin_users, name="admin_users"),
    path("admin/users/<int:user_id>/delete/", views.delete_user, name="delete_user"),
    path("admin/issues/", views.admin_issues, name="admin_issues"),
    path("admin/issues/<int:issue_id>/status/", views.update_issue_status, name="update_issue_status"),
    path("admin/issues/<int:issue_id>/delete/", views.delete_issue, name="delete_issue"),
    path("admin/feedback/", views.admin_feedback, name="admin_feedback"),
]