import datetime
import calendar

from django.db.models import Q, Sum

from carService.models import Product, Car, Profile, Service, ServiceSituation, Situation, PaymentMovement, \
    CheckingAccount


def get_product_count():
    return Product.objects.filter(isDeleted=False).count()


def get_product_out_of_stock_count():
    return Product.objects.filter(isDeleted=False).filter(quantity__exact=0).count()


def get_car_count():
    return Car.objects.filter(isDeleted=False).count()


def get_customer_count():
    return Profile.objects.filter(user__groups__name__exact='Customer').count()


def get_uncompleted_services_count():
    # x = ServiceSituation.objects.all().order_by('service', '-id').distinct('service').values()
    x = ServiceSituation.objects.order_by('service', '-id').distinct('service')
    return ServiceSituation.objects.filter(id__in=x).filter(
        situation__in=Situation.objects.filter(name__exact='İşlemde')).count()


def get_waiting_approve_services_count():
    # x = ServiceSituation.objects.all().order_by('service', '-id').distinct('service').values()
    x = ServiceSituation.objects.order_by('service', '-id').distinct('service')
    return ServiceSituation.objects.filter(id__in=x).filter(
        situation__in=Situation.objects.filter(name__exact='Müşteri Onayı Bekleniyor')).count()


def get_completed_services_count():
    # x = ServiceSituation.objects.all().order_by('service', '-id').distinct('service').values()
    x = ServiceSituation.objects.order_by('service', '-id').distinct('service')
    return ServiceSituation.objects.filter(id__in=x).filter(
        situation__in=Situation.objects.filter(Q(name__exact='Tamamlandı') | Q(name__exact='Teslim Edildi'))).count()


def get_canceled_services_count():
    # x = ServiceSituation.objects.all().order_by('service', '-id').distinct('service').values()
    x = ServiceSituation.objects.order_by('service', '-id').distinct('service')
    return ServiceSituation.objects.filter(id__in=x).filter(
        situation__in=Situation.objects.filter(name__exact='İptal Edildi')).count()


def get_remain():
    # x = ServiceSituation.objects.all().order_by('service', '-id').distinct('service').values()

    return CheckingAccount.objects.filter(~Q(paymentSituation__name='Ödendi')).aggregate(
        Sum('remainingDebt'))['remainingDebt__sum']


def get_total_checking_account_for_line_chart():
    income_array = []
    today = datetime.date.today()

    for i in range(12):
        x=PaymentMovement.objects.filter(~Q(paymentType__name='İndirim')).filter(
            creationDate__month=i+1).filter(creationDate__year=today.year).aggregate(
            Sum('paymentAmount'))['paymentAmount__sum']
        if x is None:
            income_array.append(0)
        else:
            income_array.append(x)

    return income_array


def get_total_checking_account(time_type):
    today = datetime.date.today()

    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
    given_date = datetime.datetime.today().date()

    if time_type == 'monthly':

        first_day_of_month = given_date - datetime.timedelta(days=int(given_date.strftime("%d")) - 1)
        last_day_of_month = calendar.monthrange(given_date.year, given_date.month)[1]
        print(1)
        first = datetime.datetime(int(given_date.year), int(given_date.month), int(first_day_of_month.day))
        last = datetime.datetime(int(given_date.year), int(given_date.month), int(last_day_of_month))

        if PaymentMovement.objects.filter(~Q(paymentType__name='İndirim')).filter(
                creationDate__range=(first, last)).aggregate(
            Sum('paymentAmount'))['paymentAmount__sum'] is None:
            return 0
        else:
            return PaymentMovement.objects.filter(~Q(paymentType__name='İndirim')).filter(
                creationDate__range=(first, last)).aggregate(
                Sum('paymentAmount'))['paymentAmount__sum']
    elif time_type == 'daily':

        if PaymentMovement.objects.filter(~Q(paymentType__name='İndirim')).filter(
                creationDate__range=(today_min, today_max)).aggregate(
            Sum('paymentAmount'))['paymentAmount__sum'] is None:
            return 0
        else:
            return PaymentMovement.objects.filter(~Q(paymentType__name='İndirim')).filter(
                creationDate__range=(today_min, today_max)).aggregate(
                Sum('paymentAmount'))['paymentAmount__sum']



    elif time_type == 'yearly':

        first_day_of_month = given_date - datetime.timedelta(days=int(given_date.strftime("%d")) - 1)
        last_day_of_mount = calendar.monthrange(given_date.year, 12)[1]

        first = datetime.datetime(int(given_date.year), int(1), int(1))
        last = datetime.datetime(int(given_date.year), int(12), int(last_day_of_mount))

        if PaymentMovement.objects.filter(~Q(paymentType__name='İndirim')).filter(
                creationDate__range=(first, last)).aggregate(
            Sum('paymentAmount'))['paymentAmount__sum'] is None:
            return 0
        else:
            return PaymentMovement.objects.filter(~Q(paymentType__name='İndirim')).filter(
                creationDate__range=(first, last)).aggregate(
                Sum('paymentAmount'))['paymentAmount__sum']
    else:
        return 0


# Serviceman


def serviceman_get_uncompleted_services_count(user):
    profile = Profile.objects.get(user=user)
    services = Service.objects.filter(serviceman=profile).order_by('-id')
    x = ServiceSituation.objects.order_by('service', '-id').distinct('service')
    return ServiceSituation.objects.filter(id__in=x, service__in=services).filter(
        situation__in=Situation.objects.filter(Q(name__exact='İşlemde') | Q(name__exact='İşlem Bekleniyor'))).count()


def serviceman_get_completed_services_count(user):
    profile = Profile.objects.get(user=user)
    services = Service.objects.filter(serviceman=profile).order_by('-id')
    x = ServiceSituation.objects.order_by('service', '-id').distinct('service')
    return ServiceSituation.objects.filter(id__in=x, service__in=services).filter(
        situation__in=Situation.objects.filter(Q(name__exact='Tamamlandı') | Q(name__exact='Teslim Edildi'))).count()


def serviceman_get_waiting_approve_services_count(user):
    profile = Profile.objects.get(user=user)
    services = Service.objects.filter(serviceman=profile).order_by('-id')
    x = ServiceSituation.objects.order_by('service', '-id').distinct('service')
    return ServiceSituation.objects.filter(id__in=x, service__in=services).filter(
        situation__in=Situation.objects.filter(name__exact='Arıza Tespiti Bekleniyor')).count()


def serviceman_get_waiting_customer_approve_services_count(user):
    profile = Profile.objects.get(user=user)
    services = Service.objects.filter(serviceman=profile).order_by('-id')
    x = ServiceSituation.objects.order_by('service', '-id').distinct('service')
    return ServiceSituation.objects.filter(id__in=x, service__in=services).filter(
        situation__in=Situation.objects.filter(name__exact='Müşteri Onayı Bekleniyor')).count()


def serviceman_get_canceled_services_count(user):
    profile = Profile.objects.get(user=user)
    services = Service.objects.filter(serviceman=profile).order_by('-id')
    x = ServiceSituation.objects.order_by('service', '-id').distinct('service')
    return ServiceSituation.objects.filter(id__in=x, service__in=services).filter(
        situation__in=Situation.objects.filter(name__exact='İptal Edildi')).count()


# Customer

def customer_get_car_count(user):
    profile = Profile.objects.get(user=user)
    result = Car.objects.filter(isDeleted=False, profile=profile)
    return result.count()


def customer_get_uncompleted_services_count(user):
    profile = Profile.objects.get(user=user)
    cars = Car.objects.filter(profile=profile)
    services = Service.objects.filter(car__in=cars).order_by('-id')
    x = ServiceSituation.objects.order_by('service', '-id').distinct('service')
    return ServiceSituation.objects.filter(id__in=x, service__in=services).filter(
        situation__in=Situation.objects.filter(Q(name__exact='İşlemde') | Q(name__exact='İşlem Bekleniyor'))).count()


def customer_get_completed_services_count(user):
    profile = Profile.objects.get(user=user)
    cars = Car.objects.filter(profile=profile)
    services = Service.objects.filter(car__in=cars).order_by('-id')
    x = ServiceSituation.objects.order_by('service', '-id').distinct('service')
    return ServiceSituation.objects.filter(id__in=x, service__in=services).filter(
        situation__in=Situation.objects.filter(Q(name__exact='Tamamlandı') | Q(name__exact='Teslim Edildi'))).count()


def customer_get_waiting_approve_services_count(user):
    profile = Profile.objects.get(user=user)
    cars = Car.objects.filter(profile=profile)
    services = Service.objects.filter(car__in=cars).order_by('-id')
    x = ServiceSituation.objects.order_by('service', '-id').distinct('service')
    return ServiceSituation.objects.filter(id__in=x, service__in=services).filter(
        situation__in=Situation.objects.filter(name__exact='Müşteri Onayı Bekleniyor')).count()


def customer_get_canceled_services_count(user):
    profile = Profile.objects.get(user=user)
    cars = Car.objects.filter(profile=profile)
    services = Service.objects.filter(car__in=cars).order_by('-id')
    x = ServiceSituation.objects.order_by('service', '-id').distinct('service')
    return ServiceSituation.objects.filter(id__in=x, service__in=services).filter(
        situation__in=Situation.objects.filter(name__exact='İptal Edildi')).count()


def customer_get_remain(user):
    # x = ServiceSituation.objects.all().order_by('service', '-id').distinct('service').values()
    profile = Profile.objects.get(user=user)
    services = Service.objects.filter(car__in=Car.objects.filter(profile=profile))

    remain = CheckingAccount.objects.filter(service__in=services).aggregate(
        Sum('remainingDebt'))['remainingDebt__sum']

    if remain is not None:
        return remain
    else:
        return 0


def customer_get_total_checking_account(user):
    profile = Profile.objects.get(user=user)
    services = Service.objects.filter(car__in=Car.objects.filter(profile=profile))
    checking_accounts = CheckingAccount.objects.filter(service__in=services)
    if PaymentMovement.objects.filter(~Q(paymentType__name='İndirim')).filter(
            checkingAccount__in=checking_accounts).aggregate(
        Sum('paymentAmount'))['paymentAmount__sum'] is None:
        return 0
    else:
        return PaymentMovement.objects.filter(~Q(paymentType__name='İndirim')).filter(
            checkingAccount__in=checking_accounts).aggregate(
            Sum('paymentAmount'))['paymentAmount__sum']


def customer_checking_account_total(user):
    profile = Profile.objects.get(user=user)
    total = services = Service.objects.filter(car__in=Car.objects.filter(profile=profile)) \
        .aggregate(Sum('totalPrice'))['totalPrice__sum']

    if total is not None:
        return total
    else:
        return 0
