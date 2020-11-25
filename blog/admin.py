from django.contrib import admin
from .models import BLOG, COMMENT

# Register your models here.
admin.site.register((BLOG, COMMENT))