from django.db import models


class Whisky(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200, blank=False, null=False)
    country = models.CharField(max_length=30, blank=True)
    alcohol = models.CharField(max_length=10, blank=True)
    img = models.ImageField(blank=True, null=True)
    price = models.CharField(max_length=30, blank=True)
    owner = models.ForeignKey(
        "accounts.CustomUser",
        related_name="owned_whiskies",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class TastingNote(models.Model):
    whisky = models.ForeignKey(
        Whisky, related_name="tasting_note", on_delete=models.CASCADE
    )
    post_date = models.DateField(auto_now_add=True)
    note = models.TextField(blank=False, null=False)
    owner = models.ForeignKey(
        "accounts.CustomUser",
        related_name="tasting_notes",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.note
