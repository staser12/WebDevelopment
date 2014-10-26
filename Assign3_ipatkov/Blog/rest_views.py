from rest_framework.views import APIView
from rest_framework.decorators import api_view, renderer_classes,\
    authentication_classes, permission_classes

from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from django.http import HttpResponse

from Blog.models import MyBlog
from Blog.serializers import MyBlogSerializer

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)
        
@api_view(['GET', 'PUT'])
@renderer_classes([JSONRenderer,])
def blog_list(request):
    if request.method == 'GET':
        blogs = MyBlog.objects.all()
        serializer = MyBlogSerializer(blogs, many=True)
        #print serializer.data
        #return JSONResponse(serializer.data)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = MyBlogSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        else:
            return JSONResponse(serializer.errors, status=400)
        
        
@api_view(['GET', 'POST'])
#@authentication_classes([BasicAuthentication])
#@permission_classes([IsAuthenticated])
def blog_detail(request, pk):
    """
    Retrieve, update or delete a blog.
    """
    try:
        blog = MyBlog.objects.get(pk=pk)
    except MyBlog.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = MyBlogSerializer(blog)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        #data = JSONParser().parse(request)
        data = request.DATA
        print request.DATA
        serializer = MyBlogSerializer(blog, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        blog.delete()
        return HttpResponse(status=204)