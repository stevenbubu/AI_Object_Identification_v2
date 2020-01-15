import os, io
import pandas as pd
import tensorflow as tf

from PIL import Image
from collections import namedtuple, OrderedDict

from utils import dataset_util
from utils import config

import logging
import config.log_config as logcfg
logging.config.dictConfig(logcfg.config)
log = logging.getLogger("StreamLogger")

""" FLAGS """
flags = tf.compat.v1.flags
flags.DEFINE_string(name="INIT_CONFIGS_PATH", default="config/hand_dataset_generate_tfrecord.config", help="Config file path.")
FLAGS = flags.FLAGS


# TO-DO replace this with label map
# hands = ['PalmarRight', 'DorsalRight', 'PalmarLeft', 'DorsalLeft']
# def class_text_to_int(row_label):
#     if row_label == 'PalmarRight': return 1
#     elif row_label == 'DorsalRight': return 2
#     elif row_label == 'PalmarLeft': return 3
#     elif row_label == 'DorsalLeft': return 4
#     else: None


def split(df, group):
    data = namedtuple('data', ['filename', 'object'])
    gb = df.groupby(group)
    return [data(filename, gb.get_group(x)) for filename, x in zip(gb.groups.keys(), gb.groups)]


def create_tf_example(group, path):
    with tf.io.gfile.GFile(os.path.join(path, '{}'.format(group.filename)), 'rb') as fid:
        encoded_jpg = fid.read()
    encoded_jpg_io = io.BytesIO(encoded_jpg)
    image = Image.open(encoded_jpg_io)
    width, height = image.size

    filename = group.filename.encode('utf8')
    image_format = b'jpg'
    xmins = []
    xmaxs = []
    ymins = []
    ymaxs = []
    classes_text = []
    classes = []

    for index, row in group.object.iterrows():
        xmins.append(row['xmin'] / width)
        xmaxs.append(row['xmax'] / width)
        ymins.append(row['ymin'] / height)
        ymaxs.append(row['ymax'] / height)
        classes_text.append(str(row['class']).encode('utf8'))
        classes.append(int(row['class']))

    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(height),
        'image/width': dataset_util.int64_feature(width),
        'image/filename': dataset_util.bytes_feature(filename),
        'image/source_id': dataset_util.bytes_feature(filename),
        'image/encoded': dataset_util.bytes_feature(encoded_jpg),
        'image/format': dataset_util.bytes_feature(image_format),
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
        'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
        'image/object/class/label': dataset_util.int64_list_feature(classes),
    }))
    
    return tf_example


def getConfig(config, name):
    Config = config["Flags"]
    Train = Config[name]
    IMAGE_PATH = Train["IMAGE"]["path"]
    CSV_FILE = os.path.join(Train["CSV"]["path"], Train["CSV"]["file"])
    TF_FILE = os.path.join(Train["TF_FILE"]["path"], Train["TF_FILE"]["file"])
    return IMAGE_PATH, CSV_FILE, TF_FILE


def writeTFRecord(imgpath, csvpath, outputpath, name):
    # Write the serialized example to a record file.
    with tf.io.TFRecordWriter(outputpath) as writer:
        examples = pd.read_csv(csvpath)
        grouped = split(examples, 'filename')
        file_index=0
        for group in grouped:
            file_index += 1
            tf_example = create_tf_example(group, imgpath)
            writer.write(tf_example.SerializeToString())
            log.info(name + ":" + str(file_index) + " file: " + group.filename + " process finish.")
    log.info("Successfully created the TFRecords: {}".format(outputpath))


def main():
    # import config
    InitConfig = config.get_config_from_init_config(init_configs_path=FLAGS.INIT_CONFIGS_PATH)
    Train_flag = InitConfig["Flags"]["Option"]["Train"]
    Test_flag = InitConfig["Flags"]["Option"]["Test"]

    if Train_flag:
        train_IMAGE_PATH, train_CSV_FILE, train_TF_FILE = getConfig(InitConfig, name="Train")
        writeTFRecord(imgpath=train_IMAGE_PATH, 
                        csvpath=train_CSV_FILE, 
                        outputpath=train_TF_FILE,
                        name="Train")

    if Test_flag:
        test_IMAGE_PATH, test_CSV_FILE, test_TF_FILE = getConfig(InitConfig, name="Test")
        writeTFRecord(imgpath=test_IMAGE_PATH, 
                        csvpath=test_CSV_FILE, 
                        outputpath=test_TF_FILE,
                        name="Test")


if __name__ == '__main__':
    main()