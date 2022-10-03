"""
Usage:
python convert_rec_dataset_2_easyocr_format.py --datasetRootPath "/path-to/paddleocr/recognition/splitted/dataset"

"""
import os
import shutil
import random
import argparse
import pandas as pd
from nb_utils.file_dir_handling import list_files
from pathlib import Path

def convert_2_easyocr_format(dataset_root_path, out_dataset_path):
    # List all validation files
    label_files = list_files(dataset_root_path, filter_ext=[".txt"])
    for label_file in label_files:
        df = pd.read_csv(
            label_file, sep='\t', names=["filename", "words"], 
            engine='python', error_bad_lines=False
        ) ## read paddleocr format label file
        
        #
        obj_path = Path(label_file)
        label_file_stem = obj_path.stem

        ## Check is input folder exists with stem name ex. train, val or test
        dir_subset_path = os.path.join(dataset_root_path, label_file_stem)
        if not os.path.exists(dir_subset_path):
            print(f"Warning subset dir path `{dir_subset_path}` not exists for label file `{label_file}`")
            continue

        out_path = os.path.join(out_dataset_path, label_file_stem)
        os.makedirs(out_path, exist_ok=True)

        new_filenames = []
        labels = []

        for index, row in df.iterrows():
            # print(f"index: ", index)
            # print(f"row: ", row)
            filepath = row["filename"]
            file_suffix = Path(filepath).suffix
            file_name = Path(filepath).name
            input_file_fullpath = os.path.join(dir_subset_path, file_name)

            new_filename = f"{index}{file_suffix}"
            out_filepath = os.path.join(out_path, new_filename)

            if os.path.exists(input_file_fullpath):
                dest = shutil.copy2(input_file_fullpath, out_filepath)
                # dest = shutil.move(input_file_fullpath, out_filepath)

                new_filenames.append(new_filename)
                labels.append(row["words"])
            else:
                print(f"Error.. Input filepath {input_file_fullpath} not exists...")

        ## Append filename string at index 0 in new files
        ## and append words string at index 0 in labels
        ## as per easyocr format

        if not new_filenames[0] == "filename":
            new_filenames.insert(0, "filename")
            labels.insert(0, "words")

        new_val_df = pd.DataFrame(
            {
                "filename": new_filenames,
                "words": labels
            }
        )

        # new_val_df.head()

        ## Save new df
        out_label_filepath = os.path.join(out_path, "labels.csv")
        new_val_df.to_csv(out_label_filepath, header=None, index=False)

    return True

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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--datasetRootPath",
        type=str,
        default="./train_data/rec",
        help="path to the recognition dataset splitted by gen_ocr_train_val_test.py script in paddle format"
    )
    parser.add_argument(
        "-o", "--outDatasetPath",
        type=str,
        default="./train_data/rec_dataset_easyocr_format",
        help="path to output recognition dataset - easyocr format"
    )
    args = parser.parse_args()
    dataset_root_path = args.datasetRootPath
    out_dataset_path = args.outDatasetPath
    convert_2_easyocr_format(dataset_root_path, out_dataset_path)

if __name__ == "__main__":
    main()