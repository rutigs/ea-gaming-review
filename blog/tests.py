from django.test import TestCase
from django.utils import timezone

import datetime

from .models import Post, Comment


class PostModelTestCases(TestCase):

    def test_create_snippet(self):
        """
            create_snippet should return of length <50 and three dots (...)
            based on the contents of the post body.
        """

        # test a body length that is longer than the snippet max
        post_long = Post(title="title", body="a" * 51, snippet="", pub_date=timezone.now())
        snippet = post_long.create_snippet()
        self.assertEqual(len(snippet), 53)
        self.assertEqual(snippet[-4:], "a...")

        # test a post body length that is shorter than snippet max
        post_short = Post(title="title", body="b", snippet="", pub_date=timezone.now())
        snippet = post_short.create_snippet()
        self.assertEqual(len(snippet), 4)
        self.assertEqual(snippet, "b...")


    def test_save_override(self):
        """
            if a snippet is not supplied the save override should call and create one.
        """
        # the author has provided a snippet
        post_with_snip = Post(title="title", body="a" * 51, snippet="a...", pub_date=timezone.now())
        post_with_snip.save()
        self.assertEqual(len(post_with_snip.snippet), 4)
        self.assertEqual(post_with_snip.snippet, "a...")

        # the author has not provided a snippet
        post_no_snip = Post(title="title", body="b" * 51, snippet="", pub_date=timezone.now())
        post_no_snip.save()
        self.assertEqual(len(post_no_snip.snippet), 53)
        self.assertEqual(post_no_snip.snippet, "b" * 50 + "...")


class CommentModelTestCases(TestCase):

    def test_created_at_time(self):
        """
            tests that comments `created_at` time are created when new comments
            are saved.
        """
        post = Post(title="title", body="a" * 51, snippet="a...", pub_date=timezone.now())
        post.save()

        now = timezone.now()

        new_comment = Comment(post=post, author="ABC", body="abc")
        new_comment.save()

        self.assertGreater(new_comment.created_at, now)
        self.assertLess(new_comment.created_at, timezone.now())


class IndexViewTestCases(TestCase):

    def test_future_posts(self):
        """
            tests that future blog posts that haven't been published yet do
            not appear on the index page
        """
        future_time = timezone.now() + datetime.timedelta(days=2)
        Post.objects.create(title="title", body="a", snippet="a...", pub_date=future_time)

        response = self.client.get("/")
        self.assertContains(response, "No blog posts available.")
        self.assertQuerysetEqual(response.context['latest_posts'], [])


    def test_past_posts(self):
        """
            tests that posts published before now are appearing on the
            index page
        """
        past_time = timezone.now() + datetime.timedelta(days=-2)
        Post.objects.create(title="title", body="a", snippet="a...", pub_date=past_time)

        response = self.client.get("/")
        self.assertQuerysetEqual(
            response.context['latest_posts'], 
            ['<Post: title by >']
        )
        