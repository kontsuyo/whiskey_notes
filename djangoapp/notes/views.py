from rest_framework import generics, permissions

from notes.models import Whiskey
from notes.permissions import IsOwnerOrReadOnly
from notes.serializers import WhiskeySerializer


class WhiskeyList(generics.ListCreateAPIView):
    queryset = Whiskey.objects.all()
    serializer_class = WhiskeySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class WhiskeyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Whiskey.objects.all()
    serializer_class = WhiskeySerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]
