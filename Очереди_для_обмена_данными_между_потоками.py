import threading
from queue import Queue
import random
import time

class Table:
    def __init__(self, number):
        self.__number = number
        self.guest = None

    @property
    def number(self):
        return self.__number

class Guest(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.__name = name

    def run(self):
        time.sleep(random.randint(3, 10))

    @property
    def name(self):
        return self.__name

class Cafe:
    def __init__(self, *tables):
        self.queue = Queue()
        self.tables = tables

    def guest_arrival(self, *guests):
        for guest in guests:
            seated = False
            for table in self.tables:
                if table.guest is None:  # Проверяем, есть ли свободный стол
                    table.guest = guest
                    guest.start()  # Запускаем поток
                    print(f'{guest.name} сел(-а) за стол номер {table.number}')
                    seated = True
                    break
            
            if not seated:
                self.queue.put(guest)  # Ставим в очередь, если нет свободных столов
                print(f"{guest.name} в очереди")

    def discuss_guests(self):
        while not self.queue.empty() or any(table.guest is not None for table in self.tables):
            for table in self.tables:
                if table.guest is not None and not table.guest.is_alive():  # Если гость покинул стол
                    print(f"{table.guest.name} покушал(-а) и ушёл(ушла)")
                    print(f"Стол номер {table.number} свободен")
                    table.guest = None  # Освобождаем стол

                    if not self.queue.empty():  # Если есть очередь, присаживаем следующего
                        next_guest = self.queue.get()  # Берем следующего из очереди
                        table.guest = next_guest
                        next_guest.start()  # Запускаем поток следующего гостя
                        print(f"{next_guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}")
            time.sleep(1)  # Задержка, чтобы избежать излишней загрузки процессора


# Пример использования
if __name__ == "__main__":
    # Создание столов
    tables = [Table(number) for number in range(1, 6)]
    # Имена гостей
    guests_names = [
        'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 
        'Arman', 'Vitoria', 'Nikita', 'Galina', 'Pavel', 
        'Ilya', 'Alexandra'
    ]
    # Создание гостей
    guests = [Guest(name) for name in guests_names]
    # Заполнение кафе столами
    cafe = Cafe(*tables)
    # Приём гостей
    cafe.guest_arrival(*guests)
    # Обслуживание гостей
    cafe.discuss_guests()