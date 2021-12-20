class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type: str, duration: float,
                 distance: float, speed: float, calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
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
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        workout_type = self.__class__.__name__
        duration = self.duration
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        return InfoMessage(workout_type, duration, distance, speed, calories)


class Running(Training):
    """Тренировка: бег."""
    def __init__(self, action: int, duration: float, weight: float):
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        return (
            (coeff_calorie_1 * self.get_mean_speed()) - coeff_calorie_2
            * self.weight / self.M_IN_KM * (self.duration * 60)
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: float):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        ratio_walking_1: float = 0.035
        ratio_walking_2: float = 0.029
        return (
            (ratio_walking_1 * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * ratio_walking_2 * self.weight) * (self.duration * 60)
        )


class Swimming(Training):
    LEN_STEP = 1.38

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int):
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
    dict = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    class_name = dict[training_type]
    return class_name(*input_data)


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
