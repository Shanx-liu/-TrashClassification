import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

#gpu設定
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)
        print("GPU已啟用")
else:
    print("使用CPU")

from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from tensorflow.keras.optimizers import Adam
import seaborn as sns
from sklearn.metrics import confusion_matrix

#所有相關參數
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
NUM_CLASSES = 10
EPOCHS_HEAD = 16
EPOCHS_FINE = 10    

#載入資料
train_df = tf.keras.preprocessing.image_dataset_from_directory(
    "資料集檔案庫(改)/train",
    image_size = IMG_SIZE,
    batch_size = BATCH_SIZE,
    shuffle = True
)
val_df = tf.keras.preprocessing.image_dataset_from_directory(
    "資料集檔案庫(改)/val",
    image_size = IMG_SIZE,
    batch_size = BATCH_SIZE,
    shuffle = False
)
test_df = tf.keras.preprocessing.image_dataset_from_directory(
    "資料集檔案庫(改)/test",
    image_size = IMG_SIZE,
    batch_size = BATCH_SIZE,
    shuffle = False
)

#資料增強
data_augmentation = tf.keras.Sequential([
    tf.keras.layers.RandomFlip("horizontal"),
    tf.keras.layers.RandomRotation(0.1),
    tf.keras.layers.RandomZoom(0.1),
    tf.keras.layers.RandomContrast(0.1),
])

#根據模型學習程度逐漸縮小學習率
reduce_lr = ReduceLROnPlateau(
    monitor="val_loss",     #監控驗證損失
    factor=0.5,             #每次下降0.5
    patience=3,             #容忍3個epoch沒有改善
    min_lr=3e-5,            #設定最小學習率
    mode="min",             #監控目標
    verbose=1               #每次變動時顯示詳細訊息
)

#將資料預處理放至模型內
train_ds = train_df     #.map(lambda x, y: (preprocess_input(x), y))
val_ds = val_df         #.map(lambda x, y: (preprocess_input(x), y))
test_ds  = test_df      #.map(lambda x, y: (preprocess_input(x), y))


base_model = MobileNetV2 (  #MobileNet本身就是一個訓練好的ImageNet模型
    input_shape = (224, 224, 3),
    include_top = False,    #移除MobileNet最上層的全聯接層
    weights = "imagenet"
)
base_model.trainable = False #凍結基底模型

#下面為主要自訂模型
inputs = tf.keras.Input(shape=(224, 224, 3))
x = data_augmentation(inputs)
x = tf.keras.applications.mobilenet_v2.preprocess_input(x)
x = base_model(x, training=False)
x = GlobalAveragePooling2D()(x)
x = Dense(512, activation='relu')(x)    #自訂神經層不須太深，一層即足夠
x = Dropout(0.5)(x)
predictions = Dense(NUM_CLASSES, activation='softmax')(x)
model = Model(inputs=inputs, outputs=predictions)

#編譯模型
model.compile(
    optimizer=Adam(learning_rate=1e-3),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

#模型達到最佳並且準確率不再增加時，等待一段週期並且記住最佳那次的權重
callbacks = [
    EarlyStopping(
        monitor="val_accuracy",     #性能監控指標為 "驗證集準確率"
        patience=5,                 #若連續5次訓練準確率不再上升，則停止訓練
        mode="max",                 #監控指標的改善方向
        restore_best_weights=True), #訓練停止後，模型的權重會恢復到性能最佳的那個
    ModelCheckpoint("mobilenet_best.h5", 
                    save_best_only=True),
    reduce_lr       #新增學習率排程器
]

#第一階段訓練（只訓練分類頭）
history_head = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=EPOCHS_HEAD,
    callbacks=callbacks
)


#第二階段訓練
#Fine-tuning（微調 MobileNet）
for layer in base_model.layers[-40:]:       #可解凍多層MobileNet神經層，最後40層
    layer.trainable = True

model.compile(
    optimizer=Adam(learning_rate=6e-5),     #第二次編譯（Fine-tuning 微調階段）的初始學習率
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

history_fine = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=EPOCHS_FINE,
    callbacks=callbacks
)


#最終測試集評估
model.summary()
test_loss, test_acc = model.evaluate(test_ds)
print(f"驗證資料集準確度: {test_acc:.4f}")
print(f"驗證資料集損失度: {test_loss:.4f}")

# 儲存Keras模型
print("儲存模型: MobileNet.keras ...")
model.save("MobileNet.keras")

# 顯示訓練和驗證損失
# 合併 loss
loss = history_head.history["loss"] + history_fine.history["loss"]
val_loss = history_head.history["val_loss"] + history_fine.history["val_loss"]

epochs = range(1, len(loss) + 1)

plt.figure()
plt.plot(epochs, loss, "bo-", label="Training Loss")
plt.plot(epochs, val_loss, "ro--", label="Validation Loss")


# Fine-tuning 起始位置

plt.axvline(
    x=EPOCHS_HEAD,
    linestyle="--",
    label="Start Fine-tuning"
)


plt.title("Training and Validation Loss (Head + Fine-tuning)")
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.legend()
plt.show()

# 顯示訓練和驗證準確度
# 合併 accuracy
acc = history_head.history["accuracy"] + history_fine.history["accuracy"]
val_acc = history_head.history["val_accuracy"] + history_fine.history["val_accuracy"]

epochs = range(1, len(acc) + 1)

plt.figure()
plt.plot(epochs, acc, "bo-", label="Training Accuracy")
plt.plot(epochs, val_acc, "ro--", label="Validation Accuracy")

# Fine-tuning 起始位置

plt.axvline(
    x=EPOCHS_HEAD,
    linestyle="--",
    label="Start Fine-tuning"
)


plt.title("Training and Validation Accuracy (Head + Fine-tuning)")
plt.xlabel("Epochs")
plt.ylabel("Accuracy")
plt.legend()
plt.show()



#新增：混淆矩陣函式
def plot_confusion_matrix(model, test_ds):
    y_true = []
    y_pred = []
    
    # 預測測試集
    for images, labels in test_ds:
        preds = model.predict(images)
        y_true.extend(labels.numpy())
        y_pred.extend(np.argmax(preds, axis=1))
    
    # 計算矩陣
    cm = confusion_matrix(y_true, y_pred)
    # 取得類別名稱（假設你的 test_ds 有 class_names）
    class_names = test_df.class_names 
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=class_names, yticklabels=class_names)
    plt.title("Confusion Matrix")
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.show()

# 在評估完後呼叫
plot_confusion_matrix(model, test_ds)