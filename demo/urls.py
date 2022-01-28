from django.urls import path
from demo import views

app_name = 'demo'

urlpatterns = [
    path('', views.home, name='home'),
    path('profiles/', views.ProfileListView.as_view(), name='profiles'),
    path('workers/', views.WorkerListView.as_view(), name='workers'),

    # HTMX
    path('check_username/', views.check_names, name='check_names'),
    path('todo/create', views.create_todo, name='todo-create'),
    path('todo/edit/<int:pk>', views.edit_todo, name='todo-edit'),
    path('todo/update/<int:pk>', views.update_todo, name='todo-update'),
    path('todo/delete/<int:pk>', views.delete_todo, name='todo-delete'),
    path('search/', views.search_profile, name='search'),
    path('dropdown/', views.dropdown_modules, name='dropdown'),
]
