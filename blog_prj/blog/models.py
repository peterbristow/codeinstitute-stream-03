from django.db import models
from django.utils import timezone


class Post(models.Model):
    """
    Here we'll define our Post model
    """
    # author is linked to a registered
    # user in the 'auth_user' table.
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)  # identify when post created
    published_date = models.DateTimeField(blank=True, null=True)  # set date to blank and null
    views = models.IntegerField(default=0)  # record how often a post is seen
    tag = models.CharField(max_length=30, blank=True, null=True)
    image = models.ImageField(upload_to="images", blank=True, null=True)  # upload_to specifies subdirectory name

    def publish(self):
        """
        used to publish a blog entry and update db
        """
        self.published_date = timezone.now()
        self.save()

    def __unicode__(self):
        """
        use title to identify each blog entry in the admin
        """
        return self.title
