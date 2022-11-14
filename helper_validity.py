import datetime

# Has helper functions to check string validity, etc.

def is_month(s, return_format=False):
    months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
    for month in months:
        if month in s.lower():
            return "%b" if return_format else True
    if s.isdecimal():
        if int(s) > 0 and int(s) < 13:
            return "%m" if return_format else True
    return False

def is_date(s, return_format=False):
    if s.isdecimal():
        if int(s) > 0 and int(s) < 32:
            return "%d" if return_format else True
    return False

def is_year(s, return_format=False):
    if len(s) == 2 and s.isdecimal():
        return "%y" if return_format else True
    if len(s) == 4 and s.isdecimal():
        if int(s) >= 1900 and int(s) < 3000:
            return "%Y" if return_format else True
    return False

def is_valid_date(d, return_value=False):
    separators = ["-", "/", " "]
    for separator in separators:
        c = d.split(separator)
        if len(c) == 3:
            if is_date(c[0]) and is_month(c[1]) and is_year(c[2]):
                f = is_date(c[0], return_format=True) + separator + is_month(c[1], return_format=True) + separator + is_year(c[2], return_format=True)
                dt = datetime.datetime.strptime(d, f)
                return dt if return_value else True
            if is_date(c[1]) and is_month(c[0]) and is_year(c[2]):
                f = is_date(c[1], return_format=True) + separator + is_month(c[0], return_format=True) + separator + is_year(c[2], return_format=True)
                dt = datetime.datetime.strptime(d, f)
                return dt if return_value else True
            if is_date(c[2]) and is_month(c[1]) and is_year(c[0]):
                f = is_year(c[0], return_format=True) + separator + is_month(c[1], return_format=True) + separator + is_date(c[2], return_format=True)
                dt = datetime.datetime.strptime(d, f)
                return dt if return_value else True
        if len(c) == 2:
            if is_date(c[0]) and is_month(c[1]):
                f = is_date(c[0], return_format=True) + separator + is_month(c[1], return_format=True)
                dt = datetime.datetime.strptime(d, f)
                return dt if return_value else True
            if is_date(c[1]) and is_month(c[0]):
                f = is_date(c[1], return_format=True) + separator + is_month(c[0], return_format=True)
                dt = datetime.datetime.strptime(d, f)
                return dt if return_value else True
    return False

def is_valid_amount(a, return_value=False):
    a = a.replace(",", "")
    a = a.replace("₹", "")
    try:
        r = float(a)
        return r if return_value else True
    except ValueError:
        return False
