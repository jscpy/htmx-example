from random import randint
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, View
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import render

from demo.models import Todo, Profile, Course, Module
from demo.forms import TodoForm, ProfileForm

def home(request):
    data_random = {
        'tweets': randint(1, 1000),
        'following': randint(1, 1000),
        'followers': randint(1, 1000),
        'likes': randint(1, 1000),
    }
    context = {
        'todos': Todo.objects.all(),
        'profiles': Profile.objects.all()[:5],
        'courses': Course.objects.all(),
        'data_random': data_random
    }
    
    return render(
        template_name='index.html', request=request, context=context
    )

@require_http_methods(['POST'])
def check_names(request):
    import time
    names = ['abril', 'juan', 'victor', 'manuel', 'jesus']
    name = request.POST.get('name')
    if name != '' and len(name) >= 4:
        if name.lower() in names:
            message = '<p class="help is-danger">¡Este nombre ya existe!, intenta con otro</p>'
        else:
            message = '<p class="help is-success">Este nombre esta disponible</p>'
    else:
        message = '<p class="help is-info">Escribe un nombre valido</p>'
    time.sleep(1)
    return HttpResponse(message)
    
@require_http_methods(['POST'])
def create_todo(request):
    context = {}
    template_name='partials/todo-list.html'
    form = TodoForm(request.POST)
    if form.is_valid():
        form.save()
        context['todos'] = Todo.objects.all()
    else:
        context['todos'] = Todo.objects.all()
        context['form'] = form
    return render(request, template_name, context)

@require_http_methods(['GET'])
def edit_todo(request, pk):
    context = {}
    template_name = 'partials/todo-edit.html'
    todo = Todo.objects.get(pk=pk)
    context['form'] = TodoForm(instance=todo)
    context['todo_id'] = todo.id
    return render(request, template_name, context)

@require_http_methods(['POST', 'PUT'])
def update_todo(request, pk):
    context = {}
    template_name = 'partials/todo-list.html'
    todo = Todo.objects.get(pk=pk)
    form = TodoForm(request.POST, instance=todo)
    if form.is_valid():
        form.save()
        context['todos'] = Todo.objects.all()
    return render(request, template_name, context)

@require_http_methods(['DELETE'])
def delete_todo(request, pk):
    context = {}
    template_name='partials/todo-list.html'
    todo = Todo.objects.get(pk=pk)
    todo.delete()
    context['todos'] = Todo.objects.all()
    return render(request, template_name, context)

@require_http_methods(['POST'])
def search_profile(request):
    q = request.POST.get('q')
    results = Profile.objects.filter(
        Q(first_name__icontains=q) | Q(last_name__icontains=q) | \
            Q(company__icontains=q) | Q(job__icontains=q)
    )
    return render(
        template_name='partials/search.html',
        request=request,
        context={'profiles': results[:10]}
    )

@require_http_methods(['GET'])
def dropdown_modules(request):
    course_id = request.GET.get('course')
    modules = Module.objects.filter(course=course_id)
    return render(
        request=request,
        template_name='partials/dropdown.html',
        context={'modules':modules}
    )


class ProfileListView(ListView):
    model = Profile
    context_object_name = 'profiles'
    paginate_by = 10
    
    def get_template_names(self):
        if self.request.htmx:
            return 'partials/list-items.html'
        return 'profiles.html'


class ProfilesOnLoadView(ListView):
    model = Profile
    context_object_name = 'profiles'
    paginate_by = 10

    def get_template_names(self):
        if self.request.htmx:
            return 'partials/list-items-on-load.html'
        return 'profiles_on_load.html'


class WorkerListView(View):
    model = Profile
    paginate_by = 10
    partial_name = 'partials/active_search/table.html'
    template_name = 'workers.html'

    def get(self, request, *args, **kwargs):
        if request.htmx:
            q = request.GET.get('q', '')
            workers_list = self.model.objects.filter(
                Q(first_name__icontains=q) | Q(last_name__icontains=q) | \
                Q(company__icontains=q) | Q(job__icontains=q)
            )
            template_name = self.partial_name
        else:
            workers_list = self.model.objects.all()
            template_name = self.template_name
        page_number = request.GET.get('page', 1)
        paginator = Paginator(workers_list, self.paginate_by)
        pag_obj = paginator.get_page(page_number)
        return render(request, template_name, {'page_obj': pag_obj})

@require_http_methods(['GET'])
def edit_profile(request, id):
    context = {}
    profile = Profile.objects.get(id=id)
    context['profile'] = profile
    context['form'] = ProfileForm(instance=profile)
    template_name = 'profiles/edit-item.html'
    return render(request, template_name, context)

@require_http_methods(['POST'])
def update_profile(request, id):
    context = {}
    template_name = 'partials/item.html'
    profile = Profile.objects.get(id=id)
    form = ProfileForm(request.POST, instance=profile)
    if form.is_valid():
        form.save()
    context['profile'] = Profile.objects.get(id=id)
    return render(request, template_name, context)

@require_http_methods(['GET'])
def profiles_bullk(request):
    context = {}
    template_name = 'profiles_bulk_update.html'
    context['profiles'] = Profile.objects.all()[:20]
    return render(request, template_name, context)

@require_http_methods(['POST'])
def profiles_bulk_update(request, status):
    context = {}
    data = {'activate': True, 'deactivate': False}
    template_name = 'partials/table-bulk.html'
    ids = request.POST.getlist('ids')
    Profile.objects.filter(id__in=ids).update(status=data[status])
    context['profiles'] = Profile.objects.all()[:20]
    context['ids'] = ids
    context['tr_status'] = status
    return render(request, template_name, context)

@require_http_methods(['DELETE'])
def delete_profile(request, pk):
    context = {}
    template_name = 'partials/table-bulk.html'
    profile = Profile.objects.get(pk=pk)
    profile.delete()
    context['profiles'] = Profile.objects.all()[:20]
    return render(request, template_name, context)


def periodic_refresh(request):
    context = {}
    data_random = {
        'tweets': randint(1, 500),
        'following': randint(1, 500),
        'followers': randint(1, 500),
        'likes': randint(1, 500),
    }
    context['data_random'] = data_random
    if request.htmx:
        return render(request, 'partials/periodic_refresh.html', context)