import scipy.io as sio
import numpy as np
import os
import six.moves.urllib as urllib
import cv2
import time
import random
import zipfile
import csv
import libs.gesture as gesture
import libs.data_11khands_class_lib as hands_lib
from config.data_11khands_class_config import FLAGS
import shutil 

'''
Replace a set of multiple sub strings with a new string in main string.
'''
def replaceMultiple(mainString, toBeReplaces, newString):
    # Iterate over the strings to be replaced
    for elem in toBeReplaces :
        # Check if string is in the main string
        if elem in mainString :
            # Replace the string
            mainString = mainString.replace(elem, newString)
    
    return  mainString


def save_csv(csv_path, csv_content):
    with open(csv_path, 'w') as csvfile:
        wr = csv.writer(csvfile)
        for i in range(len(csv_content)):
            wr.writerow(csv_content[i])


def create_directory(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


# combine all individual csv files for each image into a single csv file per folder.
def generate_label_files(image_dir):
    header = ['filename', 'width', 'height',
              'class', 'xmin', 'ymin', 'xmax', 'ymax']
    for root, dirs, filenames in os.walk(image_dir):
        for dir in dirs:
            csvholder = []
            csvholder.append(header)
            loop_index = 0
            for f in os.listdir(image_dir + dir):
                if (f.split(".")[1] == "csv"):
                    loop_index += 1
                    
                    csv_file = open(image_dir + dir + "/" + f, 'r')
                    reader = csv.reader(csv_file)
                    for row in reader:
                        csvholder.append(row)
                    csv_file.close()
                    os.remove(image_dir + dir + "/" + f)
            save_csv(image_dir + dir + "/" + dir + "_labels.csv", csvholder)
            print("Saved label csv for ", dir, image_dir +
                  dir + "/" + dir + "_labels.csv")


# Split data, copy to train/test folders
def split_data_test_eval_train(image_dir):

    base_path = image_dir.rpartition('/')[0]
    create_directory(base_path + "/images")
    create_directory(base_path + "/images/train")
    create_directory(base_path + "/images/test")

    data_size = len([file for file in os.listdir(image_dir)])
    loop_index = 0
    data_sampsize = int(0.1 * data_size)
    test_samp_array = random.sample(range(data_size), k=data_sampsize)

    for root, _, filenames in os.walk(image_dir):
        for filename in filenames:
            if(filename.split(".")[1] == "jpg"):
                loop_index += 1

                if loop_index in test_samp_array:
                    os.rename(image_dir + "/" + filename, base_path + "/images/test/" + filename)
                    os.rename(image_dir + "/" + filename.split(".")[0] + ".csv", 
                            base_path + "/images/test/" + filename.split(".")[0] + ".csv")
                else:
                    os.rename(image_dir + "/" + filename, base_path + "/images/train/" + filename)
                    os.rename(image_dir + "/" + filename.split(".")[0] + ".csv", 
                            base_path + "/images/train/" + filename.split(".")[0] + ".csv")
                print(loop_index, image_dir + filename)
        os.remove(base_path + "/HandInfo.mat")
        os.rmdir(image_dir)

        print("Train/test content generation complete!")
        generate_label_files(base_path + "/images/")


def get_bbox(image_dir):
    
    base_path = image_dir.rpartition('/')[0]
    image_path_array = []
    for root, _, filenames in os.walk(image_dir):
        for f in filenames:
            if(f.split(".")[1] == "jpg"):
                img_path = root + "/" + f
                image_path_array.append(img_path)
    
    #sort image_path_array to ensure its in the low to high order expected in polygon.mat
    image_path_array.sort()
    boxes = sio.loadmat(base_path + "/" + "HandInfo.mat")

    handinfo = boxes["HandInfo"][0]
    pointindex = 0
 
    for first in handinfo:
        csvholder = []
        font = cv2.FONT_HERSHEY_SIMPLEX

        img_id = image_path_array[pointindex]
        img = cv2.imread(img_id)
        frame_img, [xmin, ymin, xmax, ymax]= gesture.grdetect(img)
        height, width, _ = img.shape
        path, tail = os.path.split(img_id)
        print("Processing index", pointindex, ": ", tail)
        pointindex += 1

        hand = replaceMultiple(str(first[6]), ['[', ']', '\''] , "")
        labelrow = [tail, width, height, hand, xmin, ymin, xmax, ymax]
        csvholder.append(labelrow)

        imgcsv = img_id.split(".")[0] + ".csv"
        if not os.path.exists(imgcsv):
            save_csv(imgcsv, csvholder)
        else:
            os.remove(imgcsv)
            save_csv(imgcsv, csvholder)
        print("===== saving csv file for ", csvholder)

        if not os.path.exists(os.path.split(path)[0] + "/" + "frame_image"):
            create_directory(os.path.split(path)[0] + "/" + "frame_image")

        frame_img_path = os.path.split(path)[0] + "/" + "frame_image" + "/" + tail
        if not os.path.exists(frame_img_path):
            cv2.imwrite(frame_img_path, frame_img)
        else:
            os.remove(frame_img_path)
            cv2.imwrite(frame_img_path, frame_img)
        print("===== saving frame image path:", frame_img_path)


def generate_csv_files(image_dir):
    get_bbox(image_dir)

    print("CSV generation complete!\nGenerating train/test/eval folders")
    split_data_test_eval_train(image_dir)


def extract_folder(zip_dataset):
    print("Hands dataset already downloaded.\nGenerating CSV files")
    dataset_path = os.path.dirname(os.path.abspath(zip_dataset))
    if not os.path.exists("Hands"):
        zip_ref = zipfile.ZipFile(zip_dataset, 'r')
        print("> Extracting Dataset files")
        # zip_ref.extractall("Hands")
        zip_ref.extractall()
        print("> Extraction complete")
        zip_ref.close()    
        hands_lib.hand_dataset_split(dataset_path)
        # generate_csv_files(os.path.abspath("Hands"))
    else:
        hands_lib.hand_dataset_split(dataset_path)
        # generate_csv_files(os.path.abspath("Hands"))


def download_hands_dataset(path, zipfile, csvfile):
    
    try:
        os.makedirs(FLAGS.filepath)
    except OSError:
        print ("image_11k file already exist.")
    else:
        print ("Successfully create the file.")
    
    os.chdir(FLAGS.filepath) 
    
    is_zip = os.path.exists(os.path.join(path, zipfile))
    is_csv = os.path.exists(os.path.join(path, csvfile))
    # is_txt = os.path.exists("HandInfo.txt")
    # is_mat = os.path.exists("HandInfo.mat")

    if not is_csv:
        print("> downloading HandInfo.csv file.")
        opener = urllib.request.URLopener()
        opener.retrieve(FLAGS.HANDS_CSV_URL, csvfile)
        print("> csv download complete")
    else:
        [shutil.copy(os.path.join(path, csvfile), os.path.join(FLAGS.filepath, csvfile)) if not os.path.exists(csvfile) else None]

    try:
        if not is_zip:
            print(
                "> downloading egohands dataset. This may take a while (1.3GB, say 3-5mins). Coffee break?")
            opener = urllib.request.URLopener()
            opener.retrieve(FLAGS.HANDS_DATASET_URL, zipfile)
            print("> zip download complete")
        else:
            [shutil.copy(os.path.join(path, zipfile), os.path.join(FLAGS.filepath, zipfile)) if not os.path.exists(zipfile) else None]
    except OSError:
        print ("> zip download failure")
    else:
        extract_folder(zipfile)

    # if not is_txt:
    #     print("> downloading HandInfo.txt file.")
    #     opener = urllib.request.URLopener()
    #     opener.retrieve(txt_url, "HandInfo.txt")

    # if not is_mat:
    #     print("> downloading HandInfo.mat file.")
    #     opener = urllib.request.URLopener()
    #     opener.retrieve(mat_url, "HandInfo.mat")


start_time = time.time()
download_hands_dataset(path=os.getcwd(), zipfile=FLAGS.HANDS_FILE, csvfile=FLAGS.HANDS_INFO)
end_time = time.time()
total_spend = hands_lib.timing(end_time - start_time)
hands_lib.save_txt(FLAGS.filepath+'/time.txt', total_spend, string="total: ")
