# EasyOCR format


## 1. Text recognition

### 1.1 EasyOCR text recognition format annotation

If you want to use your own data for training, please refer to the following to organize your data.

- Training set

It is recommended to put the training images in the same folder, and use a txt file (label.txt) to store the image name and label. The contents of the txt file are as follows:

* Note: by default, the image path and image label are split with comma, if you use other methods to split, it will cause training error

```
filename,words
word_001.jpg,India
word_002.jpg,Government
...
```

The final training set should have the following file structure:

```
|- train
    |- word_001.png
    |- word_002.jpg
    |- word_003.jpg
    | ...
    |- label.txt
```

- Validation set

Similar to the training set, the val set also needs to be provided a folder containing all images (val) and a label.txt. The structure of the val set is as follows:

```
|-val
    |- word_001.png
    |- word_002.jpg
    |- word_003.jpg
    | ...
    |- label.txt
```

## 2. Converting paddleocr format annotation to EasyOCR

  You can use `convert_rec_dataset_2_easyocr_format.py` file to convert paddleocr format dataset to easyocr. [download code file](../assets/dataset_preparation/convert_rec_dataset_2_easyocr_format.py "download"){:target="_blank" rel="noopener"}


```python title="convert_rec_dataset_2_easyocr_format.py"
--8<-- "docs/assets/dataset_preparation/convert_rec_dataset_2_easyocr_format.py"
```
