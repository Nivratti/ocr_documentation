
# Recognition models

Models will be loaded from directory `.ocr_models` located in user's home directory.

## Updating paddleocr recognition model:

After exporting new trained paddleocr model to pytorch format using step number `9- Export model in Pytorch format` in colab notebook, you are ready to use new models.

To update models in docker, you can rename "checkpoint_filename.pth" that you have trained to "rec_ft_v3.0.2.pth" and put that inside `data/.ocr_models/PaddleOCR2Pytorch-models` and build docker again.

To use different name for model you can set filepath of that to environment variable `PADDLE_REC_MODEL_PATH`.

## Updating EasyOCR recognition model:

After updating easyocr model, you can directly use it.

To update models in docker, you can rename "checkpoint_filename.pth" that you have trained to "english_ft_v8.pth" and put that inside `data/.ocr_models/EasyOCR/model/` and build docker again.
