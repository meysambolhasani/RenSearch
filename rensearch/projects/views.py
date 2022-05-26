
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Project, Review, Tag
from .forms import ProjectForm, ReviewForm
from .utils import search_project, paginate_projects


def projects(request):
   
    projects, search_query = search_project(request)
    custom_range, projects = paginate_projects(request, projects, 3)

    context = {'projects': projects, 'search_query': search_query,
               'custom_range': custom_range}
    return render(request, 'projects/projects.html', context)


def single_project(request, pk):

    project = Project.objects.get(id=pk)
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.owner = request.user.profile
        review.project = project
        review.save()
        messages.success(request, 'your review was successfully submitted')
        return redirect('single-project', pk=project.id)
    try:
        project.get_vote_count
    except ZeroDivisionError:
        messages.info(request, 'Project has not have  review yet')

    context = {'project': project, 'form': form}
    return render(request, 'projects/single-project.html', context)


@login_required(login_url='login')
def add_project(request):

    profile = request.user.profile
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('user-account')

    context = {'form': form}
    return render(request, 'projects/add-project.html', context)

@login_required(login_url='login')
def update_project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',',  " ").split()

        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            
            return redirect('user-account')

    context = {'form': form,'project': project}
    return render(request, 'projects/add-project.html', context)


@login_required(login_url='login')
def delete_project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('user-account')
    context = {'object': project}
    return render(request, 'delete-form.html', context)
