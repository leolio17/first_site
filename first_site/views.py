from django.shortcuts import render, get_object_or_404, redirect
#edited
#from django.http import HttpResponse
from .models import Question
from django.utils import timezone

# Create your views here.
def index(request):
    question_list = Question.objects.order_by('-create_date')
    context = {'question_list': question_list}
    return render(request, 'first_site/question_list.html', context)
    #return HttpResponse("===첫 페이지 ===")


def detail(request, question_id):
    #question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'first_site/question_detail.html', context)


def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
    return redirect('first_site:detail', question_id=question.id)

