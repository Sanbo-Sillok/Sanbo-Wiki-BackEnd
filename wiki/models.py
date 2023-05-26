from django.db import models

# Create your models here.
class Post(models.Model):
    
    CHOICES = (
        ('PROTECTED', 'PROTECTED'),
        ('ACTIVE', 'ACTIVE'),
        ('REPORTED', 'REPORTED')
    )
    
    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name="제목", max_length=30)
    contents = models.TextField(verbose_name="내용")
    
    status = models.CharField(verbose_name="상태", choices=CHOICES, default='ACTIVE', max_length=20)
    
    created_at = models.DateTimeField(verbose_name="작성일시", auto_now_add=True)
    update_at = models.DateTimeField(verbose_name="수정일시", auto_now=True)