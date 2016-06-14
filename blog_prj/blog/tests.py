from django.test import TestCase
from .models import Post


class PostTests(TestCase):
    """
    run tests against the Post Model
    """

    def test_str(self):
        test_title = Post(title='My latest blog post')
        self.assertEquals(str(test_title), 'My latest blog post')
