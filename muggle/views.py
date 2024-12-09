from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
    """用户登录视图"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', '/')
                return redirect(next_url)
    else:
        form = AuthenticationForm()
    return render(request, 'muggle/login.html', {'form': form})

def logout_view(request):
    """用户登出视图"""
    logout(request)
    return redirect('muggle:login')

@login_required
def profile(request):
    """用户资料视图"""
    return render(request, 'muggle/profile.html')
