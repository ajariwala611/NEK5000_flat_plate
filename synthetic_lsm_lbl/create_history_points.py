import numpy as np

if __name__ == '__main__':

    # x coordinates
    x_ = np.linspace(3.5, 8.5, 81)

    # y coordinates
    betam = 3.5 # DNS is using 3.7, but 2.0 should be fine for a coarser grid
    ymin = 0
    ymax = 0.8
    yi = np.linspace(0,1,31)
    y_ = ymin + (ymax - ymin) * (np.tanh(betam * (yi-1.)) / np.tanh(betam) + 1.)

    # z coordinates
    z_ = np.linspace(0.5, 1.5, 31)

    # Generate grid
    x, y, z = np.meshgrid(x_, y_, z_, indexing='ij')

    x = x.flatten()
    y = y.flatten()
    z = z.flatten()

    # Write to file
    filename = 'flat_plate.his'
    with open(filename, 'w') as f:
        f.write('%d\n' % len(x))
        for i in range(len(x)):
            f.write('%f %f %f\n' % (x[i], y[i], z[i]))


