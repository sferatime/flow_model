from Config import Config

DEFAULT_TARGET_SPEED = 1.3
DEFAULT_REACTION_TIME = 0.5
DEFAULT_REPULSION_RATE_A = 2 * 10 ** 3
DEFAULT_REPULSION_RATE_B = 0.08
DEFAULT_PRESSURE_RESISTANCE_COEFFICIENT = 1.2 * 10 ** 5
DEFAULT_DIRECTION_CHANGE_COEFFICIENT = 2.4 * 10 ** 5


class Person:
    # Constant parameters
    mass = None
    radius = None
    # Target speed
    target_speed_x = 0
    target_speed_y = 0
    # Target pos
    target_pos_x = 0
    target_pos_y = 0
    # Dynamic parameters
    pos_x = 0
    pos_y = 0
    speed_x = 0
    speed_y = 0
    acceleration_x = 0
    acceleration_y = 0

    def __init__(self, mass, radius):
        self.mass = mass
        self.radius = radius

    def show_parameters(self):
        print("""
             MASS: {0}
             RADIUS: {1}
             TARGET_SPD: {2}
             REACTION: {3}
             REPULSION_A: {4}
             REPULSION_B: {5}
             PRESSURE_RESISTANCE: {6}
             DIRECTION_CHANGE: {7}
            """.format(self.mass,
                       self.radius,
                       self.target_speed,
                       self.reaction_time,
                       self.repulsion_rate_B,
                       self.repulsion_rate_A,
                       self.pressure_resistance_coefficient,
                       self.direction_change_coefficient
                       ))

    def set_position(self, x, y):
        self.pos_x, self.pos_y = x, y

    def set_speed(self, speed_x, speed_y):
        self.speed_x, self.speed_y = speed_x, speed_y

    def set_target_speed(self, target_speed_x, target_speed_y):
        self.target_speed_x, self.target_speed_y = target_speed_x, target_speed_y

    def set_target_pos(self, x, y):
        self.target_pos_x, self.target_pos_y = x, y

    def move(self, d_time):
        self.speed_x = self.speed_x + self.acceleration_x * d_time
        self.speed_y = self.speed_y + self.acceleration_y * d_time
        self.pos_x += self.speed_x * d_time
        self.pos_y += self.speed_y * d_time

    def set_acceleration(self, a_x, a_y):
        self.acceleration_x = a_x
        self.acceleration_y = a_y

    def get_radius(self):
        return self.radius

    def get_mass(self):
        return self.mass
