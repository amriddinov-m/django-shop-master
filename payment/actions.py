import datetime

from payment.consts import *
import time


def is_expired(transaction):
    return transaction.state == STATE_CREATED and ((datetime2timestamp(datetime.datetime.now())) - (datetime2timestamp(transaction.create_time))) > TIMEOUT


def timestamp2datetime(dt):
    if dt is not None:
        return datetime.datetime.fromtimestamp(dt / 1e3)
    else:
        return dt


def datetime2timestamp(dt):
    if dt is not None:
        return time.mktime(dt.timetuple()) * 1e3
    else:
        return dt


def set_order_complete(transaction):
    transaction.state = STATE_COMPLETED
    transaction.save()


def set_order_cancel(transaction):
    order = transaction.order
    ad = order.ad
    order.state = transaction.state
    ad.is_paid = False
    ad.is_showing = False
    ad.end_date = None
    order.save()
    ad.save()
