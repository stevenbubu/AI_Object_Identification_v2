# Utilities for object detector.

import numpy as np
import sys
import tensorflow as tf
import os
from threading import Thread
from datetime import datetime
import cv2
from utils import label_map_util
from utils import func_util
from collections import defaultdict
import datetime


detection_graph = tf.Graph()

def load_label_category(label_path, num):
    # load label map
    label_map = label_map_util.load_labelmap(label_path)
    categories = label_map_util.convert_label_map_to_categories(
        label_map, max_num_classes=num, use_display_name=True)
    label_item = dict()
    for item in categories:
        label_item[item["id"]] = item["name"]
    return label_item


# Load a frozen infrerence graph into memory
def load_inference_graph(PATH_TO_CKPT, option):
    # load frozen tensorflow model into memory
    print("> ====== loading HAND frozen graph into memory")
    detection_graph = tf.Graph()
    config          = tf.ConfigProto()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')
            
        gpu_id = int(option["gpu"])
        gpu_memory_fraction = float(option["mem_percent"])
        gpus = tf.config.experimental.list_physical_devices("GPU")
        if gpus:
            try:
                tf.config.experimental.set_visible_devices(gpus[gpu_id], "GPU")
                config.gpu_options.per_process_gpu_memory_fraction = gpu_memory_fraction
            except RuntimeError as e:
                print("GPU setting error. Msg:" + e)

        sess = tf.Session(config=config, graph=detection_graph)
    print(">  ====== Hand Inference graph loaded.")
    return detection_graph, sess


# draw the detected bounding boxes on the images
# You can modify this to also draw a label.
def draw_box_on_image(score_thresh, scores, boxes, classes, 
                        im_width, im_height, image_np, labels, recordpath):
    handclass = -1
    for i in range(len(scores)):
        if scores[i] > score_thresh:
            (left, right, top, bottom) = (boxes[i][1] * im_width, boxes[i][3] * im_width,
                                            boxes[i][0] * im_height, boxes[i][2] * im_height)
            p1 = (int(left), int(top))
            p2 = (int(right), int(bottom))
            handclass = int(classes[i])

            cv2.rectangle(image_np, p1, p2, (77, 255, 9), 3, 1)
            cv2.putText(image_np, str(labels[int(classes[i])]), p1, 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, (30, 144, 255), 2, cv2.LINE_AA)
            
            func_util.save_txt(recordpath, string="\n" + str(datetime.datetime.now()))
            func_util.save_txt(recordpath, str(labels[int(classes[i])])+" "+ str(scores[i]), string="\n")
            func_util.save_txt(recordpath, string="\n")

    return image_np, handclass

# Show fps value on image.
def draw_fps_on_image(fps, image_np):
    cv2.putText(image_np, fps, (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (77, 255, 9), 2)


# Actual detection .. generate scores and bounding boxes given an image
def detect_objects(image_np, detection_graph, sess):
    # Definite input and output Tensors for detection_graph
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
    # Each box represents a part of the image where a particular object was detected.
    detection_boxes = detection_graph.get_tensor_by_name(
        'detection_boxes:0')
    # Each score represent how level of confidence for each of the objects.
    # Score is shown on the result image, together with the class label.
    detection_scores = detection_graph.get_tensor_by_name(
        'detection_scores:0')
    detection_classes = detection_graph.get_tensor_by_name(
        'detection_classes:0')
    num_detections = detection_graph.get_tensor_by_name(
        'num_detections:0')

    image_np_expanded = np.expand_dims(image_np, axis=0)

    (boxes, scores, classes, num) = sess.run(
        [detection_boxes, detection_scores,
            detection_classes, num_detections],
        feed_dict={image_tensor: image_np_expanded})
    return np.squeeze(boxes), np.squeeze(scores), np.squeeze(classes)
