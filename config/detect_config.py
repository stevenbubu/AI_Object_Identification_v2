class FLAGS(object):
    """
    General parameter
    """   
    # video type : 'VIDEO', 'WEBCAM', 'URL'
    TYPE = 'WEBCAM'             
    # video source
    # 'https://www.youtube.com/watch?v=BZP1rYjoBgI'
    # '/home/jdwei/Desktop/github/HandDetect/handtracking/handvideo5.mp4'
    video_source = 0
    video_width = 640   # video width
    video_height = 480  # video height
    # max number of hands we want to detect/track
    num_hands_detect = 2  

    score_thresh = 0.95  # score threshold
    gpu_memory = 0.5    # Set gpu memory used

    # Control flag
    display = True                      # Display video
    fps = True                          # Display fps
    Right_Hand_flag = False             # Display Right Hand video
    Right_Hand_Gesture_flag = False     # Display Right Hand Gesture video
    Left_Hand_flag = False              # Display Left Hand video
    Left_Hand_Gesture_flag = False      # Display Left Hand Gesture video


    """
    tracker parameter
    """   
    track_img_size = 384


    