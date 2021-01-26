import h5py
import joblib
import os
from FeatureExtraction import FeatureExtract as fe
from sklearn import preprocessing, svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

x_data = []
y_data = []

dir_path = '../train_data'
index = 1
for dir_name in os.listdir(dir_path):
    dir_loc = dir_path + '/' + dir_name
    for filename in os.listdir(dir_loc):
        file   = h5py.File(dir_loc + '/' + filename, 'r')
        data   = file['00:07:80:4D:2E:9E']['raw']['channel_1'][:,0]
        for i in range(6):
            click_index      = 5000 * (i + 1)
            noclick_index    = click_index - 1500
            
            if index == 1:
                x_data.append(fe.getAllData(fe, data[click_index:click_index + 1500]))
                y_data.append(1)
                x_data.append(fe.getAllData(fe, data[noclick_index:noclick_index + 1500]))
                y_data.append(0)
            else :
                x_data.append(fe.getAllData(fe, data[click_index:click_index + 1500]))
                y_data.append(2) 
    index+=1
        
min_max_scaler  = preprocessing.MinMaxScaler()
min_max_scaler.fit(x_data)
x_data          = min_max_scaler.transform(x_data)

x_train, x_test = train_test_split(x_data, test_size=0.2, random_state=42)
y_train, y_test = train_test_split(y_data, test_size=0.2, random_state=42)

kernel_list = ['linear', 'poly', 'rbf', 'sigmoid']
for k in kernel_list:
    clf = svm.SVC(kernel=k)
    clf.fit(x_train, y_train)
    
    svm_prediction = clf.predict(x_test)
    svm_accuracy = accuracy_score(y_test, svm_prediction) * 100
    svm_report = classification_report(y_test, svm_prediction)
    print('SVM Accuracy (' + k + '): ', svm_accuracy, '%')
    print(svm_report)
    
    svm_filename        = 'svm_' + k + '_model.pkl'
    joblib.dump(clf, svm_filename)

for n in (3, 5, 7, 9, 11):
    knn = KNeighborsClassifier(n_neighbors=n)
    knn.fit(x_train, y_train)
    
    knn_prediction = knn.predict(x_test)
    
    knn_accuracy = accuracy_score(y_test, knn_prediction) * 100
    knn_report = classification_report(y_test, knn_prediction)
    print('KNN Accuracy K(' + str(n) + '): ', knn_accuracy, '%')
    print(knn_report)
    
    
    
    knn_filename        = 'knn_' + str(n) + '_model.pkl'
    joblib.dump(knn, knn_filename)
    
scaler_file     = 'scaler.pkl'
joblib.dump(min_max_scaler, scaler_file)