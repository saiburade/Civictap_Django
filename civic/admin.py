from django.contrib import admin
from .models import CivicUser, Issue, Feedback

@admin.register(CivicUser)
class CivicUserAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "phone", "gender", "address", "created_at")
    search_fields = ("full_name", "phone", "address")

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "phone", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("full_name", "phone", "description", "address")

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "phone", "rating", "created_at")
    search_fields = ("full_name", "phone", "message")
