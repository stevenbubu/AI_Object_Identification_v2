import os

class FLAGS(object):
    """
    General parameter
    """   
    basefile = "image_11k"
    basepath = "/home/share/"
    filepath = os.path.join(basepath, basefile)

    HANDS_FILE = "Hands.zip"
    HANDS_INFO = "HandInfo.csv"

    HANDS_DATASET_URL = "https://doc-0s-5s-docs.googleusercontent.com/docs/securesc/ha0ro937gcuc7l7deffksulhg5h7mbp1/2abtb84vn7qosfg9m1omtnbsdeom1sa6/1572595200000/13478560618660395617/*/0BwO0RMrZJCiocGlvdnJxb0lTaHM?e=download"
    HANDS_CSV_URL = "https://doc-10-5s-docs.googleusercontent.com/docs/securesc/ha0ro937gcuc7l7deffksulhg5h7mbp1/lsfff3uahdnktmgbecfm7ctioejt4ihf/1572602400000/13478560618660395617/*/1RC86-rVOR8c93XAfM9b9R45L7C2B0FdA?e=download"
    # HANDS_TXT_URL = "https://doc-10-5s-docs.googleusercontent.com/docs/securesc/ha0ro937gcuc7l7deffksulhg5h7mbp1/vhugvav1kgij0mk5vj0aoamsutatme66/1572595200000/13478560618660395617/*/1nZN5cjLE_J8AFtY_8j9KO_Y7IkqYIWQ-?e=download"
    # HANDS_MAT_URL = "https://doc-00-5s-docs.googleusercontent.com/docs/securesc/ha0ro937gcuc7l7deffksulhg5h7mbp1/h37o2ghgan5svafnnqsdnm05bc1bsjpp/1572602400000/13478560618660395617/*/0BwO0RMrZJCioMWJFVDZxczFaWEE?e=download"
 
    # train data
    threads = 32
    trainNum_per_class = 1000
    testNum_per_class = 1500  
    flips = [0, 1]
    rotates = [0, 45, 90, 135, 180, 225, 270, 315]
    scales = [0.10, 0.25, 0.50, 0.75, 1.00, 1.25]
    lumins = [0.1, 1.0, 5.0]
    noises = ['normal', 'gaussian', 's&p']

    # func control
    start_flg = False
    moveFiles_flg = False
    choseImg_flg = False
    flipHImg_flg = False
    rotateImg_flg = False
    scaleImg_flg = False
    luminImg_flg = False
    noiseImg_flg = False
    trainData_flg = False
    testData_flg = False

    # backup control 
    backupfile = "image_11k_bp"
    backuppath = "/home/share"
    backupfilepath = os.path.join(backuppath, backupfile)  
    backupall_flg = False
    moveFiles_bp_flg = False
    choseImg_bp_flg = False
    flipHImg_bp_flg = False
    rotateImg_bp_flg = False
    scaleImg_bp_flg = False
    luminImg_bp_flg = False
    noiseImg_bp_flg = False