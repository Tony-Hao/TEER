import csv, shutil, os, sys, glob, cPickle

csv.field_size_limit(sys.maxint)
from log import strd_logger
import W_utility.preprocessing as pre
# logger
global log
log = strd_logger('file')


# check if a file exist
def file_exist(fname):
    try:
        open(fname, 'r')
        return True
    except IOError:
        return False


# create directory if not existing
def mkdir(dirname):
    try:
        os.makedirs(dirname)
    except OSError:
        pass
    except Exception as e:
        log.error(e)
        return False
    return True


# create directory (delete if one with the same name already exists)
def mk_new_dir(dirname):
    try:
        os.makedirs(dirname)
    except OSError:
        shutil.rmtree(dirname)
        os.makedirs(dirname)
    except Exception as e:
        log.error(e)
        return False
    return True


# copy a file from "source" to "destination"
def fcopy(source, destination):
    try:
        shutil.copy2(source, destination)
    except Exception as e:
        log.error(e)
        return False
    return True


# return the files of a directory with extension "ext"
def flist(directory, ext):
    try:
        os.chdir(directory)
        if ext[0:2] != '*.':
            ext = '*.' + ext
        data = []
        for f in glob.glob(ext):
            data.append(f.strip())
        return data
    except Exception as e:
        log.error(e)
        return None


### read operations ###

# read a text file
# @param struct: save data to (1) list, (2) set, (3)string
def read_file(filename, struct=1, logout=True):
    import chardet
    tt = open(filename,'rb')
    ff=tt.read()
    enc=chardet.detect(ff)
    tt.close()

    try:

        fid = open(filename, 'r')
        if struct == 2:
            # set
            data = set()
            for line in fid:
                if len(line) > 0:
                    line=pre.strQ2B(line)
                    data.add(line.strip())
        elif struct == 1:
            # default - list
            data = []
            for line in fid.readlines():
                if len(line) > 0:
                    line=line.strip().decode(enc['encoding'])
                    #line=pre.strQ2B(line)
                    #data.append(line.strip().decode(enc['encoding']))
                    data.append(line.strip())
        else:
            data = fid.read()

        fid.close()
        return data
    except Exception as e:
        if logout is True:
            log.error(e)
        return None


def write_file(filename, data, logout=True):
    try:
        fid = open(filename, 'w')
        for d in data:
            # fid.write('%s\n' % d.encode('utf-8'))
            fid.write('%s\n' % d.encode('gb2312'))
        fid.close()
        return True
    except Exception as e:
        if logout is True:
            log.error(e)
        return False
