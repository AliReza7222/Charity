from django.db import models
from django.db.models import Q
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


class TaskManager(models.Manager):

    def related_tasks_to_charity(self, user):
        query = Task.objects.filter(charity__user=user)
        if query:
            return query
        return None

    def related_tasks_to_benefactor(self, user):
        query = Task.objects.filter(assigned_benefactor__user=user)
        if query:
            return query
        return None

    def all_related_tasks_to_user(self, user):
        query = Task.objects.filter(Q(assigned_benefactor__user=user) | Q(charity__user=user) | Q(state='P'))
        if query:
            return query
        return None


class Task(models.Model):
    STATE_CHOICE = [
        ('P', 'Pending'),
        ('W', 'Waiting'),
        ('A', 'Assigned'),
        ('D', 'Done')
    ]
    assigned_benefactor = models.ForeignKey(Benefactor, on_delete=models.SET_NULL, null=True)
    charity = models.ForeignKey(Charity, on_delete=models.CASCADE)
    title = models.CharField(max_length=60)
    state = models.CharField(max_length=1, choices=STATE_CHOICE, default='P')
    date = models.DateField(auto_now=True)
    description = models.TextField()
    objects = TaskManager()

    def __str__(self):
        return self.title
