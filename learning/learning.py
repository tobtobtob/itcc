import skimage
import sklearn
import random
import numpy as np
import os
from sklearn.externals import joblib
from sklearn import ensemble
from skimage import io
from skimage import feature

def read_folder(folder, ext):
    ret = []
    for f in os.listdir(folder):
        if ext in f:
            ret.append(skimage.io.imread(folder+'/'+f, True))
    return ret

                
def read_samples(pos_folder, neg_folder, ext=".pgm"):
    return read_folder(pos_folder, ext), read_folder(neg_folder, ext)

def extract_lbp_histogram(image, regions=(3,3)):
    splitted = np.array_split(np.array(image), regions[0]*regions[1])
    histograms = np.array([[0]*256]*regions[0]*regions[1])
    for i in range(0, regions[0]*regions[1]-1):
        temp = splitted[i].flatten()
        for v in temp:
            histograms[i][v] = histograms[i][v]+1
    return histograms
        
            
        

def extract_features(image, types=['lbp-histogram']):
    #todo: add different types of features, now only pixels possible
    for t in types:
        if t == 'pixels':
            return np.array(image, dtype=np.uint8).flatten()
        if t == 'lbp':
            return np.array(skimage.feature.local_binary_pattern(image, 8,1)).flatten()
        if t == 'lbp-histogram':
            return extract_lbp_histogram(image).flatten()
            

def train(pos_folder='train/face', neg_folder='train/non-face', ext='.pgm', feature_types=['lbp']):
    pos_data , neg_data = read_samples(pos_folder, neg_folder, ext)
    pos_data = np.array(map(extract_features, pos_data))
    neg_data = np.array(map(extract_features, neg_data))
    
    pos_labels = [1]*len(pos_data)
    neg_labels = [0]*len(neg_data)
    
    all_data = np.concatenate([pos_data, neg_data])
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

def test(pos_folder, neg_folder, ext='.pgm', feature_types=['lbp'],
         pickle='classifier/classifier.pkl'):
    clf = joblib.load(pickle)
    pos_data , neg_data = read_samples(pos_folder, neg_folder, ext)
    pos_data = np.array(map(extract_features, pos_data))
    neg_data = np.array(map(extract_features, neg_data))
    
    pos_results = map(clf.predict, pos_data)
    neg_results = map(clf.predict, neg_data)

    pos_ones = sum(pos_results)
    neg_ones = sum(neg_results)

    print pos_ones
    print neg_ones
    

    print "positives: ", pos_ones, "/", len(pos_results), " correct"
    print "negatives: ", (len(neg_results)-neg_ones), "/", len(neg_results), " correct"
    
train()    
test('test/face', 'test/non-face')
    



