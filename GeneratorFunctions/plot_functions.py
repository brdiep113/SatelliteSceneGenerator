import matplotlib.pyplot as plt
import numpy as np
from os import path
from Shape.Scene import Scene
from Shape.SimpleHouse import RotatedRect
import random


# constants
my_dpi = 96
SHAPE = (1024, 1024)


def plot_sample_img(scene, image_outpath, image_count):
    noise = np.random.normal(255. / 2, 255. / 10, SHAPE)

    img = plt.figure(figsize=(1024 / my_dpi, 1024 / my_dpi), dpi=my_dpi)
    axes = plt.gca()
    axes.imshow(noise, extent=[-1024, 1024, -1024, 1024])
    axes.set_xlim([0, 1024])
    axes.set_ylim([0, 1024])

    for structure in scene.buildings:
        img_matrix = structure.vertices
        center = structure.center
        a, b, c, d = img_matrix[:, 0], img_matrix[:, 1], img_matrix[:, 2], img_matrix[:, 3]

        p1 = np.array((a, center, b))
        p2 = np.array((b, center, c))
        p3 = np.array((c, center, d))
        p4 = np.array((d, center, a))

        plt.plot(center[0], center[1], marker='o', markersize=3, color="red")
        plt.fill(p1[:, 0], p1[:, 1], "r")
        plt.fill(p2[:, 0], p2[:, 1], "g")
        plt.fill(p3[:, 0], p3[:, 1], "b")
        plt.fill(p4[:, 0], p4[:, 1], "y")

        # Clear grid
        plt.axis('off')
        plt.grid(b=None)
        plt.box(False)

    img.savefig(path.join(image_outpath, "image_{0}.png".format(image_count)), bbox_inches='tight', pad_inches=0)
    plt.clf()


def plot_vectors(image, data_dictionary):

    x_list, y_list = read_coordinates(data_dictionary)
    edge_list = data_dictionary['Edges']

    img = plt.figure(figsize=(1024 / my_dpi, 1024 / my_dpi), dpi=my_dpi)
    ax = plt.gca()
    plt.imshow(image)

    for i in range(len(edge_list)):
        origin = x_list[i], y_list[i]
        print("The origin is: " + str(origin))
        for j in range(len(edge_list[i])):
            edge = edge_list[i][j][0], edge_list[i][j][1]
            ax.quiver(*origin, *edge)

    plt.show()


def read_coordinates(data_dictionary):
    x_list = data_dictionary['X'][1:-2]
    x_list = [float(s) for s in x_list.split(',')]
    y_list = data_dictionary['Y'][1:-2]
    y_list = [float(s) for s in y_list.split(',')]
    return x_list, y_list


def get_edges(data_dictionary):

    x_list, y_list = read_coordinates(data_dictionary)
    edge_list = []

    for i in range(0, len(x_list) - 1):
        anchor = np.array((x_list[i], y_list[i]))
        if i == 0:
            to_prev = len(x_list) - 2
            to_next = i + 1
        elif i == len(x_list) - 2:
            to_prev = i - 1
            to_next = 0

        edge_to_center = (anchor - np.array((x_list[0], y_list[0]))).tolist()
        edge_to_prev = (np.array((x_list[to_prev], y_list[to_prev])) - anchor).tolist()
        edge_to_next = (np.array((x_list[to_next], y_list[to_next])) - anchor).tolist()
        edge_list.append([edge_to_prev, edge_to_center, edge_to_next])

    return edge_list


def get_facets(structure):
    img_matrix = structure.vertices
    center, a, b, c, d = img_matrix[:, 0], img_matrix[:, 1], img_matrix[:, 2], img_matrix[:, 3], img_matrix[:, 4]

    p1 = np.array((center, a, b))
    p2 = np.array((center, b, c))
    p3 = np.array((center, c, d))
    p4 = np.array((center, a, d))

    return [p1, p2, p3, p4]


def fill_scene(max_shape_count: int, scene: Scene, json) -> None:

    generated = 0
    failed = 0

    while failed < 10 and generated < max_shape_count:
        x = random.uniform(256, 768)
        y = random.uniform(256, 768)
        w = random.uniform(40, 160)
        h = random.uniform(40, 160)
        angle = random.uniform(0, 360)
        shape = RotatedRect(x, y, w, h, angle)
        offset = np.array((random.uniform(-w / 4, w / 4), random.uniform(-h / 4, h / 4)))
        shape.offset_center(offset)

        if scene.has_overlap(shape):
            failed += 1

        else:
            scene.add_building(shape)
            x_pts = str(shape.vertices[0,:].tolist())
            y_pts = str(shape.vertices[1,:].tolist())

            structure_data = {"BuildingID": str(generated), "ImageID": scene.name, "X": x_pts, "Y": y_pts}
            structure_data["Edges"] = get_edges(structure_data)
            json.append(structure_data)
            generated += 1
            failed = 0

