from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib import messages
from MTV.models import Board, Comment
from django.views.generic import DetailView, ListView,CreateView, UpdateView, DeleteView
from MTV.forms import BoardCreateForm,CommentForm
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
import os, time
from config import settings
from MTV.models import Board
from django.contrib.auth.decorators import login_required
# Create your views here.


def index(request) :
    return render (request, 'MTV/index.html')


def subscribe(request) :
    return render (request, 'MTV/subscribe.html')

class BoardList(ListView):
    model = Board
    template_name = 'MTV/index.html'
    ordering = '-pk'
    paginate_by = 6

class Upload(CreateView) :
    model = Board
    form_class = BoardCreateForm
    template_name = 'MTV/upload.html'
    def form_valid(self, form) :
        current_user = self.request.user
        if current_user.is_authenticated :
            form.instance.author = current_user
            return super().form_valid(form)
        else :
            return redirect('/')

@login_required(login_url='common:login')
def BoardDelete(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.user != board.author:
        return redirect('MTV:get', pk=pk)
    if board.sound:
        sound_path = os.path.join(settings.MEDIA_ROOT, board.sound.path)
        if os.path.exists(sound_path):
            os.remove(sound_path)
    if board.photo:
        photo_path = os.path.join(settings.MEDIA_ROOT, board.photo.path)
        if os.path.exists(photo_path):
            os.remove(photo_path)
    board.delete()
    return redirect('MTV:index')

class Get(DetailView) :
    model = Board
    template_name = 'MTV/get.html'


                                                                                       



def document_detail(request, document_id):
    
    document = get_object_or_404(Board, pk=document_id)

    #만약 post일때만 댓글 입력에 관한 처리를 더한다.

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        comment_form.instance.author_id = request.user.id
        comment_form.instance.document_id = document_id
        if comment_form.is_valid():
            comment = comment_form.save()


    #models.py에서 document의 related_name을 comments로 해놓았다.

    comment_form = CommentForm()
    comments = document.comments.all()

    return render(request, 'MTV/comment.html', {'object':document, "comments":comments, "comment_form":comment_form})




def comment_update(request, comment_id):
    
    comment = get_object_or_404(Comment, pk=comment_id)
    document = get_object_or_404(Board, pk=comment.document.id)

    if request.user != comment.author:
        messages.warning(request, "권한 없음")
        return redirect(document)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect(document)
    else:
        form = CommentForm(instance=comment)
        return render(request,'MTV/comment_update.html',{'form':form})


def comment_delete(request, comment_id):

    comment = get_object_or_404(Comment, pk=comment_id)
    document = get_object_or_404(Board, pk=comment.document.id)

    if request.user != comment.author and not request.user.is_staff and request.user != document.author:
        messages.warning(request, '권한 없음')
        return redirect(document)
    if request.method == "POST":
        comment.delete()
        return redirect(document)
    else:
        return render(request, 'MTV/comment_delete.html', {'object':comment})


@login_required(login_url='common:login')
def result(request): 
    posts= Board.objects.all()
    start= time.time()
    query = request.GET['query']
    if query :
        posts= Board.objects.filter(title__contains=query)
        end= time.time() - start 
    return render(request, 'MTV/result.html', {'posts':posts, 'time':end})




