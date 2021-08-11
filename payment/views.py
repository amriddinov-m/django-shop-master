import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from jsonrpcserver import methods, dispatch
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from jsonrpcserver.exceptions import InvalidRequest
from rest_framework.views import APIView

from order.models import Order
from other.views import CustomPagination
from payment.actions import is_expired, datetime2timestamp, timestamp2datetime
from payment.models import Payment, Transaction
from payment.serializer import PaymentSerializer
from datetime import datetime
from payment.consts import *


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]


# region PAYCOM JSONRPC ENDPOINT



@methods.add
@csrf_exempt
def ping(**kwargs):
    print('asd')
    return 'pong'


@methods.add
@csrf_exempt
def create_transaction(**kwargs):
    if 'order_id' in kwargs['account']:
        order_id = kwargs['account']['order_id']
    else:
        order_id = ''
    if 'id' in kwargs:
        transaction_id = kwargs['id']
    else:
        transaction_id = ''
    if 'time' in kwargs:
        _time = kwargs['time']
    if 'amount' in kwargs:
        amount = kwargs['amount']
    try:
        transaction = Transaction.objects.get(paycom_transaction_id=transaction_id)
        if transaction.state == STATE_CREATED:
            if not is_expired(transaction):
                result = {
                    'state': transaction.state,
                    'create_time': datetime2timestamp(transaction.create_time.astimezone()),
                    'transaction': transaction.paycom_transaction_id,
                }
                return result
            else:
                error_message = {
                    "ru": "Ошибка, Время заказа истекло",
                    "uz": "Xatolik, Buyurtma to'lov vaqti o'tdi",
                    "en": "Error, Order expired",
                }
                InvalidRequest.code = ERROR_COULD_NOT_PERFORM
                InvalidRequest.message = error_message
                raise InvalidRequest()
        else:
            error_message = {
                "ru": "Ошибка, Заказ уже оплачен или отменен",
                "uz": "Xatolik, Buyurtma to'langan yoki bekor qilingan",
                "en": "Error, Order payed or canceled",
            }
            InvalidRequest.code = ERROR_COULD_NOT_PERFORM
            InvalidRequest.message = error_message
            raise InvalidRequest()
    except Transaction.DoesNotExist:
        try:
            payment = Payment.objects.get(pk=order_id)
            if amount != payment.total:
                error_message = {
                    "ru": "Ошибка, Суммы не совпадают",
                    "uz": "Xatolik, To'lov narxi farqlanadi",
                    "en": "Error, Amount is wrong",
                }
                InvalidRequest.code = ERROR_INVALID_AMOUNT
                InvalidRequest.message = error_message
                raise InvalidRequest()
            if payment.transaction_set.count() > 0:
                error_message = {
                    "ru": "Ошибка, Заказ уже имеет транзакцию",
                    "uz": "Xatolik, Buyurtma tranzaksiyasi mavjud",
                    "en": "Error, Order already has transaction",
                }
                InvalidRequest.code = ERROR_INVALID_ACCOUNT
                InvalidRequest.message = error_message
                raise InvalidRequest()
            if 'allow' in check_perform_transaction(**kwargs):
                transaction = Transaction()
                transaction.paycom_transaction_id = transaction_id
                transaction.paycom_time = _time
                transaction.paycom_time_datetime = timestamp2datetime(_time)
                transaction.create_time = datetime.now()
                transaction.amount = amount
                transaction.state = STATE_CREATED
                transaction.save()
                payment.transaction.add(transaction)
                payment.save()
                result = {
                    'state': transaction.state,
                    'create_time': datetime2timestamp(transaction.create_time.astimezone()),
                    'transaction': transaction.paycom_transaction_id,
                }
                return result
            else:
                error_message = {
                    "ru": "Заказ не существует",
                    "uz": "Buyurtma topilmadi",
                    "en": "Order not found",
                }
                InvalidRequest.code = ERROR_COULD_NOT_PERFORM
                InvalidRequest.message = error_message
                raise InvalidRequest()
        except Payment.DoesNotExist:
            error_message = {
                "ru": "Заказ не существует",
                "uz": "Buyurtma topilmadi",
                "en": "Order not found",
            }
            InvalidRequest.code = ERROR_INVALID_ACCOUNT
            InvalidRequest.message = error_message
            raise InvalidRequest()


@methods.add_method
@csrf_exempt
def check_perform_transaction(**kwargs):
    if 'order_id' in kwargs['account']:
        order_id = kwargs['account']['order_id']
    if 'amount' in kwargs:
        amount = kwargs['amount']
    try:
        payment = Payment.objects.get(pk=order_id)
        if payment.state == STATE_CREATED:
            if payment.total == amount:
                result = {
                    'allow': True
                }
                return result
            else:
                error_message = {
                    "ru": "Ошибка Суммы не совпадают",
                    "uz": "Xatolik, To'lov narxi farqlanadi",
                    "en": "Error, wrong amount",
                }
                InvalidRequest.code = ERROR_INVALID_AMOUNT
                InvalidRequest.message = error_message
                raise InvalidRequest()
        else:
            error_message = {
                "ru": "Ошибка",
                "uz": "Xatolik",
                "en": "Error",
            }
            InvalidRequest.code = ERROR_INVALID_ACCOUNT
            InvalidRequest.message = error_message
            raise InvalidRequest()
    except Payment.DoesNotExist:
        error_message = {
            "ru": "Заказ не существует",
            "uz": "Buyurtma topilmadi",
            "en": "Order not found",
        }
        InvalidRequest.code = ERROR_INVALID_ACCOUNT
        InvalidRequest.message = error_message
        raise InvalidRequest()


@methods.add_method
@csrf_exempt
def check_transaction(**kwargs):
    if 'id' in kwargs:
        transaction_id = kwargs['id']
    try:
        transaction = Transaction.objects.get(paycom_transaction_id=transaction_id)
        result = {
            'create_time': datetime2timestamp(transaction.create_time.astimezone()) if transaction.create_time != None else 0,
            'perform_time': datetime2timestamp(transaction.perform_time.astimezone()) if transaction.perform_time != None else 0,
            'cancel_time': datetime2timestamp(transaction.cancel_time.astimezone()) if transaction.cancel_time != None else 0,
            'transaction': transaction.paycom_transaction_id,
            'reason': transaction.reason if not None else 0,
            'state': transaction.state,
        }
        return result
    except Transaction.DoesNotExist:
        result = {
            'error': ERROR_TRANSACTION_NOT_FOUND
        }
        return result


@methods.add_method
@csrf_exempt
def perform_transaction(**kwargs):
    if 'id' in kwargs:
        transaction_id = kwargs['id']
    else:
        transaction_id = ''
    try:
        transaction = Transaction.objects.get(paycom_transaction_id=transaction_id)
        if transaction.state == STATE_CREATED:
            if not is_expired(transaction):
                transaction.state = STATE_COMPLETED
                transaction.perform_time = datetime.now()
                transaction.save()
                payment = Payment.objects.get(transaction=transaction)
                payment.state = STATE_COMPLETED
                result = {
                    'state': transaction.state,
                    'perform_time': datetime2timestamp(transaction.perform_time.astimezone()),
                    'transaction': transaction.paycom_transaction_id,
                }
                return result
            else:
                transaction.state = STATE_CANCELLED
                transaction.cancel_time = datetime.now()
                transaction.reason = REASON_CANCELLED_BY_TIMEOUT
                transaction.save()
                error_message = {
                    "ru": "Транзакция отменена по истечение срока",
                    "uz": "Tranzaksiya bekor qilindi vaqt o'tgani sabab",
                    "en": "Transaction canceled, Timeout",
                }
                InvalidRequest.code = ERROR_COULD_NOT_PERFORM
                InvalidRequest.message = error_message
                raise InvalidRequest()
        elif transaction.state == STATE_COMPLETED:
            result = {
                'state': transaction.state,
                'perform_time': datetime2timestamp(transaction.perform_time.astimezone()),
                'transaction': transaction.paycom_transaction_id,
            }
            return result
        else:
            error_message = {
                "ru": "Транзакция отменена по истечение срока",
                "uz": "Tranzaksiya bekor qilindi vaqt o'tgani sabab",
                "en": "Transaction canceled, Timeout",
            }
            InvalidRequest.code = ERROR_COULD_NOT_PERFORM
            InvalidRequest.message = error_message
            raise InvalidRequest()
    except Transaction.DoesNotExist:
        error_message = {
            "ru": "Транзакция не существует",
            "uz": "Tranzaksiya topilmadi",
            "en": "Transaction not found",
        }
        InvalidRequest.code = ERROR_TRANSACTION_NOT_FOUND
        InvalidRequest.message = error_message
        raise InvalidRequest()


@methods.add_method
@csrf_exempt
def cancel_transaction(**kwargs):
    if 'id' in kwargs:
        transaction_id = kwargs['id']
    else:
        transaction_id = ''
    if 'reason' in kwargs:
        reason = kwargs['reason']
    try:
        transaction = Transaction.objects.get(paycom_transaction_id=transaction_id)
        if transaction.state == STATE_CREATED:
            transaction.state = STATE_CANCELLED
            transaction.cancel_time = datetime.now()
            transaction.reason = reason
            transaction.save()
            payment = Payment.objects.get(transaction=transaction)
            payment.state = transaction.state
            payment.save()
            result = {
                'state': transaction.state,
                'cancel_time': datetime2timestamp(transaction.cancel_time.astimezone()),
                'transaction': transaction.paycom_transaction_id,
            }
            return result
        elif transaction.state == STATE_COMPLETED:
            transaction.state = STATE_CANCELLED_AFTER_COMPLETE
            transaction.cancel_time = datetime.now()
            transaction.reason = reason
            transaction.save()
            payment = Payment.objects.get(transaction=transaction)
            payment.state = transaction.state
            payment.save()
            result = {
                'state': transaction.state,
                'cancel_time': datetime2timestamp(transaction.cancel_time.astimezone()),
                'transaction': transaction.paycom_transaction_id,
            }
            return result
        else:
            result = {
                'state': transaction.state,
                'cancel_time': datetime2timestamp(transaction.cancel_time.astimezone()),
                'transaction': transaction.paycom_transaction_id,
            }
            return result
    except Transaction.DoesNotExist:
        error_message = {
            "ru": "Транзакция не существует",
            "uz": "Tranzaksiya topilmadi",
            "en": "Transaction not found",
        }
        InvalidRequest.code = ERROR_TRANSACTION_NOT_FOUND
        InvalidRequest.message = error_message
        raise InvalidRequest()


if __name__ == '__main__':
    methods.serve_forever()


@csrf_exempt
def jsonrpc(request):
    try:
        decoded_json = json.loads(request.body.decode())
        print(request.body.decode())
        response = methods.dispatch(request.body.decode(), context={'context': decoded_json})
        return JsonResponse(response, status=response.http_status)
    except Exception as ex:
        print('asd')
        print(ex)
        return JsonResponse({'Error': True})
#endregions


# region Apelsin ENDPOINT

class ApelsinEndPoint(APIView):

    @csrf_exempt
    def post(self, request):
        try:
            order_id = request.data['order_id']
            user_id = request.data['user_id']
            payment_aggregator = request.data['payment_aggregator']
            amount = request.data['amount']
            transaction_id = request.data['transactionId']
            order = Order.objects.get(pk=order_id)
            order.is_paid = True
            order.save()
            payment = Payment()
            payment.order_id = order_id
            payment.amount = amount
            payment.payment_aggregator = payment_aggregator
            payment.payment_type = 'card'
            payment.save()
            return JsonResponse({'status': True})
        except Exception as ex:
            print(ex)
            return JsonResponse({'status': False})

            pass


# endregion
