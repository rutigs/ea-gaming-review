from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.CharField(max_length=5000)
    snippet = models.CharField(max_length=53, blank=True, default="")
    author = models.CharField(max_length=100)
    pub_date = models.DateTimeField('date published')


    def __str__(self):
        return f'{self.title} by {self.author}'


    def create_snippet(self):
        body_len = len(self.body)
        if body_len < 50:
            return self.body + "..."
        return self.body[:50] + "..."


    def save(self, *args, **kwargs):
        if not self.snippet or self.snippet == "":
            self.snippet = self.create_snippet()
        super(Post, self).save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    body = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        post = Post.objects.get(pk=self.post.id)
        return f'Comment #{self.id} on {post.title} written by {self.author}'