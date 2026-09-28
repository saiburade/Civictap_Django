from django.db import models

class CivicUser(models.Model):
    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    ]

    full_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=15, unique=True)
    address = models.CharField(max_length=255, blank=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} ({self.phone})"


class Issue(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Resolved", "Resolved"),
    ]

    user = models.ForeignKey(CivicUser, on_delete=models.CASCADE, related_name="issues")
    full_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=CivicUser.GENDER_CHOICES)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to="issues/", blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"#{self.pk} - {self.description[:45]}"


class Feedback(models.Model):
    user = models.ForeignKey(CivicUser, on_delete=models.CASCADE, related_name="feedback")
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    message = models.TextField()
    rating = models.PositiveSmallIntegerField()
    gender = models.CharField(max_length=10, choices=CivicUser.GENDER_CHOICES, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} - {self.rating}/5"
