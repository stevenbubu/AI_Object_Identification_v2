import os, csv
import random
import libs.gesture as gesture
import skimage, shutil, cv2
import time
import zipfile
import six.moves.urllib as urllib
from config.data_11khands_class_config import FLAGS
import threading
from queue import Queue


def Testlen(DorsalRight=[], PalmarRight=[], DorsalLeft=[], PalmarLeft=[]):
    print("dorsal_right length: ", len(DorsalRight))
    print("palmar_right length: ", len(PalmarRight))
    print("dorsal_left length: ", len(DorsalLeft))
    print("palmar_left length: ", len(PalmarLeft))


def save_txt(txt_path, txt_content, string=""):
    with open(txt_path, 'a') as txtfile:
        txtfile.writelines(string + txt_content)


def save_csv(csv_path, csv_content):
    with open(csv_path, 'a') as csvfile:
        wr = csv.writer(csvfile)
        for i in range(len(csv_content)):
            wr.writerow(csv_content[i])


def read_csv(csv_path, name="", header=[]):
    with open(csv_path, newline='') as csvfile:
        # 讀取 CSV 檔案內容
        csvholder=[]
        rows = csv.reader(csvfile)
        for row in rows:
            if row == header:
                continue
            else:
                row[0] = str(name) + row[0]
                csvholder.append(row)
    return csvholder


def SeperateClass(filepath):
    DorsalRight = []
    PalmarRight = []
    DorsalLeft = []
    PalmarLeft = []
    # 開啟 CSV 檔案
    with open(filepath, newline='') as csvfile:
        # 讀取 CSV 檔案內容
        rows = csv.reader(csvfile)
        header = ['id', 'age', 'gender', 'skinColor', 'accessories', 'nailPolish', 
                    'aspectOfHand', 'imageName', 'irregularities']
        # 以迴圈輸出每一列
        for row in rows:
            if "dorsal right" in row:
                DorsalRight.append(row[header.index('imageName')])
            elif "palmar right" in row:
                PalmarRight.append(row[header.index('imageName')])
            elif "dorsal left" in row:
                DorsalLeft.append(row[header.index('imageName')])
            elif "palmar left" in row:
                PalmarLeft.append(row[header.index('imageName')])
 
        Testlen(DorsalRight, PalmarRight, DorsalLeft, PalmarLeft)
    
    return DorsalRight, PalmarRight, DorsalLeft, PalmarLeft


def createFolder(folders, path=None):
    for folder in folders:
        if path is not None:
            fdpath = os.path.join(path, folder)    
        else:
            fdpath = folder
        try:
            if not os.path.exists(fdpath):
                os.makedirs(fdpath)
            else:
               print('Folder already exists: ' +  folder) 
        except OSError:
            print ('Error: Creating directory. ' + fdpath)


def moveFiles(path, folders=[], **dict):   
    DorsalRight = []
    PalmarRight = []
    DorsalLeft = []
    PalmarLeft = []
    for key, value in dict.items():
        for k, v in value.items():
            if "DorsalRight" == folders[folders.index(k)]:
                DorsalRight = v
            elif "PalmarRight" == folders[folders.index(k)]:
                PalmarRight = v
            elif "DorsalLeft" == folders[folders.index(k)]:
                DorsalLeft = v
            elif "PalmarLeft" == folders[folders.index(k)]:
                PalmarLeft = v
            else:
                print("Error: no folder in " + folders)
            
    Testlen(DorsalRight, PalmarRight, DorsalLeft, PalmarLeft)

    for folder in folders:
        fdpath = os.path.join(path, folder)
        if folder == "DorsalRight":
            try:
                for file in DorsalRight:
                    img_sor_path = os.path.join(path, file)
                    img_des_path = os.path.join(fdpath, file)
                    shutil.move(img_sor_path, img_des_path)
            except OSError:
                print ('Error: no images in: ' + folder)
        elif folder == "PalmarRight":
            try:
                for file in PalmarRight:
                    img_sor_path = os.path.join(path, file)
                    img_des_path = os.path.join(fdpath, file)
                    shutil.move(img_sor_path, img_des_path)
            except OSError:
                print ('Error: no images in: ' + folder)
        elif folder == "DorsalLeft":
            try:
                for file in DorsalLeft:
                    img_sor_path = os.path.join(path, file)
                    img_des_path = os.path.join(fdpath, file)
                    shutil.move(img_sor_path, img_des_path)
            except OSError:
                print ('Error: no images in: ' + folder)
        elif folder == "PalmarLeft":
            try:
                for file in PalmarLeft:
                    img_sor_path = os.path.join(path, file)
                    img_des_path = os.path.join(fdpath, file)
                    shutil.move(img_sor_path, img_des_path)
            except OSError:
                print ('Error: no images in: ' + folder)

        [print(folder + " length: ", len(files)) for root, dirs, files in os.walk(fdpath)]
            

def choseImg(path, Num, folders=[], **dict):
    DorsalRight = []
    PalmarRight = []
    DorsalLeft = []
    PalmarLeft = []
    for key, value in dict.items():
        for k, v in value.items():
            if "DorsalRight" == folders[folders.index(k)]:
                DorsalRight = v
            elif "PalmarRight" == folders[folders.index(k)]:
                PalmarRight = v
            elif "DorsalLeft" == folders[folders.index(k)]:
                DorsalLeft = v
            elif "PalmarLeft" == folders[folders.index(k)]:
                PalmarLeft = v
            else:
                print("Error: no folder in " + folders)
   
    Testlen(DorsalRight, PalmarRight, DorsalLeft, PalmarLeft)
    
    random.shuffle(DorsalRight)
    random.shuffle(PalmarRight)
    random.shuffle(DorsalLeft)
    random.shuffle(PalmarLeft)
    img_dict = {}
    img_dict["DorsalRight"] = DorsalRight[:Num]
    img_dict["PalmarRight"] = PalmarRight[:Num]
    img_dict["DorsalLeft"] = DorsalLeft[:Num]
    img_dict["PalmarLeft"] = PalmarLeft[:Num]

    Testlen(DorsalRight, PalmarRight, DorsalLeft, PalmarLeft)
   
    moveTestFiles(path=path, folders=folders, dict=img_dict)


def moveTestFiles(path, folders=[], **dict):
    DorsalRight = []
    PalmarRight = []
    DorsalLeft = []
    PalmarLeft = []
    for key, value in dict.items():
        for k, v in value.items():
            if "DorsalRight" == folders[folders.index(k)]:
                DorsalRight = v
            elif "PalmarRight" == folders[folders.index(k)]:
                PalmarRight = v
            elif "DorsalLeft" == folders[folders.index(k)]:
                DorsalLeft = v
            elif "PalmarLeft" == folders[folders.index(k)]:
                PalmarLeft = v
            else:
                print("Error: no folder in " + folders2)
            
    Testlen(DorsalRight, PalmarRight, DorsalLeft, PalmarLeft)

    for folder in folders:
        fdpath = os.path.join(path, folder)
        fdpath_Test = os.path.join(path, 'Test')
        if folder == "DorsalRight":
            DorsalRight_tmp = [f for f in os.listdir(fdpath) if f not in DorsalRight]
            try:
                for file in DorsalRight_tmp:
                    img_sor_path = os.path.join(fdpath, file)
                    img_des_path = os.path.join(fdpath_Test, folder, file)
                    shutil.move(img_sor_path, img_des_path)
            except OSError:
                print ('Error: no images in: ' + folder)
        elif folder == "PalmarRight":
            PalmarRight_tmp = [f for f in os.listdir(fdpath) if f not in PalmarRight]
            try:
                for file in PalmarRight_tmp:
                    img_sor_path = os.path.join(fdpath, file)
                    img_des_path = os.path.join(fdpath_Test, folder, file)
                    shutil.move(img_sor_path, img_des_path)
            except OSError:
                print ('Error: no images in: ' + folder)
        elif folder == "DorsalLeft":
            DorsalLeft_tmp = [f for f in os.listdir(fdpath) if f not in DorsalLeft]
            try:
                for file in DorsalLeft_tmp:
                    img_sor_path = os.path.join(fdpath, file)
                    img_des_path = os.path.join(fdpath_Test, folder, file)
                    shutil.move(img_sor_path, img_des_path)
            except OSError:
                print ('Error: no images in: ' + folder)
        elif folder == "PalmarLeft":
            PalmarLeft_tmp = [f for f in os.listdir(fdpath) if f not in PalmarLeft]
            try:
                for file in PalmarLeft_tmp:
                    img_sor_path = os.path.join(fdpath, file)
                    img_des_path = os.path.join(fdpath_Test, folder, file)
                    shutil.move(img_sor_path, img_des_path)
            except OSError:
                print ('Error: no images in: ' + folder)

        [print(folder + " length: ", len(files)) for root, dirs, files in os.walk(fdpath)]
            

def checkOldFolders(sentence, words): 
    sentence_tmp = []
    [sentence_tmp.append(j) for k in words for j in sentence if k in j]
    return sentence_tmp


def delOldFolders(path, folders=[], name=[]): 
    files = os.listdir(path)
    files_tmp = []
    [files_tmp.append(f) for f in files for d in name if d in f]     
    [files.remove(f) for f in files_tmp]  
    files_tmp = []
    [files_tmp.append(j) for k in folders for j in files if k in j and not "jpg" in j]
    [shutil.rmtree(os.path.join(path, f)) for f in files_tmp]
    print("Delete old files finish. Folders:" + str(files_tmp) + " Len:" + str(len(files_tmp)))


def recordHandLoc(path, name=[]):
    files = os.listdir(path)
    usefd = []
    [usefd.append(f) for f in files for d in name if d in f] 
    for folder in usefd:
        basepath = os.path.join(path, folder)
        csvholder = []
        header = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
        csvholder.append(header)
        index = 0
        for f in os.listdir(basepath):
            xmin=0; ymin=0; xmax=0; ymax=0
            labelrow = []
            if(f.split(".")[-1] == "jpg"):
                index += 1
                img_sor_path = os.path.join(basepath, f)
                img = cv2.imread(img_sor_path)
                h, w, _ = img.shape
                frame_img, [xmin, ymin, xmax, ymax]= gesture.grdetect(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                labelrow = [f, w, h, folder.split("_")[0], xmin, ymin, xmax, ymax]
                csvholder.append(labelrow)
                print("Folder:" + folder + ", [" + str(index) + "] image:" + f + " temp location process finish.")

        csv_path = os.path.join(basepath, folder + ".csv")
        if os.path.exists(csv_path):
            os.remove(csv_path)
            save_csv(csv_path, csvholder)
        else:
            save_csv(csv_path, csvholder)
        print("Folder:" + folder + " record location process finish.")
        cv2.waitKey(2)  # close window when a key press is detected
    print("Images record location process finish. Len:" + str(len(usefd)))


def filterUseFolders(path, folders=[]):
    files = os.listdir(path)
    files_tag = []
    [files_tag.append(f) for f in files for d in folders if d in f]
    return files_tag


def flipHImg(queues, path, folders=[], flips=[]):
    flipfd = []
    [flipfd.append("flipH" + str(fp)) for fp in flips]
    for folder in folders:
        basepath = os.path.join(path, folder)
        flipfdpath = [os.path.join(basepath + '_' + f) for f in flipfd]
        createFolder(flipfdpath)
        index = 0
        for f in os.listdir(basepath):
            if(f.split(".")[-1] == "jpg"):
                index += 1
                img_sor_path = os.path.join(basepath, f)
                img = cv2.imread(img_sor_path)
                for idx in flips:
                    img_des_path = os.path.join(flipfdpath[flips.index(idx)], f)
                    flipH_img = cv2.flip(img, 1) if idx == 1 else img
                    cv2.imwrite(img_des_path, flipH_img)
                    print("Folder:" + folder + ", [" + str(index) + "] image:" + f + " flip:" + str(idx) + " process finish.")
        print("Folder:" + folder + " process finish. Len:" + str(len(os.listdir(basepath))))
    print("Images flip process finish. Len:" + str(len(flipfd)))
    return queues.put(flipfd[0])


def rotateImg(queues, path, folders=[], usefd=[], rotates=[]):
    rotatefd = []
    [rotatefd.append("rotate" + str(rt)) for rt in rotates]
    for folder in usefd:
        basepath = os.path.join(path, folder)
        rotatefdpath = [os.path.join(basepath + '_' + f) for f in rotatefd] 
        createFolder(rotatefdpath)
        index = 0
        for f in os.listdir(basepath):
            if(f.split(".")[-1] == "jpg"):
                index += 1
                img_sor_path = os.path.join(basepath, f)
                img = cv2.imread(img_sor_path)
                h, w, _ = img.shape
                center = (int(w/2), int(h/2))
                for idx in rotates:
                    img_des_path = os.path.join(rotatefdpath[rotates.index(idx)], f)
                    M = cv2.getRotationMatrix2D(center, idx, 1)
                    rotate_img = cv2.warpAffine(img, M, (w,h), borderValue=(255,255,255))
                    cv2.imwrite(img_des_path, rotate_img)
                    print("Folder:" + folder + ", [" + str(index) + "] image:" + f + " rotate:" + str(idx)+ " process finish.")
        print("Folder:" + folder + " process finish. Len:" + str(len(os.listdir(basepath))))
    print("Images rotate process finish. Len:" + str(len(rotatefd)))
    return queues.put(rotatefd[0])
    
   
def scaleImg(queues, path, folders=[], usefd=[], scales=[]):
    scalefd = []
    [scalefd.append("scale" + str(scl)) for scl in scales]
    for folder in usefd:
        basepath = os.path.join(path, folder)
        scalefdpath = [os.path.join(basepath + '_' + f) for f in scalefd] 
        createFolder(scalefdpath)
        index = 0
        for f in os.listdir(basepath):
            if(f.split(".")[-1] == "jpg"):
                index += 1
                img_sor_path = os.path.join(basepath, f)
                img = cv2.imread(img_sor_path)
                h, w, _ = img.shape
                center = (int(w/2), int(h/2))
                for idx in scales:
                    img_des_path = os.path.join(scalefdpath[scales.index(idx)], f)
                    M = cv2.getRotationMatrix2D(center, 0, idx)
                    scale_img = cv2.warpAffine(img, M, (w,h), borderValue=(255,255,255))
                    cv2.imwrite(img_des_path, scale_img)
                    print("Folder:" + folder + ", [" + str(index) + "] image:" + f + " scale:" + str(idx)+ " process finish.")
        print("Folder:" + folder + " process finish. Len:" + str(len(os.listdir(basepath))))
    print("Images rotate process finish. Len:" + str(len(scalefd)))
    return queues.put(scalefd[0])


def luminImg(queues, path, folders=[], usefd=[], lumins=[]):
    luminfd = []
    [luminfd.append("lumin" + str(lu)) for lu in lumins]
    for folder in usefd:
        basepath = os.path.join(path, folder)
        luminfdpath = [os.path.join(basepath + '_' + f) for f in luminfd] 
        createFolder(luminfdpath)
        index = 0
        for f in os.listdir(basepath):
            if(f.split(".")[-1] == "jpg"):
                index += 1
                img_sor_path = os.path.join(basepath, f)
                img = cv2.imread(img_sor_path)
                h, w, _ = img.shape
                center = (int(w/2), int(h/2))
                for idx in lumins:
                    img_des_path = os.path.join(luminfdpath[lumins.index(idx)], f)
                    lumin_img = skimage.exposure.adjust_gamma(img, gamma=idx)
                    cv2.imwrite(img_des_path, lumin_img)
                    print("Folder:" + folder + ", [" + str(index) + "] image:" + f + " lumin:" + str(idx)+ " process finish.")
            if(f.split(".")[-1] == "csv"):  
                img_sor_path = os.path.join(basepath, f)  
                for idx in lumins:
                    img_des_path = os.path.join(luminfdpath[lumins.index(idx)], (f[:-4] + "_lumin" + str(idx) + f[-4:]))
                    shutil.copy(img_sor_path, img_des_path)
                    print("Folder:" + folder + " file:" + f + " lumin:" + str(idx)+ " process finish.")
        print("Folder:" + folder + " process finish. Len:" + str(len(os.listdir(basepath))))
    print("Images lumin process finish. Len:" + str(len(luminfd)))
    return queues.put(luminfd[0])


def noiseImg(queues, path, folders=[], usefd=[], noises=[]):
    noisefd = []
    [noisefd.append("noise_" + str(ns)) for ns in noises]
    for folder in usefd:
        basepath = os.path.join(path, folder)
        noisefdpath = [os.path.join(basepath + '_' + f) for f in noisefd] 
        createFolder(noisefdpath)
        index = 0
        for f in os.listdir(basepath):
            if(f.split(".")[-1] == "jpg"):
                index += 1
                img_sor_path = os.path.join(basepath, f)
                noise_img = skimage.io.imread(img_sor_path)
                for idx in noises:
                    img_des_path = os.path.join(noisefdpath[noises.index(idx)], f)
                    if idx is not 'normal':
                        noise_img = skimage.util.random_noise(noise_img, mode=idx)
                    skimage.io.imsave(img_des_path, noise_img)
                    print("Folder:" + folder + ", [" + str(index) + "] image:" + f + " noise:" + str(idx)+ " process finish.")
            if(f.split(".")[-1] == "csv"):  
                img_sor_path = os.path.join(basepath, f)  
                for idx in noises:
                    img_des_path = os.path.join(noisefdpath[noises.index(idx)], (f[:-4] + "_noise" + str(idx) + f[-4:]))
                    shutil.copy(img_sor_path, img_des_path)
                    print("Folder:" + folder + " file:" + f + " noise:" + str(idx)+ " process finish.")
        print("Folder:" + folder + " process finish. Len:" + str(len(os.listdir(basepath))))
    print("Images lumin process finish. Len:" + str(len(noisefd)))
    return queues.put(noisefd[0])


def trainData(path, folders=[]):
    trainfdpath = os.path.join(path, 'Train')
    createFolder([trainfdpath])
    usefd = filterUseFolders(path, folders)
    # Create train_labels.csv
    csv_des_path = os.path.join(trainfdpath, 'train_labels.csv')
    csvholder = []
    header = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    csvholder.append(header)
    save_csv(csv_des_path, csvholder)
    for folder in usefd:
        basepath = os.path.join(path, folder)
        csvholder = []
        index = 0
        for f in os.listdir(basepath):
            if(f.split(".")[-1] == "jpg"):
                index += 1
                img_sor_path = os.path.join(basepath, f)
                img_des_path = os.path.join(trainfdpath, (folder + "_" + f))
                shutil.move(img_sor_path, img_des_path)
                print("Folder:" + folder + ", [" + str(index) + "] image:" + f + " move process finish.")
            if(f.split(".")[-1] == "csv"):  
                csv_sor_path = os.path.join(basepath, f)  
                csvholder = read_csv(csv_sor_path, name=folder+"_", header=header)
                save_csv(csv_des_path, csvholder)
                print("Folder:" + folder + " file:" + f + " csv process finish.")
        print("Folder:" + folder + " process finish.")
    print("Images train data process finish. Len:" + str(len(usefd)))

    delOldFolders(path, folders=usefd)


def testData(path, folders=[]):
    testfdpath = os.path.join(path, 'Test')
    usefd = filterUseFolders(testfdpath, folders)
    recordHandLoc(testfdpath, name=usefd)
    # Create test_labels.csv
    csv_des_path = os.path.join(testfdpath, 'test_labels.csv')
    csvholder = []
    header = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    csvholder.append(header)
    save_csv(csv_des_path, csvholder)
    for folder in usefd:
        basepath = os.path.join(testfdpath, folder)
        csvholder = []
        index = 0
        for f in os.listdir(basepath):
            if(f.split(".")[-1] == "jpg"):
                index += 1
                img_sor_path = os.path.join(basepath, f)
                img_des_path = os.path.join(testfdpath, (folder + "_" + f))
                shutil.move(img_sor_path, img_des_path)
                print("Folder:" + folder + ", [" + str(index) + "] image:" + f + " move process finish.")
            if(f.split(".")[-1] == "csv"):  
                csv_sor_path = os.path.join(basepath, f)  
                csvholder = read_csv(csv_sor_path, name=folder+"_", header=header)
                save_csv(csv_des_path, csvholder)
                print("Folder:" + folder + " file:" + f + " csv process finish.")
        print("Folder:" + folder + " process finish.")
    print("Images train data process finish. Len:" + str(len(usefd)))
    
    delOldFolders(testfdpath, folders=usefd)


def timing(sec):
    day = int(sec//(60*60*24));  day_rm = sec%(60*60*24)
    hour = int(day_rm//(60*60)); hour_rm = day_rm%(60*60)
    mins = int(hour_rm//60);     sec = hour_rm%60

    day = str("0"+str(day)) if day<10 else str(day)
    hour = str("0"+str(hour)) if hour<10 else str(hour)
    mins = str("0"+str(mins)) if mins<10 else str(mins)
    sec = str("0"+str(sec)) if sec<10 else str("%.2f"%sec)
    string = str(day) + ":" + str(hour) + ":" + str(mins) + ":" + str(sec)
    print("Time: " + string)
    return string


def hand_dataset_split(path):
    DorsalRight = []
    PalmarRight = []
    DorsalLeft = []
    PalmarLeft = []

    csvpath = os.path.join(path, FLAGS.HANDS_INFO)
    DorsalRight, PalmarRight, DorsalLeft, PalmarLeft = SeperateClass(csvpath)

    img_dict = {}
    img_dict["DorsalRight"] = DorsalRight
    img_dict["PalmarRight"] = PalmarRight
    img_dict["DorsalLeft"] = DorsalLeft
    img_dict["PalmarLeft"] = PalmarLeft
    cntlen_time = time.time()
    cntlen_spend = timing(cntlen_time - start_time)
    save_txt(path+'/time.txt', cntlen_spend, string="\ncntlen: ")

    imgfdpath = os.path.join(os.getcwd(), "Hands")
    folders = ['DorsalRight', 'PalmarRight', 'DorsalLeft', 'PalmarLeft']
    createFolder(folders, path=imgfdpath)
    folders_Test = ['Test/'+f for f in folders]
    createFolder(folders_Test, path=imgfdpath)
    moveFiles(path=imgfdpath, folders=folders, dict=img_dict)
    moveFiles_time = time.time()
    moveFiles_spend = timing(moveFiles_time - cntlen_time)
    save_txt(imgfdpath+'/time.txt', moveFiles_spend, string="\nmoveFiles: ")

    choseImg(path=imgfdpath, Num=FLAGS.trainNum_per_class, folders=folders, dict=img_dict)
    choseImg_time = time.time()
    choseImg_spend = timing(choseImg_time - moveFiles_time)
    save_txt(imgfdpath+'/time.txt', choseImg_spend, string="\nchoseImg: ")

    q =Queue()
    threads = []; flipfd = []
    flips = FLAGS.flips
    for i in range(len(flips)):
        t = threading.Thread(target=flipHImg, args=(q, imgfdpath, folders, [flips[i]]))
        t.start()
        threads.append(t) 
    for thread in threads:
        thread.join()
    for _ in range(len(flips)):
        flipfd.append(q.get())
    delOldFolders(imgfdpath, folders=folders, name=flipfd)
    flipHImg_time = time.time()
    flipHImg_spend = timing(flipHImg_time - choseImg_time)
    save_txt(imgfdpath+'/time.txt', flipHImg_spend, string="\nflipHImg: ") 
    
    threads = []; usefd = []; rotatefd = []
    rotates = FLAGS.rotates
    usefd = filterUseFolders(imgfdpath, folders)
    for i in range(len(rotates)):
        t = threading.Thread(target=rotateImg, args=(q, imgfdpath, folders, usefd, [rotates[i]]))
        t.start()
        threads.append(t) 
    for thread in threads:
        thread.join()
    for _ in range(len(rotates)):
        rotatefd.append(q.get())
    delOldFolders(imgfdpath, folders=folders, name=rotatefd)
    rotateImg_time = time.time()
    rotateImg_spend = timing(rotateImg_time - flipHImg_time)
    save_txt(imgfdpath+'/time.txt', rotateImg_spend, string="\nrotateImg: ")

    threads = []; usefd = []; scalefd = []
    scales = FLAGS.scales
    usefd = filterUseFolders(imgfdpath, folders)
    for i in range(len(scales)):
        t = threading.Thread(target=scaleImg, args=(q, imgfdpath, folders, usefd, [scales[i]]))
        t.start()
        threads.append(t) 
    for thread in threads:
        thread.join()
    for _ in range(len(scales)):
        scalefd.append(q.get())
    delOldFolders(imgfdpath, folders=folders, name=scalefd)
    threads = []
    for i in range(len(scalefd)):
        t = threading.Thread(target=recordHandLoc, args=(imgfdpath, [scalefd[i]]))
        t.start()
        threads.append(t) 
    for thread in threads:
        thread.join()
    scaleImg_time = time.time()
    scaleImg_spend = timing(scaleImg_time - rotateImg_time)
    save_txt(imgfdpath+'/time.txt', scaleImg_spend, string="\nscaleImg: ")

    threads = []; usefd = []; luminfd = []
    lumins = FLAGS.lumins
    usefd = filterUseFolders(imgfdpath, folders)
    for i in range(len(lumins)):
        t = threading.Thread(target=luminImg, args=(q, imgfdpath, folders, usefd, [lumins[i]]))
        t.start()
        threads.append(t) 
    for thread in threads:
        thread.join()
    for _ in range(len(lumins)):
        luminfd.append(q.get())
    delOldFolders(imgfdpath, folders=folders, name=luminfd)
    luminImg_time = time.time()
    luminImg_spend = timing(luminImg_time - scaleImg_time)
    save_txt(imgfdpath+'/time.txt', luminImg_spend, string="\nluminImg: ")

    threads = []; usefd = []; noisefd = []
    noises = FLAGS.noises
    usefd = filterUseFolders(imgfdpath, folders)
    for i in range(len(noises)):
        t = threading.Thread(target=noiseImg, args=(q, imgfdpath, folders, usefd, [noises[i]]))
        t.start()
        threads.append(t) 
    for thread in threads:
        thread.join()
    for _ in range(len(noises)):
        noisefd.append(q.get())
    delOldFolders(imgfdpath, folders=folders, name=noisefd)
    noiseImg_time = time.time()
    noiseImg_spend = timing(noiseImg_time - luminImg_time)
    save_txt(imgfdpath+'/time.txt', noiseImg_spend, string="\nnoiseImg: ")

    trainData(path=imgfdpath, folders=folders)
    trainData_time = time.time()
    trainData_spend = timing(trainData_time - noiseImg_time)
    save_txt(imgfdpath+'/time.txt', trainData_spend, string="\ntrainData: ")

    testData(path=imgfdpath, folders=folders)
    testData_time = time.time()
    testData_spend = timing(testData_time - trainData_time)
    save_txt(imgfdpath+'/time.txt', testData_spend, string="\ntestData: ")
    
    end_time = time.time()
    total_spend = timing(end_time - start_time)
    save_txt(imgfdpath+'/time.txt', total_spend, string="\ntotal: ")


def extract_folder(zip_dataset):
    print("Hands dataset already downloaded.\nGenerating CSV files")
    dataset_path = os.path.dirname(os.path.abspath(zip_dataset))
    if not os.path.exists("Hands"):
        zip_ref = zipfile.ZipFile(zip_dataset, 'r')
        print("> Extracting Dataset files")
        zip_ref.extractall()
        print("> Extraction complete")
        zip_ref.close()    
        hand_dataset_split(dataset_path)
    else:
        hand_dataset_split(dataset_path)


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

