import os

class FLAGS(object):

    '''
    Seperate dataset
    '''
    # Train dataset
    train_csvfile = "train_labels.csv"
    train_csvpath = "/home/jdwei/Desktop/github/image_11k/Train/Train/Train"
    train_csvfilepath = os.path.join(train_csvpath, train_csvfile)

    train_imgfile = ""
    train_imgpath = "/home/jdwei/Desktop/github/image_11k/Train/Train/Train"
    train_imgfilepath = os.path.join(train_csvpath, train_imgfile)

    # Test dataset
    test_csvfile = "test_labels.csv"
    test_csvpath = "/home/share/image_11k/Hands/Test"
    test_csvfilepath = os.path.join(test_csvpath, test_csvfile)

    test_imgfile = ""
    test_imgpath = "/home/share/image_11k/Hands/Test"
    test_imgfilepath = os.path.join(test_imgpath, test_imgfile)

    # Control flag
    train_data_split_flag = False
    test_data_split_flag = False


    '''
    Collect dataset
    '''
    infd = ""
    infdpath = "/home/share/image_11k/Hands/Train"
    infdfilepath = os.path.join(infdpath, infd)

    outfd = "Train"
    outfdpath = "/home/jdwei/Desktop/github/image_11k/Train/"
    outfdfilepath = os.path.join(outfdpath, outfd)

    fd_include_name = ["rotate"]
    fd_remove_name = ["lumin0.1", "lumin5.0"]
    # Control flag
    collect_data_flag = False
    copy_flag = False
    traindata_flag = True
