from django.forms import widgets
from rest_framework import serializers
from Blog.models import MyBlog

class MyBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyBlog
        fields = ('id', 'title', 'content', 'pub_date')
