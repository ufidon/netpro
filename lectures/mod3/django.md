# [Django tutorial](https://docs.djangoproject.com/)

Part 1: create a project and an app
---
- Install and test Django
  ```bash
  # install Django
  python3 -m pip install Django
  
  # verify installation
  python3 -m django --version
  ```
- Create a project
  ```bash
  # create a project
  django-admin startproject mysite

  # view files created
  cd mysite && tree .

  # test the project
  # python3 manage.py runserver ip:port
  python3 manage.py runserver

  # create the app
  python manage.py startapp polls
  # view files created
  tree polls
  ```
- Write your first view
  ```python
  # polls/views.py
  from django.http import HttpResponse

  def index(request):
    return HttpResponse("Here is the polls index.")
  ```
- Map the view to a URL with a URLconf
  - create polls/urls.py
    ```python
    # polls/urls.py
    from django.urls import path
    from . import views

    urlpatterns = [ path("", views.index, name="index"), ]
    ```
  - point the root URLconf at the polls.urls module
    ```bash
    # mysite/urls.py
    from django.contrib import admin
    from django.urls import include, path

    urlpatterns = [
      path("polls/", include("polls.urls")),
      path("admin/", admin.site.urls)
    ]
    ```

Part 2: setup database and create models
---
- setup databases, time zone and installed apps in mysite/settings.py
  - create a database if the DBMS is not sqlite3
- create tables in the database for the installed apps
  ```bash
  python3 manage.py migrate
  ```
- create models: database tables represented by Python classes
  - object-relational mapper (ORM) helps Django
    - create database schemas from the models
    - create a Python database-access API for accessing objects of models
  ```python
  # polls/models.py
  from django.db import models

  class Questions(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

  class Choice(models.Model):
    # relationship
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
  ```
- plug the polls app into the project
  ```python
  # mysite/settings.py
  INSTALLED_APPS=[
    "polls.apps.PollsConfig",
    # ...
  ]
  ```
- Create migrations for changes to the models
  - changes are stored as migrations
    - can be tweaked manually
  ```bash
  python3 manage.py makemigrations polls
  ```
- View migrations (SQL statements to be executed)
  ```bash
  python3 manage.py sqlmigrate polls 0001

  # check problems
  python3 manage.py check
  ```
- Commit migrations (execute SQL statements to apply changes)
  - the applications of migrations are tracked in the database django_migrations
  - synchronize models with schemas
  - upgrade database lively without losing data
  ```bash
  python3 manage.py migrate
  ```

Playing with the API
---
- Invoke an interactive Python shell configured with Django API
  ```bash
  # set up the DJANGO_SETTINGS_MODULE  environment variable
  python3 manage.py shell
  ```
- Explore database API
  ```python
  from polls.models import Choice, Question

  Question.objects.all() # show all records

  from django.utils import timezone
  # create a record and save it to the database
  q = Question(question_text="Do you support Trump?", pub_date=timezone.now())
  q.save()

  # the properties of attributes can be updated
  q.question_text = 'Do you support Biden?'
  q.save()
  ```
- add \_\_str\_\_() methods to models
  - give human-readable info in the interactive shell
  - used throughout Django’s automatically-generated admin
  ```python
  # polls/models.py
  # ...
  class Question(models.Model):
    # ...
    def __str__(self):
      return self.question_text
    # add a new method
    def was_published_recently(self):
      return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

  # ...
  class Choice(models.Model):
    # ...
    def __str__(self):
      return self.choice_text
  # ...
  ```
- interact with the models again
  ```python
  # view all records
  Question.objects.all()

  # view specified records
  Question.objects.filter(id=1)
  Question.objects.filter(question_text__startswith="What")
  Question.objects.get(id=2) # exception raised for nonexistent records
  q = Question.objects.get(pk=1) # lookup by primary key
  q.was_published_recently()

  # create choices for a question
  q.choice_set.all()
  q.choice_set.create(choice_text="Yes", votes=0)
  q.choice_set.create(choice_text="No", votes=0)

  c = q.choice_set.create(choice_text="Unsure", votes=0)
  c.question

  q.choice_set.all()
  q.choice_set.count()

  # Use double underscores to separate relationships
  Choice.objects.filter(question__pub_date__year=current_year)
  c = q.choice_set.filter(choice_text__startswith="Y")
  c.delete()
  ```


Introducing the Django Admin
---
- creation of admin interfaces for models is entirely automated
- content publishers and public site are clearly separated
- create an admin user
  ```bash
  # follow the prompts to complete the creation
  # supply username, email and password
  python3 manage.py createsuperuser
  ```
- login the admin web interface as the superuser created
  - http://127.0.0.1:8000/admin/
    - the editable content is provided by django.contrib.auth
- Make the poll app modifiable in the admin
  - to enable adding questions easily
  ```python
  # polls/admin.py
  from django.contrib import admin
  form .models import Question
  
  admin.site.register(Question)
  ```
  - explore the admin functionality


Part 3: create views
---
- A view is a “type” of web page that 
  - serves a specific function 
  - has a specific template
  - returns a HttpResponse object or raises an exception such as Http404
  - represented by a Python function 
    - or method in the case of class-based views
  - used to handle a URL relative to the site
    - URLconf maps URL patterns to views
- views in the poll app

| view | function |
| --- | --- |
| Question index | shows the latest few questions |
| Question detail | displays a question text, with no results but with a form to vote |
| Question results | displays results for a particular question |
| Vote action | handles voting for a particular choice in a particular question |

- Add more views to polls/views.py
  ```python
  # polls/views.py
  def detail(request, question_id):
    return HttpResponse("You are looking at question %s." % question_id)

  def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

  def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
  ```
- Wire the views into polls.urls
  ```python
  # polls/urls.py
  from django.urls import path
  from . import views

  urlpatterns = [
    # ex: /polls/
    path("", views.index, name="index"),
    # ex: /polls/5/
    path("<int:question_id>/", views.detail, name="detail"),
    # ex: /polls/5/results/
    path("<int:question_id>/results/", views.results, name="results")
    # ex: /polls/5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),
  ]
  ```
- Write views that actually do something
  - displays the latest 5 poll questions in the index() view
  ```python
  # polls/views.py
  from django.http import HttpResponse
  from .models import Question

  def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    output = ", ".join([q.question_text for q in latest_question_list])
    return HttpResponse(output)
  # ...
  ```
- Separate page appearance from views code using templates
  - create directory polls/templates
    - because DjangoTemplates looks for a “templates” subdirectory in each of the INSTALLED_APPS
  - create a template polls/templates/polls/index.html
    ```html
    <!-- polls/templates/polls/index.html -->
    <!-- ... -->
    {% if latest_question_list %}
      <ul>
      {% for question in latest_question_list %}
          <li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
      {% endfor %}
      </ul>
    {% else %}
        <p>No polls are available.</p>
    {% endif %}
    <!-- ... -->
    ```
  - update our index view in polls/views.py to use the template
    ```python
    # polls/views.py
    from django.http import HttpResponse
    from django.template import loader
    from .models import Question

    def index(request):
      latest_question_list = Question.objects.order_by("-pub_date")[:5]
      template = loader.get_template("polls/index.html")
      context = { 
        # a dictionary mapping template variable names to Python objects
        "latest_question_list": latest_question_list,
        }
      return HttpResponse(template.render(context, request))
    ```
  - A shortcut: render()
    ```python
    # polls/views.py
    from django.shortcuts import render
    from .models import Question
    def index(request):
      latest_question_list = Question.objects.order_by("-pub_date")[:5]
      context = { 
        # a dictionary mapping template variable names to Python objects
        "latest_question_list": latest_question_list,
        }
      return render(request, "polls/index.html", context)    
    ```
- Raising a 404 error
  - detail
    ```python
    # polls/views.py
    from django.http import Http404
    from django.shortcuts import render
    from .models import Question

    # ...
    def detail(request, question_id):
      try:
        question = Question.objects.get(pk=question_id)
      except Question.DoesNotExist:
        raise Http404("Question does not exist")
      return render(request, "polls/detail.html", {"question": question})
    ```
  - a short template
    ```html
    <!-- polls/templates/polls/detail.html -->
    {{ question }}
    ```
  - A shortcut: get_object_or_404()
    ```python
    from django.shortcuts import get_object_or_404, render
    from .models import Question

    # ...
    def detail(request, question_id):
      question = get_object_or_404(Question, pk=question_id)
      return render(request, "polls/detail.html", {"question": question})    
    ```
- Use the template system
  ```html
  <!-- polls/templated/polls/detail.html -->
  <h1>{{ question.question_text }}</h1>
  <ul>
  {% for choice in question.choice_set.all %}
      <li>{{ choice.choice_text }}</li>
  {% endfor %}
  </ul>  
  ```
- Removing hardcoded URLs in templates with url names
  ```html
  <!-- polls/templates/polls/index.html -->
  <!-- partially hardcoded template --> 
  <li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>

  <!-- use url name to remove the ard code -->
  <li><a href="{% url 'detail' question.id %}">{{ question.question_text }}</a></li>
  ```
- Namespacing URL names with *app_name*
  ```python
  from django.urls import path
  from . import views

  app_name = "polls" # impose a namespace
  urlpatterns = [
      path("", views.index, name="index"),
      path("<int:question_id>/", views.detail, name="detail"),
      path("<int:question_id>/results/", views.results, name="results"),
      path("<int:question_id>/vote/", views.vote, name="vote"),
  ]
  ```
  - namespaced detail view
    ```html
    <!-- polls/templates/polls/index.html -->
    <li><a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a></li>
    ```

Part 4: Forms and generic views
---
- Write a minimal form in poll detail template
  ```html
  <!-- polls/templates/polls/detail.html -->
  <form action="{% url 'polls:vote' question.id %}" method="post">
  {% csrf_token %}
  <fieldset>
      <legend><h1>{{ question.question_text }}</h1></legend>
      {% if error_message %}<p><strong>{{ error_message }}</strong></p>{% endif %}
      {% for choice in question.choice_set.all %}
          <input type="radio" name="choice" id="choice{{ forloop.counter }}" value="{{ choice.id }}">
          <label for="choice{{ forloop.counter }}">{{ choice.choice_text }}</label><br>
      {% endfor %}
  </fieldset>
  <input type="submit" value="Vote">
  </form>  
  ```
- Implement the view *vote*
  ```python
  # polls/views.py
  from django.http import HttpResponse, HttpResponseRedirect
  from django.shortcuts import get_object_or_404, render
  from django.urls import reverse

  from .models import Choice, Question

  # ...
  def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
      selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
      # Redisplay the question voting form.
      return render(
        request,
        "polls/detail.html",
        {
          "question": question,
          "error_message": "You didn't select a choice.",
        },
      )
    else:
      selected_choice.votes += 1
      selected_choice.save()
      # Always return an HttpResponseRedirect after successfully dealing
      # with POST data. This prevents data from being posted twice if a
      # user hits the Back button.
      return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

  def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})
  ```
- create a polls/results.html template
  ```html
  <!-- polls/templates/polls/results.html -->
  <h1>{{ question.question_text }}</h1>

  <ul>
  {% for choice in question.choice_set.all %}
    <li>{{ choice.choice_text }} -- {{ choice.votes }} vote{{ choice.votes|pluralize }}</li>
  {% endfor %}
  </ul>

  <a href="{% url 'polls:detail' question.id %}">Vote again?</a>
  ```
Use generic views: Less code is better
---
- Examples
  - ListView: display a list of objects
  - DetailView: display a detail page for a particular type of object
- Amend URLconf
  ```python
  # polls/urls.py
  from django.urls import path
  from . import views

  app_name = "polls"
  urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
  ]
  ```
- Amend views
  - remove old index, detail, and results views
  - use Django’s generic views
```python
# polls/views.py
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Choice, Question

class IndexView(generic.ListView):
  template_name = "polls/index.html"
  context_object_name = "latest_question_list"

  def get_queryset(self):
    """Return the last five published questions."""
    return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
  model = Question
  template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
  model = Question
  template_name = "polls/results.html"

# ...
```


Part 5: automated testing
---


Part 6: manage static files
---


Part 7: customize the admin form
---


Part 8: integrate third-party packages
---
