# coding=utf-8
import arrow
from django import template
from django.core.urlresolvers import reverse

register = template.Library()


@register.filter
def get_total_subject_posts(subject):
    """
    Returns a count of all the posts associated with a particular thread,
    which in turn is associated with a subject.
    """
    total_posts = 0
    for thread in subject.threads.all():
        total_posts += thread.posts.count()
    return total_posts


@register.filter
def started_time(created_at):
    """
    Reformats created_at using arrow
    e.g., “Five minutes ago”, or ‘Just now’.
    """
    return arrow.get(created_at).humanize()


@register.simple_tag
def last_posted_user_name(thread):
    """
    Last person to post on a thread.
    """
    posts = thread.posts.all().order_by('created_at')
    return posts[posts.count() - 1].user.username


@register.filter
def vote_percentage(subject):
    """
    Return # of votes per subject as a percentage.
    """
    count = subject.votes.count()
    if count == 0:
        return 0
    total_votes = subject.poll.votes.count()
    return (100 / total_votes) * count


@register.simple_tag
def user_vote_button(thread, subject, user):
    """
    Hide the voting buttons from our view if user already voted.
    """
    vote = thread.poll.votes.filter(user_id=user.id).first()

    if not vote:
        if user.is_authenticated():
            link = """
            <div class="col-md-2 btn-vote">
                <a href="%s" class="btn btn-default btn-sm">
                    Add my vote!
                </a>
            </div>
            """ % reverse('cast_vote', kwargs={
                'thread_id': thread.id,
                'subject_id': subject.id
            })

            return link

    return ""
