import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question

# Create your tests here.

class QuestionModelTests(TestCase):

    def test_was_published_recently_false_if_in_future(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertFalse(future_question.was_published_recently())

    def test_was_published_recently_false_if_in_past(self):
        time = timezone.now() - datetime.timedelta(days=30)
        old_q = Question(pub_date=time)
        self.assertFalse(old_q.was_published_recently(), "It is too long ago")

    def test_was_published_recently_false_if_in_last_30_days(self):
        time = timezone.now() - datetime.timedelta(hours=23)
        recent_question = Question(pub_date=time)
        self.assertTrue(recent_question.was_published_recently(), "It is recent")


class QuestionViewTests(TestCase):

    def test_no_questions(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_basic(self):
        q1 = Question.objects.create(question_text="test1", pub_date=timezone.now()-datetime.timedelta(minutes=5))
        q2 = Question.objects.create(question_text="test2", pub_date=timezone.now() - datetime.timedelta(minutes=5))

        response = self.client.get(reverse('polls:index'))

        self.assertEquals(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: test2>', '<Question: test1>'])

    def test_question_in_future(self):
        Question.objects.create(question_text="test1", pub_date=timezone.now() - datetime.timedelta(minutes=5))
        Question.objects.create(question_text="test2", pub_date=timezone.now() + datetime.timedelta(minutes=5))

        response = self.client.get(reverse('polls:index'))

        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: test1>'])

    def test_only_most_recent_5(self):
        Question.objects.create(question_text="test1", pub_date=timezone.now() - datetime.timedelta(minutes=1))
        Question.objects.create(question_text="test2", pub_date=timezone.now() - datetime.timedelta(minutes=2))
        Question.objects.create(question_text="test3", pub_date=timezone.now() - datetime.timedelta(minutes=3))
        Question.objects.create(question_text="test4", pub_date=timezone.now() - datetime.timedelta(minutes=4))
        Question.objects.create(question_text="test5", pub_date=timezone.now() - datetime.timedelta(minutes=5))
        Question.objects.create(question_text="test6", pub_date=timezone.now() - datetime.timedelta(minutes=6))

        response = self.client.get(reverse('polls:index'))

        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: test1>', '<Question: test2>',
                                                                            '<Question: test3>', '<Question: test4>',
                                                                            '<Question: test5>'])
