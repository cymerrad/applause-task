from django.test import TestCase
from .views import search_db_count_bugs, parse_db_count_bugs
from .models import Bug
from django.db.models import Count
import re


class DBSearchBugCount(TestCase):
    '''
    These tests should be using only search_db_count_bugs() - no parsing.
    '''

    fixtures = {'fixture.test.json'}

    def test_matching_none(self):
        qs = search_db_count_bugs([], [])

        self.assertEqual(len(qs), 0)

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
    Assuming DB Searching is correct, we _maybe_ will use it for generating test cases.
    We can pass in just lists of dictionaries, this will work exactly the same as QuerySets.
    '''

    essential_fields = ['testerId', 'deviceId__description', 'submissions']
    semi_useful = ['deviceId']

    @staticmethod
    def mock_qs_element(testerId: int, deviceId__description: str, submissions: int, **nonessential):
        return {
            'testerId': testerId,
            'deviceId__description': deviceId__description,
            'submissions': submissions,
            **nonessential,
        }

    @staticmethod
    def mock_tester_data(first_name: str = None, last_name: str = None, country: str = None):
        temp = {}
        if first_name:
            temp['testerId__firstName'] = first_name
        if last_name:
            temp['testerId__lastName'] = last_name
        if country:
            temp['testerId__country'] = country

        return temp

    def test_just_essential_fields(self):
        qs = [self.mock_qs_element(1, 'iDevice 42', 1)]
        parsed = parse_db_count_bugs(qs)

        # writing these by hand somewhat makes sense
        self.assertDictEqual(parsed, {
            1: {
                'submissions': {'iDevice 42': 1},
                'total': 1,
            }
        })

    def test_ill_formed_query_set(self):
        # all these fields should raise a KeyError
        for missing_field in self.essential_fields:
            obj = self.mock_qs_element(1, 'Whatever', 1)
            del obj[missing_field]
            qs = [obj]

            with self.assertRaises(KeyError):
                parse_db_count_bugs(qs)

    def test_nonessential_fields(self):
        mock_obj = self.mock_qs_element(
            1, 'Whatever', 2, **self.mock_tester_data('First', 'Last', 'XO'))
        qs = [mock_obj]
        parsed = parse_db_count_bugs(qs)

        self.assertDictEqual(parsed, {
            1: {
                'submissions': {'Whatever': 2},
                'total': 2,
                'first_name': 'First',
                'last_name': 'Last',
                'country': 'XO'
            }
        })

    def test_non_accepted_fields(self):
        mock_obj = self.mock_qs_element(2, 'Eh', 3)
        mock_obj['some_random_field'] = 'aaa'
        mock_obj['deviceId'] = "shouldn't matter at all"

        self.assertEqual(parse_db_count_bugs([mock_obj]), {
            2: {
                'submissions': {'Eh': 3},
                'total': 3,
            }
        })

    def test_can_it_count(self):
        # using the example in function's docstring

        # I find this very amusing
        # docstring_example = {}
        # exec("docstring_example = " +
        #      re.compile(r"[ ]+\{[\w\W]+\}", re.UNICODE | re.MULTILINE)
        #      .findall(parse_db_count_bugs.__doc__)[0].replace(' '*8, ''))

        docstring_example = {
            5: {'first_name': 'Mingquan',
                'last_name': 'Zheng',
                'submissions': {'iPhone 4': 21},
                'total': 21},
            8: {'first_name': 'Sean',
                'last_name': 'Wellington',
                'country': 'GB',
                'submissions': {'iPhone 4': 28, 'iPhone 5': 30},
                'total': 58}
        }

        obj1_data = self.mock_tester_data('Mingquan', 'Zheng')
        obj1 = self.mock_qs_element(5, 'iPhone 4', 21, **obj1_data)

        obj2_data = self.mock_tester_data('Sean', 'Wellington', 'GB')
        obj2 = self.mock_qs_element(8, 'iPhone 4', 28, **obj2_data)
        obj2point5 = self.mock_qs_element(8, 'iPhone 5', 30, **obj2_data)

        parsed = parse_db_count_bugs([obj1, obj2, obj2point5])

        self.assertDictEqual(parsed, docstring_example)


class IntegrationTests(TestCase):
    pass
