import os

class FLAGS(object):

    # Train dataset
    train_csvfile = "train_labels.csv"
    train_csvpath = "/media/steven/6c8bd309-73d3-432c-8a3c-a1ddfbc3575e/image_11k_500/Hands/Train/"
    train_csvfilepath = os.path.join(train_csvpath, train_csvfile)

    train_imgfile = ""
    train_imgpath = "/media/steven/6c8bd309-73d3-432c-8a3c-a1ddfbc3575e/image_11k_500/Hands/Train/"
    train_imgfilepath = os.path.join(train_imgpath, train_imgfile)
    
    train_outputfile = "train.record"
    train_outputpath = "/media/steven/21105186-d3fb-4fbe-9609-3c53cdb1275d/images_11k_500"
    train_outputfilepath = os.path.join(train_outputpath, train_outputfile)


    # Test dataset
    test_csvfile = "test_labels.csv"
    test_csvpath = "/media/steven/6c8bd309-73d3-432c-8a3c-a1ddfbc3575e/image_11k_500/Hands/Test/"
    test_csvfilepath = os.path.join(test_csvpath, test_csvfile)

    test_imgfile = ""
    test_imgpath = "/media/steven/6c8bd309-73d3-432c-8a3c-a1ddfbc3575e/image_11k_500/Hands/Test/"
    test_imgfilepath = os.path.join(test_imgpath, test_imgfile)
    
    test_outputfile = "test.record"
    test_outputpath = "/media/steven/21105186-d3fb-4fbe-9609-3c53cdb1275d/images_11k_500"
    test_outputfilepath = os.path.join(test_outputpath, test_outputfile)


    # func control
    Train_tfrecord_flg = True
    Test_tfrecord_flg = True
