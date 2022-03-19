from utils import benchmark
import random

# Оценить сложность приведенного ниже алгоритма:
# a = len(arr) - 1  # O(1)
# out = list()
# while a > 0:  (O(logn)
#    out.append(arr[a])
#    a = a // 1.7
# out.merge_sort().(nlogn)

# Аренда ракет Вы – компания, дающая в аренду ракеты. Каждый день к вам приходит список заявок на использование ракет
# в виде: (час_начала, час_конца), (час_начала, час_конца), ... Если аренда ракеты заканчивается в час X,
# то в этот же час ее уже можно взять в аренду снова (т.е. час_начала может начинаться с Х). Дано: список заявок на
# использование ракет Задача: вывести ответ, хватит ли вам одной ракеты, чтобы удовлетворить все заявки на этот день

def roket_sharing(order_list: list[tuple]) -> bool:
    """
    Ф-я определения достаточности 1 ракеты для удовлетворения всех заявок
    :param order_list: список заявок (start, end)
    :return: True or False
    """
    order_list.sort(key=lambda x: x[0])
    for i in range(len(order_list) - 1):
        if order_list[i][1] > order_list[i+1][0]:
            return False
    return True

# Сорт
# Дано: массив из 10**6 целых чисел, каждое из которых лежит на отрезке [13, 25].
# Задача отсортировать массив наиболее эффективным способом

@benchmark(5)
def sort_exam(arr: list[int]) -> list[int]:
    """
    Сотрировка массива-миллионника
    :param arr: неотсортированный массив
    :return: отсортированный массив
    """

    #Среднее время выполнения: 0.2966901238 секунд.
    def quicksort(container: list):
        if len(container) <= 1:
            return container
        else:
            q = random.choice(container)
        left = [n for n in container if n < q]
        equals = [q] * container.count(q)
        right = [n for n in container if n > q]
        return quicksort(left) + equals + quicksort(right)

    #Среднее время выполнения: 0.17605683500000002 секунд.
    def counter_sort(arr_: list):
        """Сортировка через подсчет количества повторяющихся значений"""
        value_in_arr = set(arr_)
        result = []
        dict_c = {}
        for value in value_in_arr:
            dict_c[value] = arr_.count(value)
        for key in dict_c.keys():
            result += [key] * dict_c[key]
        return result

    #arr.sort() [*] Среднее время выполнения: 0.018777056199999986 секунд.
    return  counter_sort(arr)



if __name__ == '__main__':

    #roket_test
    order_list_false = [(1, 3), (3, 5), (0, 1), (6, 13), (19, 21), (15, 18), (21, 24), (12, 14)]
    order_list_true = [(1, 3), (3, 5), (0, 1), (6, 9), (19, 21), (15, 18), (21, 24), (12, 14)]
    print(roket_sharing(order_list_false))

    #sort_test
    unsort = [random.randint(13, 26) for _ in range(10**6)]

    sort_exam(unsort)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
