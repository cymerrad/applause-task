from django.test import TestCase
from .views import search_db_count_bugs, parse_db_count_bugs
from .models import Bug
from django.db.models import Count


class DbSearchBugCount(TestCase):

    fixtures = {'fixture.test.json'}

    # this will flush the database after each test
    # databases = {'test'}

    def test_matching_none(self):
        '''
        • Criteria: Country=[] and Device=[]
        • Result: []
        '''
        qs = search_db_count_bugs([], [])
        parsed = parse_db_count_bugs(qs)

        self.assertEqual(len(qs), 0)
        self.assertDictEqual(parsed, {})

    def test_matching_all(self):
        '''
        • Criteria: Country="ALL" and Device="ALL"
        • Result: every user
        We'll check consistency by summing up all the bug submissions per user and device.
        '''
        qs = search_db_count_bugs(["ALL"], ["ALL"])
        parsed = parse_db_count_bugs(qs)

        bugs_count = Bug.objects.aggregate(Count('bugId'))['bugId__count']
        bugs_sum = 0
        for user in parsed.values():
            for bug_c in user['submissions'].values():
                bugs_sum += bug_c

        self.assertEqual(bugs_count, bugs_sum)

    def test_matching_only_1_country(self):
        '''
        • Criteria: Country="JP" and Device="ALL"
        • Result: 3 users from Japan
        '''
        qs = search_db_count_bugs(["JP"], ["ALL"])
        for row in qs:
            self.assertEqual(row['testerId__country'], "JP")
