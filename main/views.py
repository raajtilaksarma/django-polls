from django.shortcuts import render
from django.views import generic
from django.utils import timezone
from polls.models import Question, Choice

# Create your views here.
def home(request):
	return render(request, "main/home.html", {})

class AllView(generic.ListView):    
    template_name = 'main/all.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
            Return the last 5 published questions
        """
        return Question.objects.filter(
            pub_date__lte = timezone.now()
        ).order_by('-pub_date')
