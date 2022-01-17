from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from .forms import UserRegisterForm, ProfileRegisterForm, ProfileUpdateForm, UserUpdateForm
from django.contrib import messages
from .models import Profile,Notification
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from home.models import Project
from home.filters import ProjectFilter
from functions import *
from django.core.serializers import serialize

def signup(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        profile_form = ProfileRegisterForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            newusername = user_form.cleaned_data.get('username')
            newuser = User.objects.filter(username = newusername).first()

            profile_form = ProfileRegisterForm(request.POST,request.FILES, instance = newuser.profile)
            profile_form.save()

            messages.success(request, f"Account created for {newusername}!")
            return redirect('login')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserRegisterForm()
        profile_form = ProfileRegisterForm()

    context = {
        'title': 'Register',
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'users/signup.html', context)


@login_required
def profile(request, user_id):
    all_project_list = Project.objects.all().order_by('-DatePosted')

    user_projects_id = []
    user_starred_projects_id = []
    user_requested_projects_id = []

    user = User.objects.get(id=user_id)
    user_applied_projects = all_project_list.filter(AlreadyApplied=user)
    user_floated_projects = all_project_list.filter(FloatedBy=user)
    user_requested_projects = all_project_list.filter(ApplyRequest=request.user)
    user_starred_projects = request.user.profile.starred_projects.all()
    for project in user_applied_projects:
        user_projects_id.append(project.id)
    for project in user_floated_projects:
        user_projects_id.append(project.id)
    for project in user_requested_projects:
        user_requested_projects_id.append(project.id)
    for project in user_starred_projects:
        user_starred_projects_id.append(project.id)

    context = {
        'title': 'Profile',
        'num_projects_applied': user_applied_projects.count(),
        'num_projects_req': len(user_requested_projects_id),
        'num_projects_floated': user_floated_projects.count(),
        'user_starred_projects_id' : user_starred_projects_id,
        'projects_applied': user_applied_projects[0:5],
        'projects_floated': user_floated_projects[0:5],
        'projects_requested': user_requested_projects[0:5],
        'projects_starred': user_starred_projects[0:5],
        'notifications': Notification.objects.filter(user=request.user).order_by('-time'),
        'profile_user': User.objects.get(id = user_id)
    }

    return render(request, 'users/profile.html', context)

@login_required
def profile_edit(request):
    if request.method == 'POST':
        user_update_form = UserUpdateForm(request.POST, instance = request.user)
        profile_update_form = ProfileUpdateForm(request.POST, request.FILES, instance = request.user.profile)

        if user_update_form.is_valid() and profile_update_form.is_valid():
            user_profile = Profile.objects.get(user = request.user)
            user_img = str(user_profile.image)
            user_cv = str(user_profile.cv)

            if len(request.FILES)!=0:
                if request.FILES.get('image') and user_img!="default.jpg":
                    default_storage.delete(user_img)
                elif request.FILES.get('cv') and user_cv:
                    default_storage.delete(user_cv)

            user_update_form.save()
            profile_update_form.save()

            messages.success(request, "Your profile has been updated!")
            return redirect('/profile/'+ str(request.user.id))
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_update_form = UserUpdateForm(instance = request.user)
        profile_update_form = ProfileUpdateForm(instance = request.user.profile)

    context = {
        'title': 'Profile Edit',
        'user_form': user_update_form,
        'notifications': Notification.objects.filter(user=request.user).order_by('-time'),
        'profile_form': profile_update_form,
    }

    return render(request, 'users/profile_edit.html', context)


@login_required
def projects_view(request):
    view = request.GET.get('view')
    all_projects = Project.objects.all()
    if view == "applied":
        req_projects = all_projects.filter(AlreadyApplied = request.user)
        title = 'Projects Applied'
        heading = "Projects Applied For:"
    elif view == "requested":
        req_projects = all_projects.filter(ApplyRequest = request.user)
        title = 'Projects Requested'
        heading = "Projects Requested:"
    elif view == "floated":
        req_projects = all_projects.filter(FloatedBy = request.user)
        title = 'Projects Floated'
        heading = "Projects Floated:"
    else:
        req_projects = request.user.profile.starred_projects.all()
        title = 'Projects Starred'
        heading = "Projects Starred:"
    req_projects = req_projects.order_by('-DatePosted')

    projects = get_filtered_projects(request, req_projects)
    projects = get_paginated_projects(request, projects)
    projects_id = get_projects_id(request)
    common_tags = get_most_common_tags(5)

    context = {
        'title': title,
        'users':User.objects.all(),
        'tags': Tag.objects.all(),
        'users_html':serialize("json", User.objects.all()),
        'tags_html':serialize("json", Tag.objects.all()),
        'projects': projects,
        'projects_id': projects_id,
        'notifications': Notification.objects.filter(user = request.user).order_by('-time'),
        'common_tags':common_tags,
        'heading': heading
    }

    return render(request, 'users/projects_view.html', context)

def oauth(request):
    url = '/accounts/google/login/?process=login/'
    return redirect(url)