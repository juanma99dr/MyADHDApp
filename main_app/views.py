from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from main_app.forms import NewUserForm, UpdateUserForm, UpdateProfileForm, PostForm, EventForm
from django.contrib.auth.models import User
from main_app.models import *
from django.views import generic
from django.utils import timezone
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .serializers import UserSerializer, PomodoroSerializer
from rest_framework import generics
from rest_framework.decorators import api_view
from .utils import Calendar
from datetime import datetime
from django.utils.safestring import mark_safe
import calendar

# INDEX VIEW
def index(request):
    pomodoros = Pomodoro.objects.all()
    tags = PomodoroTag.objects.all()
    return render(request, 'index.html',
                  {
                      'pomodoros': pomodoros,
                      'tags': tags,
                  }
                  )


# USER VIEWS

# USER REGISTRATION VIEW
def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
        messages.error(
            request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="register.html", context={"register_form": form})

# PROFILE VIEW
class ProfileDetailView(LoginRequiredMixin, generic.DetailView):
    model = Profile
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orderingByDate = ['-date_posted']
        context["postsByUser"] = Post.objects.filter(
            author=self.object).order_by(*orderingByDate)[:8]
        return context

# PROFILE UPDATE VIEW
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['profilePic', 'bio']
    template_name = 'profile_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.object.user.id})


# POMODORO VIEWS

# POMODORO CREATE VIEW
class PomodoroCreateView(CreateView):
    model = Pomodoro
    fields = ['name', 'description', 'duration', 'tag']
    template_name = 'pomodoro.html'
    success_url = reverse_lazy("pomodoro")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['numTag'] = PomodoroTag.objects.all()
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# POMODORO TAG VIEWS

# POMODORO TAG CREATE VIEW
class PomodoroTagCreateView(CreateView, LoginRequiredMixin):
    model = PomodoroTag
    fields = ['name']
    template_name = 'pomodoro_tag_form.html'
    success_url = reverse_lazy("pomodoro")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pageTitle"] = "Create Tag"
        return context

# POMODORO TAG UPDATE VIEW
class PomodoroTagUpdateView(UpdateView, LoginRequiredMixin):
    model = PomodoroTag
    fields = ['name']
    template_name = 'pomodoro_tag_form.html'
    success_url = reverse_lazy("pomodoro")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pageTitle"] = "Update Tag"
        return context

# POMODORO TAG DELETE VIEW

class PomodoroTagDeleteView(DeleteView, LoginRequiredMixin):
    model = PomodoroTag
    template_name = 'pomodoro_tag_confirm_delete.html'
    success_url = reverse_lazy("pomodoro")


# EVENT VIEWS

# CALENDAR VIEW
class CalendarView(generic.ListView, LoginRequiredMixin):
    model = Event
    template_name = 'cal/calendar.html'

    def get_context_data(self, **kwargs):
        # use today's date for the calendar
        d = get_date(self.request.GET.get('day', None))

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month, self.request.user)

        context = super().get_context_data(**kwargs)

        # Call the formatmonth method, which returns our calendar as a table
        if self.request.user.is_authenticated:
            html_cal = cal.formatmonth(withyear=True)
            context['calendar'] = mark_safe(html_cal)
            context['prev_month'] = prev_month(d)
            context['next_month'] = next_month(d)   

        return context

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()
    
    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('calendar'))
    return render(request, 'cal/event.html', {'form': form})


# TASK VIEWS

# TASK CREATE VIEW
class TaskCreateView(CreateView, LoginRequiredMixin):
    model = Task
    fields = ['title', 'content', 'tag']
    template_name = 'task.html'
    success_url = reverse_lazy("task")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # filter by user and by status
        if self.request.user.is_authenticated:
            context['tasks'] = Task.objects.filter(
                user=self.request.user, status=False)
            context['completedTasks'] = Task.objects.all().filter(
                user=self.request.user, status=True)
        context['tags'] = TaskTag.objects.all().filter()
        context["pageTitle"] = "Create Task"
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# TASK UPDATE VIEW
class TaskUpdateView(UpdateView, LoginRequiredMixin):
    model = Task
    fields = ['title', 'content', 'tag']
    template_name = 'task.html'
    success_url = reverse_lazy("task")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.filter(
            user=self.request.user, status=False)
        context['completedTasks'] = Task.objects.all().filter(
            user=self.request.user, status=True)
        context['tags'] = TaskTag.objects.all().filter()
        context["pageTitle"] = "Update Task"
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# TASK DELETE VIEW
class TaskDeleteView(DeleteView, LoginRequiredMixin):
    model = Task
    template_name = 'task_confirm_delete.html'
    success_url = reverse_lazy("task")


# TASK TAG VIEWS

# TASK TAG CREATE VIEW
class TaskTagCreateView(CreateView, LoginRequiredMixin):
    model = TaskTag
    fields = ['name']
    template_name = 'task_tag_form.html'
    success_url = reverse_lazy("task")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pageTitle"] = "Create Tag"
        return context

# TASK TAG UPDATE VIEW
class TaskTagUpdateView(UpdateView, LoginRequiredMixin):
    model = TaskTag
    fields = ['name']
    template_name = 'task_tag_form.html'
    success_url = reverse_lazy("task")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pageTitle"] = "Update Tag"
        return context
    
# TASK TAG DELETE VIEW
class TaskTagDeleteView(DeleteView, LoginRequiredMixin):
    model = TaskTag
    template_name = 'task_tag_confirm_delete.html'
    success_url = reverse_lazy("task")



# FORUM VIEWS (POSTS AND COMMENTS)

# LIST VIEW
class PostListView(generic.ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'post_list.html'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get("query")
        orderingByDate = ['-date_posted']
        if query:
            # only five posts are shown
            object_list = self.model.objects.filter(
                title__icontains=query).order_by(*orderingByDate)
        else:
            object_list = self.model.objects.all().order_by(*orderingByDate)
        return object_list

    def get_context_data(self, **kwargs):
        orderingByVisits = ['-visits']
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        context["users"] = Profile.objects.all().count()
        context["postNum"] = Post.objects.all().count()
        context["tags"] = ForumTag.objects.all()
        context["postByVisits"] = self.model.objects.order_by(
            *orderingByVisits)[:5]
        return context

# DETAIL VIEW
class PostDetailView(generic.DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'post_detail.html'
    # each time a post is viewed, the view count is incremented

    def get(self, request, *args, **kwargs):
        orderingByVisits = ['-visits']
        self.object = self.get_object()
        self.object.visits += 1
        self.object.save()
        context = self.get_context_data(object=self.object)
        # comments
        context['comments'] = Comment.objects.filter(post=self.object)
        context["now"] = timezone.now()
        context["users"] = User.objects.all().count()
        context["postNum"] = Post.objects.all().count()
        profile = self.object.author
        context["profilePic"] = profile.profilePic
        # relatedPosts filter by tags and exclude the current post
        context["relatedPosts"] = Post.objects.filter(tag=self.object.tag).exclude(
            post_id=self.object.post_id).order_by(*orderingByVisits)[:5]
        return self.render_to_response(context)

# CREATE VIEW
class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    fields = ['title', 'image', 'content', 'tag','commentable']
    template_name = 'post_form.html'
    success_url = reverse_lazy("forum")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["numTag"] = ForumTag.objects.all()
        context["pageTitle"] = "Create Post"
        return context

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        form.instance.author = profile
        return super().form_valid(form)


# UPDATE VIEW
class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Post
    fields = ['title', 'image', 'content', 'tag','commentable']
    template_name = 'post_form.html'
    # get the post data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["numTag"] = ForumTag.objects.all()
        context["pageTitle"] = "Update Post"
        return context

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        form.instance.author = profile
        form.instance.edited = True
        return super().form_valid(form)

# DELETE VIEW
class PostDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Post
    success_url = reverse_lazy("forum")
    template_name = 'post_confirm_delete.html'


# COMMENT VIEWS

# CREATE VIEW
class CommentCreateView(LoginRequiredMixin, generic.CreateView):
    model = Comment
    fields = ['content', 'image']
    template_name = 'comment_form.html'
    # go to the post detail page after creating a comment

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.post_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pageTitle"] = "Create Comment"
        return context

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        form.instance.user = profile
        postSel = Post.objects.get(post_id=self.kwargs['post_id'])
        if postSel.commentable == False:
            return HttpResponseForbidden()
        form.instance.post = postSel
        return super().form_valid(form)

# UPDATE VIEW
class CommentUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Comment
    fields = ['content', 'image']
    template_name = 'comment_form.html'

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.post_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pageTitle"] = "Update Comment"
        return context

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        form.instance.user = profile
        form.instance.edited = True
        return super().form_valid(form)


# DELETE VIEW
class CommentDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Comment
    template_name = 'comment_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.post_id})


# FORUM TAG VIEWS

# CREATE VIEW
class ForumTagCreateView(LoginRequiredMixin, generic.CreateView):
    model = ForumTag
    fields = ['name']
    template_name = 'forum_tag_form.html'
    success_url = reverse_lazy("forum")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pageTitle"] = "Create Tag"
        return context

# UPDATE VIEW
class ForumTagUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = ForumTag
    fields = ['name']
    template_name = 'forum_tag_form.html'
    success_url = reverse_lazy("forum")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pageTitle"] = "Update Tag"
        return context

# DELETE VIEW
class ForumTagDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = ForumTag
    success_url = reverse_lazy("forum")
    template_name = 'forum_tag_confirm_delete.html'


# API VIEWS

# REST FRAMEWORK
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'pomodoros': reverse('AllPomodoros', request=request, format=format),
        'users': reverse('AllUsers', request=request, format=format)
    })

# ALL USERS
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# ALL POMODOROS
class PomodoroList(generics.ListAPIView):
    queryset = Pomodoro.objects.all()
    serializer_class = PomodoroSerializer
