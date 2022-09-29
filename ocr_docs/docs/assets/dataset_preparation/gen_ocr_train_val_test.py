"""
Usage: 

python gen_ocr_train_val_test.py --trainValTestRatio "8:1:1" --datasetRootPath "/Philippines-ids/driving-license/" --detRootPath "../train_data/det_phl_driving_license" --recRootPath "../train_data/rec_phl_driving_license"
"""
# coding:utf8
import os
import shutil
import random
import argparse
from pathlib import Path


# Delete the divided training set, validation set, and test set folder and recreate an empty folder
def isCreateOrDeleteFolder(path, flag):
    flagPath = os.path.join(path, flag)

    if os.path.exists(flagPath):
        shutil.rmtree(flagPath)

    os.makedirs(flagPath)
    flagAbsPath = os.path.abspath(flagPath)
    return flagAbsPath

def get_relative_path(imageCopyPath):
    """
    Get relative label path from absolute

    Args:
        imageCopyPath (_type_): _description_

    Returns:
        _type_: _description_
    """
    # ## Get dynamic length -- but if absolute dir path passed for saving labels, it will give more length and it will not give desired result
    # len_rel_folders = len(Path(args.recRootPath.strip('.').strip('/')).parents)

    ## We need only last 2 folders and filename of abs path
    len_rel_folders = 2

    base_parent_folder = Path(imageCopyPath).parents[len_rel_folders]
    relative_path = Path(imageCopyPath).relative_to(base_parent_folder)
    return relative_path

def splitTrainVal(root, absTrainRootPath, absValRootPath, absTestRootPath, trainTxt, valTxt, testTxt, flag, args=None):
    # Divide the training set, validation set, and test set according to the specified ratio
    dataAbsPath = os.path.abspath(root)

    if flag == "det":
        labelFilePath = os.path.join(dataAbsPath, args.detLabelFileName)
    elif flag == "rec":
        labelFilePath = os.path.join(dataAbsPath, args.recLabelFileName)

    labelFileRead = open(labelFilePath, "r", encoding="UTF-8")
    labelFileContent = labelFileRead.readlines()
    random.shuffle(labelFileContent)
    labelRecordLen = len(labelFileContent)

    for index, labelRecordInfo in enumerate(labelFileContent):
        imageRelativePath = labelRecordInfo.split('\t')[0]
        imageLabel = labelRecordInfo.split('\t')[1]
        imageName = os.path.basename(imageRelativePath)

        if flag == "det":
            imagePath = os.path.join(dataAbsPath, imageName)
        elif flag == "rec":
            imagePath = os.path.join(dataAbsPath, os.path.join(args.recImageDirName, imageName))

        # Divide the training set, validation set, and test set according to the preset ratio
        trainValTestRatio = args.trainValTestRatio.split(":")
        trainRatio = eval(trainValTestRatio[0]) / 10
        valRatio = trainRatio + eval(trainValTestRatio[1]) / 10
        curRatio = index / labelRecordLen

        # import ipdb;ipdb.set_trace()
        try:
            if curRatio < trainRatio:
                imageCopyPath = os.path.join(absTrainRootPath, imageName)
                shutil.copy(imagePath, imageCopyPath)

                if args.relative_path:
                    relative_path = get_relative_path(imageCopyPath)
                    trainTxt.write("{}\t{}".format(relative_path, imageLabel))
                else:
                    trainTxt.write("{}\t{}".format(imageCopyPath, imageLabel))
            elif curRatio >= trainRatio and curRatio < valRatio:
                imageCopyPath = os.path.join(absValRootPath, imageName)
                shutil.copy(imagePath, imageCopyPath)
                if args.relative_path:
                    relative_path = get_relative_path(imageCopyPath)
                    valTxt.write("{}\t{}".format(relative_path, imageLabel))
                else:
                    valTxt.write("{}\t{}".format(imageCopyPath, imageLabel))
            else:
                imageCopyPath = os.path.join(absTestRootPath, imageName)
                shutil.copy(imagePath, imageCopyPath)
                if args.relative_path:
                    relative_path = get_relative_path(imageCopyPath)
                    testTxt.write("{}\t{}".format(relative_path, imageLabel))
                else:
                    testTxt.write("{}\t{}".format(imageCopyPath, imageLabel))
        except Exception as e:
            print(f"Error: {e}")

# delete existing files
def removeFile(path):
    if os.path.exists(path):
        os.remove(path)


def genDetRecTrainVal(args):
    detAbsTrainRootPath = isCreateOrDeleteFolder(args.detRootPath, "train")
    detAbsValRootPath = isCreateOrDeleteFolder(args.detRootPath, "val")
    detAbsTestRootPath = isCreateOrDeleteFolder(args.detRootPath, "test")
    recAbsTrainRootPath = isCreateOrDeleteFolder(args.recRootPath, "train")
    recAbsValRootPath = isCreateOrDeleteFolder(args.recRootPath, "val")
    recAbsTestRootPath = isCreateOrDeleteFolder(args.recRootPath, "test")

    removeFile(os.path.join(args.detRootPath, "train.txt"))
    removeFile(os.path.join(args.detRootPath, "val.txt"))
    removeFile(os.path.join(args.detRootPath, "test.txt"))
    removeFile(os.path.join(args.recRootPath, "train.txt"))
    removeFile(os.path.join(args.recRootPath, "val.txt"))
    removeFile(os.path.join(args.recRootPath, "test.txt"))

    detTrainTxt = open(os.path.join(args.detRootPath, "train.txt"), "a", encoding="UTF-8")
    detValTxt = open(os.path.join(args.detRootPath, "val.txt"), "a", encoding="UTF-8")
    detTestTxt = open(os.path.join(args.detRootPath, "test.txt"), "a", encoding="UTF-8")
    recTrainTxt = open(os.path.join(args.recRootPath, "train.txt"), "a", encoding="UTF-8")
    recValTxt = open(os.path.join(args.recRootPath, "val.txt"), "a", encoding="UTF-8")
    recTestTxt = open(os.path.join(args.recRootPath, "test.txt"), "a", encoding="UTF-8")

    splitTrainVal(args.datasetRootPath, detAbsTrainRootPath, detAbsValRootPath, detAbsTestRootPath, detTrainTxt, detValTxt,
                  detTestTxt, "det", args=args)

    for root, dirs, files in os.walk(args.datasetRootPath):
        for dir in dirs:
            if dir == 'crop_img':
                splitTrainVal(root, recAbsTrainRootPath, recAbsValRootPath, recAbsTestRootPath, recTrainTxt, recValTxt,
                              recTestTxt, "rec", args=args)
            else:
                continue
        break

def str2bool(v):
    import argparse
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 'True', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'False', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

if __name__ == "__main__":
    # Function description: separate the training set, validation set, and test set for detection and recognition
    # Description: You can adjust the parameters according to your own path and needs. Image data is often labeled in batches by multiple people. Each batch of image data is placed in a folder and labeled with PPOCRLabel.
    # In this way, there will be multiple labeled image folders to aggregate and divide the training set, validation set, and test set requirements
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--trainValTestRatio",
        type=str,
        default="7:2:1",
        help="ratio of trainset:valset:testset")
    parser.add_argument(
        "--datasetRootPath",
        type=str,
        default="../train_data/",
        help="path to the dataset marked by ppocrlabel, E.g, dataset folder named 1,2,3..."
    )
    parser.add_argument(
        "--detRootPath",
        type=str,
        default="../train_data/det",
        help="the path where the divided detection dataset is placed")
    parser.add_argument(
        "--recRootPath",
        type=str,
        default="../train_data/rec",
        help="the path where the divided recognition dataset is placed"
    )
    parser.add_argument(
        "--detLabelFileName",
        type=str,
        default="Label.txt",
        help="the name of the detection annotation file")
    parser.add_argument(
        "--recLabelFileName",
        type=str,
        default="rec_gt.txt",
        help="the name of the recognition annotation file"
    )
    parser.add_argument(
        "--recImageDirName",
        type=str,
        default="crop_img",
        help="the name of the folder where the cropped recognition dataset is located"
    )
    parser.add_argument(
        "-r", "--relative_path", type=str2bool, nargs='?', 
        const=True, default=True, 
        help="Whether to write relative paths in label file-name"
    )
    args = parser.parse_args()
    genDetRecTrainVal(args)
