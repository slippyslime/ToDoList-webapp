from django import forms
from .models import Task, SubTask

class TaskForm(forms.ModelForm):
    user_id = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Task
        fields = ['title', 'description', 'user_id']

class SubTaskForm(forms.ModelForm):
    class Meta:
        model = SubTask
        fields = ['title']
