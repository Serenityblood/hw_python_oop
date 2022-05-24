from dataclasses import dataclass
from typing import Dict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
        )


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float
    M_IN_KM: float = 1000
    LEN_STEP: float = 0.65
    mins_in_hour: int = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (
            self.action
            * self.LEN_STEP
            / self.M_IN_KM
        )

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (
            self.get_distance()
            / self.duration
        )

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
    def __init__(
        self,
        action: int,
        duration: float,
        weight: float
    ):
        super().__init__(
            action,
            duration,
            weight
        )

    def get_spent_calories(self) -> float:
        duration_in_min = self.duration * self.mins_in_hour
        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        return (
            (coeff_calorie_1
             * self.get_mean_speed()
             - coeff_calorie_2
             )
            * self.weight
            / self.M_IN_KM
            * duration_in_min
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        height: float
    ):
        super().__init__(
            action,
            duration,
            weight
        )
        self.height: float = height

    def get_spent_calories(self) -> float:
        duration_in_min = self.duration * self.mins_in_hour
        coeff_calorie_1 = 0.035
        coeff_calorie_2 = 0.029
        return (
            (coeff_calorie_1
             * self.weight
             + ((self.get_mean_speed())**2
                // self.height
                )
             * coeff_calorie_2
             * self.weight
             )
            * duration_in_min
        )


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: float,
        count_pool: float
    ):
        super().__init__(
            action,
            duration,
            weight
        )
        self.length_pool: float = length_pool
        self.count_pool: float = count_pool

    def get_spent_calories(self) -> float:
        coeff_callorie_1: float = 1.1
        coeff_callorie_2: float = 2
        return (
            (self.get_mean_speed()
             + coeff_callorie_1
             )
            * coeff_callorie_2
            * self.weight
        )

    def get_mean_speed(self) -> float:
        return (
            self.length_pool
            * self.count_pool
            / self.M_IN_KM
            / self.duration
        )

    def get_distance(self) -> float:
        return (
            self.action
            * self.LEN_STEP
            / self.M_IN_KM
        )


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    typetraining_dict: Dict[str, Training] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type in typetraining_dict:
        return typetraining_dict[workout_type](*data)
    else:
        raise KeyError('Допустимые значения тренировок: SWM, RUN, WLK')


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
