from django.db import models
from accounts.models import User


class Benefactor(models.Model):
    EXPERIENCE_CHOICE = [
        (0, 'junior'),
        (1, 'middle'),
        (2, 'senior')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    experience = models.SmallIntegerField(choices=EXPERIENCE_CHOICE, default=0)
    free_time_per_week = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.user.username


class Charity(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    reg_number = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Task(models.Model):
    STATE_CHOICE = [
        ('P', 'Pending'),
        ('W', 'Waiting'),
        ('A', 'Assigned'),
        ('D', 'Done')
    ]
    assigned_benefactor = models.ForeignKey(Benefactor, on_delete=models.SET_NULL, null=True)
    charity = models.ForeignKey(Charity, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=60)
    state = models.CharField(max_length=1, choices=STATE_CHOICE, default='P')
    date = models.DateField(auto_now=True)
    description = models.TextField()

    def __str__(self):
        return self.title
