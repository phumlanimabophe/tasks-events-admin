from django.urls import path
from dash_area import  views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='index'),
    path('calender/', views.CalendarViewNew.as_view(), name='calender'),
    path('management-table/', views.management_table, name='management_table'),
    path('task-form-view/', views.task_form_view, name='task_form_view'),
    path('all-task-list/', views.AllTasksListView.as_view(), name='all_tasks'),
    path('pending-task-list/', views.NewTasksListView.as_view(), name='new_tasks'),
    path('profile/update/', views.profile_update_view, name='profile_update'),
    path('ajax-datatable-tasks/', views.ajax_datatable_tasks, name='ajax_datatable_tasks'),
    path('successful-submit/', views.successful_submit, name='successful_submit'),
    path('delete-event/', views.CalendarViewNew.as_view(), name='delete_event'),
    path('delete-item-manage/', views.delete_item, name='delete_item_manage'),
    path('ongoing-task-list/', views.OngoingTasksListView.as_view(), name='ongoing_tasks'),
    path('completed-task-list/', views.CompletedTasksListView.as_view(), name='completed_tasks'),


  # Authentication
    path('login/', views.user_login_view, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('register-user/', views.register_user, name='register_user'),
    path('accounts/password-change/', views.user_password_change_view, name='password_change'),
    path('accounts/password-change-done/', views.password_change_done, name="password_change_done"),
    path('accounts/password-reset/', views.user_password_reset_view, name='password_reset'),
    path('accounts/password-reset-confirm/<uidb64>/<token>/', views.user_password_reset_confirm_view, name='password_reset_confirm'),
    path('accounts/password-reset-done/', views.password_reset_done, name='password_reset_done'),
    path('accounts/password-reset-complete/', views.password_reset_complete, name='password_reset_complete'),

]
