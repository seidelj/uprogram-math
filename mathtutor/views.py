from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import auth
from .models import Constants, Quiz, QuizGroup, SubCategory, LearnItem, Theme
from django.utils import timezone
from django.http import HttpResponseRedirect
from mathtutor.decorators import check_category_access

constants = Constants()
# Create your views here.

@login_required(login_url='/login/')
def index(request):
    if request.user.is_authenticated:
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

@login_required
def theme_selection(request):
    user = request.user
    assent_and_consent = [
        {'title': "Tutor Child Assent", 'q_id': "somestring", 'status': user.student.assent},
        {'title': "Tutor Parent Consent", "q_id": "somestring", "status": user.student.consent},
    ]

    form = Theme.objects.all()
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
    updated = request.user.student.set_null_theme()
    student = request.user.student
    categories = Constants.categories[student.group]
    for c in categories:
        c['results']=student.get_overall_progress(c['key'])
    context = {
        'categories': zip(constants.accessBools(student.district), categories),
        "Constants": Constants,
    }
    return render(request, 'mathtutor/dashboard.html', context)

def post_surveys(request):
	pass

@login_required
@check_category_access
def quiz_or_practice(request, category):
    student = request.user.student
    context = {
        'category': filter(lambda c: c['key']==category, Constants.categories[student.group]),
        'Constants': Constants,
    }
    return render(request, 'mathtutor/quiz_or_practice.html', context)

@login_required
@check_category_access
def list_quizes(request, category):
    student = request.user.student
    quizGroup = QuizGroup.objects.get(group=student.group)
    quizListObjects = quizGroup.quiz_set.filter(q_category=category)
    quizList = quizListObjects.values()
    for quizObj in quizListObjects:
        results = quizObj.get_results(request.user)
        name = quizObj.get_display_name()
        quiz = filter(lambda q: q['q_id']==quizObj.q_id, quizList)[0]
        quiz['display_name'] = name
        quiz['results'] = results

    context = {
        'category': filter(lambda c: c['key']==category, Constants.categories[student.group]),
        'quizList': quizList,
        "Constants": Constants,
    }
    return render(request, "mathtutor/quiz_list.html", context)

@login_required
@check_category_access
def practice(request, category, which, itemId=None):
    student = request.user.student
    quizGroup = QuizGroup.objects.get(group=student.group)
    learnItems = []
    for subCategory in SubCategory.objects.all():
        learnItems.append(subCategory.get_list_of_items(quizGroup, category, which))
    context = {
        'category': filter(lambda c: c['key']==category, Constants.categories[student.group]),
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





