from django.db import models

from accounts.models import CustomUser


class Whisky(models.Model):
    SCOTLAND = "SC"
    IRELAND = "IR"
    AMERICA = "AM"
    CANADA = "CA"
    JAPAN = "JA"
    EXTRA = "EX"
    COUNTRY_CHOICES = [
        (SCOTLAND, "スコットランド"),
        (IRELAND, "アイルランド"),
        (AMERICA, "アメリカ"),
        (CANADA, "カナダ"),
        (JAPAN, "日本"),
        (EXTRA, "その他"),
    ]

    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES, blank=True)
    # 関数を作成し、choicesに追加。国によって選べる地域を変えられるように。
    # region = models.CharField(choices=, blank=True)
    alcohol = models.FloatField(blank=True, null=True)
    cask = models.CharField(max_length=200, blank=True)
    img = models.ImageField(blank=True, null=True)
    price = models.CharField(max_length=200, blank=True)
    owner = models.ForeignKey(
        CustomUser, related_name="whisky", on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.name)


class TastingNote(models.Model):
    whisky = models.ForeignKey(
        Whisky, related_name="tasting_note", on_delete=models.CASCADE
    )
    post_date = models.DateField(auto_now_add=True)
    note = models.TextField()
    owner = models.ForeignKey(
        CustomUser, related_name="tasting_note", on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return self.note
