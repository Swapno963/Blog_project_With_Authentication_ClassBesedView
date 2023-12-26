from typing import Any
from django.shortcuts import render,redirect
from . import forms
from . import models
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin


from django.utils.decorators import method_decorator
from django.views.generic import DetailView
# Create your views here.
@login_required
def add_post(request):
    if request.method == 'POST':
        post_form = forms.PostForm(request.POST)
        if post_form.is_valid():
            post_form.instance.author = request.user
            post_form.save()
            messages.success(request, 'Post Created Successfully.')

            return redirect("homepage")
    else:
        post_form = forms.PostForm()
    return render(request,'add_post.html',{"form":post_form})

@login_required
def edit_post(request, id):
    post = models.Post.objects.get(pk = id)
    # print(post.title)
    post_form = forms.PostForm(instance=post)
    if request.method == 'POST':
        post_form = forms.PostForm(request.POST, instance=post)
        if post_form.is_valid():
            post_form.instance.author = request.user
            post_form.save()
            messages.success(request, 'Post Edited Successfully.')

            return redirect("homepage")
    
    return render(request,'add_post.html',{"form":post_form})


@login_required
def delete_post(request, id):
    post = models.Post.objects.get(pk = id)
    post.delete()
    messages.success(request, 'Post Deleted Successfully.')

    return redirect('homepage')


# add post useing class based view
@method_decorator(login_required, name='dispatch')
class AddPostCreateView(SuccessMessageMixin,CreateView):
    model = models.Post
    form_class = forms.PostForm
    template_name = 'add_post.html'
    success_url =reverse_lazy('homepage')
    success_message = 'Post Created Successfully'
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class EditPostView(SuccessMessageMixin, UpdateView):
    model = models.Post
    form_class = forms.PostForm
    template_name = 'add_post.html'
    pk_url_kwarg = 'id'
    success_message = 'Post Edited Successfully'
    success_url = '/author/profile'


@method_decorator(login_required, name='dispatch')
class DeletePostView(SuccessMessageMixin, DeleteView):
    model = models.Post
    template_name = 'delete.html'
    success_message = 'Post Deleted Successfully'
    success_url = reverse_lazy('profile')
    pk_url_kwarg = 'id'



class DetailPostView(DetailView):
    model = models.Post
    template_name = 'post_detail.html'

    def post(self, request, *args, **kwargs):
        comment_form = forms.CommentForm(self.request.POST)
        post = self.get_object()
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
        return self.get(request, *args, **kwargs)
     
            
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        post = self.object 
        comments = post.comments.all()
        comment_form = forms.CommentForm()
           

        context['comments'] = comments
        context['comment_form'] = comment_form
        return context

