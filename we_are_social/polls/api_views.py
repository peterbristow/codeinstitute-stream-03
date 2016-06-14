from rest_framework import generics
from models import Poll, Vote, Thread, PollSubject
from serializers import PollSerializer, VoteSerializer


# generics.ListAPIView, which is a basic class defined to allow us to render
# a simple list of objects from our models.
class PollViewSet(generics.ListAPIView):
    # List polls
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
