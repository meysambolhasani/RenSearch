from email.mime import image
from django.db import models
from django.contrib import messages
from users.models import Profile
# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    owner = models.ForeignKey(
        Profile, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(
        null=True, blank=True, default='default.jpg')
    tags = models.ManyToManyField(Tag, blank=True)
    project_address = models.CharField(max_length=2000, null=True, blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    images_link = models.CharField(max_length=2000, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    #  ordering list projects on page base on date that those created
    # minus (- created) is  for descending order
    # class Meta:
    #     ordering = ['-created']
    class Meta:
        ordering = ['-vote_ratio', '-vote_total', 'title']

    def __str__(self):
        return self.title

    @property
    def imageURL(self):
        try:
            url = self.featured_image.url
        except:
            url=''
        return url    

    @property
    def reviewers(self):
        # Get list of profiles id that commented on project
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset

    @property
    def get_vote_count(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()

        ratio = (upVotes/totalVotes)*100
        self.vote_total = totalVotes
        self.vote_ratio = ratio
        self.save()


class Review(models.Model):

    VOTE_TYPE = [
        ('up', 'Up Vote'),
        ('down', 'Down Vote')
    ]
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=100, null=True,
                             blank=True, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['owner', 'project']]

    def __str__(self):
        return self.value
