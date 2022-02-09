from django.urls import path

from .views import (GenereicAllTaskView, GenereicCompletedTaskView,
                    GenereicPendingTaskView, GenericTaskCreateView,
                    GenericTaskDeleteView, GenericTaskDetailView,
                    GenericTaskUpdateView, completeTask)

urlpatterns = [

    path('create/' , GenericTaskCreateView.as_view() ),
    path('delete/<pk>' ,   GenericTaskDeleteView.as_view()),
    path('update/<pk>' , GenericTaskUpdateView.as_view() ),
    path('complete/<pk>' , completeTask),
    path('task/<pk>/' , GenericTaskDetailView.as_view() ),
    path('' , GenereicPendingTaskView.as_view()),
    path('all/' , GenereicAllTaskView.as_view() ),
    path('completed/' , GenereicCompletedTaskView.as_view() ),


]
