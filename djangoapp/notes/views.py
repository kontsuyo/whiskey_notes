from rest_framework import generics, permissions

from notes.models import TastingNote, Whisky
from notes.permissions import IsOwnerOrReadOnly
from notes.serializers import TastingNoteSerializer, WhiskySerializer


class WhiskyList(generics.ListCreateAPIView):
    queryset = Whisky.objects.all()
    serializer_class = WhiskySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class WhiskyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Whisky.objects.all()
    serializer_class = WhiskySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class TastingNoteList(generics.ListCreateAPIView):
    queryset = TastingNote.objects.all()
    serializer_class = TastingNoteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TastingNoteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TastingNote.objects.all()
    serializer_class = TastingNoteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
