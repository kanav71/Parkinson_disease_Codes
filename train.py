import tensorflow as tf
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint
from net.vgg16 import model
from preprocess.generator import train_generator, valid_generator
from fingertip import Fingertips ## Kanav adding this so that we can use transfer learning

#import os
#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def loss_function(y_true, y_pred):
    square_diff = tf.squared_difference(y_true, y_pred)
    square_diff = tf.reduce_mean(square_diff, 1)
    loss = tf.reduce_mean(square_diff)
    return loss


# creating the model
model = model()
#model.load_weights('weights/vgg16.h5') # Kanav added this so we can use transfer learning.
model.summary()

# compile
adam = Adam(lr=1e-2, beta_1=0.9, beta_2=0.999, epsilon=1e-10, decay=0.0) #changing lr to 1e-2 from 1e-5
model.compile(optimizer=adam, loss=loss_function)

# train
epochs = 2 # kanav changed from 10 to 2
train_gen = train_generator(sample_per_batch=1, batch_number=8232) # kanav changed from 1690 to 5, sample_per_batch to 1
val_gen = valid_generator(sample_per_batch=3, batch_number=2) # kanav changed sample_per_batch from 50 to 3 & batch number from 10 to 2 

checkpoints = ModelCheckpoint('weights/weights{epoch:03d}.h5', save_weights_only=True, period=1)
history = model.fit_generator(train_gen, steps_per_epoch=8232, epochs=epochs, verbose=1, shuffle=True,  # kanav changed from 1690 to 3
                              validation_data=val_gen, validation_steps=2, #changed from 10 to 2 - nto sure of original though
                              callbacks=[checkpoints], max_queue_size=100)

with open('history.txt', 'a+') as f:
    print(history.history, file=f)

print('All Done!')
