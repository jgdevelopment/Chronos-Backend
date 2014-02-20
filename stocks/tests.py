"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.core.urlresolvers import reverse

class quoteTest(TestCase):
    def testQuote(self):
		response = self.client.get(reverse('quote','AAPL'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "")
