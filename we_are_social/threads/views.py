from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.template.context_processors import csrf
from django.forms import formset_factory

from forms import ThreadForm, PostForm
from threads.models import Subject, Posts, Thread
from polls.models import PollSubject
from polls.forms import PollSubjectForm, PollForm


def forum(request):
    return render(request, 'forum/forum.html', {'subjects': Subject.objects.all()})


def threads(request, subject_id):
    """
    Maps to the thread url.
    """
    subject = get_object_or_404(Subject, pk=subject_id)
    return render(request, 'forum/threads.html', {'subject': subject})


@login_required
def new_thread(request, subject_id):
    """
    Allows logged in users to create a new thread and post at the same time.
    Also, gives the option of creating a poll when creating a new thread.
    """
    subject = get_object_or_404(Subject, pk=subject_id)
    poll_subject_formset = formset_factory(PollSubjectForm, extra=3)  # makes a set of 3 forms in this case.

    if request.method == "POST":
        thread_form = ThreadForm(request.POST)
        post_form = PostForm(request.POST)
        poll_form = PollForm(request.POST)
        poll_subject_formset = poll_subject_formset(request.POST)

        # When calling the is_valid, the formset will validate all forms in
        # one go, so you can effectively treat them like they are one form.
        if thread_form.is_valid() and post_form.is_valid() and poll_form.is_valid() and poll_subject_formset.is_valid():
            thread = thread_form.save(False)  # get memory only version of the model
            thread.subject = subject
            thread.user = request.user
            thread.save()

            post = post_form.save(False)
            post.user = request.user
            post.thread = thread  # newly created thread id
            post.save()

            if request.POST.get('is_a_poll', None):
                poll = poll_form.save(False)
                poll.thread = thread
                poll.save()

                # To pull out the values from each form, loop through each one.
                # It is the same when rendering.
                for subject_form in poll_subject_formset:
                    subject = subject_form.save(False)
                    subject.poll = poll
                    subject.save()

            messages.success(request, "You have created a new thread!")

            return redirect(reverse('thread', args={thread.pk}))
    else:
        thread_form = ThreadForm()
        post_form = PostForm(request.POST)
        poll_form = PollForm()
        poll_subject_formset = poll_subject_formset()

        args = {
            'thread_form': thread_form,
            'post_form': post_form,
            'subject': subject,
            'poll_form': poll_form,
            'poll_subject_formset': poll_subject_formset,  # loop through the formset of 3 forms when rendering.
        }

        args.update(csrf(request))

        return render(request, 'forum/thread_form.html', args)


def thread(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    args = {'thread': thread}
    args.update(csrf(request))
    return render(request, 'forum/thread.html', args)


@login_required
def new_post(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(False)
            post.thread = thread
            post.user = request.user
            post.save()

            messages.success(request, "Your post has been added to the thread!")

            return redirect(reverse('thread', args={thread.pk}))
    else:
        form = PostForm()

    args = {
        'form': form,
        'form_action': reverse('new_post', args={thread.id}),
        'button_text': 'Update Post'
    }
    args.update(csrf(request))

    return render(request, 'forum/post_form.html', args)


@login_required
def edit_post(request, thread_id, post_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    post = get_object_or_404(Posts, pk=post_id)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "You have updated your thread!")

            return redirect(reverse('thread', args={thread.pk}))
    else:
        form = PostForm(instance=post)

    args = {
        'form': form,
        'form_action': reverse('edit_post', kwargs={"thread_id": thread.id, "post_id": post.id}),
        'button_text': 'Update Post'
    }
    args.update(csrf(request))

    return render(request, 'forum/post_form.html', args)


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Posts, pk=post_id)
    thread_id = post.thread.id
    post.delete()

    messages.success(request, "Your post was deleted!")

    return redirect(reverse('thread', args={thread_id}))


@login_required
def thread_vote(request, thread_id, subject_id):

    # get the thread data
    thread = Thread.objects.get(id=thread_id)

    # check the thread.poll for votes by the user
    votes = thread.poll.votes.filter(user=request.user)  # query not run at this point.

    if votes.exists():  # query is only run at this point.
        messages.error(request, "You already voted on this! ... You're not trying to cheat are you?")
        return redirect(reverse('thread', args={thread_id}))

    # get the polls subject by using subject_id from PollSubject
    subject = PollSubject.objects.get(id=subject_id)

    # Add users vote to votes db table
    subject.votes.create(poll=subject.poll, user=request.user)

    messages.success(request, "We've registered your vote!")

    return redirect(reverse('thread', args={thread_id}))
