from django.contrib import admin
from .models import Benefactor, Charity, Task


admin.site.register(Benefactor)
admin.site.register(Charity)
admin.site.register(Task)