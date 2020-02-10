import os
import shutil
import xml.etree.ElementTree as ET
import tensorflow as tf
from utils import config
from utils import func_util

import logging
import config.log_config as logcfg
logging.config.dictConfig(logcfg.config)
log = logging.getLogger("StreamLogger")

""" FLAGS """
flags = tf.compat.v1.flags
flags.DEFINE_string(name="INIT_CONFIGS_PATH", default="config/hand_dataset_process.config", help="Config file path.")
FLAGS = flags.FLAGS


def getConfig(config, name):
    Config = config["Flags"]
    Train = Config[name]
    IMAGE_PATH = Train["IMAGE"]["path"]
    XML_PATH = Train["XML"]["path"]
    ERROR_FILE_PATH = Train["ERROR"]["path"]
    CSV_FILE = os.path.join(Train["CSV"]["path"], Train["CSV"]["file"])
    return IMAGE_PATH, XML_PATH, ERROR_FILE_PATH, CSV_FILE


def DataProcess(image_path, xml_path, error_file_path, csv_file, name):
    IMGfile = []
    XMLfile = []
    [IMGfile.append(f) for f in os.listdir(image_path) if f.endswith(".jpg")]
    [XMLfile.append(f) for f in os.listdir(xml_path) if f.endswith(".xml")]

    rowname = ["filename", "width", "height", "class", "xmin", "ymin", "xmax", "ymax"]
    csv_label = []
    csv_label.append(rowname)
    file_index = 0
    for xmlfile in XMLfile:
        break_fg = False
        xmlfilepath = os.path.join(xml_path, xmlfile)
        tree = ET.parse(xmlfilepath)
        root = tree.getroot()

        for item in root:
            if item.tag == "filename":
                filename = item.text
                filepath  = os.path.join(image_path, filename)
                if not os.path.isfile(filepath):
                    break_fg = True
                    if not os.path.isdir(error_file_path):
                        os.mkdir(error_file_path)
                    shutil.move(xmlfilepath, os.path.join(error_file_path, xmlfile))
                    log.info("Image: " + filepath + " not exist.")
                    break
            elif item.tag == "size":
                width = item.find('width').text
                height = item.find('height').text
            elif item.tag == "object":
                object_label = []
                classes = item.find('name').text
                xmin = item.find('bndbox').find('xmin').text
                ymin = item.find('bndbox').find('ymin').text
                xmax = item.find('bndbox').find('xmax').text
                ymax = item.find('bndbox').find('ymax').text
                object_label = [filepath, width, height, classes, xmin, ymin, xmax, ymax]
                csv_label.append(object_label)

        if not break_fg:
            file_index += 1
            log.info(name + ":" + str(file_index) + " file: " + xmlfilepath + " process finish.")
    
    func_util.save_csv(csv_file, csv_label)


def Train(config):
    train_IMAGE_PATH, train_XML_PATH, train_ERROR_FILE_PATH, train_CSV_FILE = getConfig(config, name="Train")
    DataProcess(train_IMAGE_PATH, train_XML_PATH, train_ERROR_FILE_PATH, train_CSV_FILE, name="Train")


def Test(config):
    test_IMAGE_PATH, test_XML_PATH, test_ERROR_FILE_PATH, test_CSV_FILE = getConfig(config, name="Test")
    DataProcess(test_IMAGE_PATH, test_XML_PATH, test_ERROR_FILE_PATH, test_CSV_FILE, name="Test")
    

def main():
    # import config
    InitConfig = config.get_config_from_init_config(init_configs_path=FLAGS.INIT_CONFIGS_PATH)
    Train_flag = InitConfig["Flags"]["Option"]["Train"]
    Test_flag = InitConfig["Flags"]["Option"]["Test"]

    if Train_flag:
        Train(InitConfig)

    if Test_flag:
        Test(InitConfig)



if __name__ == '__main__':
    main()

