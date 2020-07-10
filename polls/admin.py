from django.contrib import admin
from .models import Question, Choice, Votes, UserProfile

# Register your models here.
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Votes)
admin.site.register(UserProfile)

