from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import User, ExecutiveRole, WorkerUnit, Post, Level
from django.forms import inlineformset_factory
from chat.models import ChatRoom

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        role = request.POST.get('role', 'student')

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                role=role
            )
            general_room, created = ChatRoom.objects.get_or_create(name='General', room_type='public')
            general_room.participants.add(user)
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')

    return render(request, 'registration/register.html')

@login_required
def directory(request):
    users_list = User.objects.filter(is_active=True).exclude(role='admin')

    # Filters
    role_filter = request.GET.get('role')
    if role_filter:
        users_list = users_list.filter(role=role_filter)

    search_query = request.GET.get('search')
    if search_query:
        users_list = users_list.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query)
        )

    paginator = Paginator(users_list.order_by('username'), 12)
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)

    roles = User.ROLE_CHOICES

    context = {
        'users': users,
        'roles': roles,
        'current_role': role_filter,
        'search_query': search_query,
    }
    return render(request, 'users/directory.html', context)


def profile(request, user_id):
    user = get_object_or_404(User, id=user_id, is_active=True)

    # Get executive roles
    executive_roles = ExecutiveRole.objects.filter(user=user)

    # Get worker units
    worker_units = WorkerUnit.objects.filter(user=user)

    # Get posts
    posts = Post.objects.filter(user=user)

    # Get levels
    levels = Level.objects.filter(user=user)

    context = {
        'profile_user': user,
        'executive_roles': executive_roles,
        'worker_units': worker_units,
        'posts': posts,
        'levels': levels,
    }
    return render(request, 'users/profile.html', context)


@login_required
def edit_profile(request):
    ExecutiveRoleFormSet = inlineformset_factory(User, ExecutiveRole, fields=('position', 'session', 'start_year', 'end_year'), extra=1, can_delete=True)
    WorkerUnitFormSet = inlineformset_factory(User, WorkerUnit, fields=('unit_name', 'session', 'start_year', 'end_year'), extra=1, can_delete=True)
    PostFormSet = inlineformset_factory(User, Post, fields=('post_name', 'session', 'start_year', 'end_year'), extra=1, can_delete=True)
    LevelFormSet = inlineformset_factory(User, Level, fields=('level_name', 'session', 'start_year', 'end_year'), extra=1, can_delete=True)

    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.phone = request.POST.get('phone', '')
        user.bio = request.POST.get('bio', '')
        user.address = request.POST.get('address', '')

        # Handle birthday
        birthday_month = request.POST.get('birthday_month')
        birthday_day = request.POST.get('birthday_day')
        if birthday_month and birthday_day:
            user.birthday_month = int(birthday_month)
            user.birthday_day = int(birthday_day)

        # Handle fellowship years
        fellowship_years = request.POST.get('fellowship_years', '')
        if fellowship_years:
            years_list = [year.strip() for year in fellowship_years.split(',') if year.strip()]
            user.set_fellowship_years(years_list)

        # Handle profile picture
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']

        executive_formset = ExecutiveRoleFormSet(request.POST, instance=user, prefix='executives')
        worker_formset = WorkerUnitFormSet(request.POST, instance=user, prefix='workers')
        post_formset = PostFormSet(request.POST, instance=user, prefix='posts')
        level_formset = LevelFormSet(request.POST, instance=user, prefix='levels')

        if executive_formset.is_valid() and worker_formset.is_valid() and post_formset.is_valid() and level_formset.is_valid():
            user.save()
            executive_formset.save()
            worker_formset.save()
            post_formset.save()
            level_formset.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('users:profile', user_id=user.id)

    else:
        executive_formset = ExecutiveRoleFormSet(instance=request.user, prefix='executives')
        worker_formset = WorkerUnitFormSet(instance=request.user, prefix='workers')
        post_formset = PostFormSet(instance=request.user, prefix='posts')
        level_formset = LevelFormSet(instance=request.user, prefix='levels')

    context = {
        'months': [(i, i) for i in range(1, 13)],
        'days': [(i, i) for i in range(1, 32)],
        'executive_formset': executive_formset,
        'worker_formset': worker_formset,
        'post_formset': post_formset,
        'level_formset': level_formset,
    }
    return render(request, 'users/edit_profile.html', context)
