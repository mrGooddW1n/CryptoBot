import zklib
import time
from datetime import datetime

class ZKtecoInBio460Controller:
    def __init__(self, ip_address, port=4370, timeout=5):
        self.ip_address = ip_address
        self.port = port
        self.timeout = timeout
        self.zk = zklib.ZKLib(ip_address, port, timeout)
        
    def connect(self):
        """Установка соединения с контроллером"""
        try:
            conn = self.zk.connect()
            if conn:
                print(f"Успешное подключение к контроллеру {self.ip_address}")
                return True
            else:
                print("Ошибка подключения к контроллеру")
                return False
        except Exception as e:
            print(f"Ошибка подключения: {str(e)}")
            return False
    
    def disconnect(self):
        """Разрыв соединения с контроллером"""
        try:
            self.zk.disconnect()
            print("Соединение с контроллером закрыто")
        except Exception as e:
            print(f"Ошибка при отключении: {str(e)}")
    
    def unlock_door(self, door_number=1, duration=5):
        """Открытие двери на указанное время"""
        try:
            if self.zk.unlock(door_number, duration):
                print(f"Дверь {door_number} открыта на {duration} секунд")
                return True
            else:
                print(f"Не удалось открыть дверь {door_number}")
                return False
        except Exception as e:
            print(f"Ошибка при открытии двери: {str(e)}")
            return False
    
    def lock_door(self, door_number=1):
        """Принудительное закрытие двери"""
        try:
            if self.zk.lock(door_number):
                print(f"Дверь {door_number} закрыта")
                return True
            else:
                print(f"Не удалось закрыть дверь {door_number}")
                return False
        except Exception as e:
            print(f"Ошибка при закрытии двери: {str(e)}")
            return False
    
    def enable_reader(self, reader_number=1):
        """Активация считывателя"""
        try:
            if self.zk.enable_device(reader_number):
                print(f"Считыватель {reader_number} активирован")
                return True
            else:
                print(f"Не удалось активировать считыватель {reader_number}")
                return False
        except Exception as e:
            print(f"Ошибка при активации считывателя: {str(e)}")
            return False
    
    def disable_reader(self, reader_number=1):
        """Деактивация считывателя"""
        try:
            if self.zk.disable_device(reader_number):
                print(f"Считыватель {reader_number} деактивирован")
                return True
            else:
                print(f"Не удалось деактивировать считыватель {reader_number}")
                return False
        except Exception as e:
            print(f"Ошибка при деактивации считывателя: {str(e)}")
            return False
    
    def get_attendance_logs(self):
        """Получение журнала событий"""
        try:
            logs = self.zk.get_attendance()
            if logs:
                print(f"Получено {len(logs)} записей:")
                for log in logs:
                    print(f"ID: {log['user_id']}, Время: {log['timestamp']}, Статус: {log['status']}")
                return logs
            else:
                print("Журнал событий пуст или не получен")
                return None
        except Exception as e:
            print(f"Ошибка при получении журнала: {str(e)}")
            return None
    
    def add_user(self, user_id, name, privilege=0, password=''):
        """Добавление нового пользователя"""
        try:
            if self.zk.set_user(user_id, name, privilege, password):
                print(f"Пользователь {name} (ID: {user_id}) успешно добавлен")
                return True
            else:
                print(f"Не удалось добавить пользователя {name}")
                return False
        except Exception as e:
            print(f"Ошибка при добавлении пользователя: {str(e)}")
            return False
    
    def delete_user(self, user_id):
        """Удаление пользователя"""
        try:
            if self.zk.delete_user(user_id):
                print(f"Пользователь с ID {user_id} удален")
                return True
            else:
                print(f"Не удалось удалить пользователя с ID {user_id}")
                return False
        except Exception as e:
            print(f"Ошибка при удалении пользователя: {str(e)}")
            return False
    
    def set_time(self):
        """Установка времени на контроллере"""
        try:
            current_time = datetime.now()
            if self.zk.set_time(current_time):
                print(f"Время на контроллере установлено: {current_time}")
                return True
            else:
                print("Не удалось установить время на контроллере")
                return False
        except Exception as e:
            print(f"Ошибка при установке времени: {str(e)}")
            return False
    
    def get_time(self):
        """Получение времени с контроллера"""
        try:
            device_time = self.zk.get_time()
            if device_time:
                print(f"Текущее время контроллера: {device_time}")
                return device_time
            else:
                print("Не удалось получить время с контроллера")
                return None
        except Exception as e:
            print(f"Ошибка при получении времени: {str(e)}")
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
        controller.add_user(123, "Иванов Иван", 0, "1234")
        
        # Получение журнала событий
        logs = controller.get_attendance_logs()
        
        # Управление временем
        controller.set_time()
        controller.get_time()
        
        # Отключение
        controller.disconnect()
