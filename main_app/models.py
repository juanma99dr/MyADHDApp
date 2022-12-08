from django.db import models
from django.urls import reverse
from datetime import *
from django.utils.html import mark_safe
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator


# ------ COMMONS SECTION ------

# Model for the user profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profilePic = models.ImageField(upload_to='profile-pictures',blank=True, null=True, default="default.jpg")
    bio = models.TextField(max_length=500, blank=True)
    
    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.profilePic.url))
    image_tag.short_description = 'Profile Picture'
    
    def __str__(self):
        return f'{self.user.username} Profile'
    
    def get_bio(self):
        return self.bio 
    
    def get_absolute_url(self):
        return reverse('profile', args=[str(self.id)])
    

# ------ POMDORO SECTION ------

# Model for Pomodoro tag
class PomodoroTag(models.Model):
    tag_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular tag")
    name = models.CharField(
        max_length=200, help_text='Enter a tag (e.g. Work, School, etc.)')

    def __str__(self):
        return self.name


# Model for pomodoro
class Pomodoro(models.Model):
    """Model representing a pomodoro."""
    pomodoro_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular pomodoro")
    name = models.CharField(
        max_length=200, help_text='Enter a pomodoro name', default='Pomodoro')
    user = models.ForeignKey(
        User, related_name='pomodoros', on_delete=models.CASCADE, null=True, blank=True)
    duration = models.PositiveIntegerField(
        help_text='Enter the duration of the pomodoro in minutes', default=25, validators=[MinValueValidator(1), MaxValueValidator(60)])
    description = models.CharField(
        max_length=200, help_text="Enter a description of the pomodoro", null= True, blank=True) 
    tag = models.ForeignKey(PomodoroTag, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        """String for representing the Model object."""
        return f'{self.pomodoro_id} ({self.user})'

    def get_absolute_url(self):
        """Returns the url to access a particular pomodoro instance."""
        return reverse('pomodoro-detail', args=[str(self.pomodoro_id)])

    def get_duration(self):
        """Returns the duration of the pomodoro in minutes."""
        return self.duration

    def get_start_time(self):
        """Returns the start time of the pomodoro."""
        return self.start_time

    def get_end_time(self):
        """Returns the end time of the pomodoro."""
        return self.end_time

    def get_description(self):
        """Returns the description of the pomodoro."""
        return self.description

    def get_user(self):
        """Returns the user who created the pomodoro."""
        return self.user

    def get_id(self):
        """Returns the id of the pomodoro."""
        return self.pomodoro_id

    def get_name(self):
        """Returns the name of the pomodoro."""
        return self.name

    def get_tags(self):
        """Returns the tags of the pomodoro."""
        return self.tags

# ------ FORUM SECTION ------

# Model for Forum tag
class ForumTag(models.Model):
    tag_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular tag")
    name = models.CharField(
        max_length=200, help_text='Enter a tag (e.g. Work, School, etc.)')

    def __str__(self):
        return self.name

# Model for post
class Post(models.Model):
    """Model representing a post."""
    post_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular post")
    title = models.CharField(max_length=100, help_text='Enter a post title')
    author = models.ForeignKey(
        Profile, related_name='posts', on_delete=models.CASCADE, null=True, blank=True)
    date_posted = models.DateTimeField(
        default=datetime.now, help_text="Enter the date and time the post was posted")
    edited = models.BooleanField(default=False)
    content = models.TextField(
        max_length=5000, help_text="Enter the content of the post")
    image = models.ImageField(upload_to='post-images', blank=True, null=True)
    visits = models.PositiveIntegerField(default=0,)
    tag = models.ForeignKey(ForumTag, on_delete=models.SET_NULL, null=True, blank=True, help_text="Select a tag for this post")
    commentable = models.BooleanField(default=True, help_text="Check if you want to allow comments on this post") 
    class Meta:
        permissions = (("is_admin", "Can do admin things"),)

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def image_tagView(self):
        return mark_safe('<img id="post-image" alt="post image" src="%s" />' % (self.image.url))


    image_tag.short_description = 'Image'
    
    def display_tags(self):
        """Create a string for the Tag. This is required to display tags in Admin."""
        return ', '.join(tag.name for tag in self.tags.all()[:3])
    display_tags.short_description = 'Tags'

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.post_id} ({self.author})'

    def get_absolute_url(self):
        """Returns the url to access a particular post instance."""
        return reverse('post-detail', args=[str(self.post_id)])

    def get_title(self):
        """Returns the title of the post."""
        return self.title

    def get_date_posted(self):
        """Returns the date and time the post was posted."""
        return self.date_posted

    def get_updated(self):
        """Returns the date and time the post was last updated."""
        return self.updated

    def get_content(self):
        """Returns the content of the post."""
        return self.content

    def get_image(self):
        """Returns the image of the post."""
        return self.image

    def get_upvotes(self):
        """Returns the number of upvotes the post has."""
        return self.upvotes

    def get_downvotes(self):
        """Returns the number of downvotes the post has."""
        return self.downvotes

    def get_visits(self):
        """Returns the number of times the post has been visited."""
        return self.visits

    def get_tag(self):
        """Returns the tags of the post."""
        return self.tag

    def get_comments(self):
        """Returns the comments of the post."""
        return self.comments

    def get_author(self):
        """Returns the user who created the post."""
        return self.author

    def get_id(self):
        """Returns the id of the post."""
        return self.post_id


# Model for comment
class Comment(models.Model):
    """Model representing a comment."""
    comment_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular comment")
    user = models.ForeignKey(
        Profile, related_name='comments', on_delete=models.CASCADE, null=True, blank=True)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, null=True, blank=True)
    date_posted = models.DateTimeField(
        default=datetime.now, help_text="Enter the date and time the comment was posted")
    edited = models.BooleanField(default=False)
    content = models.TextField(
        max_length=1000, help_text="Enter the content of the comment")
    image = models.ImageField(upload_to="comment-images", null=True, blank=True)
    
    def display_post(self):
        return self.post.title

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def image_tagView(self):
        return mark_safe('<img id="post-image" alt="post image" src="%s" />' % (self.image.url))
    
    def image_tagViewComment(self):
        return mark_safe('<img id="post-image-comment" alt="post image" src="%s" />' % (self.image.url))

    image_tag.short_description = 'Image'
    
    def __str__(self):
        """String for representing the Model object."""
        return f'{self.comment_id} ({self.user})'

    def get_absolute_url(self):
        """Returns the url to access a particular comment instance."""
        return reverse('comment-detail', args=[str(self.comment_id)])

    def get_date_posted(self):
        """Returns the date and time the comment was posted."""
        return self.date_posted

    def get_updated(self):
        """Returns the date and time the comment was last updated."""
        return self.updated

    def get_content(self):
        """Returns the content of the comment."""
        return self.content

    def get_image(self):
        """Returns the image of the comment."""
        return self.image

    def get_upvotes(self):
        """Returns the number of upvotes the comment has."""
        return self.upvotes

    def get_downvotes(self):
        """Returns the number of downvotes the comment has."""
        return self.downvotes

    def get_replies(self):
        """Returns the replies to the comment."""
        return self.replies

    def get_user(self):
        """Returns the user who created the comment."""
        return self.user

    def get_id(self):
        """Returns the id of the comment."""
        return self.comment_id

    def get_post(self):
        """Returns the post the comment is on."""
        return self.post



# ------ TASKS SECTION ------

# Model Task Tag
class TaskTag(models.Model):
    tag_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=50, help_text="Enter a tag (e.g. Python, Django, etc.)")

    def __str__(self):
        return self.name

# Model for Task
class Task(models.Model):
    task_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular task")
    title = models.CharField(max_length=100)
    content = models.TextField()
    status = models.BooleanField(default=False)
    user = models.ForeignKey(
        User, related_name='tasks', on_delete=models.SET_NULL, null=True, blank=True)
    tag = models.ForeignKey(TaskTag, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_description(self):
        return self.description

    def get_user(self):
        """Returns the user who created the event."""
        return self.user

# Model for Event
class Event(models.Model):
    event_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular event")
    title = models.CharField(help_text="Enter the title of the event", max_length=100)
    content = models.TextField(help_text="Enter the description of the event", max_length=1000, null=True, blank=True)  
    start_time = models.DateTimeField(help_text="Enter the start time of the event")
    user = models.ForeignKey(
        User, related_name='events', on_delete=models.CASCADE, null=True, blank=True)
    @property
    def get_html_url(self):
        url = reverse('event_edit', args=(self.event_id,))
        return f'<a href="{url}"> {self.title} </a>'
            
    def __str__(self):
        return self.title

    def get_content(self):
        return self.content

    def get_user(self):
        """Returns the user who created the event."""
        return self.user

    def get_date(self):
        """Returns the date of the event."""
        return self.date

    def get_time(self):
        """Returns the time of the event."""
        return self.time