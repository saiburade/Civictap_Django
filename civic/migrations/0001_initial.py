from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="CivicUser",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("full_name", models.CharField(max_length=100)),
                ("gender", models.CharField(choices=[("Male","Male"),("Female","Female"),("Other","Other")], max_length=10)),
                ("phone", models.CharField(max_length=15, unique=True)),
                ("address", models.CharField(blank=True, max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="Feedback",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("full_name", models.CharField(max_length=100)),
                ("phone", models.CharField(max_length=15)),
                ("message", models.TextField()),
                ("rating", models.PositiveSmallIntegerField()),
                ("gender", models.CharField(blank=True, max_length=10, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="feedback", to="civic.civicuser")),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="Issue",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("full_name", models.CharField(max_length=100)),
                ("gender", models.CharField(max_length=10)),
                ("phone", models.CharField(max_length=15)),
                ("address", models.CharField(blank=True, max_length=255)),
                ("description", models.TextField()),
                ("image", models.ImageField(blank=True, null=True, upload_to="issues/")),
                ("status", models.CharField(choices=[("Pending","Pending"),("In Progress","In Progress"),("Resolved","Resolved")], default="Pending", max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="issues", to="civic.civicuser")),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
