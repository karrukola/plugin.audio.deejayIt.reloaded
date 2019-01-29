#!/usr/bin/python2


def is_leap_year(year):
    return (
        year % 4 == 0 and
        year % 100 != 0 or
        year % 400 == 0)


def month_days(mese, anno):
    """30 giorni a novembre, con april, giugno e settembre.
    Di 28 ce ne e uno.
    Tutti gli altri ne han 31"""
    if mese in ('11', '04', '06', '09'):
        days = '30'
    elif mese == '02':
        if is_leap_year(int(anno)):
            days = '29'
        else:
            days = '28'
    elif mese in ('01', '03', '05', '07', '08', '10', '12'):
        days = '31'
    else:
        raise TypeError
    return days


def get_dates(yyyymm):
    if len(yyyymm) != 6:
        raise TypeError
    mm = yyyymm[4:6]
    yyyy = yyyymm[0:4]

    if mm == '01':
        month = '12'
        year = str(int(yyyy)-1)
    else:
        month = str(int(mm)-1).zfill(2)
        year = yyyy
    last_day = month_days(month, year)

    start_date = '%s-%s-%s' % (year, month, '01')
    end_date = '%s-%s-%s' % (year, month, last_day)

    return end_date, start_date
