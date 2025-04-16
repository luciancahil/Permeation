import matplotlib.pyplot as plt
import numpy as np

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
    # info: 'ITEM: ATOMS id type x y z vx vy vz fx fy fz\n'

    # read atom info:
    atoms_info = []
    for i in range(num_atoms):
        atom_line = file.readline()

        info = [float(num) for num in atom_line.split(" ")]
        atoms_info.append(info)
    
    # sort by ID
    sorted(atoms_info, key = lambda info: info[0])

    # sort by type
    sorted(atoms_info, key = lambda info: info[1])

    return step_num, atoms_info, lengths


def plot_hist(list, name):
    counts, bins = np.histogram(list)
    plt.stairs(counts, bins)
    plt.savefig('./pics/{}.png'.format(name))
    plt.close()


log_file = open("./logs/diffuse.txt", mode='r')

coord_file = open("./outputs/permanent/penetrant_C92x5x5.data_CH4.lmp_diffusion.xyz")

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

new_cycle = []
while(line):
    step_num, atoms_info, lengths = read_block(coord_file)

    if(step_num == jiggling_stopping_steps[cycle]):
        
        if(cycle % 100 == 0):
            print(cycle)
        cycle += 1
        cycles_info.append(new_cycle)
        new_cycle = []
        box_lenths = lengths

        if(cycle == len(minimization_stoppages)):
            break
    
    if(step_num >= minimization_stoppages[cycle]):
        main_atom = atoms_info[0][2:5]     
        new_cycle.append(main_atom)

    

    line = coord_file.readline()


breakpoint()
x_coords = []
y_coords = []
z_coords = []


x_MSD = []
y_MSD = []
z_MSD = []

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
    

    x_diff = [num for num in x_diff if abs(num) < box_lenths[0] / 2]
    y_diff = [num for num in y_diff if abs(num) < box_lenths[1] / 2]
    z_diff = [num for num in z_diff if abs(num) < box_lenths[2] / 2]

    if(x_diff == [] or y_diff == [] or z_diff == []):
        continue
    x_MSD.append(sum(x_diff) / len(x_diff))
    y_MSD.append(sum(y_diff) / len(y_diff))
    z_MSD.append(sum(z_diff) / len(z_diff))


# [16.715041999676394, 12.957574372484338, 90.70302060737704]


# Okay, we have a problem. The box dims actually vary quite a lot here, unfortunately.

# So what do I do?....

plt.scatter(range(len(x_MSD)), x_MSD)
plt.savefig('./pics/x_MSD.png')
plt.close()
plt.scatter(range(len(y_MSD)), y_MSD)
plt.savefig('./pics/y_MSD.png')
plt.close()
plt.scatter(range(len(z_MSD)), z_MSD)
plt.savefig('./pics/y_MSD.png')
plt.close()

plot_hist(x_coords, "x_coords")
plot_hist(y_coords, "y_coords")
plot_hist(z_coords, "z_coords")

avg_x = sum(x_MSD) / len(x_MSD)
avg_y = sum(y_MSD) / len(y_MSD)
avg_z = sum(z_MSD) / len(z_MSD)


print("X Diffusion Coef: {}".format(avg_x * avg_x / 2))
print("Y Diffusion Coef: {}".format(avg_y * avg_y / 2))
print("Z Diffusion Coef: {}".format(avg_z * avg_z / 2))

print("Done!")