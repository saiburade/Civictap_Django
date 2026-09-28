from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("civic", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="civicuser",
            name="password",
            field=models.CharField(default="!", max_length=128),
            preserve_default=False,
        ),
    ]
