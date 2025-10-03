from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import TestForm, QuestionForm, ChoiceFormSet
from .models import Test, Question, Choice, UserTest
from django.forms import modelformset_factory
from .models import StudentTest, StudentAnswer


@login_required
def create_test(request):
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            test.created_by = request.user
            test.save()
            return redirect('test_list')  # you'll need to define this view
    else:
        form = TestForm()
    return render(request, 'tests/create_test.html', {'form': form})


@login_required
def create_question(request, test_id=None):
    if test_id:
        test = get_object_or_404(Test, id=test_id, created_by=request.user)
    else:
        test = None

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            if test:
                question.test = test
            question.save()

            if question.question_type == 'mcq':
                formset = ChoiceFormSet(request.POST, instance=question)
                if formset.is_valid():
                    formset.save()
            return redirect('test_list')
    else:
        form = QuestionForm(initial={'test': test})
        formset = ChoiceFormSet()

    return render(request, 'tests/create_question.html', {'form': form, 'formset': formset})


@login_required
def test_list(request):
    tests = Test.objects.filter(created_by=request.user)  # show only teacher's tests
    return render(request, 'tests/test_list.html', {'tests': tests})


@login_required
def available_tests(request):
    # students see all available tests
    tests = Test.objects.all()
    return render(request, 'tests/available_tests.html', {'tests': tests})


@login_required
def take_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)

    # Create StudentTest record
    student_test, created = StudentTest.objects.get_or_create(
        student=request.user, test=test
    )

    if request.method == 'POST':
        for question in test.questions.all():
            answer_key = f"question_{question.id}"
            if question.question_type == 'mcq':
                selected_choice_id = request.POST.get(answer_key)
                if selected_choice_id:
                    choice = Choice.objects.get(id=selected_choice_id)
                    StudentAnswer.objects.create(
                        student_test=student_test,
                        question=question,
                        selected_choice=choice
                    )
            else:  # short answer
                text_ans = request.POST.get(answer_key)
                StudentAnswer.objects.create(
                    student_test=student_test,
                    question=question,
                    text_answer=text_ans
                )
        return redirect('test_result', student_test.id)

    return render(request, 'tests/take_test.html', {'test': test})


@login_required
def test_result(request, student_test_id):
    student_test = get_object_or_404(StudentTest, id=student_test_id, student=request.user)

    # Basic scoring for MCQs
    score = 0
    total = student_test.test.questions.filter(question_type='mcq').count()

    for answer in student_test.answers.all():
        if answer.selected_choice and answer.selected_choice.is_correct:
            score += 1

    student_test.score = (score / total * 100) if total > 0 else 0
    student_test.save()

    return render(request, 'tests/test_result.html', {'student_test': student_test})
