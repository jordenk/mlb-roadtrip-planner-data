"""
Unit tests for select helper functions. Scraping favors data inspection and warning over testing.
"""
from mlb_trip_planner_data.scrapers.scrapers import date_string_to_timestamp
import pytest


def test_date_string_to_timestamp_transforms_valid_dates():
    assert 1546326000 == date_string_to_timestamp(2019, 1, 1, '12:00 AM MST')
    assert 1557529200 == date_string_to_timestamp(2019, 5, 10, '5:00 PM MDT')
    assert 1571158800 == date_string_to_timestamp("2019", "10", "15", '11:00 AM MDT')


def test_date_string_to_timestamp_raises_error_when_time_cannot_be_split():
    with pytest.raises(AssertionError):
        date_string_to_timestamp(2019, 1, 1, '12:00 A M MT')


def test_date_string_to_timestamp_raises_error_with_unknown_timezones():
    with pytest.raises(KeyError):
        date_string_to_timestamp(2019, 1, 1, '12:00 AM JUNK')
