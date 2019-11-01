#-*- coding: utf-8 -*-
from django.test import TestCase
from model_mommy import mommy

from log.models import LogReview


class LogReviewModelTest(TestCase):
    def test_create(self):
        obj = LogReview(
            log=mommy.make('LogEntry'),
            status=-1
        )
        obj.save()

        self.assertTrue(LogReview.objects.exists())
