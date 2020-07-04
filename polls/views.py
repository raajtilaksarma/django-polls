from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import Question, Choice, Votes
from .forms import CreateListForm
from django.views import generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages 


# Create your views here.

class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
            Return published questions
        """
        return Question.objects.filter(
            pub_date__lte = timezone.now()
        ).order_by('-pub_date')


class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Question
    template_name = 'polls/detail.html' 
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(LoginRequiredMixin, generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if Votes.objects.filter(question_id=question, user_id=request.user).exists():
        # WHY THE BELOW CODE DOESNT WORK?
        # return render(request, 'polls/detail.html', {
        # 'question': question,
        # 'error_message': "You have already voted for this question."
        # })
        messages.success(request, 'Already voted for the question')
        return redirect('/polls/',permanent=True)
        # return HttpResponseRedirect('polls/index.html')

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # save vote
        v = Votes(question_id = question, user_id=request.user)
        v.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

@login_required
def create(request):
    if request.method == "POST":
        form = CreateListForm(request.POST)
        print('a')
        if form.is_valid():
            n = form.cleaned_data['name']
            q = Question(user_id=request.user, question_text=n, pub_date=timezone.now())
            q.save()      
            return HttpResponseRedirect('/polls/options/%i'%q.id)
    else:
        form = CreateListForm()
    return render(request, 'polls/create.html',{"form":form})

@login_required
def options(request, id):
    ls = Question.objects.get(id=id)
    if request.user != ls.user_id:
        return redirect('/all/',permanent=True)
    if request.method =='POST':
        if request.POST.get('save'):
            for item in ls.choice_set.all():
                p = request.POST
                if "text"+str(item.id) in p:
                    item.choice_text = p.get("text"+str(item.id))
                item.save()
            return redirect('/all/', permanent=True)
        elif request.POST.get('add'):
            newChoice = request.POST.get('new')
            if newChoice != '':
                ls.choice_set.create(choice_text = newChoice, votes = 0)
            else:
                print("Invalid choice")
    return render(request, 'polls/options.html', {'ls':ls})