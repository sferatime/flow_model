from Wall import Wall
from Field import Field, f_ij, f_i_w, v_0
from Config import Config
import random
import threading
from numba import njit
import time
from Person import DEFAULT_REACTION_TIME

do_simulation = False
tick = 1
delta_time = 0.1
space = 750
field = None
out_flag = False


def print_to_file(line):
    with open("./results.txt", "a") as file:
        file.write(line)


class Simulation:
    # config = Config('./config.toml')
    counts = 0
    persons_count_pos = 0
    persons_count_neg = 0
    time = 0
    threads = []
    field = None

    def __init__(self):
        global field
        field = Field()
        self.field = field
        self.init_walls()
        self.init_simulation()

    def init_simulation(self):
        simulating_thread = threading.Thread(target=self.simulate, daemon=True)
        simulating_thread.start()

    def simulate(self):
        global out_flag
        global tick
        global do_simulation
        global stop_thread
        global field
        global delta_time
        global space
        step_of_person_each_tick = 5
        # MOVE TO CONFIG
        person_each_tick = 500
        experiment_time_ticks = 900 / delta_time
        restart_flag = True
        # field.add_person(10, 11, 1.3, 0, 80, 12.5)
        # field.add_person(30, 11.4, -1.3, 0, 0, 12.5)
        while True:
            # self.add_persons(100, 110, 5, 1.3, 0, 800, 110)
            # self.add_persons(700, 110, 5, -1.3, 0, 0, 110)
            while do_simulation and restart_flag:
                self.calculate_persons()
                self.move_persons()
                self.delete_persons(200, 111, 50, 99)
                if tick % person_each_tick == 1:
                    self.add_persons(60, 105, 2, 1.3, 0, 800, 105)
                    self.add_persons(190, 105, 2, -1.3, 0, 0, 105)
                if tick > experiment_time_ticks:
                    print("end of experiment")
                    restart_flag = False
                    out_flag = True
                    time.sleep(1)
                    self.delete_all_persons()
                    break
                tick += 1
            if out_flag:
                results = "FLOW_POS: {0}; FLOW_NEG: {1}; TIME:{2}; PERSON_EACH_TICK: {3}\n".format(
                    self.persons_count_pos / (tick * delta_time * space),
                    self.persons_count_neg / (tick * delta_time * space),
                    tick * delta_time, person_each_tick)
                print(results)
                results_to_file = "{0} {1} {2}\n".format(person_each_tick, self.persons_count_pos / (tick * delta_time * space), self.persons_count_neg / (tick * delta_time * space))
                print_to_file(results_to_file)
                out_flag = False
                person_each_tick -= step_of_person_each_tick
                tick = 0
                self.persons_count_neg = 0
                self.persons_count_pos = 0
                # experiment_time_ticks = random.randrange(400, 800, 100) / delta_time
                restart_flag = True
                time.sleep(10)
        exit()

    def add_persons(self, x, y, r, speed_x, speed_y, target_pos_x, target_pos_y):
        x_position = random.randrange(x - r, x + r)
        y_position = random.randrange(y - r, y + r)
        field.add_person(x_position, y_position, speed_x, speed_y, target_pos_x, target_pos_y)

    def delete_all_persons(self):
        field.persons.clear()

    def delete_persons(self, max_x, max_y, min_x, min_y):
        global field
        for person in field.persons:
            if person.pos_x > max_x or person.pos_x < min_x or person.pos_y > max_y or person.pos_y < min_y:
                if person.pos_x > max_x and person.target_pos_x >= max_x:
                    self.persons_count_pos += 1
                if person.pos_x < min_x and person.target_pos_x <= min_x:
                    self.persons_count_neg += 1

                field.persons.remove(person)
                del person

    def calculate_persons(self):
        global field
        for person_i in field.persons:
            persons_f_x = 0
            persons_f_y = 0
            wall_f_x = 0
            wall_f_y = 0

            for person_j in field.persons:
                if person_j != person_i:
                    f_x, f_y = f_ij(person_i.pos_x, person_i.pos_y,
                                    person_j.pos_x, person_j.pos_y,
                                    person_i.radius, person_j.radius,
                                    person_i.speed_x, person_i.speed_y,
                                    person_j.speed_x, person_j.speed_y)
                    persons_f_x += f_x
                    persons_f_y += f_y

            for wall in field.walls:
                f_x, f_y = f_i_w(person_i.pos_x, person_i.pos_y,
                                 wall.x_1, wall.y_1,
                                 wall.x_2, wall.y_2,
                                 person_i.radius,
                                 person_i.speed_x, person_i.speed_y)
                wall_f_x += f_x
                wall_f_y += f_y

            v_0_x, v_0_y = v_0(person_i.pos_x, person_i.pos_y, person_i.target_pos_x, person_i.target_pos_y)
            # print("v_0_x: {0}, v_0_y: {1}".format(v_0_x, v_0_y))

            a_x = ((v_0_x - person_i.speed_x) / DEFAULT_REACTION_TIME + persons_f_x + wall_f_x) / person_i.mass
            a_y = ((v_0_y - person_i.speed_y) / DEFAULT_REACTION_TIME + persons_f_y + wall_f_y) / person_i.mass

            # print(person_i.speed_x)
            # print(persons_f_x, persons_f_y)
            person_i.set_acceleration(a_x, a_y)

    def move_persons(self):
        # MOVE TO CONFIG
        global delta_time
        # delta_time = 0.0009
        for person_i in self.field.persons:
            person_i.move(delta_time)

    def init_walls(self):
        global field
        wall_1 = Wall(50, 100, 200, 100)
        wall_2 = Wall(50, 110, 200, 110)
        # wall_1 = Wall(5, 10, 75, 10)
        # wall_2 = Wall(5, 15, 75, 15)
        field.add_wall(wall_1)
        field.add_wall(wall_2)

    def switch_state(self):
        global out_flag
        global do_simulation
        if do_simulation:
            out_flag = True
        do_simulation = not do_simulation
