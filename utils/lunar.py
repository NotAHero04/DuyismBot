"""
(c) 2006 Ho Ngoc Duc.
Astronomical algorithms
from the book "Astronomical Algorithms" by Jean Meeus, 1998
"""

import datetime
import math


def jd_from_date(dd, mm, yy):
    """def jdFromDate(dd, mm, yy): Compute the (integral) Julian day number of day dd/mm/yyyy, i.e., the number of
    days between 1/1/4713 BC (Julian calendar) and dd/mm/yyyy."""
    a = int((14 - mm) / 12.)
    y = yy + 4800 - a
    m = mm + 12 * a - 3
    jd = dd + int((153 * m + 2) / 5.) + 365 * y + int(y / 4.) - int(y / 100.) + int(y / 400.) - 32045
    if jd < 2299161:
        jd = dd + int((153 * m + 2) / 5.) + 365 * y + int(y / 4.) - 32083
    return jd


def jd_to_date(jd):
    """def jdToDate(jd): Convert a Julian day number to day/month/year. jd is an integer."""
    if jd > 2299160:
        # After 5/10/1582, Gregorian calendar
        a = jd + 32044
        b = int((4 * a + 3) / 146097.)
        c = a - int((b * 146097) / 4.)
    else:
        b = 0
        c = jd + 32082
    d = int((4 * c + 3) / 1461.)
    e = c - int((1461 * d) / 4.)
    m = int((5 * e + 2) / 153.)
    day = e - int((153 * m + 2) / 5.) + 1
    month = m + 3 - 12 * int(m / 10.)
    year = b * 100 + d - 4800 + int(m / 10.)
    return [day, month, year]


def new_moon(k):
    """def NewMoon(k): Compute the time of the k-th new moon after the new moon of 1/1/1900 13:52 UCT (measured as
    the number of days since 1/1/4713 BC noon UCT), e.g., 2451545.125 is 1/1/2000 15:00 UTC. Returns a floating
    number, e.g., 2415079.9758617813 for k=2 or 2414961.935157746 for k=-2."""
    # Time in Julian centuries from 1900 January 0.5
    t = k / 1236.85
    t2 = t * t
    t3 = t2 * t
    dr = math.pi / 180.
    jd1 = 2415020.75933 + 29.53058868 * k + 0.0001178 * t2 - 0.000000155 * t3 + 0.00033 * math.sin(
        (166.56 + 132.87 * t - 0.009173 * t2) * dr)
    # Mean new moon
    m = 359.2242 + 29.10535608 * k - 0.0000333 * t2 - 0.00000347 * t3
    # Sun's mean anomaly
    mpr = 306.0253 + 385.81691806 * k + 0.0107306 * t2 + 0.00001236 * t3
    # Moon's mean anomaly
    f = 21.2964 + 390.67050646 * k - 0.0016528 * t2 - 0.00000239 * t3
    # Moon's argument of latitude
    c1 = (0.1734 - 0.000393 * t) * math.sin(m * dr) + 0.0021 * math.sin(2 * dr * m) - 0.4068 * math.sin(mpr * dr) \
        + 0.0161 * math.sin(dr * 2 * mpr) - 0.0004 * math.sin(dr * 3 * mpr) + 0.0104 * math.sin(dr * 2 * f) \
        - 0.0051 * math.sin(dr * (m + mpr)) - 0.0074 * math.sin(dr * (m - mpr)) + 0.0004 * math.sin(dr * (2 * f + m)) \
        - 0.0004 * math.sin(dr * (2 * f - m)) - 0.0006 * math.sin(
        dr * (2 * f + mpr)) + 0.0010 * math.sin(dr * (2 * f - mpr)
                                                ) \
        + 0.0005 * math.sin(dr * (2 * mpr + m))
    if t < -11:
        delta_t = 0.001 + 0.000839 * t + 0.0002261 * t2 - 0.00000845 * t3 - 0.000000081 * t * t3
    else:
        delta_t = -0.000278 + 0.000265 * t + 0.000262 * t2
    jd_new = jd1 + c1 - delta_t
    return jd_new


def sun_longitude(jdn):
    """def SunLongitude(jdn): Compute the longitude of the sun at any time. Parameter: floating number jdn,
    the number of days since 1/1/4713 BC noon."""
    t = (jdn - 2451545.0) / 36525.
    # Time in Julian centuries
    # from 2000-01-01 12:00:00 GMT
    t2 = t * t
    dr = math.pi / 180.  # degree to radian
    m = 357.52910 + 35999.05030 * t \
        - 0.0001559 * t2 - 0.00000048 * t * t2
    # mean anomaly, degree
    l0 = 280.46645 + 36000.76983 * t + 0.0003032 * t2
    # mean longitude, degree
    dl = (1.914600 - 0.004817 * t - 0.000014 * t2) * math.sin(dr * m)
    dl += (0.019993 - 0.000101 * t) * math.sin(dr * 2 * m) + 0.000290 * math.sin(dr * 3 * m)
    long = (l0 + dl) * dr
    long = long - math.pi * 2 * (int(long / (math.pi * 2)))
    # Normalize to (0, 2*math.pi)
    return long


def get_sun_longitude(day_number, time_zone):
    """def getSunLongitude(dayNumber, timeZone):  Compute sun position at midnight of the day with the given Julian
    day number. The time zone if the time difference between local time and UTC: 7.0 for UTC+7:00. The function
    returns a number between 0 and 11.  From the day after March equinox and the 1st major term after March equinox,
    0 is returned. After that, return 1, 2, 3 ..."""
    return int(
        sun_longitude(day_number - 0.5 - time_zone / 24.)
        / math.pi * 6)


def get_new_moon_day(k, time_zone):
    """def getNewMoonDay(k, timeZone): Compute the day of the k-th new moon in the given time zone. The time zone if
    the time difference between local time and UTC: 7.0 for UTC+7:00."""
    return int(new_moon(k) + 0.5 + time_zone / 24.)


def get_lunar_month_11(yy, time_zone):
    """def getLunarMonth11(yy, timeZone):  Find the day that starts the lunar month 11of the given year for the given
    time zone."""
    # off = jdFromDate(31, 12, yy) \
    #            - 2415021.076998695
    off = jd_from_date(31, 12, yy) - 2415021.
    k = int(off / 29.530588853)
    nm = get_new_moon_day(k, time_zone)
    sun_long = get_sun_longitude(nm, time_zone)
    # sun longitude at local midnight
    if sun_long >= 9:
        nm = get_new_moon_day(k - 1, time_zone)
    return nm


def get_leap_month_offset(a11, time_zone):
    """def getLeapMonthOffset(a11, timeZone): Find the index of the leap month after the month starting on the day
    a11."""
    k = int((a11 - 2415021.076998695) / 29.530588853 + 0.5)
    i = 1  # start with month following lunar month 11
    arc = get_sun_longitude(
        get_new_moon_day(k + i, time_zone), time_zone)
    while True:
        last = arc
        i += 1
        arc = get_sun_longitude(
            get_new_moon_day(k + i, time_zone),
            time_zone)
        if not (arc != last and i < 14):
            break
    return i - 1


def S2L(dd, mm, yy, time_zone=7):
    """def S2L(dd, mm, yy, timeZone = 7): Convert solar date dd/mm/yyyy to the corresponding lunar date."""
    day_number = jd_from_date(dd, mm, yy)
    k = int((day_number - 2415021.076998695) / 29.530588853)
    month_start = get_new_moon_day(k + 1, time_zone)
    if month_start > day_number:
        month_start = get_new_moon_day(k, time_zone)
    # alert(dayNumber + " -> " + monthStart)
    a11 = get_lunar_month_11(yy, time_zone)
    b11 = a11
    if a11 >= month_start:
        lunar_year = yy
        a11 = get_lunar_month_11(yy - 1, time_zone)
    else:
        lunar_year = yy + 1
        b11 = get_lunar_month_11(yy + 1, time_zone)
    lunar_day = day_number - month_start + 1
    diff = int((month_start - a11) / 29.)
    lunar_leap = 0
    lunar_month = diff + 11
    if b11 - a11 > 365:
        leap_month_diff = get_leap_month_offset(a11, time_zone)
        if diff >= leap_month_diff:
            lunar_month = diff + 10
            if diff == leap_month_diff:
                lunar_leap = 1
    if lunar_month > 12:
        lunar_month = lunar_month - 12
    if lunar_month >= 11 and diff < 4:
        lunar_year -= 1
    return [lunar_day, lunar_month, lunar_year, lunar_leap]


def L2S(lunar_day, lunar_month, lunar_year, lunar_leap, time_zone=7):
    """def L2S(lunarD, lunarM, lunarY, lunarLeap, tZ = 7): Convert a lunar date to the corresponding solar date."""
    if lunar_month < 11:
        a11 = get_lunar_month_11(lunar_year - 1, time_zone)
        b11 = get_lunar_month_11(lunar_year, time_zone)
    else:
        a11 = get_lunar_month_11(lunar_year, time_zone)
        b11 = get_lunar_month_11(lunar_year + 1, time_zone)
    k = int(0.5 + (a11 - 2415021.076998695) / 29.530588853)
    off = lunar_month - 11
    if off < 0:
        off += 12
    if b11 - a11 > 365:
        leap_off = get_leap_month_offset(a11, time_zone)
        leap_m = leap_off - 2
        if leap_m < 0:
            leap_m += 12
        if lunar_leap != 0 and lunar_month != leap_m:
            return [0, 0, 0]
        elif lunar_leap != 0 or off >= leap_off:
            off += 1
    month_start = get_new_moon_day(k + off, time_zone)
    return jd_to_date(month_start + lunar_day - 1)


def run(date: str):
    value = ""
    res = tuple(S2L(*list(datetime.datetime.fromisoformat(date).timetuple()[:3])[::-1]))
    date = datetime.date(*reversed(res[0:3]))
    value += date.isoformat()
    if res[3] == 1:
        value += ", leap month"
    return value
