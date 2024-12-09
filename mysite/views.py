from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    """主页视图函数"""
    context = {
        'title': '主页',
        'page_title': '系统概览',
        'page_subtitle': 'Dashboard Overview'
    }
    return render(request, 'home_page.html', context)