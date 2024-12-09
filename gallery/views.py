from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Category
from .forms import CategoryForm

@login_required
def category_list(request):
    """分类列表视图"""
    # 获取搜索参数
    search_query = request.GET.get('search', '')
    
    # 基础查询：获取所有顶级类目
    categories = Category.objects.filter(parent=None)
    
    # 如果有搜索条件，应用搜索过滤
    if search_query:
        # 先找出所有匹配的类目
        matching_categories = Category.objects.filter(
            Q(category_name_zh__icontains=search_query) |
            Q(category_name_en__icontains=search_query)
        )
        # 获取匹配类目的所有父类目ID
        parent_ids = set()
        for category in matching_categories:
            current = category
            while current.parent_id:
                parent_ids.add(current.parent_id)
                current = current.parent
        
        # 合并匹配的类目和它们的父类目
        categories = categories.filter(
            Q(id__in=matching_categories.filter(parent=None).values_list('id', flat=True)) |
            Q(id__in=parent_ids)
        )
    
    # 排序并预加载关联数据
    categories = categories.order_by('rank_id', 'id').prefetch_related(
        'children',
        'children__children',
        'children__children__children'
    )
    
    context = {
        'title': '分类管理',
        'page_title': '分类列表',
        'page_subtitle': 'Category List',
        'categories': categories,
        'search_query': search_query,  # 将搜索词传递给模板
    }
    return render(request, 'gallery/category/list.html', context)

@login_required
def category_add(request):
    """创建分类视图"""
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, '类目创建成功！')
            return redirect('gallery:category_list')
    else:
        form = CategoryForm()
    
    context = {
        'title': '创建类目',
        'page_title': '创建新类目',
        'page_subtitle': 'Create New Category',
        'form': form,
        'submit_text': '创建',
    }
    return render(request, 'gallery/category/form.html', context)

@login_required
def category_update(request, pk):
    """更新分类视图"""
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, f'类目"{category.category_name_zh}"更新成功！')
            return redirect('gallery:category_list')
    else:
        form = CategoryForm(instance=category)
    
    context = {
        'title': '编辑类目',
        'page_title': f'编辑类目: {category.category_name_zh}',
        'page_subtitle': 'Edit Category',
        'form': form,
        'submit_text': '保存',
        'category': category,
    }
    return render(request, 'gallery/category/form.html', context)

@login_required
def category_delete(request, pk):
    """删除分类视图"""
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        try:
            category.delete()
            messages.success(request, f'类目"{category.category_name_zh}"已成功删除！')
        except Exception as e:
            messages.error(request, f'删除类目时发生错误：{str(e)}')
    
    return redirect('gallery:category_list')
