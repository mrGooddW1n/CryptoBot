# -*- coding: utf-8 -*-
import zk
from datetime import datetime
import time

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
                print("Успешное подключение к контроллеру {}".format(self.ip_address))
                return True
            else:
                print("Ошибка подключения к контроллеру")
                return False
        except Exception as e:
            print("Ошибка подключения: {}".format(str(e)))
            return False
    
    def disconnect(self):
        """Разрыв соединения с контроллером"""
        try:
            if self.conn:
                self.conn.disconnect()
                print("Соединение с контроллером закрыто")
        except Exception as e:
            print("Ошибка при отключении: {}".format(str(e)))
    
    def unlock_door(self, door_number=1, duration=5):
        """Открытие двери на указанное время"""
        try:
            if self.conn.unlock(door_number, duration):
                print("Дверь {} открыта на {} секунд".format(door_number, duration))
                return True
            else:
                print("Не удалось открыть дверь {}".format(door_number))
                return False
        except Exception as e:
            print("Ошибка при открытии двери: {}".format(str(e)))
            return False
    
    def lock_door(self, door_number=1):
        """Принудительное закрытие двери"""
        try:
            if self.conn.lock(door_number):
                print("Дверь {} закрыта".format(door_number))
                return True
            else:
                print("Не удалось закрыть дверь {}".format(door_number))
                return False
        except Exception as e:
            print("Ошибка при закрытии двери: {}".format(str(e)))
            return False
    
    def enable_reader(self, reader_number=1):
        """Активация считывателя"""
        try:
            if self.conn.enable_device():
                print("Считыватель {} активирован".format(reader_number))
                return True
            else:
                print("Не удалось активировать считыватель {}".format(reader_number))
                return False
        except Exception as e:
            print("Ошибка при активации считывателя: {}".format(str(e)))
            return False
    
    def disable_reader(self, reader_number=1):
        """Деактивация считывателя"""
        try:
            if self.conn.disable_device():
                print("Считыватель {} деактивирован".format(reader_number))
                return True
            else:
                print("Не удалось деактивировать считыватель {}".format(reader_number))
                return False
        except Exception as e:
            print("Ошибка при деактивации считывателя: {}".format(str(e)))
            return False
    
    def get_attendance_logs(self):
        """Получение журнала событий"""
        try:
            logs = self.conn.get_attendance()
            if logs:
                print("Получено {} записей:".format(len(logs)))
                for log in logs:
                    print("ID: {}, Время: {}, Статус: {}".format(
                        log.user_id, log.timestamp, log.status))
                return logs
            else:
                print("Журнал событий пуст или не получен")
                return None
        except Exception as e:
            print("Ошибка при получении журнала: {}".format(str(e)))
            return None
    
    def add_user(self, user_id, name, privilege=0, password=''):
        """Добавление нового пользователя"""
        try:
            if self.conn.set_user(uid=user_id, name=name, privilege=privilege, password=password):
                print("Пользователь {} (ID: {}) успешно добавлен".format(name, user_id))
                return True
            else:
                print("Не удалось добавить пользователя {}".format(name))
                return False
        except Exception as e:
            print("Ошибка при добавлении пользователя: {}".format(str(e)))
            return False
    
    def delete_user(self, user_id):
        """Удаление пользователя"""
        try:
            if self.conn.delete_user(user_id):
                print("Пользователь с ID {} удален".format(user_id))
                return True
            else:
                print("Не удалось удалить пользователя с ID {}".format(user_id))
                return False
        except Exception as e:
            print("Ошибка при удалении пользователя: {}".format(str(e)))
            return False
    
    def set_time(self):
        """Установка времени на контроллере"""
        try:
            current_time = datetime.now()
            if self.conn.set_time(current_time):
                print("Время на контроллере установлено: {}".format(current_time))
                return True
            else:
                print("Не удалось установить время на контроллере")
                return False
        except Exception as e:
            print("Ошибка при установке времени: {}".format(str(e)))
            return False
    
    def get_time(self):
        """Получение времени с контроллера"""
        try:
            device_time = self.conn.get_time()
            if device_time:
                print("Текущее время контроллера: {}".format(device_time))
                return device_time
            else:
                print("Не удалось получить время с контроллера")
                return None
        except Exception as e:
            print("Ошибка при получении времени: {}".format(str(e)))
            return None

# Пример использования
if __name__ == "__main__":
    controller = ZKtecoInBio460Controller("192.168.1.201")
    
    if controller.connect():
        # Управление дверьми
        controller.unlock_door(door_number=1, duration=5)
        time.sleep(5)
        controller.lock_door(door_number=1)
        
        # Управление считывателями
        controller.enable_reader(reader_number=1)
        
        # Работа с пользователями
        controller.add_user(123, u"Иванов Иван", 0, "1234")
        
        # Получение журнала событий
        logs = controller.get_attendance_logs()
        
        # Управление временем
        controller.set_time()
        controller.get_time()
        
        # Отключение
        controller.disconnect()
