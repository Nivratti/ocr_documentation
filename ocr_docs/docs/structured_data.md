# Structured data

## key information extraction

Key information extraction (KIE) refers to extracting key information from text or images. As the downstream task of OCR, KIE of document image has many practical application scenarios, such as form recognition, ticket information extraction, ID card information extraction, etc. However, it is time-consuming and laborious to extract key information from these document images by manpower. It's challengeable but also valuable to combine multi-modal features (visual, layout, text, etc) together and complete KIE tasks.

Methods:

1. Text
2. Text + layout
3. Text + layout + Visual

### 1. Text only methods:

Only text content based kie methods such as Named entity recognition will give less accuracy as compare to other methods.

### 2. Text + layout (We are using this method for English structured data):

It combines text and layout features. For text content manipulation we can use regex and fuzzy library, for layout part we can use numpy library to handle the layout i.e coordinates values. This method will be faster and it avoids need of key data labeling and kie model training. Sometimes it may take longer time if ocr result not good and different formats for ID, to adjust.

### 3. Text + layout + Visual:

In this method we train one deep learning based model for key information extraction. We need to train model for each card to give best result and avoid complexity. key value data needs to be annotated to train model. At least 50 card images are required to train kie model to get good result.
