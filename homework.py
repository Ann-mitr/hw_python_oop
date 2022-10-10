from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        message = (f'Тип тренировки: {self.training_type}; '
                   f'Длительность: {self.duration:.3f} ч.; '
                   f'Дистанция: {self.distance:.3f} км; '
                   f'Ср. скорость: {self.speed:.3f} км/ч; '
                   f'Потрачено ккал: {self.calories:.3f}.')
# Числовые значения должны округляться при выводе до тысячных долей
# (до третьего знака после запятой).
        return message


class Training:
    """Базовый класс тренировки."""
    """
    Базовый класс
    В классах, описывающих любой из видов тренировки, применяются одни и те же
    свойства и методы. Чтобы избежать дублирования кода, необходимо создать
    базовый класс Training. Он должен содержать все основные свойства и методы
    для тренировок. Каждый класс, описывающий определённый вид тренировки,
    будет дополнять и расширять базовый класс.
    """

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        """Возвращает дистанцию (в километрах), которую преодолел пользователь
        за время тренировки."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        """Возвращает значение средней скорости движения во время тренировки.
        """
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        """
        Возвращает количество килокалорий, израсходованных за время тренировки.
        Логика подсчета калорий для каждого вида тренировки будет своя,
        поэтому в базовом классе не нужно описывать поведение метода, в его
        теле останется ключевое слово pass."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        """Информационное сообщение о тренировке."""
        info = InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())
        return info


class Running(Training):
    """Тренировка: бег."""
    coeff_calorie_1: int = 18
    coeff_calorie_2: int = 20

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        middle_speed = self.get_mean_speed()
        time_in_minute = self.duration * 60
        spent_calories = ((self.coeff_calorie_1 * middle_speed
                          - self.coeff_calorie_2)
                          * self.weight / self.M_IN_KM * time_in_minute)
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    coeff_calorie_3: float = 0.035
    coeff_calorie_4: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        middle_speed = self.get_mean_speed()
        time_in_minute = self.duration * 60
        spent_calories = ((self.coeff_calorie_3 * self.weight
                          + (middle_speed**2 // self.height)
                          * self.coeff_calorie_4 * self.weight)
                          * time_in_minute)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    coeff_calorie_5: float = 1.1
    coeff_calorie_6: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        """Возвращает дистанцию (в километрах), которую преодолел пользователь
        за время тренировки."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        middle_speed = (self.length_pool * self.count_pool
                        / self.M_IN_KM / self.duration)
        return middle_speed

    def get_spent_calories(self):
        spent_calories = ((self.get_mean_speed() + self.coeff_calorie_5)
                          * self.coeff_calorie_6 * self.weight)
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_dist = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return training_dist[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    show = training.show_training_info()
    print(show.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)