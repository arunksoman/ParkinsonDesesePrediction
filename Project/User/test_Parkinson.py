# Necessary imports
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import confusion_matrix
from skimage import feature
from imutils import build_montages
from imutils import paths
import numpy as np
import argparse
import cv2
import os
from random import uniform
import base64
from ..configurations import DATASET_SPLIT_DIR

########################## Functions #################################
def base64_to_image(encoded_data):
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

def quantify_image(image):
    # compute the histogram of oriented gradients feature vector for
    # the input image
    features = feature.hog(image, orientations=9,
        pixels_per_cell=(10, 10), cells_per_block=(2, 2),
        transform_sqrt=True, block_norm="L1")

    # return the feature vector
    return features

def load_split(path):
    # grab the list of images in the input directory, then initialize
    # the list of data (i.e., images) and class labels
    imagePaths = list(paths.list_images(path))
    data = []
    labels = []

    # loop over the image paths
    for imagePath in imagePaths:
        # extract the class label from the filename
        label = imagePath.split(os.path.sep)[-2]

        # load the input image, convert it to grayscale, and resize
        # it to 200x200 pixels, ignoring aspect ratio
        image = cv2.imread(imagePath)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.resize(image, (200, 200))

        # threshold the image such that the drawing appears as white
        # on a black background
        image = cv2.threshold(image, 0, 255,
            cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

        # quantify the image
        features = quantify_image(image)

        # update the data and labels lists, respectively
        data.append(features)
        labels.append(label)

    # return the data and labels
    return (np.array(data), np.array(labels))

def calculate_statistics():
    # loop over the number of trials to run
    for i in range(0, num_of_trials):
        # train the model
        print("[INFO] training model {} of {}...".format(i + 1, num_of_trials))
        model = RandomForestClassifier(n_estimators=100)
        model.fit(trainX, trainY)

        # make predictions on the testing data and initialize a dictionary
        # to store our computed metrics
        predictions = model.predict(testX)
        metrics = {}

        # compute the confusion matrix and and use it to derive the raw
        # accuracy, sensitivity, and specificity
        cm = confusion_matrix(testY, predictions).flatten()
        (tn, fp, fn, tp) = cm
        metrics["acc"] = (tp + tn) / float(cm.sum())
        metrics["sensitivity"] = tp / float(tp + fn)
        metrics["specificity"] = tn / float(tn + fp)

        # loop over the metrics
        for (k, v) in metrics.items():
            # update the trials dictionary with the list of values for
            # the current metric
            l = trials.get(k, [])
            l.append(v)
            trials[k] = l
    # loop over our metrics
    actual_metrics = {}
    for metric in ("acc", "sensitivity", "specificity"):
        # grab the list of values for the current metric, then compute
        # the mean and standard deviation
        values = trials[metric]
        mean = np.mean(values)
        std = np.std(values)
        actual_metrics["metric"] = metric
        key_mean  = metric + "_mean"
        actual_metrics[key_mean] = mean
        key_std = metric + "_std"
        actual_metrics[key_std] = std
        
        # show the computed metrics for the statistic
        print(metric)
        print("=" * len(metric))
        print("u={:.4f}, o={:.4f}".format(mean, std))
    return actual_metrics
############### Test Function #################

def test_base64(image):
    # image = cv2.imread(test_image_name)
    # output = image.copy()
    # pre-process the image in the same manner we did earlier
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.resize(image, (200, 200))
    image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    # quantify the image and make predictions based on the extracted
    # features using the last trained Random Forest
    features = quantify_image(image)
    model = RandomForestClassifier(n_estimators=100)

    model.fit(trainX, trainY)

    # make predictions on the testing data and initialize a dictionary
    # to store our computed metrics
    # predictions = model.predict(testX)
    preds = model.predict([features])
    label = le.inverse_transform(preds)[0]
    print(label)
    metrics = calculate_statistics()
    return label, metrics
    # draw the colored class label on the output image and add it to
    # the set of output images
    # color = (0, 255, 0) if label == "Healthy" else (0, 0, 255)
    # cv2.putText(output, label, (3, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,color, 2)
    # cv2.imshow("image", output)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

################ main Program #################
# DATASET_SPLIT_DIR = 'C:/Users/arun/Desktop/ParkinsonDesesePrediction/Project/Admin/Output'
num_of_trials = 5
dataset_dir = DATASET_SPLIT_DIR
trainingPath = os.path.sep.join([dataset_dir, "train"])
testingPath = os.path.sep.join([dataset_dir, "val"])
# loading the training and testing data
print("[INFO] loading data...")
(trainX, trainY) = load_split(trainingPath)
(testX, testY) = load_split(testingPath)

# encode the labels as integers
le = LabelEncoder()
trainY = le.fit_transform(trainY)
testY = le.transform(testY)
# initialize our trials dictionary
trials = {}

def check_parkinson(image):
    image = image.split(',')[1]
    image = base64_to_image(image)
    label, result = test_base64(image)
    result.update({"result": label})
    print(result)
    return result
if __name__ == "__main__":
    with open("C:/Users/arun/Desktop/ParkinsonDesesePrediction/Project/User/parkinson.txt") as fp:
        test_image = fp.read()
        print(test_image)
    check_parkinson(test_image)