from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    txt = ('Тип тренировки: {}; Длительность: {:.3f} ч.; Дистанция: {:.3f} км;'
           ' Ср. скорость: {:.3f} км/ч; Потрачено ккал: {:.3f}.')

    def get_message(self) -> str:
        return (self.txt.format(self.training_type, self.duration,
                self.distance, self.speed, self.calories))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError()

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_type = self.__class__.__name__
        duration = self.duration
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        return InfoMessage(training_type, duration, distance, speed, calories)


class Running(Training):
    """Тренировка: бег."""
    RUN_COEF_1: float = 18
    RUN_COEF_2: float = 20

    def get_spent_calories(self) -> float:
        return (
            (self.RUN_COEF_1 * self.get_mean_speed() - self.RUN_COEF_2)
            * self.weight / self.M_IN_KM * (self.duration * self.MIN_HOUR)
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WALK_1: float = 0.035
    WALK_2: float = 0.029

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: float):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return (
            (self.WALK_1 * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.WALK_2 * self.weight) * (self.duration * self.MIN_HOUR)
        )


class Swimming(Training):
    LEN_STEP = 1.38

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Тренировка: плавание."""
        ratio_calories_1: float = 1.1
        ratio_calories_2: int = 2
        return (
            (self.get_mean_speed() + ratio_calories_1)
            * ratio_calories_2 * self.weight
        )


def read_package(training_type: str, input_data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    try:
        diction: dict = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
        class_name = diction[training_type]
        return class_name(*input_data)
    except KeyError:
        raise ValueError("Несоответствующее значение")


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(InfoMessage.get_message(info))


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for training_type, input_data in packages:
        training = read_package(training_type, input_data)
        main(training)
