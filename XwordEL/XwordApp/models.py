from django.db import models


class common_word(models.Model):
    word = models.CharField(max_length=255)
    meaning1 = models.TextField(blank=True)
    meaning2 = models.TextField(blank=True)

    def __str__(self):
        return self.word


class User_played_words_Thai_meaning(models.Model):
    userID = models.CharField(max_length=255)
    word = models.TextField(blank=True)

    def __str__(self):
        return self.word


class User_played_words_Eng_meaning(models.Model):
    userID = models.CharField(max_length=255)
    word = models.TextField(blank=True)

    def __str__(self):
        return self.word


class all_Eng_words(models.Model):
    word = models.CharField(max_length=255)
    meaning = models.TextField(blank=True)

    def __str__(self):
        return self.word


class all_Thai_words(models.Model):
    word = models.CharField(max_length=255)
    meaning = models.TextField(blank=True)

    def __str__(self):
        return self.word
