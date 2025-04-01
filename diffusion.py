import random
import numpy as np


RUNS = 100000
LENGTH = 100
particle_ADD_RATE = 100

moves_right = np.random.choice(a=[False, True], size=(100))

particle_map = dict()

 

# number of particles we have in total
total_num_particles = 0

for i in range(RUNS):
    if i % 1000 == 1:
        # Print result
        for j in range(len(counts)):
            print(f"Bin {int(bin_edges[j])}-{int(bin_edges[j+1])}: {counts[j]}")    
        
        print(i)
        print("\n\n")

    new_particles = ["particle_{}".format(total_num_particles + i) for i in range(particle_ADD_RATE)]
    total_num_particles += particle_ADD_RATE
    for particle in new_particles:
        particle_map[particle] = 0
    
    movement = np.random.normal(size=len(particle_map.keys()))

    movement = random.uniform(-1, 1) * abs(movement)

    keys = particle_map.keys()
    bad_keys = set()
    for i, particle in enumerate(keys):
        particle_map[particle] += movement[i]
        


        if (particle_map[particle] < 0):
            bad_keys.add(particle)
        elif(particle_map[particle] > LENGTH):
            particle_map[particle] = LENGTH - (particle_map[particle] - LENGTH)
    
    for bad_key in bad_keys:
        del particle_map[bad_key]

    



    values_list = [i for i in particle_map.values()]



    # Define bin edges: 0-1, 1-2, etc.
    bins = np.arange(0, LENGTH + 1.1, 1)

    # Count numbers in each bin
    counts, bin_edges = np.histogram(values_list, bins)

