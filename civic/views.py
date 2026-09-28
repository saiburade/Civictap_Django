from functools import wraps

from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.hashers import check_password
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import FeedbackForm, IssueForm, ProfileForm, SignupForm
from .models import CivicUser, Feedback, Issue


def citizen_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get("civic_user_id"):
            return redirect("login")
        return view_func(request, *args, **kwargs)
    return wrapper


def current_citizen(request):
    user_id = request.session.get("civic_user_id")
    return CivicUser.objects.filter(pk=user_id).first()


def home(request):
    """Landing page: let the visitor choose Admin or User login."""
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("admin_dashboard")
    if request.session.get("civic_user_id"):
        return redirect("front")
    return render(request, "home.html")


def signup(request):
    if request.session.get("civic_user_id"):
        return redirect("front")
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data["phone"]
            if CivicUser.objects.filter(phone=phone).exists():
                messages.error(request, "A user with this phone number already exists.")
            else:
                user = form.save()
                request.session["civic_user_id"] = user.pk
                messages.success(request, "Account created successfully. Welcome to CivicTap!")
                return redirect("front")
    else:
        form = SignupForm()
    return render(request, "signup.html", {"form": form})


def user_login(request):
    """User entry page: choose existing account or create a new one."""
    if request.session.get("civic_user_id"):
        return redirect("front")
    return render(request, "user_login.html")


def login_view(request):
    if request.session.get("civic_user_id"):
        return redirect("front")
    if request.method == "POST":
        phone = request.POST.get("phone", "").strip()
        password = request.POST.get("password", "")
        citizen = CivicUser.objects.filter(phone=phone).first()
        if citizen and check_password(password, citizen.password):
            request.session["civic_user_id"] = citizen.pk
            messages.success(request, f"Welcome back, {citizen.full_name}!")
            return redirect("front")
        messages.error(request, "Invalid phone number or password.")
    return render(request, "login.html")


def logout_view(request):
    request.session.pop("civic_user_id", None)
    return redirect("home")


@citizen_required
def front(request):
    citizen = current_citizen(request)
    issues = Issue.objects.select_related("user").all()
    return render(request, "front.html", {"citizen": citizen, "issues": issues})


@citizen_required
def issue(request):
    citizen = current_citizen(request)
    if request.method == "POST":
        form = IssueForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = citizen
            obj.full_name = citizen.full_name
            obj.gender = citizen.gender
            obj.phone = citizen.phone
            obj.save()
            messages.success(request, "Your civic issue has been reported.")
            return redirect("front")
    else:
        form = IssueForm(initial={"address": citizen.address})
    return render(request, "issue.html", {"form": form, "citizen": citizen})


@citizen_required
def profile(request):
    citizen = current_citizen(request)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=citizen)
        if form.is_valid():
            old_phone = citizen.phone
            form.save()
            request.session["civic_user_id"] = citizen.pk
            messages.success(request, "Profile updated successfully.")
            return redirect("profile")
    else:
        form = ProfileForm(instance=citizen)
    return render(request, "profile.html", {"form": form, "citizen": citizen})


@citizen_required
def feedback(request):
    citizen = current_citizen(request)
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = citizen
            obj.full_name = citizen.full_name
            obj.phone = citizen.phone
            obj.gender = citizen.gender
            obj.save()
            messages.success(request, "Thank you for your feedback!")
            return redirect("feedback")
    else:
        form = FeedbackForm()
    return render(request, "feedback.html", {"form": form, "citizen": citizen})


@citizen_required
def my_city(request):
    citizen = current_citizen(request)
    return render(request, "my_city.html", {"citizen": citizen})


@citizen_required
def help_page(request):
    return render(request, "help.html")


@citizen_required
def privacy(request):
    return render(request, "privacy.html")


@citizen_required
def about(request):
    return render(request, "about.html")


def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("admin_dashboard")
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            auth_login(request, user)
            return redirect("admin_dashboard")
        messages.error(request, "Invalid admin credentials.")
    return render(request, "admin_login.html")


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return redirect("admin_login")
        return view_func(request, *args, **kwargs)
    return wrapper


@admin_required
def admin_logout(request):
    auth_logout(request)
    return redirect("admin_login")


@admin_required
def admin_dashboard(request):
    context = {
        "users_count": CivicUser.objects.count(),
        "issues_count": Issue.objects.count(),
        "pending_count": Issue.objects.filter(status="Pending").count(),
        "resolved_count": Issue.objects.filter(status="Resolved").count(),
        "feedback_count": Feedback.objects.count(),
    }
    return render(request, "admin_dashboard.html", context)


@admin_required
def admin_users(request):
    query = request.GET.get("search", "").strip()
    users = CivicUser.objects.all()
    if query:
        users = users.filter(Q(full_name__icontains=query) | Q(phone__icontains=query) | Q(address__icontains=query))
    return render(request, "admin_users.html", {"users": users, "query": query})


@admin_required
def delete_user(request, user_id):
    if request.method == "POST":
        user = get_object_or_404(CivicUser, pk=user_id)
        user.delete()
        messages.success(request, "User deleted.")
    return redirect("admin_users")


@admin_required
def admin_issues(request):
    query = request.GET.get("search", "").strip()
    issues = Issue.objects.select_related("user").all()
    if query:
        issues = issues.filter(
            Q(full_name__icontains=query)
            | Q(phone__icontains=query)
            | Q(description__icontains=query)
            | Q(address__icontains=query)
        )
    return render(request, "admin_issues.html", {"issues": issues, "query": query})


@admin_required
def update_issue_status(request, issue_id):
    if request.method == "POST":
        issue_obj = get_object_or_404(Issue, pk=issue_id)
        status = request.POST.get("status")
        if status in dict(Issue.STATUS_CHOICES):
            issue_obj.status = status
            issue_obj.save(update_fields=["status"])
            messages.success(request, f"Issue #{issue_obj.pk} updated.")
    return redirect("admin_issues")


@admin_required
def delete_issue(request, issue_id):
    if request.method == "POST":
        issue_obj = get_object_or_404(Issue, pk=issue_id)
        issue_obj.delete()
        messages.success(request, "Issue deleted.")
    return redirect("admin_issues")


@admin_required
def admin_feedback(request):
    query = request.GET.get("search", "").strip()
    feedback_items = Feedback.objects.select_related("user").all()
    if query:
        feedback_items = feedback_items.filter(
            Q(full_name__icontains=query) | Q(phone__icontains=query) | Q(message__icontains=query)
        )
    return render(request, "admin_feedback.html", {"feedback_items": feedback_items, "query": query})
