from django.db import models


class Corpus(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    genre = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Text(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    content = models.TextField()  # Поле с самим текстом
    corpus = models.ForeignKey(
        Corpus,
        on_delete=models.CASCADE,
        related_name='texts'
    )
    has_translation = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='translations'
    )

    def __str__(self):
        return self.title
