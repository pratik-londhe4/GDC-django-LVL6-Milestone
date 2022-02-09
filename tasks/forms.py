from .models import Task
from dataclasses import fields
from pyexpat import model
from django.core.exceptions import ValidationError
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import path
from django.views import View
from tasks.models import Task
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView , UpdateView
from django.views.generic.detail import DetailView
from django.forms import ModelForm
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

class TaskCreateForm( LoginRequiredMixin, ModelForm):
    
    def clean_title(self):
        title = self.cleaned_data["title"]
        if(len(title) < 5):
            raise ValidationError("too small")
        return title.upper()

    def clean_priority(self):
        priority = self.cleaned_data["priority"]
        if( int(priority) < 0):
            raise ValidationError("Priority Cannot be Negative")
        return priority
      
    class Meta:
        model = Task
        fields =  ("title" , "description" , "priority")