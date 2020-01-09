import os

class FLAGS(object):

    # Train dataset
    train_csvfile = "train_labels.csv"
    train_csvpath = "/home/jdwei/Desktop/github/image_11k/Train/Train/Train"
    train_csvfilepath = os.path.join(train_csvpath, train_csvfile)

    train_imgfile = ""
    train_imgpath = "/home/jdwei/Desktop/github/image_11k/Train/Train/Train"
    train_imgfilepath = os.path.join(train_imgpath, train_imgfile)
    
    train_outputfile = "train6.record"
    train_outputpath = "/home/jdwei/Desktop/github/image_11k"
    train_outputfilepath = os.path.join(train_outputpath, train_outputfile)


    # Test dataset
    test_csvfile = "test_labels.csv"
    test_csvpath = "/home/share/image_11k/Hands/Test"
    test_csvfilepath = os.path.join(test_csvpath, test_csvfile)

    test_imgfile = ""
    test_imgpath = "/home/share/image_11k/Hands/Test"
    test_imgfilepath = os.path.join(test_imgpath, test_imgfile)
    
    test_outputfile = "test.record"
    test_outputpath = "/home/share/image_11k/Hands"
    test_outputfilepath = os.path.join(test_outputpath, test_outputfile)


    # func control
    Train_tfrecord_flg = True
    Test_tfrecord_flg = False
