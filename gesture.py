import os, sys
import numpy as np
import cv2, time
import pafy
import utils.gesture_util as lib

import logging
import config.log_config as logcfg
logging.config.dictConfig(logcfg.config)
log = logging.getLogger("StreamLogger")
import utils.video_capture as vc
import urllib.request
from queue import Queue
import threading
import datetime
import utils.func_util as func
import utils.config as cfg
import tensorflow as tf
from utils import detector_utils

""" FLAGS """
flags = tf.compat.v1.flags
flags.DEFINE_string(name="INIT_CONFIGS_PATH", default="config/gesture.config", help="Config file path.")
FLAGS = flags.FLAGS

def outputpath(path):
    outputFile = path.split(".")[0] + "_frame." + path.split(".")[-1]
    outputCropFile = path.split(".")[0] + "_crop." + path.split(".")[-1]
    outputTargetFile = path.split(".")[0] + "_target.jpg"
    return outputFile, outputCropFile, outputTargetFile


def Hand_Target_Area(option):
    Object_Area = option["Object_Area"]
    Object_Width, Object_Height = Object_Area["Width"], Object_Area["Height"]
    Object_Shift = Object_Area["Shift"]
    Object_move_Horizontial, Object_move_Vertical = Object_Shift["Horizontial"], Object_Shift["Vertical"]
    return Object_Width, Object_Height, Object_move_Horizontial, Object_move_Vertical


def Object_Detect(option, image_np, outputTargetFile, recordpath):
    pbfile_path = os.path.join(option["path"], option["pbfile"])
    gpu_option = option["gpu_option"]
    detection_graph, sess = detector_utils.load_inference_graph(pbfile_path, gpu_option)
    labelfile_path = os.path.join(option["path"], option["labelfile"])
    NUM_CLASSES = option["NUM_CLASSES"]
    label_item = detector_utils.load_label_category(labelfile_path, NUM_CLASSES)
    score_thresh = option["score_thresh"]

    boxes, scores, classes = detector_utils.detect_objects(image_np, detection_graph, sess)
    # draw bounding boxes on frame
    image_np, _ = detector_utils.draw_box_on_image(score_thresh, scores, boxes, classes, 
                                    image_np.shape[1], image_np.shape[0], image_np, label_item, recordpath)
    cv2.imwrite(outputTargetFile, image_np.astype(np.uint8))


def main():
    # import config
    InitConfig = cfg.get_config_from_init_config(init_configs_path=FLAGS.INIT_CONFIGS_PATH)
    Flags = InitConfig["Flags"]
    MediaType = Flags["MediaType"]
    # Control flag
    DetectHnad = Flags["DetectHnad"]
    DetectObject = Flags["DetectObject"]
    OutputToFile = Flags["OutputToFile"]
    DisplayScreen = Flags["DisplayScreen"]
    
    # Hand Detection Info
    HandDetectInfo = Flags["Hand_Detection_Info"]
    pbfile_path = os.path.join(HandDetectInfo["path"], HandDetectInfo["pbfile"])
    # gpu option
    gpu_option = HandDetectInfo["gpu_option"]
    detection_graph, sess = detector_utils.load_inference_graph(pbfile_path, gpu_option)
    labelfile_path = os.path.join(HandDetectInfo["path"], HandDetectInfo["labelfile"])
    NUM_CLASSES = HandDetectInfo["NUM_CLASSES"]
    label_item = detector_utils.load_label_category(labelfile_path, NUM_CLASSES)
    score_thresh = HandDetectInfo["score_thresh"]
    

    start = time.time()
    # Initial Type setting
    if MediaType == "IMAGE":
        Config = Flags['IMAGE_CONFIG']
        TextPath = Config["TextPath"]
        if all(isinstance(x,float) for x in Hand_Target_Area(Config)):
            Object_Width, Object_Height, Object_move_Horizontial, Object_move_Vertical \
            = Hand_Target_Area(Config)
        else:
            log.info("MediaType: " + MediaType + ", Hand or Object area setting error.")
            sys.exit(1)

        indir = os.path.join(Config["InputPath"], Config["InputFile"])
        if os.path.isfile(indir):
            cap = cv2.VideoCapture(indir)
            outputFile, outputCropFile, outputTargetFile = outputpath(indir)
        else:
            log.info("MediaType: " + MediaType + ", indir: " + indir + " error.")
            sys.exit(1)

    elif MediaType == "VIDEO":
        Config = Flags['VIDEO_CONFIG']
        TextPath = Config["TextPath"]
        if all(isinstance(x,float) for x in Hand_Target_Area(Config)):
            Object_Width, Object_Height, Object_move_Horizontial, Object_move_Vertical \
            = Hand_Target_Area(Config)
        else:
            log.info("MediaType: " + MediaType + ", Hand or Object area setting error.")
            sys.exit(1)

        indir = os.path.join(Config["InputPath"], Config["InputFile"])
        if os.path.isfile(indir):
            cap = cv2.VideoCapture(indir)
            outputFile, outputCropFile, outputTargetFile = outputpath(indir)
            if OutputToFile:
                fourcc = cv2.VideoWriter_fourcc(*'MJPG')
                out = cv2.VideoWriter(outputFile, fourcc, 30.0, (round(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), \
                    round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
        else:
            log.info("MediaType: " + MediaType + ", indir: " + indir + " error.")
            sys.exit(1)

    elif MediaType == "URL":
        Config = Flags['URL_CONFIG']
        TextPath = Config["TextPath"]
        if all(isinstance(x,float) for x in Hand_Target_Area(Config)):
            Object_Width, Object_Height, Object_move_Horizontial, Object_move_Vertical \
            = Hand_Target_Area(Config)
        else:
            log.info("MediaType: " + MediaType + ", Hand or Object area setting error.")
            sys.exit(1)

        URL = Config["URL"]
        outdir = os.path.join(Config["OutputPath"], Config["OutputFile"])
        if urllib.request.urlopen(URL).code == 200:
            vPafy = pafy.new(URL)
            play = vPafy.getbest()
            video_source = play.url
            im_width, im_height = vc.get_video_size(video_source)
            process1 = vc.start_ffmpeg_process1(video_source) 
            outputFile, outputCropFile, outputTargetFile = outputpath(outdir)
            if OutputToFile:
                fourcc = cv2.VideoWriter_fourcc(*'MJPG')
                out = cv2.VideoWriter(outputFile, fourcc, 30.0, (round(im_width), round(im_height)))
        else:
            log.info("MediaType: " + MediaType + ", URL: " + URL + " not exist.")
            sys.exit(1)

    elif MediaType == "WEBCAM":
        Config = Flags['WEBCAM_CONFIG']
        TextPath = Config["TextPath"]
        if all(isinstance(x,float) for x in Hand_Target_Area(Config)):
            Object_Width, Object_Height, Object_move_Horizontial, Object_move_Vertical \
            = Hand_Target_Area(Config)
        else:
            log.info("MediaType: " + MediaType + ", Hand or Object area setting error.")
            sys.exit(1)

        WEBCAM = int(Config["WEBCAM"])
        outdir = os.path.join(Config["OutputPath"], Config["OutputFile"])
        if isinstance(WEBCAM,(int)):
            cap = cv2.VideoCapture(WEBCAM)
            outputFile, outputCropFile, outputTargetFile = outputpath(outdir)
            if OutputToFile:
                fourcc = cv2.VideoWriter_fourcc(*'MJPG')
                out = cv2.VideoWriter(outputFile, fourcc, 30.0, (round(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                    round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
        else:
            log.info("MediaType: " + MediaType + ", WEBCAM: " + WEBCAM + " error.")
            sys.exit(1)

    else:
        log.info("MediaType: " + MediaType + " error.")
        sys.exit(1)


    # Process media
    i = 0
    ShowHand_flg = False
    CntFin = [0, 0, 0, 0, 0, 0] # Count the time of fingers appear

    roundtime = time.time()
    tmptime = 0
    while cv2.waitKey(1) < 0:
        if MediaType == "URL":
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
            frame = np.dstack((image_np_tmp[:,:,2],image_np_tmp[:,:,1], image_np_tmp[:,:,0]))

        else:
            hasFrame, frame = cap.read()
            if not hasFrame:
                log.info("Done processing !" + \
                        "\nOutput file is stored as " + outputFile + \
                        "\nOutput crop file is stored as " + outputCropFile + \
                        "\nOutput target file is stored as " + outputTargetFile)
                cv2.waitKey(1000)
                sys.exit(1)

        if MediaType == "IMAGE":
            Resize = Config["Resize"]
            Resize_Width, Resize_Height = int(Resize["Width"]), int(Resize["Height"])
            frame = cv2.resize(frame, (Resize_Width, Resize_Height))


        # Object location
        obj_L, obj_T, obj_R, obj_B = \
            lib.frame_border(frame, Object_Width, Object_Height, Object_move_Horizontial, Object_move_Vertical)
        obj_frame = frame[obj_T:obj_B, obj_L:obj_R]         # (y, x)


        if MediaType == "IMAGE":
            Finger = Config["Finger"]
            Target = int(Finger["Target"])
            TextPath = Config["TextPath"]
            if DetectHnad:
                boxes, scores, classes = detector_utils.detect_objects(frame, detection_graph, sess)
                # draw bounding boxes on frame
                frame, handclass = detector_utils.draw_box_on_image(score_thresh, scores, boxes, classes, 
                                                frame.shape[1], frame.shape[0], frame, label_item, TextPath)
                if handclass != -1:
                    if CntFin[handclass] == 0:
                        CntFin = [0, 0, 0, 0, 0, 0]
                    CntFin[handclass] += 1
                else:
                    CntFin = [0, 0, 0, 0, 0, 0]

            if DetectObject:
                if (CntFin[Target] >= 1):
                    Object_Detect(Flags["Object_Detection_Info"], obj_frame, outputTargetFile, TextPath)
                    CntFin = [0, 0, 0, 0, 0, 0]
            
            # Draw object frame on image
            cv2.rectangle(frame, (obj_L, obj_T), (obj_R, obj_B), (0, 0, 255), 2)

            if OutputToFile:   
                cv2.imwrite(outputFile, frame.astype(np.uint8))

            if DisplayScreen:
                cv2.imshow("frame", frame)
                cv2.imshow("object_frame", obj_frame)
                cv2.waitKey(10000)
                cv2.destroyAllWindows()

        else:
            Finger = Config["Finger"]
            Target = int(Finger["Target"])
            Time = int(Finger["Time"])
            if DetectHnad:
                boxes, scores, classes = detector_utils.detect_objects(frame, detection_graph, sess)
                # control time almost 1 second
                if tmptime != int(time.time() - roundtime):
                    # draw bounding boxes on frame
                    frame, handclass = detector_utils.draw_box_on_image(score_thresh, scores, boxes, classes, 
                                                    frame.shape[1], frame.shape[0], frame, label_item, TextPath)
                    if handclass != -1:
                        if CntFin[handclass] == 0:
                            CntFin = [0, 0, 0, 0, 0, 0]
                        CntFin[handclass] += 1
                    else:
                        CntFin = [0, 0, 0, 0, 0, 0]
                    log.info(handclass)
                    log.info(CntFin)
                    log.info("Pass {:.3f} seconds".format(time.time() - roundtime))
                tmptime = int(time.time() - roundtime)

            if DetectObject:
                if (CntFin[Target] >= Time):
                    log.info("Start detect object.")
                    threading.Thread(target=Object_Detect, args=(Flags["Object_Detection_Info"], obj_frame, outputTargetFile, TextPath)).start()
                    CntFin = [0, 0, 0, 0, 0, 0]

            # Draw object frame on image
            cv2.rectangle(frame, (obj_L, obj_T), (obj_R, obj_B), (0, 0, 255), 2)
                
            if OutputToFile:
                out.write(frame)
            
            if DisplayScreen:
                cv2.imshow("frame", frame)
                cv2.imshow("object_frame", obj_frame)
                cv2.waitKey(10)


if __name__ == '__main__':
    main()
