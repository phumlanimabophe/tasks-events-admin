
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm, SetPasswordForm, \
    PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.csrf import csrf_protect

from dash_area.forms import TasksCalenderForm, TasksForm, CustomUserCreationForm, DefaultUserCreationForm, \
    CustomAuthenticationForm, \
    CustomPasswordResetForm, CustomPasswordChangeForm, ProfileUpdateForm

from dash_area.utils import JsonResponse
from django.views.generic import ListView
from .models import  Priority

from django.core.serializers import serialize
from django.http import JsonResponse

from datetime import  timedelta
from django.shortcuts import redirect
from django.views import generic
from .forms import TasksCalenderForm, TasksEditCalenderForm
import json
from django.shortcuts import render
from django.db.models import Count
from datetime import datetime
from django.conf import settings
from .models import Task, Profile, Status, User
from django.contrib.auth import get_user_model
from datetime import datetime


def user_login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = DefaultUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = DefaultUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})

@login_required
def register_user(request):
    context = {'form': CustomUserCreationForm()}
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            context = {
                'form': CustomUserCreationForm(),
                'submitted': True,
                'message': 'Created Successfully!',
                'user_name': user.username
            }
        else:
            context = {
                'form': form,
                'submitted': True,
                'message': 'Creation Failed!',
                'error': "Error creating user"
            }
    return render(request, 'accounts/register_user.html', context)

@csrf_protect
def delete_item(request):
    if request.method == 'POST':
        item_id = request.POST.get('id')
        Task.objects.filter(id=item_id).delete()
        return redirect('management_table')

@login_required
def user_password_change_view(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('password_change_done')  # Replace with your success URL
    else:
        form = CustomPasswordChangeForm(request.user)

    return render(request, 'accounts/password_change.html', {'form': form})

# for a specific url in case of unauthenticated access
@login_required(login_url='login')
def password_change_done(request):
    return render(request, 'accounts/password_change_done.html')

def user_password_reset_view(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                use_https=request.is_secure(),
                email_template_name='accounts/password_reset_complete.html',
            )
            return redirect('password_reset_done')
    else:
        form = CustomPasswordResetForm()

    return render(request, 'accounts/password_reset.html', {'form': form})

def user_password_reset_confirm_view(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect('password_reset_complete')
        else:
            form = SetPasswordForm(user)
    else:
        return redirect('password_reset_invalid')

    return render(request, 'accounts/password_reset_confirm.html', {'form': form})

def password_reset_done(request):
    return render(request, 'accounts/password_reset_done.html')

def password_reset_complete(request):
    return render(request, 'accounts/password_reset_complete.html')

def index(request):
    context = {}
    if request.user.is_authenticated:
        tasks = Task.objects.select_related('priority')
        priority_counts = {i: 0 for i in range(1, 11)}
        for task in tasks:
            priority_counts[task.priority.value] += 1

        total_tasks = sum(priority_counts.values())
        priority_percentages = {
            i: (priority_counts[i] / total_tasks) * 100 if total_tasks > 0 else 0 for i in range(1, 11)
        }
        priorities = [
            {'priority_value': i, 'count': priority_counts[i], 'percentage': priority_percentages[i]}
            for i in range(1, 11)
        ]

        # Task status and assignment data
        task_status_counts = Task.objects.values('status').annotate(count=Count('status'))
        task_assigned_to_counts = Task.objects.values('assigned_to').annotate(count=Count('assigned_to'))
        overdue_tasks = Task.objects.filter(due_date__lt=datetime.now(), status__name="Pending")
        status_distribution = {status.name: 0 for status in Status.objects.all()}
        for task in tasks:
            status_distribution[task.status.name] += 1

        total_status_tasks = sum(status_distribution.values())
        status_percentages = {
            status: (count / total_status_tasks) * 100 if total_status_tasks > 0 else 0
            for status, count in status_distribution.items()
        }

        total_assigned_tasks = sum(assigned['count'] for assigned in task_assigned_to_counts)
        for assigned in task_assigned_to_counts:
            assigned['percentage'] = (assigned['count'] / total_assigned_tasks) * 100 if total_assigned_tasks > 0 else 0

        users = get_user_model().objects.all().prefetch_related('profile')
        for user in users:
            user.is_admin = user.is_staff
            user.is_user = not user.is_superuser and not user.is_staff

        # Fetch current user's profile image if available
        users_profile = Profile.objects.filter(user=request.user).first()
        if users_profile and users_profile.image:
            users_profile.image = settings.MEDIA_URL + str(users_profile.image)

        # Prepare context data
        context = {
            'segment': 'dashboard',
            'priorities': priorities,
            'status_distribution': status_distribution,
            'status_percentages': status_percentages,
            'overdue_tasks_count': overdue_tasks.count(),
            'assigned_tasks': task_assigned_to_counts,
            'task_status_counts': task_status_counts,
            'total_tasks': total_tasks,
            'users': users
        }
    return render(request, "pages/index.html", context)


class CalendarViewNew(LoginRequiredMixin, generic.View):
    login_url = "login"
    template_name = "pages/calender.html"
    form_class = TasksCalenderForm
    filter_by_name = 'created_by'
    def process_task_data(self, filter_by=None):
        user = self.request.user  # ✅ Corrected: Use self.request.user

        if filter_by == 'all' and user.is_superuser and user.is_staff:
            self.filter_by_name = 'all'
            tasks = Task.objects.all()
        elif filter_by == 'assigned_to':
            self.filter_by_name = 'assigned_to'
            tasks = Task.objects.filter(assigned_to=user)
        else:
            self.filter_by_name = 'created_by'
            tasks = Task.objects.filter(created_by=user)

        serialized_tasks = serialize('json', tasks)
        tasks_data = json.loads(serialized_tasks)

        events_month = []
        task_list = []

        for task in tasks_data:
            task_fields = task['fields']
            
            if task_fields['due_date']:
                calender_date = task_fields['due_date']
            else:
                calender_date = task_fields['created_at']

            end_time = (
                calender_date + timedelta(hours=1)
                if isinstance(calender_date, datetime) else calender_date
            )
            end = (
                end_time.strftime("%Y-%m-%dT%H:%M:%S")
                if isinstance(end_time, datetime) else end_time
            )

            start = (
                calender_date.strftime("%Y-%m-%dT%H:%M:%S")
                if isinstance(calender_date, datetime) else calender_date
            )

            if task_fields['status'] == 1:
                events_month.append({
                    "id": task['pk'],
                    "title": task_fields['title'],
                    "start": start,
                    "end": end,
                    "description": task_fields['description'],
                    'priority': task_fields['priority'],
                    'status': task_fields['status'],
                    'assigned_to': task_fields['assigned_to'],

                })

            task_list.append({
                "id": task['pk'],
                "title": task_fields['title'],
                "start": start,
                "end": end,
                "description": task_fields['description'],
                'priority': task_fields['priority'],
                'status': task_fields['status'],
                'assigned_to': task_fields['assigned_to'],

            })

        return task_list, events_month

    def get(self, request, *args, **kwargs):
        task_list, events_month = self.process_task_data()
        filter_by_name = self.filter_by_name
        context = {
            "calender_task_form": self.form_class(),
            "calender_tasks": task_list,
            "events_month": events_month,
            'form_edit': TasksEditCalenderForm(),
            'filter_by_name':filter_by_name
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        filter_by = request.POST.get('filterType')

        if filter_by:
            task_list, events_month = self.process_task_data(filter_by)
            context = {
                "calender_task_form": self.form_class(),
                "calender_tasks": task_list,
                "events_month": events_month,
                'form_edit': TasksEditCalenderForm(),
                'filter_by_name':self.filter_by_name
            }
            return render(request, self.template_name, context)

        event_id = request.POST.get('event_id')

        if event_id:
            Task.objects.filter(id=event_id).delete()
            return redirect("calender")

        edit_id = request.POST.get('id')

        if edit_id:
            task_instance = Task.objects.filter(id=edit_id).first()
            if task_instance:
                edit_form = TasksEditCalenderForm(request.POST, instance=task_instance)
                if edit_form.is_valid():
                    task_instance = edit_form.save(commit=False)

                    task_instance.save(user=request.user)
                    return redirect("calender")
            else:
                return redirect("calender")

        forms = self.form_class(request.POST)
        if forms.is_valid():
            form = forms.save(commit=False)
            form.user = request.user
            form.save(user=request.user)
            return redirect("calender")

        task_list, events_month = self.process_task_data()
        context = {
            "calender_task_form": forms,
            "calender_tasks": task_list,
            "events_month": events_month,
            "form_edit": TasksEditCalenderForm(),
            'filter_by_name': self.filter_by_name
        }
        return render(request, self.template_name, context)

class AllTasksListView(LoginRequiredMixin, ListView):
    login_url = "login"
    template_name = "pages/task-table.html"
    model = Task

    def get_queryset(self):
        return Task.objects.filter(created_by=self.request.user)

class NewTasksListView(ListView):
    login_url = "login"
    template_name = "pages/task-table.html"
    model = Task

    def get_queryset(self):
        return Task.objects.filter(status__name="New",created_by=self.request.user)

class OngoingTasksListView(ListView):
    login_url = "login"
    template_name = "pages/task-table.html"
    model = Task

    def get_queryset(self):
        return Task.objects.filter(status__name="In Progress",created_by=self.request.user)

class CompletedTasksListView(ListView):
    login_url = "login"
    template_name = "pages/task-table.html"
    model = Task

    def get_queryset(self):
        return Task.objects.filter(status__name="Completed",created_by=self.request.user)


@login_required
def management_table(request):
    context = {
        'form_edit': TasksEditCalenderForm()
    }

    edit_id = request.POST.get('id')
    if request.method == 'POST':
        if edit_id:
            task_instance = Task.objects.filter(id=edit_id).first()
            if task_instance:
                edit_form = TasksEditCalenderForm(request.POST, instance=task_instance)
                if edit_form.is_valid():
                    task_instance = edit_form.save(commit=False)

                    task_instance.save(user=request.user)

                    return redirect("management_table")
            else:
                return redirect("management_table")

    return render(request, 'pages/management-table.html', context=context)


@login_required
def ajax_datatable_tasks(request):
    tasks = Task.objects.all()
    serialized_tasks = serialize('json', tasks)
    tasks_data = json.loads(serialized_tasks)

    transformed_tasks = []
    for task in tasks_data:
        task_fields = task['fields']

        priority_value = task_fields['priority']
        status_name = task_fields['status']
        assigned_to_user = task_fields['assigned_to']

        priority = Priority.objects.get(id=priority_value).value
        status = Status.objects.get(id=status_name).name
        assigned_to = User.objects.get(id=assigned_to_user).username

        transformed_tasks.append({
            'id': task['pk'],
            'title': task_fields['title'],
            'due_date': task_fields['due_date'],
            'description': task_fields['description'],
            'priority': priority,
            'status': status,
            'assigned_to': assigned_to,
            'created_at': task_fields['created_at'],
            'updated_at': task_fields['updated_at'],
            'priority_value': task_fields['priority'],
            'status_name': task_fields['priority'],
            'assigned_to_username': task_fields['priority']
        })

    draw = int(request.GET.get("draw", 1))
    start = int(request.GET.get("start", 0))
    length = int(request.GET.get("length", len(transformed_tasks)))

    paginated_tasks = transformed_tasks[start:start + length]

    response = {
        "draw": draw,
        "recordsTotal": len(transformed_tasks),
        "recordsFiltered": len(transformed_tasks),
        "data": paginated_tasks
    }

    return JsonResponse(response)

@login_required
def task_form_view(request):
    if request.method == 'POST':
        form = TasksForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.save(user=request.user)
            return redirect('successful_submit')
        else:
            return render(request, 'pages/task_form_view.html', {'form': form})
    else:
        form = TasksForm()
        return render(request, 'pages/task_form_view.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/index')
    return render(request, 'accounts/logout.html',)

def successful_submit(request):
    return render(request, 'pages/success.html',)


@login_required
def profile_update_view(request):
    if not hasattr(request.user, 'profile'):
        Profile.objects.create(user=request.user)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if request.FILES:
            print(request.FILES)
        if form.is_valid():
            try:
                profile = form.save(commit=False)
                profile.save()  # Save the profile


                if profile.image:
                    print(f"Image saved at: {profile.image.url}")
                else:
                    print("No image uploaded.")
                return redirect('profile_update')
            except Exception as e:
                print(f"Error saving profile: {e}")
                return redirect('profile_update')
        else:
            print("Form is not valid.")
    else:
        form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'accounts/profile_update.html', {'form': form})