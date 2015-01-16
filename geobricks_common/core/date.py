import calendar
import datetime
from geobricks_common.core.log import logger

log = logger(__file__)

def get_daterange(date):
    """
    :param date: format "%dmy-%dmy" or "dmy" or "my" or "y"
    :return:
    """
    log.info(date)
    date = date.split("-")
    from_date = None
    to_date = None
    try:
        # single date (i.e. annual)
        if len(date) == 1:
            date = date[0]
            # yearly
            if len(date) == 4:
                #datetime.strptime(date, "%Y")
                from_date, to_date = get_range_dates_metadata_yearly(date)

            # monthly
            if len(date) == 6:
                from_date, to_date = get_range_dates_metadata_montly(date)

            #daily
            if len(date) == 8:
                from_date, to_date = get_range_dates_metadata_daily(date)

        # date range (i.e. 01012012-02032013)
        elif len(date) == 2:
            from_d = date[0]
            to_d = date[1]
            # yearly
            if len(from_d) == 4:
                #datetime.strptime(date, "%Y")
                from_date, to_date = get_range_from_to_dates_metadata_yearly(from_d, to_d)

                # monthly
            if len(from_d) == 6:
                from_date, to_date = get_range_from_to_dates_metadata_monthly(from_d, to_d)

                #daily
            if len(from_d) == 8:
                from_date, to_date = get_range_from_to_dates_metadata_daily(from_d, to_d)


    except Exception, e:
        log.error(e)
        pass
    finally:
        return from_date, to_date


def get_range_dates_metadata_yearly(year):
    """
    :param my: monthyear date (i.e. 2015)
    :return: the from and to date in milliseconds (i.e. 01-01-2015 to 31-12-3015
    """
    from_date = datetime.datetime(int(year), int(1), 1)
    last_day = calendar.monthrange(int(year), int(12))[1]
    to_date = datetime.datetime(int(year), int(12), last_day)
    from_date_result = calendar.timegm(from_date.timetuple()) * 1000
    to_date_result = calendar.timegm(to_date.timetuple()) * 1000
    return from_date_result, to_date_result



def get_range_dates_metadata_montly(my):
    """
    :param my: monthyear date (i.e. 012015 - january 2015)
    :return: the from and to date in milliseconds
    """
    month = int(my[:2])
    year = int(my[2:6])
    from_date = datetime.datetime(int(year), month, 1)
    last_day = calendar.monthrange(int(year), month)[1]
    to_date = datetime.datetime(int(year), int(month), last_day)
    from_date_result = calendar.timegm(from_date.timetuple()) * 1000
    to_date_result = calendar.timegm(to_date.timetuple()) * 1000
    return from_date_result, to_date_result


def get_range_dates_metadata_daily(dmy):
    """
    The from and to day returned are the same in this case
    :param dmy: daymonthyear date (i.e. 01012015 - first january 2015)
    :return:
    """
    day = int(dmy[:2])
    month = int(dmy[2:4])
    year = int(dmy[4:8])
    from_date = datetime.datetime(int(year), month, day)
    from_date_result = calendar.timegm(from_date.timetuple()) * 1000
    return from_date_result, from_date_result




def get_range_from_to_dates_metadata_yearly(from_y, to_y):
    """
    :param my: monthyear date (i.e. 2015)
    :return: the from and to date in milliseconds (i.e. 01-01-2015 to 31-12-3015
    """
    from_date = datetime.datetime(int(from_y), int(1), 1)
    last_day = calendar.monthrange(int(to_y), int(12))[1]
    to_date = datetime.datetime(int(to_y), int(12), last_day)
    from_date_result = calendar.timegm(from_date.timetuple()) * 1000
    to_date_result = calendar.timegm(to_date.timetuple()) * 1000
    return from_date_result, to_date_result


def get_range_from_to_dates_metadata_monthly(from_my, to_my):
    """
    :param my: monthyear date (i.e. 2015)
    :return: the from and to date in milliseconds (i.e. 01-01-2015 to 31-12-3015
    """
    from_month = int(from_my[:2])
    from_year = int(from_my[2:6])
    to_month = int(to_my[:2])
    to_year = int(to_my[2:6])
    from_date = datetime.datetime(int(from_year), from_month, 1)
    last_day = calendar.monthrange(int(to_year), to_month)[1]
    to_date = datetime.datetime(int(to_year), int(to_month), last_day)
    from_date_result = calendar.timegm(from_date.timetuple()) * 1000
    to_date_result = calendar.timegm(to_date.timetuple()) * 1000
    return from_date_result, to_date_result


def get_range_from_to_dates_metadata_daily(from_dmy, to_dmy):
    """
    The from and to day returned are the same in this case
    :param dmy: daymonthyear date (i.e. 01012015 - first january 2015)
    :return:
    """
    from_day = int(from_dmy[:2])
    from_month = int(from_dmy[2:4])
    from_year = int(from_dmy[4:8])
    to_day = int(to_dmy[:2])
    to_month = int(to_dmy[2:4])
    to_year = int(to_dmy[4:8])
    from_date = datetime.datetime(int(from_year), from_month, from_day)
    to_date = datetime.datetime(int(to_year), to_month, to_day)
    from_date_result = calendar.timegm(from_date.timetuple()) * 1000
    to_date_result = calendar.timegm(to_date.timetuple()) * 1000
    return from_date_result, from_date_result