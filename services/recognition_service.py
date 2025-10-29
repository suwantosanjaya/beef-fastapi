from datetime import datetime
import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.layers import Dropout
from tensorflow.keras.applications.efficientnet import preprocess_input # <-- IMPORT INI
# import efficientnet.tfkeras as efn
from fastapi import UploadFile, status
from exceptions.custom_exception import CustomException
from schemas.recognition_schema import RecognitionRequest
from utils.file_management import save_file
from core.config import UPLOAD_IMAGE_PATH, MODEL_PATH
from core.logger import get_daily_logger

logger = get_daily_logger()


class RecognitionService:
    def __init__(self):
        # bisa dipakai untuk caching model biar tidak load setiap request
        self.model_cache = {}

    def recognition(self, image: UploadFile = None):
        new_image = None
        try:
            # simpan file jika ada upload
            if image and image.filename != "":
                new_image = save_file(new_file=image, upload_dir=UPLOAD_IMAGE_PATH)

            # prediksi dengan model
            result = self.predict_image(
                model_path=MODEL_PATH,
                img_file=new_image,
                class_labels=["Sapi", "Babi", "Oplosan", "Bukan Daging"],
                size=(224, 224)
            )
            return result

        except Exception as e:
            logger.error(f"Failed to process recognition: {e}")
            raise CustomException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=f"Failed to process recognition: {str(e)}"
            )

    def recognition2(self, data: RecognitionRequest, image: UploadFile = None):
        new_image = None
        try:
            # simpan file jika ada upload
            if image and image.filename != "":
                new_image = save_file(new_file=image, upload_dir=UPLOAD_IMAGE_PATH)

            # prediksi dengan model
            result = self.predict_image(
                model_path=MODEL_PATH,
                img_file=new_image,
                class_labels=["Sapi", "Babi", "Oplosan", "Bukan Daging"],
                size=(224, 224)
            )
            return result

        except Exception as e:
            logger.error(f"Failed to process recognition: {e}")
            raise CustomException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=f"Failed to process recognition: {str(e)}"
            )

    def predict_image(self, model_path: str, img_file: str, class_labels: list[str], size: tuple = (224, 224)):
        """
        Melakukan prediksi pada gambar yang di-upload
        """
        if not os.path.exists(model_path):
            return {"status": "error", "message": f"Model not found at {model_path}"}

        # gunakan cache supaya model tidak diload berulang kali
        if model_path not in self.model_cache:
            self.model_cache[model_path] = load_model(
                model_path,
                custom_objects={
                    "FixedDropout": Dropout   # mapping ke Dropout biasa
                }
            )

        model = self.model_cache[model_path]

        # preprocess gambar
        full_path_img = os.path.join(UPLOAD_IMAGE_PATH, img_file)
        img = image.load_img(full_path_img, target_size=size)
        # img_array = image.img_to_array(img) / 255.0
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        # prediksi
        predictions = model.predict(img_array)
        predicted_class = class_labels[np.argmax(predictions)]

        return {
            "status": "success",
            "predicted_class": predicted_class,
            "confidence": float(np.max(predictions)),
            "all_confidences": {
                label: float(pred) for label, pred in zip(class_labels, predictions[0])
            }
        }
