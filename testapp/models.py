from django.db import models

# Create your models here.
class Test(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name="제목", max_length=30)
    content = models.TextField(verbose_name="내용")
    created_at = models.DateTimeField(verbose_name="작성일시", auto_now_add=True)