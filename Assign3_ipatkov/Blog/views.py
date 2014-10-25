from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.shortcuts import render

import datetime

from django.shortcuts import render
from models import MyBlog
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Template, Context, RequestContext
from django.template.loader import get_template
from Assign3_ipatkov.converter import content_to_html, html_to_content
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth



def counter(request):
    if not request.session.get("session_start"):
        request.session['session_start']=str(datetime.datetime.now())
    if request.session.get('visits')==None or request.session.get('edits')==None or request.session.get('creates')==None or request.session.get('deletes')==None:
        request.session['visits']=int(0)
        request.session['edits']=int(0)
        request.session['creates']=int(0)
        request.session['deletes']=int(0)
    session_start=request.session.get('session_start')
    visits=request.session.get('visits')
    edits=request.session.get('edits')
    creates=request.session.get('creates')
    deletes=request.session.get('deletes')


    mydict={'session_start':session_start,'visits':visits,'edits':edits,'creates':creates,'deletes':deletes}
    return mydict

def create_user(request):
    context=RequestContext(request)
    if request.method=='POST':
        if request.POST.get('password1')==request.POST.get('password2'):
            user=User.objects.create_user(username=request.POST.get('username'),password=request.POST.get('password1'))
            user.save()
            messages.success(request,"Successfully registered")
            """ createform=UserCreationForm(data=request.POST)
            if createform.is_valid():
            user=createform.save()
            user.set_password(user.password)
            user.save()
            messages.success(request,"Successfully registered")"""
        else:
            messages.error(request,"Give username and password")
        return HttpResponseRedirect('/myblog/')
    else:
        createform=UserCreationForm()
    return render_to_response('createuser.html',{'createform':createform},context)

def show_home(request):
    if request.method=='POST' and request.POST.has_key('state'):
        request.session.flush()
        return HttpResponseRedirect('/myblog/')
    elif request.method=="POST" and request.POST.has_key('username'):
        username=request.POST.get('username','')
        password=request.POST.get('password','')
        user=auth.authenticate(username=username,password=password)
        if user is not None and user.is_active:
            auth.login(request,user)
            return HttpResponseRedirect('/myblog/')
        else:
            messages.error(request,"Username or password doesn't match")
            return HttpResponseRedirect('/myblog/')

    elif request.method=="GET" and 'logout' in request.GET:
        auth.logout(request)
        return HttpResponseRedirect('/myblog/')
    try:
        blogs=MyBlog.objects.all()
        messages1 = get_messages(request)
        t=get_template("showhome.html")
        d=counter(request)

        session_start,visits,edits,creates,deletes=d['session_start'],d['visits'],d['edits'],d['creates'],d['deletes']
        html=t.render(RequestContext(request,{'blogs':blogs,
                               'messages':messages1,
                               'session_start':session_start,
                               'visits':visits,
                               'edits':edits,
                               'creates':creates,
                               'deletes':deletes
                               }))
        return HttpResponse(html)
    except IOError:
        return HttpResponse("Something went wrong")


def add_blog(request):
    blog=MyBlog()
    if request.method=='POST' and request.POST.has_key('content'):
        blog.content=request.POST['content']
        blog.pub_date = datetime.datetime.now()
        blog.title=request.POST['title'].strip()
        blog.version=1
        blog.save()
        counter(request)
        creates=request.session.get('creates')
        request.session['creates']=creates+1

        messages.success(request,"Blog entry added successfully")
        return HttpResponseRedirect('/myblog/')
    else:
       #d=counter(request)
        #session_start,visits,edits,creates,deletes=d['session_start'],d['visits'],d['edits'],d['creates'],d['deletes']
        return render(request,'addblog.html')


def edit_blog(request,id):
    if MyBlog.exists(id):
        #find an existing entry
        blog=MyBlog.getById(id)
    else:
        #create a new blog entry with add_blog()
        blog=MyBlog()
        blog.id=id
        blog.pub_date=datetime.datetime.now()
    if request.method=="POST" and request.POST.has_key("content") and request.POST.has_key("edited_version"):
        edited_version = int(request.POST["edited_version"])
        content = html_to_content(request.POST["content"])
        title = request.POST['title']
        pub_date=blog.pub_date

        if edited_version == blog.version:
            blog.content=content
            blog.title=title
            blog.pub_date=pub_date
            blog.version=blog.version+1
            blog.save()
            d=counter(request)
            session_start,visits,edits,creates,deletes=d['session_start'],d['visits'],d['edits'],d['creates'],d['deletes']
            request.session['edits']=edits+1
            return HttpResponseRedirect('/myblog/')
        else:
            d=counter(request)
            session_start,visits,edits,creates,deletes=d['session_start'],d['visits'],d['edits'],d['creates'],d['deletes']
            request.session['edits']=edits+1
            return render_to_response("conflict.html",
                                      {'id':blog.id,
                                        'title': blog.title,
                                       'content':blog.content,
                                       'user_content':content,
                                       'pub_date':blog.pub_date,
                                       'edited_version':blog.version},
                                      context_instance=RequestContext(request))
    else:
        return render_to_response("edit.html",
                                  {'id':blog.id,
                                   'title': blog.title,
                                   'content': blog.content,
                                   'pub_date': blog.pub_date,
                                   'edited_version': blog.version},
                                  context_instance=RequestContext(request)
                                  )



def show_blog(request,id):
    if MyBlog.exists(id):
        blog=MyBlog.getById(id)
        visits=request.session.get('visits')
        request.session['visits']=visits+1
    else:
        messages.error(request, 'Blog with id = '+str(id)+' not found. Create New blog')
        return edit_blog(request,id)
    t=get_template("show.html")
    html=t.render(Context({'id':blog.id,
                           'title':blog.title,
                           'content':blog.content,
                           'pub_date':blog.pub_date,
                           'version':blog.version}))
    return HttpResponse(html)

def delete_blog(request,id):
    if MyBlog.exists(id):
        blog=MyBlog.getById(id)
        blog.delete()
        deletes=request.session.get('deletes')
        request.session['deletes']=deletes+1
        messages.success(request,"Blog entry deleted successfully")
    else:
        messages.error(request, 'Blog with id = '+str(id)+' not found.')
    return HttpResponseRedirect("/myblog/")


