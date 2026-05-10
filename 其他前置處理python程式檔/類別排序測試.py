import tensorflow as tf

dataset = tf.keras.preprocessing.image_dataset_from_directory(
    "資料集檔案庫(改)/train",
    image_size=(224, 224),
    batch_size=1,
    shuffle=False
)

print(dataset.class_names)