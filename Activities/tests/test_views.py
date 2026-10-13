import os
import unittest

from django.test import TestCase, TransactionTestCase
from django.urls import reverse

from Activities.models import Group, Pattern, Sentence, Verb
from Users.models import User

FIXTURE = os.path.join(os.path.dirname(__file__), 'fixtures', 'basic.json')
AJAX = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}


class ViewTestCase(TestCase):
    fixtures = [FIXTURE]

    def setUp(self):
        self.user = User.objects.create_user(username='ana', password='not-a-real-password')
        self.client.force_login(self.user)

    def make_sentence(self, name='eu escrevo'):
        return Sentence.objects.create(
            userid=self.user, sentencename=name, subject='eu',
            verbid=Verb.objects.get(pk=1), receiver='')


class VerbCrudTests(ViewTestCase):
    def test_list_shows_fixture_verbs(self):
        response = self.client.get(reverse('verb_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'escrever')
        self.assertContains(response, 'telefonar')

    def test_list_search_filters_by_substring(self):
        response = self.client.get(reverse('verb_list'), {'search': 'telef'})
        self.assertEqual([v.verbname for v in response.context['object_list']], ['telefonar'])

    def test_create_redirects_and_saves(self):
        response = self.client.post(reverse('verb_create'),
                                    {'verbname': 'ler', 'verbtype': 'Produtivo'})
        self.assertRedirects(response, reverse('verb_list'))
        self.assertTrue(Verb.objects.filter(verbname='ler').exists())

    def test_ajax_create_returns_json_with_pk(self):
        response = self.client.post(reverse('verb_create'),
                                    {'verbname': 'ler', 'verbtype': 'Produtivo'}, **AJAX)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                         {'local': 'verbs/', 'pk': Verb.objects.get(verbname='ler').pk})

    def test_ajax_invalid_create_returns_400_with_errors(self):
        response = self.client.post(reverse('verb_create'),
                                    {'verbname': 'escrever', 'verbtype': 'Produtivo'}, **AJAX)
        self.assertEqual(response.status_code, 400)
        self.assertIn('verbname', response.json())

    def test_update_changes_the_row(self):
        self.client.post(reverse('verb_update', args=[2]),
                         {'verbname': 'ligar', 'verbtype': 'Comunicativo'})
        self.assertEqual(Verb.objects.get(pk=2).verbname, 'ligar')

    def test_delete_unused_verb(self):
        response = self.client.post(reverse('verb_delete', args=[2]))
        self.assertRedirects(response, reverse('verb_list'))
        self.assertFalse(Verb.objects.filter(pk=2).exists())


class VerbDeleteInUseTests(TransactionTestCase):
    # TransactionTestCase: the foreign-key check happens at commit, which TestCase defers.
    fixtures = [FIXTURE]

    @unittest.expectedFailure
    def test_deleting_a_verb_used_by_a_sentence_should_not_crash(self):
        # BUG (see 2_fix/review.md): Sentence.verbid uses DO_NOTHING, so the database
        # rejects the delete with an IntegrityError instead of a friendly message.
        user = User.objects.create_user(username='ana', password='not-a-real-password')
        self.client.force_login(user)
        Sentence.objects.create(userid=user, sentencename='x', subject='eu',
                                verbid=Verb.objects.get(pk=1), receiver='')
        response = self.client.post(reverse('verb_delete', args=[1]))
        self.assertIn(response.status_code, (200, 302))
        self.assertTrue(Verb.objects.filter(pk=1).exists() or not Sentence.objects.exists())


class SentenceTests(ViewTestCase):
    def test_create_sets_owner_and_creation_date(self):
        self.client.post(reverse('sentence_create'), {
            'sentencename': 'eu escrevo', 'subject': 'eu', 'verbid': 1,
            'receiver': '', 'datarealizado': '2019-01-02'})
        sentence = Sentence.objects.get()
        self.assertEqual(sentence.userid, self.user)
        self.assertIsNotNone(sentence.datecreated)
        self.assertEqual(str(sentence.datarealizado), '2019-01-02')

    def test_datarealizado_is_required_although_the_model_says_optional(self):
        # Documents current behaviour: get_form() replaces the field with a required one,
        # which makes the "default to now" branch in form_valid dead code.
        response = self.client.post(reverse('sentence_create'), {
            'sentencename': 'x', 'subject': 'eu', 'verbid': 1, 'receiver': ''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Sentence.objects.count(), 0)


class GroupPatternTests(ViewTestCase):
    def test_group_create_attaches_sentences_chosen_via_ajax_get(self):
        sentence = self.make_sentence()
        # step 1: the page asks which sentences were ticked; the view remembers them
        listing = self.client.get(reverse('group_create'), {'id[]': [sentence.pk]})
        self.assertEqual(listing.json()[0]['pk'], sentence.pk)
        # step 2: the form is submitted
        self.client.post(reverse('group_create'), {'groupname': 'rotina'})
        group = Group.objects.get(groupname='rotina')
        self.assertEqual(list(group.sentences.all()), [sentence])
        self.assertEqual(group.userid, self.user)

    def test_pattern_create_attaches_groups(self):
        group = Group.objects.create(userid=self.user, groupname='g', name='g', description='d')
        self.client.get(reverse('pattern_create'), {'id[]': [group.pk]})
        self.client.post(reverse('pattern_create'), {'patternname': 'padrao'})
        self.assertEqual(list(Pattern.objects.get().groups.all()), [group])


class AccessControlTests(ViewTestCase):
    def test_home_redirects_anonymous_to_login(self):
        self.client.logout()
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)

    @unittest.expectedFailure
    def test_anonymous_cannot_create_verbs(self):
        # BUG (see 2_fix/review.md): only Core.views.Home has @login_required; the
        # generic views in Activities/views.py are open to anonymous visitors.
        self.client.logout()
        self.client.post(reverse('verb_create'), {'verbname': 'anon', 'verbtype': 'Produtivo'})
        self.assertFalse(Verb.objects.filter(verbname='anon').exists())
