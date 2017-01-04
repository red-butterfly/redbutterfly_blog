from datetime import datetime
from util.redis_util import getmyredis

VISIT_TIMEOUT = 5*60
PAGEVIEWS_KEY = 'pageviews'


def inc_pageviews(func):
    """
    to Add the pageviews for my site, the time interval is VISIT_TIMEOUT
    :param func:
    :return:
    """
    def inc_pv(request):
        if 'view_time' not in request.session:
            request.session['view_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        visittime = datetime.strptime(request.session['view_time'], '%Y-%m-%d %H:%M:%S')
        if (datetime.now() - visittime).seconds > VISIT_TIMEOUT:
            getmyredis().incr(PAGEVIEWS_KEY, amount=1)
            request.session['view_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        return func(request)

    return inc_pv

