from django.urls import path
from . import views

urlpatterns = [
    path('', views.test_list, name='test_list'), 
    path('create/', views.create_test, name='create_test'),
    path('question/create/', views.create_question, name='create_question'),
    path('question/create/<int:test_id>/', views.create_question, name='create_question_test'),

    #student
    path('available/', views.available_tests, name='available_tests'),
    path('take/<int:test_id>/', views.take_test, name='take_test'),
    path('result/<int:student_test_id>/', views.test_result, name='test_result'),
    # Student test results
    path('results/', views.test_results, name='test_results'),

]
