from __future__ import absolute_import, division, print_function, unicode_literals

import tensorflow as tf

is_gpu_available = tf.test.is_gpu_available()
message = "GPU available: {}".format(is_gpu_available)
print(message)

with open('output.txt', 'w') as f:
    f.write(message)

mnist = tf.keras.datasets.mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

model = tf.keras.models.Sequential([
  tf.keras.layers.Flatten(input_shape=(28, 28)),
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])


print("DONE")