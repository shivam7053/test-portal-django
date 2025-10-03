from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import StudentSignUpForm, TeacherSignUpForm

def student_signup(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # log in after signup
            return redirect('home')
    else:
        form = StudentSignUpForm()
    return render(request, 'users/signup.html', {'form': form, 'role': 'Student'})

def teacher_signup(request):
    if request.method == 'POST':
        form = TeacherSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = TeacherSignUpForm()
    return render(request, 'users/signup.html', {'form': form, 'role': 'Teacher'})
