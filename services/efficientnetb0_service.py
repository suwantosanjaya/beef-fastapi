# ============================================
# EfficientNetB0 - Meat Classification (4 Class)
# Classes: Sapi, Babi, Oplosan, Bukan Daging
# ============================================

import os
import time
import numpy as np
import pandas as pd
import seaborn as sns
import tensorflow as tf
from datetime import datetime
from efficientnet import tfkeras
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adamax
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
from core.logger import get_daily_logger

from pathlib import Path


logger = get_daily_logger()


class Efficientnetb0Service:
    def __init__(self):
        # Paths
        base_dir = Path(__file__).resolve().parents[2]
        self.modeling_dir = base_dir / "modeling" # D:\\PENELITIAN\\2025\\LITAPDIMAS\\PENELITIAN_2025\\modeling
        self.data_path = "DATA_READY"
        self.model_dir = os.path.join(self.modeling_dir, "MODEL")
        os.makedirs(self.model_dir, exist_ok=True)

        # Dataset info
        self.dataset_dir = os.path.join(self.modeling_dir, self.data_path, "4B-DatasetAugmentationAll", "9010")
        self.train_dataset_path = os.path.join(self.dataset_dir, "Train")

        # Training configuration
        self.image_size: tuple[int, int] = (224, 224)
        self.learning_rate: float = 1e-4
        self.validation_split: float = 0.2
        self.batch_size: int = 32

        # Cek versi library
        self._log_versions()

    def _log_versions(self) -> None:
        logger.info(f"TensorFlow: {tf.__version__}")
        logger.info(f"NumPy: {np.__version__}")
        logger.info(f"Pandas: {pd.__version__}")
        logger.info(f"Seaborn: {sns.__version__}")

    def build_model(self, num_classes: int = 4) -> models.Model:
        """
        Membuat arsitektur model EfficientNetB0
        """
        base_model = tfkeras.EfficientNetB0(
            include_top=False, 
            input_shape=(*self.image_size, 3), 
            weights="imagenet"
        )
        base_model.trainable = False

        model = models.Sequential([
            base_model,
            layers.GlobalAveragePooling2D(),
            layers.BatchNormalization(),
            layers.Dropout(0.4),
            layers.Dense(256, kernel_initializer="he_uniform", activation="relu"),
            layers.BatchNormalization(),
            layers.Dropout(0.3),
            layers.Dense(num_classes, activation="softmax")   
        ])

        optimizer = Adamax(learning_rate=self.learning_rate)
        model.compile(
            optimizer=optimizer,
            loss="categorical_crossentropy",
            metrics=["accuracy"]
        )
        model.summary(print_fn=logger.info)
        return model
    
    def data_generator(
        self, 
        data_dir: str, 
        batch_size: int | None = None, 
        target_size: tuple[int, int] | None = None
    ):
        """
        Membuat generator untuk data training dan validasi
        """
        batch_size = batch_size or self.batch_size
        target_size = target_size or self.image_size

        datagen = ImageDataGenerator(
            rescale=1./255,
            validation_split=self.validation_split
        )

        train_gen = datagen.flow_from_directory(
            directory=data_dir,
            target_size=target_size,
            batch_size=batch_size,
            class_mode='categorical',
            subset='training'
        )

        val_gen = datagen.flow_from_directory(
            directory=data_dir,
            target_size=target_size,
            batch_size=batch_size,
            class_mode='categorical',
            subset='validation'
        )
        
        logger.info(f"Found classes: {train_gen.class_indices}")
        logger.info(f"Number of classes: {len(train_gen.class_indices)}")

        return train_gen, val_gen, train_gen.class_indices, len(train_gen.class_indices)
    
    def get_callbacks(self, model_name: str):
        """
        Membuat callbacks untuk training
        """
        checkpoint_path = os.path.join(self.model_dir, model_name)
        checkpoint = ModelCheckpoint(
            filepath=checkpoint_path,
            monitor='val_accuracy',
            save_best_only=True,
            mode='max',
            save_format="h5",
            verbose=1
        )

        early_stopping = EarlyStopping(
            monitor='val_accuracy',
            patience=10,
            mode='max',
            verbose=1
        )

        reduce_lr = ReduceLROnPlateau(
            monitor='val_accuracy',
            factor=0.2,
            patience=5,
            min_lr=1e-6,
            mode='max',
            verbose=1
        )
        
        
        return [checkpoint, early_stopping, reduce_lr, self.TimeHistory()]

    def train_model(self, epochs: int = 50):
        """
        Melatih model dengan data generator
        """
        train_data, val_data, class_indices, num_classes = self.data_generator(self.train_dataset_path)
        model = self.build_model(num_classes)
        model_name = f"efficientnetb0_{datetime.now().strftime('%Y%m%d_%H%M%S')}.h5"
        callbacks_list = self.get_callbacks(model_name)

        history = model.fit(
            x=train_data,
            validation_data=val_data,
            epochs=epochs,
            callbacks=callbacks_list,
            verbose=1
        )

        model.save(os.path.join(self.model_dir, model_name))
        
        return history, model_name

    class TimeHistory(tf.keras.callbacks.Callback):
        """Callback untuk mencatat waktu per epoch"""
        def on_train_begin(self, logs=None):
            self.epoch_times = []
            self.train_start = time.time()
        
        def on_epoch_begin(self, epoch, logs=None):
            self.epoch_start = time.time()
        
        def on_epoch_end(self, epoch, logs=None):
            elapsed = time.time() - self.epoch_start
            self.epoch_times.append(elapsed)
            logger.info(f"Epoch {epoch+1} duration: {elapsed:.2f} seconds")
        
        def on_train_end(self, logs=None):
            total = time.time() - self.train_start
            logger.info(f"\nTotal training time: {total:.2f} seconds")
