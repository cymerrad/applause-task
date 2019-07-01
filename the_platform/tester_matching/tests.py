from django.test import TestCase
from .views import search_db_count_bugs, parse_db_count_bugs
from .models import Bug
from django.db.models import Count


class DBSearchBugCount(TestCase):
    '''
    These tests should be using only search_db_count_bugs()
    '''

    fixtures = {'fixture.test.json'}

    def test_matching_none(self):
        qs = search_db_count_bugs([], [])
        parsed = parse_db_count_bugs(qs)

        self.assertEqual(len(qs), 0)
        self.assertDictEqual(parsed, {})

    def test_matching_all(self):
        '''
        We'll check consistency by summing up all the bug submissions per user and device.
        '''
        qs = search_db_count_bugs(["ALL"], ["ALL"])

        bugs_count = Bug.objects.aggregate(Count('bugId'))['bugId__count']
        bugs_sum = 0
        for row in qs:
            bugs_sum += row['submissions']

        self.assertEqual(bugs_count, bugs_sum)

    def test_non_existent_country(self):
        qs = search_db_count_bugs(["XX"], ["ALL"])
        self.assertEqual(len(qs), 0)

    def test_non_existent_device(self):
        qs = search_db_count_bugs(["ALL"], ["iDontExist XD"])
        self.assertEqual(len(qs), 0)

    def test_matching_only_1_country(self):
        for country in ["JP", "GB", "US"]:
            qs = search_db_count_bugs([country], ["ALL"])
            for row in qs:
                self.assertEqual(row['testerId__country'], country)

    def test_matching_only_1_device(self):
        for device in ["iPhone 4",
                       "iPhone 4S",
                       "iPhone 5",
                       "Galaxy S3",
                       "Galaxy S4",
                       "Nexus 4",
                       "Droid Razor",
                       "Droid DNA",
                       "HTC One",
                       "iPhone 3"]:
            qs = search_db_count_bugs(["ALL"], [device])
            for row in qs:
                self.assertEqual(row['deviceId__description'], device)

    def test_all_overrides(self):
        '''
        This is an expected behaviour I intended.
        '''
        qs = search_db_count_bugs(["JP", "GB", "ALL"], [
                                  "iPhone 4", "iPhone 4S", "ALL"])
        qs_explicit_all = search_db_count_bugs(["ALL"], ["ALL"])
        self.assertEqual(len(qs), len(qs_explicit_all))


class ParsedSearchResults(TestCase):
    '''
    Assuming DB Searching is correct, we will use it for generating test cases.
    '''

    fixtures = {'fixture.test.json'}

    def test_nothing(self):
        pass


class IntegrationTests(TestCase):
    pass
