import random

from Person import Person, DEFAULT_REPULSION_RATE_A, DEFAULT_REPULSION_RATE_B, DEFAULT_PRESSURE_RESISTANCE_COEFFICIENT, DEFAULT_DIRECTION_CHANGE_COEFFICIENT, DEFAULT_REACTION_TIME, DEFAULT_TARGET_SPEED
from Wall import Wall
from numpy.linalg import norm
from numpy import cross
from numpy import array
# from numba import jit
from numba import njit
import math


def v_0(person_x, person_y, target_pos_x, target_pos_y):
    v_0_x = DEFAULT_TARGET_SPEED * (target_pos_x - person_x)
    v_0_y = DEFAULT_TARGET_SPEED * (target_pos_y - person_y)
    norm = math.sqrt(v_0_x ** 2 + v_0_y ** 2)
    return v_0_x / norm, v_0_y / norm


def distance_iw(person_x, person_y, wall_x1, wall_y1, wall_x2, wall_y2):
    P1 = array([wall_x1, wall_y1])
    P2 = array([wall_x2, wall_y2])
    P3 = array([person_x, person_y])
    return norm(cross(P2 - P1, P1 - P3)) / norm(P2 - P1)


def distance_ij(person_i_x, person_i_y, person_j_x, person_j_y):
    return math.sqrt((person_i_x - person_j_x) ** 2 + (person_i_y - person_j_y) ** 2)


def normal_iw(person_x, persson_y, wall_x1, wall_y1, wall_x2, wall_y2):
    x12 = wall_x2 - wall_x1
    y12 = wall_y2 - wall_y1
    dotp = x12 * (person_x - wall_x1) + y12 * (persson_y - wall_y1)
    dot12 = x12 * x12 + y12 * y12
    if dot12:
        coeff = dotp / dot12
        proj_x = wall_x1 + x12 * coeff
        proj_y = wall_y1 + y12 * coeff
        norm_x = - (person_x - proj_x)
        norm_y = - (persson_y - proj_y)
        div = math.sqrt(norm_x ** 2 + norm_y ** 2)
        return norm_x / div, norm_y / div
    else:
        return None


def normal_ij(person_i_x, person_i_y, person_j_x, person_j_y):
    distance = distance_ij(person_i_x, person_i_y, person_j_x, person_j_y)
    normal_x_part = (person_j_x - person_i_x) / distance
    normal_y_part = (person_j_y - person_i_y) / distance
    # add - for debug
    return -normal_x_part, -normal_y_part


def tangent_iw(person_x, person_y, wall_x1, wall_y1, wall_x2, wall_y2):
    t_x, t_y = normal_iw(person_x, person_y, wall_x1, wall_y1, wall_x2, wall_y2)
    return -t_y, t_x


def tangent_ij(person_i_x, person_i_y, person_j_x, person_j_y):
    tangent_x_part, tangent_y_part = normal_ij(person_i_x, person_i_y, person_j_x, person_j_y)
    return -tangent_y_part, tangent_x_part


def radius_ij(person_i_radius, person_j_radius):
    return person_i_radius + person_j_radius


def delta_v_ij(person_i_x, person_i_y, person_j_x, person_j_y, person_i_v_x, person_i_v_y,  person_j_v_x, person_j_v_y):
    tangent_x_part, tangent_y_part = tangent_ij(person_i_x, person_i_y, person_j_x, person_j_y)
    delta_v_x = (person_j_v_x - person_i_v_x) * tangent_x_part
    delta_v_y = (person_j_v_y - person_i_v_y) * tangent_y_part
    return delta_v_x + delta_v_y


def f_i_w(person_i_x, person_i_y, wall_x1, wall_y1, wall_x2, wall_y2, person_i_radius, person_i_v_x, person_i_v_y):
    r = person_i_radius
    d = distance_iw(person_i_x, person_i_y, wall_x1, wall_y1, wall_x2, wall_y2)
    t_x, t_y = tangent_iw(person_i_x, person_i_y, wall_x1, wall_y1, wall_x2, wall_y2)
    n_x, n_y = normal_iw(person_i_x, person_i_y, wall_x1, wall_y1, wall_x2, wall_y2)
    A = DEFAULT_REPULSION_RATE_A
    B = DEFAULT_REPULSION_RATE_B
    K = DEFAULT_PRESSURE_RESISTANCE_COEFFICIENT
    k = DEFAULT_DIRECTION_CHANGE_COEFFICIENT

    f_w_x = (A * math.exp((r - d) / B) + K * max(0, r - d)) * n_x - k * max(0, r - d) * (person_i_v_x * t_x + person_i_v_y * t_x) * t_x
    f_w_y = (A * math.exp((r - d) / B) + K * max(0, r - d)) * n_y - k * max(0, r - d) * (person_i_v_x * t_x + person_i_v_y * t_x) * t_y
    # print("R:{0}; D:{1}; N_X:{2} N_Y:{3}; T_X:{4} T_Y:{5}; f_x:{6} f_y:{7}".format(r, d, n_x, n_y, t_x, t_y, f_w_x, f_w_y))

    return -f_w_x, -f_w_y


def f_ij(person_i_x, person_i_y, person_j_x, person_j_y, person_i_r, person_j_r, person_i_v_x, person_i_v_y,  person_j_v_x, person_j_v_y):
    r = radius_ij(person_i_r, person_j_r)
    d = distance_ij(person_i_x, person_i_y, person_j_x, person_j_y)
    A = DEFAULT_REPULSION_RATE_A
    B = DEFAULT_REPULSION_RATE_B
    n_x, n_y = normal_ij(person_i_x, person_i_y, person_j_x, person_j_y)
    if max(0, r - d) != 0:
        t_x, t_y = tangent_ij(person_i_x, person_i_y, person_j_x, person_j_y)
        d_v = delta_v_ij(person_i_x, person_i_y, person_j_x, person_j_y, person_i_v_x, person_i_v_y,  person_j_v_x, person_j_v_y)
        K = DEFAULT_PRESSURE_RESISTANCE_COEFFICIENT
        k = DEFAULT_DIRECTION_CHANGE_COEFFICIENT
        f_x = (A * math.exp((r - d) / B) + K * max(0, r - d)) * n_x + k * max(0, r - d) * t_x * d_v
        f_y = (A * math.exp((r - d) / B) + K * max(0, r - d)) * n_y + k * max(0, r - d) * t_y * d_v
    else:
        f_x = (A * math.exp((r - d) / B)) * n_x
        f_y = (A * math.exp((r - d) / B)) * n_y
    # print("R:{0}; D:{1}; N_X:{2} N_Y:{3}; T_X:{4} T_Y:{5}; d_v:{6}; f_x:{7} f_y:{8}".format(r, d, n_x, n_y, t_x, t_y, d_v, f_x, f_y))

    return f_x, f_y


class Field:

    config = None
    persons = list()
    walls = list()

    def __init__(self):
        # P1 = Person(60, 1)
        # P1.set_position(100, 100)
        # W1 = Wall(0, 200, 200, 200)
        # print(normal_iw(P1, W1))
        pass

    def add_person(self, x, y, target_speed_x, target_speed_y, target_pos_x, target_pos_y):
        weight = random.randrange(60, 80, 1)
        person = Person(mass=weight, radius=0.15)
        person.set_position(x, y)
        start_speed = random.randrange(50, 100, 1)
        person.set_speed(target_speed_x * (start_speed / 100), target_speed_y * (start_speed / 100))
        person.set_target_speed(target_speed_x, target_speed_y)
        person.set_target_pos(target_pos_x, target_pos_y)
        self.persons.append(person)

    def add_wall(self, wall):
        self.walls.append(wall)
