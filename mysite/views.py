from django.shortcuts import render

def index(request):
    """主页视图函数"""
    context = {
        'title': '主页',
        'page_title': '系统概览',
        'page_subtitle': 'Dashboard Overview'
    }
    return render(request, 'index.html', context) 