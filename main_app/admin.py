from django.contrib import admin
from .models import Pomodoro, PomodoroTag, Post, Comment, ForumTag, Task, TaskTag, Event, User, Profile

# ------ COMMON SECTION -------

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio', ]
    fields = ['user', 'bio', ("profilePic","image_tag"), ]
    readonly_fields = ['image_tag']

# ------ POMODORO SECTION ------

@admin.register(Pomodoro)
class PomodoroAdmin(admin.ModelAdmin):
    list_display = ('name', 'description','duration',
                    'user', "tag", 'pomodoro_id',)
    ordering = ('name',)
    list_filter = ('user', 'tag')
    fields = ['name', 'user', 'description', 'duration', 'tag']


@admin.register(PomodoroTag)
class PomodoroTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'tag_id')
    fields = ['name']


# ------ FORUM SECTION ------

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_posted', 'edited',
                    'visits', 'tag', 'post_id',)
    ordering = ('title',)
    list_filter = ('author', 'tag')
    fields = [('title', 'author', 'content'), ("image","image_tag"), ('date_posted'),
            'visits', 'tag','edited']
    readonly_fields = ['image_tag']
    inlines = [CommentInline]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'date_posted',
                    'edited', 'content', 'comment_id',)
    ordering = ('user',)
    list_filter = ('user', 'post')
    fields = ['user', 'post', ('date_posted'), 'content', ("image","image_tag"),'edited']
    readonly_fields = ['image_tag', 'post']


@admin.register(ForumTag)
class ForumTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'tag_id')
    fields = ['name']
    
    
# ------ TASKS SECTION ------

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'user', "tag", 'task_id',"status")
    ordering = ('title',)
    list_filter = ('user', 'tag')
    fields = ['title', 'user', 'content', 'tag',"status"]


@admin.register(TaskTag)
class TaskTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'tag_id')
    fields = ['name']

# ------ EVENTS SECTION ------

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'user', 'event_id')
    ordering = ('title',)
    list_filter = ('user',)
    fields = ['title', 'user', 'content',('start_time','end_time')]