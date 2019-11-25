"""
Usage:
  # From tensorflow/models/
  # Create train data:
  python generate_tfrecord.py --csv_input=images/train_labels.csv --image_dir=images/train --output_path=train.record
  # Create test data:
  python generate_tfrecord.py --csv_input=images/test_labels.csv  --image_dir=images/test --output_path=test.record
"""
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import io
import pandas as pd
import tensorflow as tf

from PIL import Image
from utils import dataset_util
from collections import namedtuple, OrderedDict

from config.data_11khands_gentf_config import FLAGS
from utils.function_util import FUNC
import time
import logging.config
import config.log_config as selfcfg
logging.config.dictConfig(selfcfg.config)
logger = logging.getLogger("StreamLogger")


# TO-DO replace this with label map
# hands = ['PalmarRight', 'DorsalRight', 'PalmarLeft', 'DorsalLeft']
def class_text_to_int(row_label):
    if row_label == 'PalmarRight': return 1
    elif row_label == 'DorsalRight': return 2
    elif row_label == 'PalmarLeft': return 3
    elif row_label == 'DorsalLeft': return 4
    else: None


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
        classes_text.append(row['class'].encode('utf8'))
        classes.append(class_text_to_int(row['class']))

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


def writeTFRecord(csvpath, imgpath, outputpath):
    # Write the serialized example to a record file.
    with tf.io.TFRecordWriter(outputpath) as writer:
        examples = pd.read_csv(csvpath)
        grouped = split(examples, 'filename')
        index=0
        for group in grouped:
            index += 1
            tf_example = create_tf_example(group, imgpath)
            writer.write(tf_example.SerializeToString())
            logger.info("[" + str(index) + "] Image process finish.")
    logger.info("Successfully created the TFRecords: {}".format(outputpath))


def main(_):
    
    FUNC.createFolder([FLAGS.train_outputpath, FLAGS.test_outputpath])

    # Test tfrecord
    if FLAGS.Test_tfrecord_flg:
        test_start_time = time.time()
        writeTFRecord(csvpath=FLAGS.test_csvfilepath, 
                        imgpath=FLAGS.test_imgfilepath, 
                        outputpath=FLAGS.test_outputfilepath)
        test_end_time = time.time()
        test_spend = FUNC.timing(test_end_time - test_start_time)
        FUNC.save_txt(FLAGS.test_outputpath+'/time.txt', test_spend, string="\ntest tfrecord: ")

    # Train tfrecord
    if FLAGS.Train_tfrecord_flg:
        train_start_time = time.time()
        writeTFRecord(csvpath=FLAGS.train_csvfilepath, 
                        imgpath=FLAGS.train_imgfilepath, 
                        outputpath=FLAGS.train_outputfilepath)
        train_end_time = time.time()
        train_spend = FUNC.timing(train_end_time - train_start_time)
        FUNC.save_txt(FLAGS.train_outputpath+'/time.txt', train_spend, string="\ntrain tfrecord: ")


if __name__ == '__main__':
    tf.compat.v1.app.run()