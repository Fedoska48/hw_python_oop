from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return(
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    MIN: int = 60

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
    ) -> None:
        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""
    LEN_STEP: float = 0.65
    COEF_1: float = 18
    COEF_2: float = 20

    def __init__(self, action, duration, weight):
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:

        calories_run: float = (
            (self.COEF_1
             * Training.get_mean_speed(self)
             - self.COEF_2) * self.weight
            / Training.M_IN_KM
            * (self.duration * self.MIN)
        )
        return calories_run


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    LEN_STEP: float = 0.65
    COEF_3: float = 0.035
    COEF_4: float = 0.029

    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.height: float = height

    def get_spent_calories(self) -> float:

        calories_walking = (
            (self.COEF_3 * self.weight + (
                self.get_mean_speed() ** 2 // self.height)
                * self.COEF_4 * self.weight) * (self.duration * self.MIN)
        )
        return calories_walking


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    COEF_5: float = 1.1
    COEF_6: float = 2

    def __init__(self, action, duration, weight, length_pool, count_pool):
        super().__init__(action, duration, weight)
        self.length_pool: float = length_pool
        self.count_pool: int = count_pool

    def get_spent_calories(self):
        swim_step1: float = Swimming.get_mean_speed(self) + self.COEF_5
        calories_swim: float = swim_step1 * self.COEF_6 * self.weight
        return calories_swim

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * Swimming.LEN_STEP / Training.M_IN_KM
        return distance

    def get_mean_speed(self):
        return (
            self.length_pool
            * self.count_pool / Training.M_IN_KM / self.duration
        )


def read_package(workout_type: str, _data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    types: dict = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming
    }
    if workout_type not in types:
        raise ValueError('Тип тренировки не найден')
    return types[workout_type](*_data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
