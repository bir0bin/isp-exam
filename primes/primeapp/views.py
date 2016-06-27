from django.shortcuts import render
from models import Prime, Divisor, PrimeCache, GcdCache
from django.db.models import ObjectDoesNotExist
from fractions import gcd
from json import loads, dumps


def prime_sieve(num):
    sieve = [False for _ in range(num + 1)]
    primes = []
    i = 2
    while i <= num:
        if sieve[i]:
            i += 1
            continue

        primes.append(i)
        j = i
        while j <= num:
            sieve[j] = True
            j += i

    return primes


def prime_list_cached(request, num):
    num = int(num)
    if num >= 2:
        try:
            prime_obj = PrimeCache.objects.get(n=num)
            primes = loads(prime_obj.data)
        except ObjectDoesNotExist:
            primes = prime_sieve(num)
            prime_obj = PrimeCache()
            prime_obj.data = dumps(primes)
            prime_obj.n = num
            prime_obj.save()
    else:
        primes = []

    return render(request, 'primes.html', {'primes': primes, 'num': num})


def gcd_table_cached(request, a, b):
    a, b = int(a), int(b)
    a, b = min(a, b), max(a, b)
    try:
        gcd_obj = GcdCache.objects.get(a=a, b=b)
        table = loads(gcd_obj.data)
    except ObjectDoesNotExist:
        head_row = ['X'] + range(a, b + 1)
        table = [head_row]
        for i in xrange(a, b + 1):
            row = [i]
            for j in xrange(a, b + 1):
                row.append(gcd(i, j))
            table.append(row)
        gcd_obj = GcdCache()
        gcd_obj.a = a
        gcd_obj.b = b
        gcd_obj.data = dumps(table)

    return render(request, 'gcdtable.html', {'a': a, 'b': b, 'table': table})

# Don't care about the code below this line


def prime_list(request, num):
    num = int(num)
    if num >= 2:
        check = Prime.objects.order_by('-number').first()
        if check and check.number >= num:
            primes_from_db = Prime.objects.filter(number__lte=num).order_by('number')
            primes = [x.number for x in primes_from_db]
        else:
            primes = prime_sieve(num)
            for n in primes:
                if check and n <= check.number:
                    continue
                p = Prime()
                p.number = n
                p.save()
    else:
        primes = []
    return render(request, 'primes.html', {'primes': primes, 'num': num})


def gcd_table(request, a, b):
    a, b = int(a), int(b)
    a, b = min(a, b), max(a, b)
    head_row = ['x'] + range(a, b + 1)
    table = [head_row]
    for i in xrange(a, b + 1):
        row = [i]
        for j in xrange(a, b + 1):
            try:
                result = Divisor.objects.get(a=i, b=j)
            except ObjectDoesNotExist:
                result = Divisor()
                result.a = i
                result.b = j
                result.divisor = gcd(i, j)
                result.save()
            row.append(result.divisor)
        table.append(row)
    return render(request, 'gcdtable.html', {'a': a, 'b': b, 'table': table})
