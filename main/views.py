from django.shortcuts import render,redirect
from django.views import generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from polls.models import Question, Choice, Votes, UserProfile
from .forms import UserForm

# Create your views here.
def home(request):
	return render(request, "main/home.html", {})

@login_required
def profile(request):
	return render(request, "main/profile.html", {})

@login_required
def accountSettings(request):
    user = request.user.userprofile
    form = UserForm(instance=user)
    print('first :', user.image.url)
    if request.method =='POST':
        form = UserForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            print('second :', user.image.url)
            return redirect('/profile/',permanent=True)
    context = {'form':form}
    return render(request, 'main/account_settings.html', context)
    
class AllView(generic.ListView):    
    template_name = 'main/all.html'
    context_object_name = 'question_list'

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte = timezone.now()
        ).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super(AllView, self).get_context_data(**kwargs)
        context['ques'] = []
        question_list = Question.objects.filter(
            pub_date__lte = timezone.now()
        ).order_by('-pub_date')
        for question in question_list:
            choices = []
            for choice in question.choice_set.all():
                choice_dict = dict()
                choice_dict['choice_text'] = choice.choice_text
                choice_dict['votes'] = choice.votes
                total_votes = len(question.votes_set.all())
                if total_votes>0:
                    choice_dict['perc'] = int((choice.votes/total_votes)*100)
                else:
                    choice_dict['perc'] = 0
                choices.append(choice_dict)
            if len(choices)>0:
                context['ques'].append({'question_text':question.question_text,
                'user_id' : question.user_id,
                'choices':choices})
        return context