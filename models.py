from django.db import models
from django.contrib.auth.models import User
from PIL import Image



# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()

    def __str__(self):
        return self.user.username

    # resizing images
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)





# models.py
from django.db import models

class SystemMonitor(models.Model):
    cpu_usage = models.FloatField()
    cpu_load_1min = models.FloatField()
    memory_usage = models.FloatField()
    disk_usage = models.FloatField()
    disk_io = models.FloatField()
    network_latency = models.FloatField()
    packet_loss = models.FloatField()
    bandwidth_usage = models.FloatField()
    response_time = models.FloatField()
    error_log_count = models.FloatField()
    warning_log_count = models.FloatField()
    process_count = models.FloatField()
    system_temperature = models.FloatField()
    auth_failure_count = models.FloatField()
    service_restart_count = models.FloatField()
    failure_type = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)




# models.py
from django.db import models
from django.contrib.auth.models import User

class Ticket(models.Model):
    system_monitor = models.ForeignKey(
        'SystemMonitor',
        on_delete=models.CASCADE
    )

    # ✅ FIXED
    raised_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    # ===== SYSTEM INPUT SNAPSHOT =====
    cpu_usage = models.FloatField()
    cpu_load_1min = models.FloatField()
    memory_usage = models.FloatField()
    disk_usage = models.FloatField()
    disk_io = models.FloatField()
    network_latency = models.FloatField()
    packet_loss = models.FloatField()
    bandwidth_usage = models.FloatField()
    response_time = models.FloatField()
    error_log_count = models.IntegerField()
    warning_log_count = models.IntegerField()
    process_count = models.IntegerField()
    system_temperature = models.FloatField()
    auth_failure_count = models.IntegerField()
    service_restart_count = models.IntegerField()

    failure_type = models.CharField(max_length=50)

    ai_analysis = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.raised_by.username} - {self.failure_type}"












class AdminUser(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username






















from django.db import models

class SeniorDeveloper(models.Model):
    name = models.CharField(max_length=100)
    experience_years = models.IntegerField()
    expertise = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
class DeveloperDocument(models.Model):
    developer = models.ForeignKey(
        SeniorDeveloper,
        on_delete=models.CASCADE,
        related_name='documents'
    )
    title = models.CharField(max_length=200)
    document = models.FileField(upload_to='senior_docs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
class DocumentQuestion(models.Model):
    document = models.ForeignKey(
        DeveloperDocument,
        on_delete=models.CASCADE
    )
    question = models.TextField()
    answer = models.TextField(blank=True, null=True)
    asked_at = models.DateTimeField(auto_now_add=True)
