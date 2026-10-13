import os

from django.db import IntegrityError, transaction
from django.test import TestCase

from Activities.models import Artefact, Resource, Verb

FIXTURE = os.path.join(os.path.dirname(__file__), 'fixtures', 'basic.json')


class ModelTests(TestCase):
    fixtures = [FIXTURE]

    def test_str_returns_the_name_field(self):
        self.assertEqual(str(Verb.objects.get(pk=1)), 'escrever')
        self.assertEqual(str(Resource.objects.get(pk=1)), 'portatil')
        self.assertEqual(str(Artefact.objects.get(pk=1)), 'relatorio')

    def test_verb_names_are_unique(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            Verb.objects.create(verbname='escrever', verbtype='Produtivo')

    def test_verbs_are_ordered_newest_first(self):
        self.assertEqual([v.pk for v in Verb.objects.all()], [2, 1])
