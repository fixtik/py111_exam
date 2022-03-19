from time import perf_counter


def timeit(func):
    def wrapper(*args, **kwargs):
        t1_start = perf_counter()
        result = func(*args, **kwargs)
        t1_stop = perf_counter()
        time_to_recognition = round(t1_stop - t1_start, 6)
        print(f'run {func.__name__} in: {time_to_recognition} s \n')
        return result

    return wrapper


def benchmark(iters):
    def actual_decorator(func):
        def wrapper(*args, **kwargs):
            total = 0
            for i in range(iters):
                start = perf_counter()
                return_value = func(*args, **kwargs)
                end = perf_counter()
                total = total + (end-start)
            print('[*] Среднее время выполнения: {} секунд.'.format(total/iters))
            return return_value

        return wrapper
    return actual_decorator


# @benchmark(iters=10)
# def fetch_webpage(url):
#     import requests
#     webpage = requests.get(url)
#     return webpage.text
