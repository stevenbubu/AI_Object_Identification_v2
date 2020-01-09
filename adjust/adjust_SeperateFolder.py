import os, csv
import shutil
from utils.function_util import FUNC
from config.adjust_SeperateFolder_config import FLAGS
from data_11khands_class_v3 import trainData


def save_csv(csv_path, csv_content):
    with open(csv_path, 'a') as csvfile:
        wr = csv.writer(csvfile)
        for i in range(len(csv_content)):
            wr.writerow(csv_content[i])

def SeperateFolder(folder, filepath):
    csvholder = []; labelrow = []
    # 開啟 CSV 檔案
    with open(filepath, newline='') as csvfile:
        # 讀取 CSV 檔案內容
        rows = csv.reader(csvfile)
        header = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
        csvholder.append(header)
        # 以迴圈輸出每一列
        for row in rows:
            if str(folder) in row[header.index('filename')]:
                if "Test" in filepath:
                    labelrow = [
                        '_'.join(row[header.index('filename')].split("_")[-2:]),
                        row[header.index('width')],
                        row[header.index('height')],
                        row[header.index('class')][:-1],
                        row[header.index('xmin')],
                        row[header.index('ymin')],
                        row[header.index('xmax')],
                        row[header.index('ymax')],
                    ]
                else:
                    labelrow = [
                        '_'.join(row[header.index('filename')].split("_")[-2:]),
                        row[header.index('width')],
                        row[header.index('height')],
                        row[header.index('class')],
                        row[header.index('xmin')],
                        row[header.index('ymin')],
                        row[header.index('xmax')],
                        row[header.index('ymax')],
                    ]
                csvholder.append(labelrow)
                
    csv_path = os.path.join(os.path.dirname(filepath), folder, folder + ".csv")
    if os.path.exists(csv_path):
        os.remove(csv_path)
        save_csv(csv_path, csvholder)
    else:
        save_csv(csv_path, csvholder)


'''
2019-12-24
1. Seperate to small folders from Train and Test large folders. 
2. Collect needed folders.

Main function
'''
if FLAGS.train_data_split_flag:
    os.chdir(FLAGS.train_imgfilepath) 

    for f in os.listdir(FLAGS.train_imgfilepath):
        if (f.split(".")[-1] == "jpg"):
            fdname = '_'.join(f.split("_")[:-2])
            filename = '_'.join(f.split("_")[-2:])
            if not os.path.isdir(fdname):
                FUNC.createFolder([fdname])
            img_des_path = os.path.join(fdname, filename)
            shutil.move(f, img_des_path)

    for fd in os.listdir(FLAGS.train_imgfilepath):
        if os.path.isdir(fd):
            SeperateFolder(fd, FLAGS.train_csvfilepath)
    os.remove(FLAGS.train_csvfilepath)


if FLAGS.test_data_split_flag:
    os.chdir(FLAGS.test_imgfilepath) 

    for f in os.listdir(FLAGS.test_imgfilepath):
        if (f.split(".")[-1] == "jpg"):
            fdname = '_'.join(f.split("_")[:-2])[:-1]
            filename = '_'.join(f.split("_")[-2:])
            if not os.path.isdir(fdname):
                FUNC.createFolder([fdname])
            img_des_path = os.path.join(fdname, filename)
            shutil.move(f, img_des_path)

    for fd in os.listdir(FLAGS.test_imgfilepath):
        if os.path.isdir(fd):
            SeperateFolder(fd, FLAGS.test_csvfilepath)
    os.remove(FLAGS.test_csvfilepath)
            

if FLAGS.collect_data_flag:
    os.chdir(FLAGS.infdfilepath) 
    if not os.path.isdir(FLAGS.outfdfilepath):
        FUNC.createFolder([FLAGS.outfdfilepath])
 
    usedfd = FUNC.filterUseFolders(FLAGS.infdfilepath, FLAGS.fd_include_name)
    if FLAGS.fd_remove_name:
        removefd = FUNC.filterUseFolders(FLAGS.infdfilepath, FLAGS.fd_remove_name)
        usedfd = FUNC.filterExistFolders(removefd, usedfd)
    existfd = FUNC.filterUseFolders(FLAGS.outfdfilepath, FLAGS.fd_include_name)
    usedfd = FUNC.filterExistFolders(existfd, usedfd)
    print(usedfd)
    print("\nLen: " + str(len(usedfd)))

    if FLAGS.copy_flag:
        for fd in usedfd:
            shutil.copytree(os.path.join(FLAGS.infdfilepath, fd), os.path.join(FLAGS.outfdfilepath, fd)) 


if FLAGS.traindata_flag:
    trainData(FLAGS.outfdfilepath, folders=FLAGS.fd_include_name)
