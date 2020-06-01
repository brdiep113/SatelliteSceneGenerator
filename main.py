from GeneratorFunctions.plot_functions import fill_scene, plot_sample_img, plot_vectors
from Shape.Scene import Scene
from Shape.SimpleHouse import RotatedRect
import random
import numpy as np
import json
from PIL import Image

image_outpath = "SampleImages/Image"
ground_truth_outpath = "SampleImages/GroundTruth/training_solutions.json"

final_json = []

sample_size = 4
scene_size = (1024, 1024)

for i in range(sample_size):
    curr_scene_id = "generated_img{0}".format(i)
    scene = Scene(scene_size, curr_scene_id)
    max_buildings = 24
    fill_scene(max_buildings, scene, final_json)
    plot_sample_img(scene, image_outpath, i)

#im = Image.open("SampleImages/Image/image_truth_0.png")
#imarray = np.array(im)

with open(ground_truth_outpath, 'w') as outfile:
    json.dump(final_json, outfile)

#plot_vectors(imarray, final_json[0])