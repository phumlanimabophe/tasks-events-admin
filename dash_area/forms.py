from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import gettext_lazy as _
from .models import Task, Status, Priority
from django import forms
from .models import Profile
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field, Submit

class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}))
    image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.help_text = None

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-form-label'
        self.helper.field_class = 'col-sm-9'

        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='col-md-6'),
                Column('last_name', css_class='col-md-6')
            ),
            Row(
                Column('email', css_class='col-md-12')
            ),
            Row(
                Column('image', css_class='col-md-12')
            ),
            Row(
                Column(Submit('update', 'Update Profile', css_class='btn btn-primary w-100'), css_class='col-md-12')
            )
        )

class CustomPasswordChangeForm(PasswordChangeForm):
    """
    A custom form for changing passwords with crispy form styling.
    """

    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Old Password'}),
    )
    new_password1 = forms.CharField(
        label=_("New password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'}),
    )
    new_password2 = forms.CharField(
        label=_("Confirm new password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm New Password'}),
    )

    field_order = ["old_password", "new_password1", "new_password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialize crispy form helper
        self.helper = FormHelper(self)
        self.helper.form_class = 'form'
        self.helper.form_method = 'post'

        # Define the layout
        self.helper.layout = Layout(
            Row(
                Column('old_password', css_class='col-md-6'),
                Column('new_password1', css_class='col-md-6')
            ),
            Row(
                Column('new_password2', css_class='col-md-6')
            ),
            Row(
                Column(Submit('change_password', 'Change Password', css_class='btn btn-primary w-100'),
                       css_class='col-md-12')
            )
        )

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Send Password Reset Email', css_class='btn btn-primary shadow px-sm-4'))

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form'
        self.helper.form_method = 'post'
        # Define the layout
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='col-md-6'),
                Column('password', css_class='col-md-6')
            ),
            Row(
                Column(Submit('login', 'Login', css_class='btn btn-success w-100'), css_class='col-md-12')
            )
        )

class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('superuser', 'Superuser'),
        ('standard', 'Standard User')
    ]

    roles = forms.MultipleChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        label="User Roles",
        required=True
    )

    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Suppress default help texts
        for field in self.fields.values():
            field.help_text = None

        # Add custom classes and placeholders
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter username'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm password'})

        # Crispy Forms Helper setup
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-form-label'
        self.helper.field_class = 'col-sm-9'

        # Define the layout
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='col-md-6'),
                Column('first_name', css_class='col-md-6')
            ),
            Row(
                Column('last_name', css_class='col-md-6'),
                Column('password1', css_class='col-md-6')
            ),
            Row(
                Column('password2', css_class='col-md-6'),
                Column(
                    Row(
                        Column(Field('roles', css_class='form-check'), css_class='col-md-12')
                    ),
                )
            ),
            Row(
                Column(Submit('register', 'Create New User', css_class='btn btn-success w-100'), css_class='col-md-12')
            )
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        roles = self.cleaned_data.get('roles', [])

        # Assign roles based on selected options
        if 'superuser' in roles:
            user.is_superuser = True
            user.is_staff = True
        elif 'admin' in roles:
            user.is_staff = True
        else:
            user.is_superuser = False
            user.is_staff = False

        if commit:
            user.save()

        return user

class DefaultUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Suppress default help texts
        for field in self.fields.values():
            field.help_text = None

        # Add custom classes and placeholders
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter username'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm password'})

        # Crispy Forms Helper setup
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-form-label'
        self.helper.field_class = 'col-sm-9'

        # Define the layout
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='col-md-6'),
                Column('password1', css_class='col-md-6')
            ),
            Row(
                Column('password2', css_class='col-md-6'),
            ),
            Row(
                Column(Submit('register', 'Create New User', css_class='btn btn-success w-100'), css_class='col-md-12')
            )
        )

    def save(self, commit=True):
        user = super().save(commit=False)

        # Ensure user is a normal user (non-admin, non-superuser)
        user.is_superuser = False
        user.is_staff = False

        if commit:
            user.save()

        return user

class TasksForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'due_date', 'description', 'priority', 'status', 'assigned_to']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Customize fields
        self.fields['title'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter task title'})

        # Use DateTimeInput for the due_date field
        self.fields['due_date'].widget = forms.DateTimeInput(
            attrs={
                'class': 'form-control',
                'type': 'datetime-local',  # HTML5 input type for date and time
                'placeholder': 'Select due date and time'
            }
        )

        self.fields['description'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Task description', 'rows': 3})

        self.fields['priority'] = forms.ChoiceField(
            choices=[(i, str(i)) for i in range(1, 11)], required=True, widget=forms.Select(attrs={
                'class': 'form-select'}))
        self.fields['status'] = forms.ChoiceField(
            choices=Status.STATUS_CHOICES, required=True, widget=forms.Select(attrs={
                'class': 'form-select'}))

        self.fields['assigned_to'].widget.attrs.update({'class': 'form-select'})

        # Crispy Forms Helper setup
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-form-label'
        self.helper.field_class = 'col-sm-9'

        # Define the layout
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='col-md-6'),
                Column('due_date', css_class='col-md-6')  # Updated for DateTimeInput
            ),
            Row(
                Column('description', css_class='col-md-6'),
                Column('assigned_to', css_class='col-md-6')
            ),
            Row(
                Column('priority', css_class='col-md-6'),
                Column('status', css_class='col-md-6')
            ),
            Submit('save', 'Save Task', css_class='btn btn-success w-100')
        )

    def clean(self):
        cleaned_data = super().clean()

        # Process status
        status_value = cleaned_data.get('status')
        status_obj, created = Status.objects.get_or_create(name=status_value)
        cleaned_data['status'] = status_obj

        # Process priority
        priority_value = cleaned_data.get('priority')
        priority_obj, created = Priority.objects.get_or_create(value=int(priority_value))
        cleaned_data['priority'] = priority_obj

        return cleaned_data

class TasksCalenderForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'due_date', 'description', 'priority', 'status', 'assigned_to']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Customize fields
        self.fields['title'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter task title'})

        # Use DateTimeInput for the due_date field
        self.fields['due_date'].widget = forms.DateTimeInput(
            attrs={
                'id': 'id_end_time',
                'class': 'form-control',
                'type': 'datetime-local',
                'placeholder': 'Select due date and time'
                }
        )

        self.fields['description'].widget.attrs.update(
            {'id': 'description_field', 'name':'description_field','class': 'form-control', 'placeholder': 'Task description', 'rows': 3})

        self.fields['priority'] = forms.ChoiceField(
            choices=[(i, str(i)) for i in range(1, 11)], required=True, widget=forms.Select(attrs={
                'class': 'form-select'}))
        self.fields['status'] = forms.ChoiceField(
            choices=Status.STATUS_CHOICES, required=True, widget=forms.Select(attrs={
                'class': 'form-select'}))

        self.fields['assigned_to'].widget.attrs.update({'class': 'form-select'})

        # Crispy Forms Helper setup
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-form-label'
        self.helper.field_class = 'col-sm-9'

        # Define the layout
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='col-md-6'),
                Column('due_date', css_class='col-md-6')  # Updated for DateTimeInput
            ),
            Row(
                Column('description', css_class='col-md-6'),
                Column('assigned_to', css_class='col-md-6')
            ),
            Row(
                Column('priority', css_class='col-md-6'),
                Column('status', css_class='col-md-6')
            ),
            Submit('save', 'Save Task', css_class='btn btn-success w-100')
        )

    def clean(self):
        cleaned_data = super().clean()

        # Process status
        status_value = cleaned_data.get('status')
        status_obj, created = Status.objects.get_or_create(name=status_value)
        cleaned_data['status'] = status_obj

        # Process priority
        priority_value = cleaned_data.get('priority')
        priority_obj, created = Priority.objects.get_or_create(value=int(priority_value))
        cleaned_data['priority'] = priority_obj

        return cleaned_data

class TasksEditCalenderForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput(attrs={'id': 'edit_id'}), required=False)

    class Meta:
        model = Task
        fields = ['title', 'due_date', 'description', 'priority', 'status', 'assigned_to']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter task title',
            'id': 'edit_title'
        })

        self.fields['due_date'].widget = forms.DateTimeInput(
            attrs={
                'id': 'edit_due_date',
                'class': 'form-control',
                'type': 'datetime-local',
                'placeholder': 'Select due date and time'
            }
        )

        self.fields['description'].widget.attrs.update({
            'id': 'edit_description',
            'name': 'description_field',
            'class': 'form-control',
            'placeholder': 'Task description',
            'rows': 3
        })

        self.fields['priority'] = forms.ChoiceField(
            choices=[(i.id, str(i)) for i in Priority.objects.all()],
            required=True,
            widget=forms.Select(attrs={
                'class': 'form-select',
                'id': 'edit_priority'
            })
        )

        self.fields['status'] = forms.ChoiceField(
            choices=[(status.id, status.name) for status in Status.objects.all()],
            required=True,
            widget=forms.Select(attrs={
                'class': 'form-select',
                'id': 'edit_status'
            })
        )

        self.fields['assigned_to'].widget.attrs.update({
            'class': 'form-select',
            'id': 'edit_assigned_to'
        })

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-form-label'
        self.helper.field_class = 'col-sm-9'

        self.helper.layout = Layout(
            Row(
                Column('id', css_class='d-none'),  # Hidden field
                Column('title', css_class='col-md-6'),
                Column('due_date', css_class='col-md-6')
            ),
            Row(
                Column('description', css_class='col-md-6'),
                Column('assigned_to', css_class='col-md-6')
            ),
            Row(
                Column('priority', css_class='col-md-6'),
                Column('status', css_class='col-md-6')
            ),
            Submit('save', 'Save Task', css_class='btn btn-success w-100')
        )

    def clean(self):
        cleaned_data = super().clean()

        # Convert priority and status values to objects
        status_value = cleaned_data.get('status')
        if status_value:
            status_obj = Status.objects.get(id=status_value)
            cleaned_data['status'] = status_obj

        priority_value = cleaned_data.get('priority')
        if priority_value:
            priority_obj = Priority.objects.get(id=priority_value)
            cleaned_data['priority'] = priority_obj

        return cleaned_data
