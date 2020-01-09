import os
import numpy as np
import cv2
from utils import detector_utils as detector_utils
detection_graph, sess = detector_utils.load_inference_graph()
'''
Parameter
'''
hand_detections = np.zeros(shape=(2, 2, 2), dtype=np.integer)
NUM_HANDS_DETECT = 1
SCORE_THRESH = 0.9

infile = "Hand_0000006.jpg"
infd = "images"
infdpath = "/home/steven/Desktop/github/AI_Object_Identification_v2/AI_gesture_obj/"
imgfilepath = os.path.join(infdpath, infd, infile)

outfile = "Hand_0000006_out.jpg"
outfd = "images"
outfdpath = "/home/steven/Desktop/github/AI_Object_Identification_v2/AI_gesture_obj/"
outfilepath = os.path.join(outfdpath, outfd, outfile)

'''
Main function
'''
image_np = cv2.imread(imgfilepath)
im_width=image_np.shape[1]; im_height=image_np.shape[0]

boxes, scores, classes = detector_utils.detect_objects(image_np, detection_graph, sess)
# draw bounding boxes on frame
hand_detections = detector_utils.draw_box_on_image(NUM_HANDS_DETECT, SCORE_THRESH,
                        scores, boxes, classes, im_width, im_height, image_np, hand_detections)

# cv2.imshow('Image', image_np)
cv2.imwrite(outfilepath, image_np)

if cv2.waitKey(10000) & 0xFF == ord('q'):
    cv2.destroyAllWindows()


