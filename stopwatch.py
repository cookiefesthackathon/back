from time import time

'''
правила нейминга от тимофея
переменные - snake_case
константы - UPPER_CASE
классы - PascalCase
функции - camelCase
фикс метки - FIXME
'''


# функция нужна чтобы удобно ставить временные метки
# а также возвращать пройденное время в секундах
def stopWatch(time_point = None, is_return_int = False):
    if time_point:
        raw_res = time() - time_point
        #print(STOPWATCH_MARK, 'фиксация', raw_res) if LOGGING else None
        res = round(raw_res, 4)

        res = res if is_return_int else str(res) + 's'
    
        return res

    else:
        #print(STOPWATCH_MARK, 'временная отметка:', res) if LOGGING else None
        return time()


def main():

    time_point_1 = stopWatch()

    res = 0
    numbers = [n for n in range(1_000_000)]
    for i in numbers:
        res += i

    end_1 = stopWatch(time_point_1)

    print(f"Результат первого: {res}")


    time_point_2 = stopWatch()
    res = 0
    numbers = [n for n in range(1_000_000)]
    res = sum(numbers)
    end_2 = stopWatch(time_point_2)
    
    print(f"Результат второго: {res}")


    print(f"Время выполнения первого: " + end_1)
    print(f"Время выполнения второго: " + end_2)






if __name__ == '__main__':
    main()