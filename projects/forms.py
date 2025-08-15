from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field
from .models import Project, Task, MVPRequirement


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'status', 'due_date']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('name', css_class='w-full'),
            Field('description', css_class='w-full'),
            Row(
                Column('status', css_class='form-group col-md-6 mb-0'),
                Column('due_date', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Save Project', css_class='bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded')
        )


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('title', css_class='w-full'),
            Field('description', css_class='w-full'),
            Field('priority', css_class='w-full'),
            Submit('submit', 'Add Task', css_class='bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded')
        )


class MVPRequirementForm(forms.ModelForm):
    class Meta:
        model = MVPRequirement
        fields = ['description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('description', css_class='w-full'),
            Submit('submit', 'Add MVP Requirement', css_class='bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded')
        )
