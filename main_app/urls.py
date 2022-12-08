from django.urls import re_path, path, include
from django.views.generic import RedirectView
from rest_framework.urlpatterns import format_suffix_patterns
from main_app import views

# Common urls
urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path("register", views.register_request, name="register"),
    re_path(r'^profile/(?P<pk>\d+)/$',
            views.ProfileDetailView.as_view(), name='profile'),
    re_path(r'^profile/update/(?P<pk>\d+)/$',
            views.ProfileUpdateView.as_view(), name='profile-update'),
    re_path(r'^profiles/$', views.ProfileListView.as_view(), name='profiles'),
]

# Forum urls
urlpatterns += [
    re_path(r'^forum/$', views.PostListView.as_view(), name='forum'),
    re_path(r'^post/(?P<pk>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$',
            views.PostDetailView.as_view(), name='post-detail'),
    re_path(r'^post/create/$', views.PostCreateView.as_view(), name='post-create'),
    re_path(r'^post/(?P<pk>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/update/$',
            views.PostUpdateView.as_view(), name='post-update'),
    re_path(r'^post/(?P<pk>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/delete/$',
            views.PostDeleteView.as_view(), name='post-delete'),
    re_path(r'^comment/create/(?P<post_id>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$',
            views.CommentCreateView.as_view(), name='comment-create'),
    re_path(r'^comment/(?P<pk>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/update/$',
            views.CommentUpdateView.as_view(), name='comment-update'),
    re_path(r'^comment/(?P<pk>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/delete/$',
            views.CommentDeleteView.as_view(), name='comment-delete'),
    re_path(r'^forum-tag/create/$', views.ForumTagCreateView.as_view(),
            name='forum-tag-create'),
    re_path(r'^forum-tag/(?P<pk>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/update/$',
            views.ForumTagUpdateView.as_view(), name='forum-tag-update'),
    re_path(r'^forum-tag/(?P<pk>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/delete/$',
            views.ForumTagDeleteView.as_view(), name='forum-tag-delete'),
]

# Pomodoro urls
urlpatterns += [
    re_path(r'^pomodoro/$', views.PomodoroCreateView.as_view(), name='pomodoro'),
    re_path(r'^pomodoro-tag/(?P<pk>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/update/$',
            views.PomodoroTagUpdateView.as_view(), name='pomodoro-tag-update'),
    re_path(r'^pomodoro-tag/(?P<pk>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/delete/$',
            views.PomodoroTagDeleteView.as_view(), name='pomodoro-tag-delete'),
    re_path(r'^pomodoro-tag/create/$',
            views.PomodoroTagCreateView.as_view(), name='pomodoro-tag-create'),

]

# calendar urls
urlpatterns += [
    re_path(r'^calendar/$', views.CalendarView.as_view(), name='calendar'),
    re_path(r'^event/new/$', views.event, name='event_new'),
    re_path(r'^event/edit/(?P<event_id>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$', views.event, name='event_edit'),

]

# Task urls
urlpatterns += [
    re_path(r'^task/$', views.TaskCreateView.as_view(), name='task'),
    re_path(r'^task/(?P<pk>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/update/$',
            views.TaskUpdateView.as_view(), name='task-update'),
    re_path(r'^task/(?P<pk>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/delete/$',
            views.TaskDeleteView.as_view(), name='task-delete'),
    re_path(r'^task-tag/create/$', views.TaskTagCreateView.as_view(),
            name='task-tag-create'),
    re_path(r'^task-tag/(?P<pk>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/update/$',
            views.TaskTagUpdateView.as_view(), name='task-tag-update'),
    re_path(r'^task-tag/(?P<pk>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/delete/$',
            views.TaskTagDeleteView.as_view(), name='task-tag-delete'),
]

# API
urlpatterns += [
    re_path('users/', views.UserList.as_view(), name='AllUsers'),
    re_path('pomodoros/', views.PomodoroList.as_view(), name='AllPomodoros'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
