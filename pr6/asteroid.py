class Asteroid:
    """
    Класс астероида
    """

    def __init__(self, x: float, y: float, radius: int, x_speed: float, y_speed: float):
        """
        :param x: x-координата астероида
        :param y: y-координата астероида
        :param radius: радиус астероида
        :param x_speed: скорость астероида по оси x
        :param y_speed: скорость астероида по оси y
        """
        self._x = x
        self._y = y
        self._radius = radius
        self._x_speed = x_speed
        self._y_speed = y_speed

    @property
    def x(self):
        """x-координата астероида"""
        return self._x

    @x.setter
    def x(self, x: float):
        self._x = x

    @property
    def y(self):
        """y-координата астероида"""
        return self._y

    @y.setter
    def y(self, y: float):
        self._y = y

    @property
    def x_speed(self):
        """скорость по x астероида"""
        return self._x_speed

    @x_speed.setter
    def x_speed(self, x_speed: float):
        self._x_speed = x_speed

    @property
    def y_speed(self):
        """скорость по y астероида"""
        return self._y_speed

    @y_speed.setter
    def y_speed(self, y_speed: float):
        self._y_speed = y_speed

    @property
    def radius(self):
        """радиус астероида"""
        return self._radius

    @radius.setter
    def radius(self, radius: int):
        self._radius = radius


        
    def move(self, width: int, height: int):
        """
        Функция изменяющая координаты астероида при движении, учитывает столкновение с границами поля
        :param width: ширина поля
        :param height: высота поля
        """
        self.x += self.x_speed
        if self.x < self.radius: self.x, self.x_speed = self.radius, -self.x_speed
        if self.x > width - self.radius: self.x, self.x_speed = width - self.radius, -self.x_speed

        self.y += self.y_speed
        if self.y < self.radius: self.y, self.y_speed = self.radius, -self.y_speed
        if self.y > height - self.radius: self.y, self.y_speed = height - self.radius, -self.y_speed

