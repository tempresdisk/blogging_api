from django.contrib.auth import get_user_model
from django.db import models
from pytils.translit import slugify

User = get_user_model()


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(
        "Дата публикации", auto_now_add=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts"
    )
    group = models.ForeignKey('Group',
                              on_delete=models.SET_NULL,
                              blank=True,
                              null=True,
                              related_name='posts',
                              verbose_name='Сообщество',
                              help_text='Здесь можно выбрать '
                                        'сообщество для поста')

    def __str__(self):
        return self.text


class Group(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=20)
    description = models.TextField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Group, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField()
    created = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True
    )


class Follow(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="follower")
    following = models.ForeignKey(User,
                                  on_delete=models.CASCADE,
                                  related_name="following")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'], name='follower'
            )
        ]
