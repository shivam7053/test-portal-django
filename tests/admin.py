from django.contrib import admin
from .models import Test, Question, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3  # show 3 extra empty fields by default

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]

admin.site.register(Test)
admin.site.register(Question, QuestionAdmin)
