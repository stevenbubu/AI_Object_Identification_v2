from utils import detector_utils as detector_utils
import cv2, pafy
import tensorflow as tf
import numpy as np
import datetime
import argparse
import libs.video_capture as vc
from libs import tracking_module
import libs.gesture as gesture
from config.detect_config import FLAGS
import config.log_config as log

detection_graph, sess = detector_utils.load_inference_graph()

def main(argv):
    # video source input
    if FLAGS.TYPE in ['WEBCAM']:
        cap = cv2.VideoCapture(FLAGS.video_source)

    elif FLAGS.TYPE in ['VIDEO']:
        video_source = FLAGS.video_source

    elif FLAGS.TYPE in ['URL']:
        vPafy = pafy.new(FLAGS.video_source)
        play = vPafy.getbest()
        video_source = play.url

    else:
        print(" error : TYPE is {} ".format(FLAGS.TYPE))
        sys.exit(1)

    if FLAGS.TYPE not in ['WEBCAM']:
        im_width, im_height = vc.get_video_size(video_source)
        process1 = vc.start_ffmpeg_process1(video_source) 
    else:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, FLAGS.video_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FLAGS.video_height)
        im_width, im_height = (cap.get(3), cap.get(4))

    """ Initial tracker
    """
    tracker = tracking_module.SelfTracker([im_height, im_width], FLAGS.track_img_size)

    hand_detections = np.zeros(shape=(int(FLAGS.num_hands_detect), 2, 2), dtype=np.integer)
    crop_img = np.zeros(shape=(int(FLAGS.num_hands_detect), int(FLAGS.track_img_size), 
                                int(FLAGS.track_img_size), 3), dtype=np.uint8)                       
    gesture_img = np.zeros(shape=(int(FLAGS.num_hands_detect), int(FLAGS.track_img_size), 
                                int(FLAGS.track_img_size), 3), dtype=np.uint8)  
    CntFin = np.zeros(shape=(int(FLAGS.num_hands_detect), 6), dtype=np.int)  

    start_time = datetime.datetime.now()
    num_frames = 0

    # cv2.namedWindow('Single-Threaded Detection', cv2.WINDOW_NORMAL)

    while True:
        if FLAGS.TYPE not in ['WEBCAM']:
            image_np = vc.read_frame(process1, im_width, im_height)
            # use ffmpeg need to complement color
            image_np_tmp = np.zeros(image_np.shape, dtype=np.uint8)
            # m  b
            m_r, b_r = 0.9900855673711094, 2.05757036126613
            m_g, b_g = 0.9880223010384511, 1.9458285218824187
            m_b, b_b = 0.9882212111398636, 1.777887000339831
            image_np_tmp[:,:,0] = image_np[:,:,0]*m_r + b_r
            image_np_tmp[:,:,1] = image_np[:,:,1]*m_g + b_g
            image_np_tmp[:,:,2] = image_np[:,:,2]*m_b + b_b
            # BGR
            image_np = np.dstack((image_np_tmp[:,:,2],image_np_tmp[:,:,1], image_np_tmp[:,:,0]))
        else:
            # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
            ret, image_np = cap.read()
            # image_np = cv2.flip(image_np, 1)
        try:
            image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
        except:
            print("Error converting to RGB")
         
        # Right hand
        crop_img[0] = tracker.tracking_by_hands(image_np, hand_detections=hand_detections[0])       
        gesture_img[0] = gesture.grdetect2(crop_img[0], verbose = True, show = False, hand = True, cnt = CntFin[0])
        #Left hand
        crop_img[1] = tracker.tracking_by_hands(image_np, hand_detections=hand_detections[1])       
        gesture_img[1] = gesture.grdetect2(crop_img[1], verbose = True, show = False, hand = True, cnt = CntFin[0])
        
        # Actual detection. Variable boxes contains the bounding box cordinates for hands detected,
        # while scores contains the confidence for each of these boxes.
        # Hint: If len(boxes) > 1 , you may assume you have found atleast one hand (within your score threshold)
        boxes, scores, classes = detector_utils.detect_objects(image_np, 
                                                                detection_graph, sess)

        # draw bounding boxes on frame
        hand_detections = detector_utils.draw_box_on_image(FLAGS.num_hands_detect, FLAGS.score_thresh,
                                         scores, boxes, classes, im_width, im_height, image_np, hand_detections)
        # Calculate Frames per second (FPS)
        num_frames += 1
        elapsed_time = (datetime.datetime.now() - start_time).total_seconds()
        fps = num_frames / elapsed_time

        if (FLAGS.display):
            # Display FPS on frame
            if (FLAGS.fps):
                detector_utils.draw_fps_on_image("FPS : " + str(int(fps)), image_np)

            cv2.imshow('Video', cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR))
            if FLAGS.Right_Hand_flag:
                cv2.imshow("Right Hand", cv2.cvtColor(crop_img[0], cv2.COLOR_RGB2BGR))
            if FLAGS.Right_Hand_Gesture_flag:
                cv2.imshow("Right Hand gesture", cv2.cvtColor(gesture_img[0], cv2.COLOR_RGB2BGR))
            if FLAGS.Left_Hand_flag:
                cv2.imshow("Left Hand", cv2.cvtColor(crop_img[1], cv2.COLOR_RGB2BGR))    
            if FLAGS.Left_Hand_Gesture_flag:
                cv2.imshow("Left Hand gesture", cv2.cvtColor(gesture_img[1], cv2.COLOR_RGB2BGR))          

            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
        else:
            print("frames processed: ", num_frames, "elapsed time: ",
                  elapsed_time, "fps: ", str(int(fps)))


if __name__ == '__main__':
    tf.app.run()