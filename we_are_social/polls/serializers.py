from rest_framework import serializers
from .models import Vote, PollSubject, Poll


class VoteSerializer(serializers.ModelSerializer):
    """
    The ModelSerializer knows which members are available, and will automate
    the process without you having to define what they should be.
    All we need to do is supply an l tuple with details of which ones we want
    included. If it's not in the list, it's left out.
    This serializer produces something like this:
        {
            "id": 1,
            "poll": 1,
            "subject": 1,
            "user": 1
        }
    """

    class Meta:
        model = Vote
        fields = ('id', 'poll', 'subject', 'user')


class PollSubjectSerializer(serializers.ModelSerializer):
    """
    When serializing related data, we begin to see the simplicity of the
    framework even more, as we just reference other serializers to have
    related fields included in the process.  E.g.
        {
            "id": 7,
            "name": "WingIDE !",
            "votes": [
                {
                    "id": 2,
                    "poll": 3,
                    "subject": 7,
                    "user": 1
                }
            ],
            "total_votes": 1
        },
    """
    votes = VoteSerializer(many=True)  # ref another serializer

    class Meta:
        model = PollSubject
        fields = ('id', 'name', 'votes')

    # Custom field
    def get_total_votes(self, subject):
        """
        If you need something that's not really part of your data, but needs to
        be included for simplicity or speed.
        DRF allows you to implement something called a SerializerMethodField,
        which is a function that you define on the class and will be added into
        the JSON with the name you give it as a member variable.
        The name you give to the class method is assumed to be the word get_ with
        the name of the variable appended.
        Include in the above fields.
        The second argument is generally the instance of the object the serializer
        is working on. In our case it's a subject.
        """
        return subject.votes.count()


class PollSerializer(serializers.ModelSerializer):
    # Include another serializer.
    # many=True so that our PollSerializer knows to expect more than one
    # instance of a PollSubject to be in this field and render them all.
    subjects = PollSubjectSerializer(many=True)

    user_has_voted = serializers.SerializerMethodField()

    class Meta:
        model = Poll
        fields = ('id', 'question', 'subjects', 'user_has_voted')

    # Custom field
    def get_user_has_voted(self, poll):
        # Has the user already voted?
        has_voted = False

        request = self.context.get('request', None)

        if not request:
            return False

        vote = poll.votes.filter(user_id=request.user.id).first()
        if vote:
            has_voted = True

        return has_voted
