import skimage
import sklearn
import random
import numpy as np
import os
from sklearn.externals import joblib
from sklearn import ensemble
from skimage import io

def read_folder(folder, ext):
    ret = []
    for f in os.listdir(folder):
        if ext in f:
            ret.append(skimage.io.imread(folder+'/'+f, True))
    return ret

                
def read_samples(pos_folder, neg_folder, ext=".pgm"):
    return read_folder(pos_folder, ext), read_folder(neg_folder, ext)

def extract_features(image, types=['pixels']):
    #todo: add different types of features, now only pixels possible
    return np.array(image, dtype=np.uint8).flatten()

def train(pos_folder='train/face', neg_folder='train/non-face', ext='.pgm', feature_types=['pixels']):
    pos_data , neg_data = read_samples(pos_folder, neg_folder, ext)
    pos_data = np.array(map(extract_features, pos_data))
    neg_data = np.array(map(extract_features, neg_data))
    
    pos_labels = [1]*len(pos_data)
    neg_labels = [0]*len(neg_data)
    
    all_data = numpy.concatenate([pos_data, neg_data])
    all_labels = pos_labels+neg_labels

    #shuffle the data and labels with the same random seed
    #to get the same random permutations
    random.seed()
    seed = random.randint(0,1000)
    np.random.seed(seed)
    np.random.shuffle(all_data)
    np.random.seed(seed)
    np.random.shuffle(all_labels)

    adaBoost = sklearn.ensemble.AdaBoostClassifier()
    classy = adaBoost.fit(all_data, all_labels)
    joblib.dump(classy, 'classifier/classifier.pkl')

def test(pos_folder, neg_folder, ext='.pgm', feature_types=['pixels'],
         pickle='classifier/classifier.pkl'):
    
    

train()

