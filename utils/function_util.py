import os
import logging.config
import config.log_config as selfcfg
logging.config.dictConfig(selfcfg.config)
logger = logging.getLogger("StreamLogger")

class FUNC(object):

    def save_txt(txt_path, txt_content, string=""):
        with open(txt_path, 'a') as txtfile:
            txtfile.writelines(string + txt_content)


    def timing(sec):
        day = int(sec//(60*60*24));  day_rm = sec%(60*60*24)
        hour = int(day_rm//(60*60)); hour_rm = day_rm%(60*60)
        mins = int(hour_rm//60);     sec = hour_rm%60

        day = str("0"+str(day)) if day<10 else str(day)
        hour = str("0"+str(hour)) if hour<10 else str(hour)
        mins = str("0"+str(mins)) if mins<10 else str(mins)
        sec = str("0"+str(sec)) if sec<10 else str("%.2f"%sec)
        string = str(day) + ":" + str(hour) + ":" + str(mins) + ":" + str(sec)
        logger.info("Time: " + string)
        return string


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


    def filterUseFolders(path, folders=[]):
        files = os.listdir(path)
        files_tag = []
        [files_tag.append(f) for f in files for d in folders if d in f]
        return files_tag


    def filterExistFolders(outfolder=[], infolder=[]):
        infd_tmp = []
        [infd_tmp.append(outfd) for infd in infolder for outfd in outfolder if outfd in infd]
        [infolder.remove(f) for f in infd_tmp]  
        return infolder