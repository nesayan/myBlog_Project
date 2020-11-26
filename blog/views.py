from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import BLOG, COMMENT
import datetime



# Create your views here.
#def home(request):
    #return render(request, 'blog/home.html')

# function for home page
def getAllBlogs(request):
    allBlogs = BLOG.objects.all().order_by('-dateCreated')
    return render(request, 'blog/home.html', {'allBlogs': allBlogs})

# function for signup page
def signupUser(request):
    if request.method == 'GET':
        return render(request, 'blog/signupUser.html')
    else:
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
                user = User.objects.create_user(username= username, password= password1)
                user.save()
                messages.success(request, f'Welcome {username}')
                login(request, user)
                return redirect('blogs') #render(request, 'blog/blogs.html')
            except IntegrityError:
                messages.error(request, 'Username already exists')
                return render(request, 'blog/signupUser.html')
        else:
            messages.error(request, 'Passwords did not match')
            return render(request, 'blog/signupUser.html')

# function for login page
def loginUser(request):
    if request.method == 'GET':
        return render(request, 'blog/loginUser.html')
    else:
        username = request.POST['username']
        password1 = request.POST['password1']

        user = authenticate(username= username, password= password1)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome {username}')
            return redirect('blogs') #render(request, 'blog/blogs.html')
        else:
            messages.error(request, 'Username or Password incorrect')
            return render(request, 'blog/loginUser.html')

# function for logout
@login_required(login_url= 'loginUser')
def logoutUser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('getAllBlogs')

# function for blogs page
#@login_required(login_url= 'loginUser')
def blogs(request):
    blogs = BLOG.objects.filter(user = request.user).order_by('-dateCreated')
    return render(request, 'blog/blogs.html', {'blogs': blogs})

# function for add new blog page
@login_required(login_url= 'loginUser')
def addNewBlog(request):
    if request.method == 'GET':
        return render(request, 'blog/addNewBlog.html')
    else:
        try:
            title = request.POST['title']
            description = request.POST['description']
            dateCreated = datetime.datetime.now()
            print(dateCreated)
            newBlog = BLOG(title= title, description= description, user = request.user)
            newBlog.save()
            return redirect('blogs')
        except ValueError:
            messages.error(request, 'Bad value entered')
            return render(request, 'blog/addNewBlog.html')
            
# function for view a particular blog page
#@login_required(login_url= 'loginUser')
def viewBlog(request, blog_pk):
    blog = get_object_or_404(BLOG, pk= blog_pk)#, user= request.user)
    blogComments = COMMENT.objects.filter(post= blog, parent= None)
    blogReplies = COMMENT.objects.filter(post= blog).exclude(parent= None)

    #making a dict where key= parent comment pk, value = list of all replies to that comment 
    commentToReplies = {}
    for x in blogReplies:
        if x.parent.pk not in commentToReplies.keys():
            commentToReplies[x.parent.pk] = [x]
        else:
            commentToReplies[x.parent.pk].append(x)
    
    if request.method == 'GET':
        return render(request, 'blog/viewBlog.html', {'blog': blog, 'blogComments': blogComments, 'commentToReplies': commentToReplies})
    else:
        try:
            newTitle = request.POST['title']
            newDescription = request.POST['description']
            editBlog = BLOG.objects.filter(pk= blog_pk, user= request.user)
            editBlog.update(title = newTitle, description= newDescription,  user= request.user)
            return redirect('blogs')
        except ValueError:
            messages.error(request, 'Bad value entered')
            return render(request, 'blog/viewBlog.html', {'blog': blog, 'allComments': allComments, 'commentToReplies': commentToReplies})
    
# function for delete blog
def deleteBlog(request, blog_pk):
    if request.method == 'POST':
        blog = get_object_or_404(BLOG, pk= blog_pk, user= request.user)
        blog.delete()
        return redirect('blogs')
    else:
        return HttpResponse('Not Allowed')

# function for search button
def search(request):
    searchValue = request.GET.get('search')
    searchBlogs = BLOG.objects.filter(title__contains= searchValue)
    return render(request, 'blog/search.html', {'searchBlogs':searchBlogs})

def postComment(request):
    if request.method == 'POST':
        description = request.POST['comment']
        post = BLOG.objects.filter(pk= request.POST['commentBlogID']).first()
        if request.POST['commentParent'] == "":
            newComment = COMMENT(description= description, user= request.user, post= post, parent= None)
            newComment.save()
            return redirect('viewBlog', request.POST['commentBlogID'])
        else:
            parent = COMMENT.objects.filter(pk= request.POST['commentParent']).first()
            newComment = COMMENT(description= description, user= request.user, post= post, parent= parent)
            newComment.save()
            return redirect('viewBlog', request.POST['commentBlogID'])
    else:
        HttpResponse("Not allowed")

