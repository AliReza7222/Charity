from django.db import models
from django.db.models import Q
from accounts.models import User
from .validators import reg_number_validator


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
    reg_number = models.CharField(max_length=10, validators=[reg_number_validator])

    def __str__(self):
        return self.name


class ProfileUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='image-profile/')
    address = models.CharField(max_length=300)
    description = models.TextField()
    phone = models.CharField(max_length=16)

    def delete(self, using=None, keep_parents=False):
        self.image.storage.delete(str(self.image.name))
        super().delete()

    def __str__(self):
        return self.user.username


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

    filtering_lookups = [
        ('title__icontains', 'title',),
        ('charity__name__icontains', 'charity'),
        ('description__icontains', 'description'),
        ('gender_limit__icontains', 'gender'),
    ]

    excluding_lookups = [
        ('age_limit_from__gte', 'age'),  # Exclude greater ages
        ('age_limit_to__lte', 'age'),  # Exclude lower ages
    ]

    @classmethod
    def filter_related_tasks_to_charity_user(cls, user):
        is_charity = user.is_charity
        if not is_charity:
            return []

        return cls.objects.filter(charity=user.charity)

    @classmethod
    def filter_related_tasks_to_benefactor_user(cls, user):
        is_benefactor = user.is_benefactor
        if not is_benefactor:
            return []

        return cls.objects.filter(assigned_benefactor=user.benefactor)

    @classmethod
    def filter_related_tasks_to_user(cls, user):
        charity_tasks = cls.filter_related_tasks_to_charity_user(user)
        benefactor_tasks = cls.filter_related_tasks_to_benefactor_user(user)
        return charity_tasks.union(benefactor_tasks)

    def assign_to_benefactor(self, benefactor):
        self.state = 'W'
        self.assigned_benefactor = benefactor
        self.save()

    def response_to_benefactor_request(self, response):
        if response == 'A':
            self._accept_benefactor()
        else:
            self._reject_benefactor()

    def done(self):
        self.state = 'D'
        self.save()

    def _accept_benefactor(self):
        self.state = 'A'
        self.save()

    def _reject_benefactor(self):
        self.state = 'P'
        self.assigned_benefactor = None
        self.save()
