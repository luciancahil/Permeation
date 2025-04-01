import random
import numpy as np


RUNS = 600000

LENGTH = 85
particle_ADD_RATE = 50


# Set WALL to 1 if you want particles at the end to bounce back, and WALL = 0 if you want particles to pass on through
WALL = 1

moves_right = np.random.choice(a=[False, True], size=(LENGTH))

particle_locations = [56] * LENGTH

particle_locations[0] = particle_ADD_RATE


# number of particles we have in total
total_num_particles = 0

for i in range(RUNS):

    if (i % 1000 == 0):
        print("\ni:{}".format(i))
        print(particle_locations)
        print("{}".format(particle_locations[0] / particle_ADD_RATE))


    new_counts = [0] * LENGTH

    for i in range(2, LENGTH - 1):
        new_counts[i] = (particle_locations[i - 1] + particle_locations[i + 1]) / 2
    
    new_counts[0] = particle_locations[1] / 2

    new_counts[1] = particle_locations[0] /  10 + particle_locations[2] / 2

    new_counts[-1] = particle_locations[-2] / 2 + particle_locations[-1] / 2 * WALL

    if(new_counts == particle_locations):
        print("\ni:{}".format(i))
        print(particle_locations)
        print("{}".format(particle_locations[0] / particle_ADD_RATE))
    
        break
    for i in range(LENGTH):
        particle_locations[i] = new_counts[i]

    particle_locations[0] += particle_ADD_RATE