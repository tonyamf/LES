import os
import unittest

from django.test import TestCase
from django.urls import reverse

from Activities.models import Sentence, Verb
from Users.models import User

FIXTURE = os.path.join(os.path.dirname(__file__), '..', '..', 'Activities', 'tests',
                       'fixtures', 'basic.json')

FULL_QUERY = {'name': '', 'date_initial': '', 'date_final': '', 'frase_verbo': '',
              'frase_sujeito': '', 'frase_receptor': '', 'verbo_tipo': '',
              'group_frases': '', 'pattern_groups': ''}


class HomeAndSearchTests(TestCase):
    fixtures = [FIXTURE]

    def setUp(self):
        self.user = User.objects.create_user(username='ana', password='not-a-real-password')
        self.other = User.objects.create_user(username='rui', password='not-a-real-password')
        self.client.force_login(self.user)
        verb = Verb.objects.get(pk=1)
        Sentence.objects.create(userid=self.user, sentencename='minha frase', subject='eu',
                                verbid=verb, receiver='', datecreated='2019-05-01')
        Sentence.objects.create(userid=self.other, sentencename='frase do rui', subject='rui',
                                verbid=verb, receiver='', datecreated='2019-05-01')

    def test_home_lists_only_my_sentences(self):
        response = self.client.get(reverse('home'))
        self.assertEqual([s.sentencename for s in response.context['sentences']], ['minha frase'])

    def test_search_page_renders(self):
        self.assertEqual(self.client.get(reverse('search')).status_code, 200)

    def test_search_by_name_with_full_form_finds_sentence(self):
        response = self.client.get(reverse('search_results'), {**FULL_QUERY, 'name': 'rui'})
        self.assertEqual([s.sentencename for s in response.context['sentences']], ['frase do rui'])

    def test_search_date_range_excludes_old_rows(self):
        response = self.client.get(reverse('search_results'),
                                   {**FULL_QUERY, 'date_initial': '2019-06-01'})
        self.assertEqual(list(response.context['sentences']), [])

    @unittest.expectedFailure
    def test_search_with_missing_parameters_should_not_crash(self):
        # BUG (see 2_fix/review.md): absent GET parameters become None and
        # Q(field__icontains=None) raises ValueError -> HTTP 500.
        response = self.client.get(reverse('search_results'), {'name': 'a'})
        self.assertEqual(response.status_code, 200)
