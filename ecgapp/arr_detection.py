import database_download
from matplotlib import pyplot as plt
from scipy.signal import find_peaks
import numpy as np
import cv2
from keras.models import load_model
from collections import Counter

doctor_id = "d1"
patient_id = "p1"

path = "Doctors/" + doctor_id + "/Patients/" + patient_id

def arr_detection(abs_path):
    pred_li = []
    classes = ['Normal','Premature ventricular contractions',' Premature atrial beats','Right bundle branch', 'Left bundle branch', 'Atrial premature complexes', 'ventricular flutter wave', 'Ventricular ectopic beat' ]

    data = database_download.get_values(abs_path)
    ecg = np.array(data[0])

    y,_ = find_peaks(ecg, height = .5)
    plt.figure(2,figsize=(1.4 , 1.41) , dpi= 100)
    plt.plot(ecg[y[3]-100:y[3]+100])
    plt.axis('off')
    plt.savefig('single_ecg_beat.png',bbox_inches='tight')

    model = load_model('ecg_model_own.hdf5')
    image = cv2.imread('single_ecg_beat.png')
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    pred = model.predict(image.reshape((1, 128, 128, 3)))
    y_classes = pred.argmax(axis=-1)
    pred_li.append(y_classes[0])
    result = classes[int(pred_li[0])-1]

    return result

print(arr_detection(path))
