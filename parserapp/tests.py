from django.test import TestCase
from .models import Vacancy, Skills_table
from mixer.backend.django import mixer


class PostTestCaseMixer(TestCase):

    def setUp(self):
        self.vac = mixer.blend(Vacancy)

        skils = mixer.blend(Skills_table, name='test_category')
        self.post_str = mixer.blend(Vacancy, name='test_post_str', skils=skils)

    def test_some_method(self):
        self.assertFalse(self.vac.some_method() == 'some method')
