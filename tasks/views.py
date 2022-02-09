
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import path
from django.views import View
from tasks.models import Task
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView , UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import TaskCreateForm
from django.db import transaction




def getPendingTasks(user , priority = -1):
    if priority == -1:
        return Task.objects.filter(deleted=False , completed=False , user = user )
    return Task.objects.filter(deleted=False , completed=False , user = user , priority = priority )

def getCompletedTasks(user):
    return Task.objects.filter(deleted=False , completed=True , user = user )


def getAllTasks(user):
    return Task.objects.filter(deleted=False ,  user = user )







def cascadeTasks(user,priority):
    tasksToUpdate = []
    allTasks = Task.objects.select_for_update().filter(deleted=False,completed=False,user=user,priority__gte=priority).order_by('priority','-created_date')
    with transaction.atomic():
        for task in allTasks:
            if task.priority == priority:
                task.priority += 1
                priority += 1
                tasksToUpdate.append(task)
        Task.objects.bulk_update(tasksToUpdate,['priority'])     


def save_task(self , form):
         self.object = form.save()
         self.object.user = self.request.user
         self.object.save()


def isConflictedPriority(priority , user):
    tasks = getPendingTasks(user , priority)
    return tasks.exists()

          


class AuthorizedTasksView(LoginRequiredMixin):
    def get_queryset(self):
        return Task.objects.filter(deleted=False).filter(completed=False , user = self.request.user)


class GenericTaskCreateView(LoginRequiredMixin , CreateView ):
    form_class = TaskCreateForm
    template_name = "task_create.html"
    success_url = "/tasks"    

    def form_valid(self, form):
        priority = form.cleaned_data["priority"]
        user = self.request.user
        if(isConflictedPriority(priority , user)):
            cascadeTasks(user , priority)

        save_task(self , form)    
        return HttpResponseRedirect("/tasks")
  
  

class GenereicPendingTaskView(AuthorizedTasksView ,  ListView):
    queryset = Task.objects.filter(deleted=False)
    template_name = "tasks.html"
    context_object_name = "tasks"
    paginate_by = 3
    
    def get_queryset(self):
        search_item = self.request.GET.get("search")    
        tasks = getPendingTasks(self.request.user)
        if search_item:
          tasks = tasks.filter(title__icontains=search_item)
     
        return tasks

class GenereicAllTaskView(AuthorizedTasksView ,  ListView):
    queryset = Task.objects.filter(deleted=False)
    template_name = "all_tasks.html"
    context_object_name = "tasks"
    paginate_by = 3
    
    def get_queryset(self):
        search_item = self.request.GET.get("search")    
        tasks = getAllTasks(self.request.user)
        if search_item:
          tasks = tasks.filter(title__icontains=search_item)
     
        return tasks

class GenereicCompletedTaskView(AuthorizedTasksView ,  ListView):
    queryset = Task.objects.filter(deleted=False)
    template_name = "completed_tasks.html"
    context_object_name = "tasks"
    paginate_by = 3
    
    def get_queryset(self):
        search_item = self.request.GET.get("search")    
        tasks = getCompletedTasks(self.request.user)
        if search_item:
          tasks = tasks.filter(title__icontains=search_item)
     
        return tasks

class GenericTaskUpdateView(AuthorizedTasksView ,  UpdateView):
    model = Task
    form_class = TaskCreateForm
    template_name = "task_update.html"
    success_url = "/tasks"    


class GenericTaskDetailView(AuthorizedTasksView,DetailView):
    model = Task
    template_name = "task_detail.html"
  


class GenericTaskDeleteView(AuthorizedTasksView , DeleteView):
    model = Task
    template_name = "task_delete.html"
    success_url = "/tasks"

def completeTask(req , pk):
    Task.objects.filter(id=pk).update(completed=True)
    return HttpResponseRedirect("/tasks")

