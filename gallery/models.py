from django.db import models

class Category(models.Model):
    """分类模型"""
    STATUS_CHOICES = (
        (1, '启用'),
        (0, '禁用'),
    )
    
    id = models.AutoField('ID', primary_key=True)
    category_name_en = models.CharField('英文名称', max_length=100)
    category_name_zh = models.CharField('中文名称', max_length=100)
    description = models.TextField('描述', blank=True)
    image = models.ImageField('图片', upload_to='images', blank=True)
    parent = models.ForeignKey('self', verbose_name='父级分类', 
                             on_delete=models.CASCADE, 
                             null=True, blank=True,
                             related_name='children')
    rank_id = models.IntegerField('排序ID', default=0)
    original_data = models.JSONField('原始数据', null=True, blank=True)
    level = models.IntegerField('层级', default=1)
    is_last_level = models.BooleanField('是否最后一级', default=False)
    status = models.IntegerField('状态', choices=STATUS_CHOICES, default=1)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
        ordering = ['rank_id', 'id']
        db_table = 'gallery_category'

    def __str__(self):
        return f"{self.category_name_zh} ({self.category_name_en})"

    def save(self, *args, **kwargs):
        if not self.parent:
            self.level = 1
        else:
            self.level = self.parent.level + 1
        super().save(*args, **kwargs)
