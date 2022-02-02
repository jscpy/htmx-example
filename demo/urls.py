from django.urls import path
from demo import views

app_name = 'demo'

urlpatterns = [
    path('', views.home, name='home'),
    path('profiles/', views.ProfileListView.as_view(), name='profiles'),
    path('profiles/list/', views.ProfilesOnLoadView.as_view(), name='profiles-to-load'),
    path('profiles/bulk/', views.profiles_bullk, name='profiles-bulk'),
    path('profiles/bulk/update/<str:status>/', views.profiles_bulk_update, name='profiles-bulk-update'),
    path('profiles/delete/<int:pk>', views.delete_profile, name='profiles-delete'),

    path('profiles/edit/<int:id>', views.edit_profile, name='profile-edit'),
    path('profiles/update/<int:id>', views.update_profile, name='profile-update'),
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
