# -*- coding: utf-8 -*-
import zk
from datetime import datetime
import time
import sys

class ZKtecoInBio460Controller:
    def __init__(self, ip_address, port=4370, timeout=5):
        self.ip_address = ip_address
        self.port = port
        self.timeout = timeout
        self.conn = None
        
    def connect(self):
        """Установка соединения с контроллером"""
        try:
            self.conn = zk.ZK(self.ip_address, port=self.port, timeout=self.timeout)
            if self.conn.connect():
                print(u"Успешное подключение к контроллеру {}".format(self.ip_address))
                return True
            else:
                print(u"Ошибка подключения к контроллеру")
                return False
        except Exception as e:
            print(u"Ошибка подключения: {}".format(str(e)))
            return False
    
    def disconnect(self):
        """Разрыв соединения с контроллером"""
        try:
            if self.conn:
                self.conn.disconnect()
                print(u"Соединение с контроллером закрыто")
        except Exception as e:
            print(u"Ошибка при отключении: {}".format(str(e)))
    
    def unlock_door(self, door_number=1, duration=5):
        """Открытие двери на указанное время"""
        try:
            if self.conn.unlock(door_number, duration):
                print(u"Дверь {} открыта на {} секунд".format(door_number, duration))
                return True
            else:
                print(u"Не удалось открыть дверь {}".format(door_number))
                return False
        except Exception as e:
            print(u"Ошибка при открытии двери: {}".format(str(e)))
            return False
    
    def lock_door(self, door_number=1):
        """Принудительное закрытие двери"""
        try:
            if self.conn.lock(door_number):
                print(u"Дверь {} закрыта".format(door_number))
                return True
            else:
                print(u"Не удалось закрыть дверь {}".format(door_number))
                return False
        except Exception as e:
            print(u"Ошибка при закрытии двери: {}".format(str(e)))
            return False
    
    def enable_reader(self, reader_number=1):
        """Активация считывателя"""
        try:
            if self.conn.enable_device():
                print(u"Считыватель {} активирован".format(reader_number))
                return True
            else:
                print(u"Не удалось активировать считыватель {}".format(reader_number))
                return False
        except Exception as e:
            print(u"Ошибка при активации считывателя: {}".format(str(e)))
            return False
    
    def disable_reader(self, reader_number=1):
        """Деактивация считывателя"""
        try:
            if self.conn.disable_device():
                print(u"Считыватель {} деактивирован".format(reader_number))
                return True
            else:
                print(u"Не удалось деактивировать считыватель {}".format(reader_number))
                return False
        except Exception as e:
            print(u"Ошибка при деактивации считывателя: {}".format(str(e)))
            return False
    
    def get_attendance_logs(self):
        """Получение журнала событий"""
        try:
            logs = self.conn.get_attendance()
            if logs:
                print(u"Получено {} записей:".format(len(logs)))
                for log in logs:
                    print(u"ID: {}, Время: {}, Статус: {}".format(
                        log.user_id, log.timestamp, log.status))
                return logs
            else:
                print(u"Журнал событий пуст или не получен")
                return None
        except Exception as e:
            print(u"Ошибка при получении журнала: {}".format(str(e)))
            return None
    
    def add_user(self, user_id, name, privilege=0, password=''):
        """Добавление нового пользователя"""
        try:
            if self.conn.set_user(uid=user_id, name=name, privilege=privilege, password=password):
                print(u"Пользователь {} (ID: {}) успешно добавлен".format(name, user_id))
                return True
            else:
                print(u"Не удалось добавить пользователя {}".format(name))
                return False
        except Exception as e:
            print(u"Ошибка при добавлении пользователя: {}".format(str(e)))
            return False
    
    def delete_user(self, user_id):
        """Удаление пользователя"""
        try:
            if self.conn.delete_user(user_id):
                print(u"Пользователь с ID {} удален".format(user_id))
                return True
            else:
                print(u"Не удалось удалить пользователя с ID {}".format(user_id))
                return False
        except Exception as e:
            print(u"Ошибка при удалении пользователя: {}".format(str(e)))
            return False
    
    def set_time(self):
        """Установка времени на контроллере"""
        try:
            current_time = datetime.now()
            if self.conn.set_time(current_time):
                print(u"Время на контроллере установлено: {}".format(current_time))
                return True
            else:
                print(u"Не удалось установить время на контроллере")
                return False
        except Exception as e:
            print(u"Ошибка при установке времени: {}".format(str(e)))
            return False
    
    def get_time(self):
        """Получение времени с контроллера"""
        try:
            device_time = self.conn.get_time()
            if device_time:
                print(u"Текущее время контроллера: {}".format(device_time))
                return device_time
            else:
                print(u"Не удалось получить время с контроллера")
                return None
        except Exception as e:
            print(u"Ошибка при получении времени: {}".format(str(e)))
            return None

def print_menu():
    """Вывод главного меню"""
    print(u"\n" + "="*50)
    print(u"Управление контроллером ZKteco InBio460")
    print(u"="*50)
    print(u"1. Управление дверьми")
    print(u"2. Управление считывателями")
    print(u"3. Управление пользователями")
    print(u"4. Работа с журналом событий")
    print(u"5. Управление временем")
    print(u"0. Выход")
    print(u"="*50)

def door_menu(controller):
    """Меню управления дверьми"""
    while True:
        print(u"\n" + "-"*50)
        print(u"Управление дверьми")
        print(u"-"*50)
        print(u"1. Открыть дверь")
        print(u"2. Закрыть дверь")
        print(u"0. Назад")
        
        choice = raw_input(u"Выберите действие: ").strip()
        
        if choice == "1":
            door = raw_input(u"Введите номер двери (по умолчанию 1): ").strip()
            duration = raw_input(u"Введите время открытия в секундах (по умолчанию 5): ").strip()
            
            door = int(door) if door.isdigit() else 1
            duration = int(duration) if duration.isdigit() else 5
            
            controller.unlock_door(door, duration)
        elif choice == "2":
            door = raw_input(u"Введите номер двери (по умолчанию 1): ").strip()
            door = int(door) if door.isdigit() else 1
            
            controller.lock_door(door)
        elif choice == "0":
            break
        else:
            print(u"Неверный выбор, попробуйте снова")

def reader_menu(controller):
    """Меню управления считывателями"""
    while True:
        print(u"\n" + "-"*50)
        print(u"Управление считывателями")
        print(u"-"*50)
        print(u"1. Активировать считыватель")
        print(u"2. Деактивировать считыватель")
        print(u"0. Назад")
        
        choice = raw_input(u"Выберите действие: ").strip()
        
        if choice == "1":
            reader = raw_input(u"Введите номер считывателя (по умолчанию 1): ").strip()
            reader = int(reader) if reader.isdigit() else 1
            
            controller.enable_reader(reader)
        elif choice == "2":
            reader = raw_input(u"Введите номер считывателя (по умолчанию 1): ").strip()
            reader = int(reader) if reader.isdigit() else 1
            
            controller.disable_reader(reader)
        elif choice == "0":
            break
        else:
            print(u"Неверный выбор, попробуйте снова")

def user_menu(controller):
    """Меню управления пользователями"""
    while True:
        print(u"\n" + "-"*50)
        print(u"Управление пользователями")
        print(u"-"*50)
        print(u"1. Добавить пользователя")
        print(u"2. Удалить пользователя")
        print(u"0. Назад")
        
        choice = raw_input(u"Выберите действие: ").strip()
        
        if choice == "1":
            user_id = raw_input(u"Введите ID пользователя: ").strip()
            name = raw_input(u"Введите имя пользователя: ").strip()
            privilege = raw_input(u"Введите уровень привилегий (0-обычный, 1-админ): ").strip()
            password = raw_input(u"Введите пароль (если требуется): ").strip()
            
            user_id = int(user_id) if user_id.isdigit() else 0
            privilege = int(privilege) if privilege.isdigit() else 0
            
            controller.add_user(user_id, name, privilege, password)
        elif choice == "2":
            user_id = raw_input(u"Введите ID пользователя для удаления: ").strip()
            user_id = int(user_id) if user_id.isdigit() else 0
            
            controller.delete_user(user_id)
        elif choice == "0":
            break
        else:
            print(u"Неверный выбор, попробуйте снова")

def log_menu(controller):
    """Меню работы с журналом событий"""
    while True:
        print(u"\n" + "-"*50)
        print(u"Журнал событий")
        print(u"-"*50)
        print(u"1. Показать журнал событий")
        print(u"0. Назад")
        
        choice = raw_input(u"Выберите действие: ").strip()
        
        if choice == "1":
            logs = controller.get_attendance_logs()
        elif choice == "0":
            break
        else:
            print(u"Неверный выбор, попробуйте снова")

def time_menu(controller):
    """Меню управления временем"""
    while True:
        print(u"\n" + "-"*50)
        print(u"Управление временем")
        print(u"-"*50)
        print(u"1. Установить время контроллера")
        print(u"2. Получить время с контроллера")
        print(u"0. Назад")
        
        choice = raw_input(u"Выберите действие: ").strip()
        
        if choice == "1":
            controller.set_time()
        elif choice == "2":
            controller.get_time()
        elif choice == "0":
            break
        else:
            print(u"Неверный выбор, попробуйте снова")

def main():
    """Главная функция программы"""
    print(u"Программа управления контроллером ZKteco InBio460")
    
    ip = raw_input(u"Введите IP-адрес контроллера (по умолчанию 192.168.1.201): ").strip()
    ip = ip if ip else "192.168.1.201"
    
    controller = ZKtecoInBio460Controller(ip)
    
    if not controller.connect():
        print(u"Не удалось подключиться к контроллеру. Программа завершена.")
        return
    
    try:
        while True:
            print_menu()
            choice = raw_input(u"Выберите раздел меню: ").strip()
            
            if choice == "1":
                door_menu(controller)
            elif choice == "2":
                reader_menu(controller)
            elif choice == "3":
                user_menu(controller)
            elif choice == "4":
                log_menu(controller)
            elif choice == "5":
                time_menu(controller)
            elif choice == "0":
                print(u"Завершение работы программы...")
                break
            else:
                print(u"Неверный выбор, попробуйте снова")
    except KeyboardInterrupt:
        print(u"\nПрограмма прервана пользователем")
    finally:
        controller.disconnect()

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    main()
