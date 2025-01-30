from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

class Priority(models.Model):
    PRIORITY_CHOICES = [(i, str(i)) for i in range(1, 11)]

    value = models.IntegerField(choices=PRIORITY_CHOICES, unique=True)

    def __str__(self):
        return str(self.value)


class Status(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('On Hold', 'On Hold'),
        ('Cancelled', 'Cancelled')
    ]

    name = models.CharField(max_length=50, unique=True, choices=STATUS_CHOICES)

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=255)
    due_date = models.DateTimeField(null=True, blank=True)
    description = models.TextField(blank=True)
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, related_name="assigned_tasks", on_delete=models.CASCADE)

    created_by = models.ForeignKey(User, related_name="created_tasks", on_delete=models.SET_NULL, null=True, editable=False)
    updated_by = models.ForeignKey(User, related_name="updated_tasks", on_delete=models.SET_NULL, null=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def save(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        if user:
            if not self.pk:
                self.created_by = user
            self.updated_by = user

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


