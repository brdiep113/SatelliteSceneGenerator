from GeneratorFunctions.plot_functions import fill_scene, plot_sample_img, plot_vectors, plot_ground_truth
from Shape.Scene import Scene
from Shape.SimpleHouse import RotatedRect
import random
import numpy as np
import json
import os
from PIL import Image

image_outpath = "SampleImages/Image"
ground_truth = "SampleImages/GroundTruth"
ground_truth_outpath = "SampleImages/GroundTruth/training_solutions.json"

test_outpath = "SampleImages/Test_Image"
test_ground_truth_outpath = "SampleImages/Test_GroundTruth"

final_json = []

sample_size = 200
scene_size = (1024, 1024)

test_size = 10

for i in range(sample_size):
    curr_scene_id = "generated_img{0}".format(i)
    scene = Scene(scene_size, curr_scene_id)
    max_buildings = 24
    fill_scene(max_buildings, scene, final_json)
    plot_sample_img(scene, image_outpath, i)
    plot_ground_truth(scene, ground_truth, i)

for i in range(test_size):
    curr_scene_id = "test_img{0}".format(i)
    scene = Scene(scene_size, curr_scene_id)
    max_buildings = 24
    fill_scene(max_buildings, scene, final_json)
    plot_sample_img(scene, test_outpath, i)
    plot_ground_truth(scene, test_ground_truth_outpath, i)

with open(ground_truth_outpath, 'w') as outfile:
    json.dump(final_json, outfile)