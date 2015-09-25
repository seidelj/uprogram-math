from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import auth
from .models import Constants, Quizes, QuizGroup, SubCatagory, LearnItem, Themes
from django.utils import timezone
from django.http import HttpResponseRedirect

# Create your views here.

@login_required(login_url='/login/')
def index(request):
	if request.user.is_authenticated:
                request.user.student.set_null_theme()
		return HttpResponseRedirect(reverse('m:dashboard'))
	else:
		return render(request, 'login.html',)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('m:index'))

def noaccess(request):
    activation = request.user.student.access_date()
    end_date = activation + Constants.investment_time
    end_date_bool = timezone.localtime(timezone.now())
    if timezone.localtime(timezone.now()) < activation:
        auth.logout(request)
        context = {
            'activation': activation,
            'end_date_bool': end_date_bool,
            'tooSoon': True,
            "Constants": Constants,
        }
        return render(request, "registration/noaccess.html", context)
    else:
        return HttpResponseRedirect(reverse('m:index'))

def theme_selection(request):
    user = request.user
    assent_and_consent = [
        {'title': "Tutor Child Assent", 'q_id': "somestring", 'status': user.student.assent},
        {'title': "Tutor Parent Consent", "q_id": "somesrting", "status": user.student.consent},
    ]

    form = Themes.objects.all()
    error = False
    if request.method == "POST":
        if 'theme' in request.POST:
            user.student.theme_id = request.POST['theme']
            user.student.save()
            return HttpResponseRedirect(reverse('m:dashboard'))
        else:
            error = True

    context = {
        'username': request.user.username,
        'form': form,
        'info': assent_and_consent,
        'error': error,
        "Constants": Constants,
    }
    return render(request, 'mathtutor/theme_selection.html', context)

@login_required
def dashboard(request):
    student = request.user.student
    context = {
        'categories':Constants.categories[student.group],
        "Constants": Constants,
    }
    return render(request, 'mathtutor/dashboard.html', context)

def post_surveys(request):
	pass

def quiz_or_practice(request, category):
    student = request.user.student
    context = {
        'category': [ category, Constants.categories[student.group][category] ],
        'Constants': Constants,
    }
    return render(request, 'mathtutor/quiz_or_practice.html', context)

def list_quizes(request, category):
    student = request.user.student
    quizGroup = QuizGroup.objects.get(group=student.group)
    quizList = quizGroup.quizes_set.filter(q_catagory=category)
    context = {
        'category': [category, Constants.categories[student.group][category]],
        'quizList': quizList,
        "Constants": Constants,
    }
    return render(request, "mathtutor/quiz_list.html", context)

def practice(request, category, which, itemId=None):
    student = request.user.student
    quizGroup = QuizGroup.objects.get(group=student.group)
    learnItems = []
    for subCategory in SubCatagory.objects.all():
        learnItems.append(subCategory.get_list_of_items(quizGroup, category, which))
    context = {
        'category': [category, Constants.categories[student.group][category]],
        'learnItems': learnItems,
        "Constants": Constants,
        }
    if itemId == None:
        return render(request, "mathtutor/practice_list.html", context)
    else:
        context['learnItem'] = LearnItem.objects.get(id=itemId)
        return render(request, "mathtutor/practice_item.html", context)

def glossary(request, itemId=None):
	pass





