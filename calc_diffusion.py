import matplotlib.pyplot as plt
import numpy as np


import statistics
def read_block(file):
    # first dummy line
    step_num = int(file.readline())
    # atoms + num
    file.readline()
    num_atoms = int(file.readline())

    # ignore boxes
    file.readline()
    lengths = []

    for i in range(3):
        bounds = file.readline().split(" ")
        length = float(bounds[1]) - float(bounds[0])
        lengths.append(length)
    
    file.readline()
    # info: 'ITEM: ATOMS id type x y z vx vy vz fx fy fz molecule\n'

    # read atom info:
    atoms_info = []
    for i in range(num_atoms):
        atom_line = file.readline()

        info = [float(num) for num in atom_line.split(" ")]
        atoms_info.append(info)
    

    # sort by molecular id, then atom ID, then atom type
    atoms_info.sort(key=lambda info: (info[-1], info[0], info[1]))


    return step_num, atoms_info, lengths


def plot_hist(list, name):
    counts, bins = np.histogram(list)
    plt.stairs(counts, bins)
    plt.savefig('./pics/{}.png'.format(name))
    plt.close()


log_file = open("./logs/diffuseMix.txt", mode='r')

coord_file = open("./outputs/permanent/penetrant_C92x5x5.data_H2.lmp_2_diffusion.xyz")
file_type_name = "H2_mix_"


minimization_stoppages = []

jiggling_stopping_steps = []



for line in log_file:
    if("The Minimization Stopped at Step" in line):
        minimization_stoppages.append(int(line.split("=")[1]))
    elif("The Jiggling Stopped at Step" in line):
        jiggling_stopping_steps.append(int(line.split("=")[1]))


cycle = 0

line = coord_file.readline()

cycles_info = []
box_lenths = []
distances = []
# stores a 3x100 matrix, where each row is the coords of the main atom at a given time step.
new_cycle = []
distance_added = False
while(line):
    step_num, atoms_info, lengths = read_block(coord_file)

    if(step_num == jiggling_stopping_steps[cycle]):
        # finished a round. Reset everything
        if(cycle % 100 == 0):
            print(cycle)
        cycle += 1
        cycles_info.append(new_cycle)
        new_cycle = []
        box_lenths = lengths
        distance_added = False

        if(cycle == len(minimization_stoppages)):
            break
    
    if(step_num >= minimization_stoppages[cycle]):
        # add in coordinate info of atoms
        main_atom = atoms_info[0][2:5]     

        if(not distance_added):
            aux_atom = atoms_info[2][2:5]

            distance = sum([(main_atom[i] - aux_atom[i])**2 for i in range(3)])**(1/2)
            distances.append(distance)

            distance_added = True

        new_cycle.append(main_atom)

    

    line = coord_file.readline()


x_coords = []
y_coords = []
z_coords = []


x_MSD = []
y_MSD = []
z_MSD = []
total_MSD = []

# look at 1

for cycle in cycles_info:
    prev_step = cycle[0]
    x_coords.append(prev_step[0])
    y_coords.append(prev_step[1])
    z_coords.append(prev_step[2])

    x_diff = []
    y_diff = []
    z_diff = []
    
    for round in cycle[1:]:
        x_coords.append(round[0])
        y_coords.append(round[1])
        z_coords.append(round[2])

        x_diff.append(round[0] - prev_step[0])
        y_diff.append(round[1] - prev_step[1])
        z_diff.append(round[2] - prev_step[2])


        prev_step = round

    x_diff = [num*num for num in x_diff if abs(num) < box_lenths[0] / 2]
    y_diff = [num*num for num in y_diff if abs(num) < box_lenths[1] / 2]
    z_diff = [num*num for num in z_diff if abs(num) < box_lenths[2] / 2]

    if(x_diff == [] or y_diff == [] or z_diff == []):
        breakpoint()
        continue
        
    x_MSD.append(sum(x_diff) / len(x_diff))
    y_MSD.append(sum(y_diff) / len(y_diff))
    z_MSD.append(sum(z_diff) / len(z_diff))



# [16.715041999676394, 12.957574372484338, 90.70302060737704]


# Okay, we have a problem. The box dims actually vary quite a lot here, unfortunately.

# So what do I do?

# just drop all the atoms.


# add axes and title.

# write a function

plt.scatter(range(len(x_MSD)), x_MSD)
plt.savefig('./pics/{}x_MSD.png'.format(file_type_name))
plt.close()
plt.scatter(range(len(y_MSD)), y_MSD)
plt.savefig('./pics/{}y_MSD.png'.format(file_type_name))
plt.close()
plt.scatter(range(len(z_MSD)), z_MSD)
plt.savefig('./pics/{}z_MSD.png'.format(file_type_name))
plt.close()

plot_hist(x_coords, "{}x_coords".format(file_type_name))
plot_hist(y_coords, "{}y_coords".format(file_type_name))
plot_hist(z_coords, "{}z_coords".format(file_type_name))

avg_x = sum(x_MSD) / len(x_MSD)
avg_y = sum(y_MSD) / len(y_MSD)
avg_z = sum(z_MSD) / len(z_MSD)

diffusion_file = open("{}_diffusions.csv".format(file_type_name), mode="w")
diffusion_file.write("{}\n{}\n{}\n".format(x_MSD,y_MSD, z_MSD))



print("X Diffusion Coef: {}".format(avg_x / 2))
print("X Diffuseion stdev: {}".format(statistics.stdev(x_MSD)))
print("Y Diffusion Coef: {}".format(avg_y / 2))
print("Y Diffuseion stdev: {}".format(statistics.stdev(y_MSD)))
print("Z Diffusion Coef: {}".format(avg_z / 2))
print("Z Diffuseion stdev: {}".format(statistics.stdev(z_MSD)))
print("Total Diffusion: ")
print("Num samples: {}".format(len(x_MSD)))

file = ""
print("Done!")



"""

Units: Angstroms ^2 / fs
H2 alone:
X Diffusion Coef: 3.5868667597388445e-05
Y Diffusion Coef: 3.60909780024294e-05
Z Diffusion Coef: 3.7740240479389096e-05
Diffusion Coef:   3.656662869306898e-05

H2 with CH4:

X Diffusion Coef: 3.297382266605165e-05
Y Diffusion Coef: 3.3248013049559864e-05
Z Diffusion Coef: 3.52204368200141e-05
Diffusion Coef:   3.381409084520854e-05

CH4 with H2:
X Diffusion Coef: 4.3388338049547655e-06
Y Diffusion Coef: 4.41920272674957e-06
Z Diffusion Coef: 5.563779518824443e-06
"""