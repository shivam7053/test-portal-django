from django.contrib import admin
from .models import Test, Question, Choice, StudentTest, StudentAnswer

# --- Inline Choice for each Question ---
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3  # show 3 extra empty fields by default

# --- Question admin to show Choices inline ---
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('text', 'test')  # shows these fields in list view

# --- Register Test ---
@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at')
    search_fields = ('title', 'description')

# --- Register Choice (optional — since already inline, but okay to keep for direct edit) ---
@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')
    list_filter = ('is_correct',)

# --- Register StudentTest to see student results ---
@admin.register(StudentTest)
class StudentTestAdmin(admin.ModelAdmin):
    list_display = ('student', 'test', 'score', 'taken_at')
    list_filter = ('test', 'student')

# --- Register StudentAnswer (optional, for checking answers) ---
@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ('student_test', 'question', 'selected_choice', 'text_answer')
    list_filter = ('question',)
