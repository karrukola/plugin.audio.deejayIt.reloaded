"""
Translate the month name (string) to its corresponding number.
Strings are written in Italian since this module is used to parse Radio Deejay's
website (www.deejay.it).
"""
def month_to_num(date):
    """
    Return the month number given the Italian month name
    """
    return{
    'Gennaio' : 1,
    'Febbraio' : 2,
    'Marzo' : 3,
    'Aprile' : 4,
    'Maggio' : 5,
    'Giugno' : 6,
    'Luglio' : 7,
    'Agosto' : 8,
    'Settembre' : 9,
    'Ottobre' : 10,
    'Novembre' : 11,
    'Dicembre' : 12
    }[date]
