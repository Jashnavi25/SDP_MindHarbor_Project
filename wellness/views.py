from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, SignInForm, WellnessResourceForm, CounselingSessionForm, AnonymousSupportForm
from .models import Profile, WellnessResource, CounselingSession, AnonymousSupport



# --- Authentication ---
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data['role']
            Profile.objects.create(user=user, role=role)
            return redirect('signin')
    else:
        form = SignUpForm()
    return render(request, 'wellness/signup.html', {'form': form})

def signin_view(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            role = form.cleaned_data['role']
            try:
                user = User.objects.get(email=email)
                auth_user = authenticate(username=user.username, password=password)
                if auth_user is not None:
                    login(request, auth_user)
                    profile = Profile.objects.get(user=auth_user)
                    if profile.role == 'admin':
                        return redirect('admin_dashboard')
                    elif profile.role == 'student':
                        return redirect('student_dashboard')
                    elif profile.role == 'counselor':
                        return redirect('counselor_dashboard')
            except User.DoesNotExist:
                form.add_error('email', 'User not found')
    else:
        form = SignInForm()
    return render(request, 'wellness/signin.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('signin')

# --- Dashboards ---
@login_required
def admin_dashboard(request):
    resources = WellnessResource.objects.all()
    sessions = CounselingSession.objects.all()
    supports = AnonymousSupport.objects.all()
    return render(request, 'wellness/admin_dashboard.html', {
        'resources': resources,
        'sessions': sessions,
        'supports': supports
    })

@login_required
def student_dashboard(request):
    resources = WellnessResource.objects.all()
    sessions = CounselingSession.objects.filter(student=request.user)
    supports = AnonymousSupport.objects.all()
    return render(request, 'wellness/student_dashboard.html', {
        'resources': resources,
        'sessions': sessions,
        'supports': supports
    })

@login_required
def counselor_dashboard(request):
    sessions = CounselingSession.objects.filter(counselor=request.user)
    supports = AnonymousSupport.objects.all()
    return render(request, 'wellness/counselor_dashboard.html', {
        'sessions': sessions,
        'supports': supports
    })

# --- Wellness Resources CRUD ---
@login_required
def add_resource(request):
    if request.method == 'POST':
        form = WellnessResourceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = WellnessResourceForm()
    return render(request, 'wellness/add_resource.html', {'form': form})

@login_required
def edit_resource(request, pk):
    resource = get_object_or_404(WellnessResource, pk=pk)
    if request.method == 'POST':
        form = WellnessResourceForm(request.POST, instance=resource)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = WellnessResourceForm(instance=resource)
    return render(request, 'wellness/edit_resource.html', {'form': form})

@login_required
def delete_resource(request, pk):
    resource = get_object_or_404(WellnessResource, pk=pk)
    resource.delete()
    return redirect('admin_dashboard')

# --- Counseling Sessions CRUD ---
@login_required
def add_session(request):
    if request.method == 'POST':
        form = CounselingSessionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = CounselingSessionForm()
    return render(request, 'wellness/add_session.html', {'form': form})

@login_required
def edit_session(request, pk):
    session = get_object_or_404(CounselingSession, pk=pk)
    if request.method == 'POST':
        form = CounselingSessionForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = CounselingSessionForm(instance=session)
    return render(request, 'wellness/edit_session.html', {'form': form})

@login_required
def delete_session(request, pk):
    session = get_object_or_404(CounselingSession, pk=pk)
    session.delete()
    return redirect('admin_dashboard')

# --- Anonymous Support CRUD ---
@login_required
def add_support(request):
    if request.method == 'POST':
        form = AnonymousSupportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = AnonymousSupportForm()
    return render(request, 'wellness/add_support.html', {'form': form})

@login_required
def edit_support(request, pk):
    support = get_object_or_404(AnonymousSupport, pk=pk)
    if request.method == 'POST':
        form = AnonymousSupportForm(request.POST, instance=support)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = AnonymousSupportForm(instance=support)
    return render(request, 'wellness/edit_support.html', {'form': form})

@login_required
def delete_support(request, pk):
    support = get_object_or_404(AnonymousSupport, pk=pk)
    support.delete()
    return redirect('admin_dashboard')


def resources_list(request):
    resources = WellnessResource.objects.all()
    return render(request, 'wellness/resources_list.html', {'resources': resources})

def counseling_list(request):
    sessions = CounselingSession.objects.all()
    return render(request, 'wellness/counseling_list.html', {'sessions': sessions})

def support_list(request):
    supports = AnonymousSupport.objects.all()
    return render(request, 'wellness/support_list.html', {'supports': supports})


