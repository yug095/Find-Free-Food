import datetime

from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import Question

class QuestionMethodTests(TestCase):
	def test_was_published_recently_with_future_question(self):
		"""
		was_published_recently() should return False for a 
		question whose pub_date is in the future.
		"""
		time = timezone.now() + datetime.timedelta(days=30)
		future_question = Question(pub_date=time)

		self.assertEqual(future_question.was_published_recently(), False)

	def test_was_published_recently_with_old_question(self):
		"""
		was_published_recently() should return False for a 
		question whose pub_date is older than 1 day.
		"""
		time = timezone.now() - datetime.timedelta(days=30)
		old_question = Question(pub_date=time)
		self.assertEqual(old_question.was_published_recently(),False)

	def test_was_published_recently_with_recent_question(self):
		"""
		was_published_recently() should return True for a
		question whose pub_date is within the last day.
		"""
		time = timezone.now() - datetime.timedelta(hours=1)
		recent_question = Question(pub_date=time)
		self.assertEqual(recent_question.was_published_recently(),True)

def create_question(question_text, days):
		"""
		creates a question with args given
		number of 'days' offset to now (negative for past)
		"""
		time = timezone.now() + datetime.timedelta(days=days)
		return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionViewTests(TestCase):
	def test_index_view_with_no_questions(self):
		"""
		if no questions exist, an appropriate message should be displayed
		"""
		response = self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No polls are available")
		self.assertQuerysetEqual(response.context['latest_question_list'],[])

	def test_index_view_with_a_past_question(self):
		"""
		questions with a pub_date in the past should be displayed
		"""
		create_question(question_text="Past question.",days=-30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_question_list'],
			['<Question: Past question.>']
		)

	def test_index_view_with_a_future_question(self):
		"""
		questions with a pub_date in the future should not be displayed
		"""
		create_question(question_text="future question", days=30)
		response = self.client.get(reverse('polls:index'))
		self.assertContains(response, "No polls are available", status_code=200)
		self.assertQuerysetEqual(response.context['latest_question_list'], [])

	def test_index_view_with_future_and_past_question(self):
		"""
		with both past and future questions, only past should be displayed
		"""
		create_question(question_text="past question", days=-30)
		create_question(question_text="future question", days=30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_question_list'],
			['<Question: past question>']
		)


	def test_index_view_with_two_past_questions(self):
		"""
		questions index page may display multiple questions
		"""
		create_question(question_text="past question 1", days=-30)
		create_question(question_text="past question 2", days=-5)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_question_list'],
			['<Question: past question 2>', '<Question: past question 1>']
		)		


class QuestionIndexDetailTests(TestCase):
	def test_detail_view_with_a_future_question(self):
		"""
		detail view of a question with a pub_date in the 
		future should return a 404 not found
		"""
		future_question = create_question(question_text='Future question.',days=5)
		response = self.client.get(reverse('polls:detail',args=(future_question.id,)))
		self.assertEqual(response.status_code, 404)

	def test_detail_view_with_a_past_question(self):
		"""
		detail view a question with a pub_date in the past
		should display the question's text
		"""
		past_question = create_question(question_text='Past Question.', days=-5)
		response = self.client.get(reverse('polls:detail', args=(past_question.id,)))
		self.assertContains(response, past_question, status_code=200)






