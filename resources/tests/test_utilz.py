#!/usr/bin/python2
from resources.lib.utilz import UtilzException, is_leap_year, month_days
import pytest


class TestMonthDays:

    def test_30_giorni_a_novembre(self):
        assert month_days('11', '2018') == '30'

    def test_con_april(self):
        assert month_days('04', '2018') == '30'

    def test_giugno(self):
        assert month_days('06', '2018') == '30'

    def test_settembre(self):
        assert month_days('09', '2018') == '30'

    def test_febbraio(self):
        assert month_days('02', '2018') == '28'

    def test_ne_ha_trentuno_gennaio(self):
        assert month_days('01', '2018') == '31'

    def test_ne_ha_trentuno_marzo(self):
        assert month_days('03', '2018') == '31'

    def test_ne_ha_trentuno_maggio(self):
        assert month_days('05', '2018') == '31'

    def test_ne_ha_trentuno_luglio(self):
        assert month_days('07', '2018') == '31'

    def test_ne_ha_trentuno_agosto(self):
        assert month_days('08', '2018') == '31'

    def test_ne_ha_trentuno_ottobre(self):
        assert month_days('10', '2018') == '31'

    def test_ne_ha_trentuno_dicembre(self):
        assert month_days('12', '2018') == '31'

    def test_gennaio_ne_ha_trentuno(self):
        assert month_days('01', '2018') == '31'

    def test_mese_zero(self):
        with pytest.raises(UtilzException):
            month_days('00', '2018')

    def test_mese_tredici(self):
        with pytest.raises(UtilzException):
            month_days('13', '2018')

    def test_mese_int_no_str(self):
        with pytest.raises(UtilzException):
            month_days(2, '2018')

    def test_mese_anno_no_str(self):
        assert month_days('02', 2018) == '28'

    def test_febbraio_bisestile(self):
        assert month_days('02', '2016') == '29'

    def test_mese_no_leading_zero(self):
        with pytest.raises(UtilzException):
            month_days('2', '2018')

    def test_mese_too_many_leading_zero(self):
        with pytest.raises(UtilzException):
            month_days('002', '2018')


class TestIsLeapYear:

    def test_is_leap_year_2000(self):
        assert is_leap_year(2000) is True

    def test_is_leap_year_1900(self):
        assert is_leap_year(1900) is False

    def test_is_leap_year_2016(self):
        assert is_leap_year(2000) is True

    def test_is_leap_year_2017(self):
        assert is_leap_year(2017) is False
