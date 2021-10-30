from django.utils import timezone
from django.db import models
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.views.generic import UpdateView, DeleteView, CreateView
from .forms import CreateForm, CreateChoice
from .models import Question, Choice


class Indexview(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:10]
        #return Question.objects.order_by('-pub_date')[:5]


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:10]
    template = loader.get_template('polls/Index.html')
    output = ', '.join([q.question_text for q in latest_question_list])
    context = {
       'latest_question_list': latest_question_list,
    }
    return render(request, 'polls/Index.html', context)


def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "Вы не выбрали вариант ответа.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))


def create_form(request):
    return render(request, 'polls/create_form.html')


def create(request):
    error =''
    if request.method == 'POST':
        form = CreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('polls:success_saved'))
        else:
            error = 'Wrong form filling'
    form = CreateForm()
    data = {
        'form': form,
        'error': error
    }
    return render(request, 'polls/create.html', data)


def success_saved(request):
    return render(request, 'polls/success_saved.html')


class Update(UpdateView):
    model = Question
    pk_url_kwarg = "question_id"
    template_name = 'polls/update.html'
    form_class = CreateForm


class Delete(DeleteView):
    model = Question
    pk_url_kwarg = "question_id"
    success_url = '/polls/'
    template_name = 'polls/delete.html'


class ChoiceUpdateView(UpdateView):
    model = Choice
    pk_url_kwarg = "choice_id"
    fields = ['question', 'choice_text']
    success_url = '/polls/'
    template_name = 'polls/choice_update_form.html'


def ChoiceCreateView(request):
    error =''
    if request.method == 'POST':
        form = CreateChoice(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('polls:success_saved'))
        else:
            error = 'Wrong form filling'
    form = CreateChoice()
    data = {
        'form': form,
        'error': error
    }
    return render(request, 'polls/choice_create_form.html', data)


class ChoiceDeleteView(DeleteView):
    model = Choice
    pk_url_kwarg = "choice_id"
    success_url = '/polls/'
    template_name = 'polls/choice_delete_form.html'


