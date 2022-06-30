from django.shortcuts import render, get_object_or_404, redirect
#edited
#from django.http import HttpResponse
from django.http import HttpResponseNotAllowed
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

#for video
from .models import Video

# Create your views here.
def intro(request):
    page = request.GET.get('page', '1')
    question_list = Question.objects.order_by('-create_date')
    paginator = Paginator(question_list, 15)
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj}
    return render(request, 'first_site/intro.html', context)

def board_list(request):
    page = request.GET.get('page', '1')
    question_list = Question.objects.order_by('-create_date')

    ## category filter
    qna_obj = Question.objects.filter(category="qna").order_by('-create_date')
    study_obj = Question.objects.filter(category="study").order_by('-create_date')
    etc_obj = Question.objects.filter(category="etc").order_by('-create_date')

    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)
    ## category filter
    paginator_qna = Paginator(qna_obj, 10)
    page_obj_qna = paginator_qna.get_page(page)
    paginator_study = Paginator(study_obj, 10)
    page_obj_study = paginator_study.get_page(page)
    paginator_etc = Paginator(etc_obj, 10)
    page_obj_etc = paginator_etc.get_page(page)

    context = {'question_list': page_obj, 'qna_list': page_obj_qna, 'study_list': page_obj_study, 'etc_list': page_obj_etc}
    return render(request, 'first_site/board_list.html', context)
    

def homescreen(request):
    page = request.GET.get('page', '1')     #페이지
    question_list = Question.objects.order_by('-create_date')
    paginator = Paginator(question_list, 15)
    page_obj = paginator.get_page(page)

    #for video
    video_list = Video.objects.all()

    context = {'question_list': page_obj, 'video_list': video_list}
    return render(request, 'first_site/homescreen.html', context)
    #return HttpResponse("===첫 페이지 ===")


def detail(request, question_id):
    #question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'first_site/question_detail.html', context)

@login_required(login_url='common:login')
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('first_site:detail', question_id=question.id)
    else:
        return HttpResponseNotAllowed('Only POST is possible.')
    context = {'question': question, 'form': form}

    return render(request, 'first_site/question_detail.html', context)

@login_required(login_url='common:login')
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()
            question.save()
            return redirect('first_site:board_list')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'first_site/question_form.html', context)


@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('first_site:detail', question_id=question.id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()  # 수정일시 저장
            question.save()
            return redirect('first_site:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}

    return render(request, 'first_site/question_form.html', context)

@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('first_site:detail', question_id=question.id)
    question.delete()
    return redirect('first_site:board_list')


@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('first_site:detail', question_id=answer.question.id)
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('first_site:detail', question_id=answer.question.id)
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'first_site/answer_form.html', context)


