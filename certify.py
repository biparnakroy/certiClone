import cv2
import csv
import shutil
import os

PATH = "temp1.png"
NAME_LIST_PATH = "Shankh_Mitra_Regestration_Final - Form Responses 1.csv"


def convert(list):
    return tuple(list)


def getNames(csv_path):
    with open(csv_path) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        names = []
        for row in readCSV:
            name = row[1]
            names.append(name)
        return(names)


def fillSpace(path):
    image = cv2.imread(path)

    image_roi = image[int(image.shape[0]/4):int(-image.shape[0]/3),
                      int(image.shape[1]/4):int(-image.shape[1]/4)]

    gray = cv2.cvtColor(image_roi, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(
        gray, 0, 155, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (148, 1))
    detected_lines = cv2.morphologyEx(
        thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)

    cnts = cv2.findContours(
        detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    #name_list = getNames(name_list_path)

    for c in cnts:
        c[0][0][0] = c[0][0][0]+int(image.shape[1]/4)
        c[0][0][1] = c[0][0][1]+int(image.shape[0]/4)
        #image_out = cv2.putText(image, name, convert(c[0][0]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA, False)
        #cv2.imwrite('out/{}.png'.format(name), cv2.putText(image, name, convert(c[0][0]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA, False))
        return (convert(c[0][0]))
    #cv2.waitKey()

def fillName(path, name_list_path):
    name_list = getNames(name_list_path)
    location = fillSpace(path)
    for name in name_list:
        certificate = cv2.imread(path)
        certificate_out=cv2.putText(certificate , name, location, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA, False)
        #certificate_out = cv2.imencode('out/{}.png'.format(name), certificate_out)
        cv2.imwrite('out/{}.png'.format(name), certificate_out)

def certificateGen(path,name_list_path):
    os.mkdir('out')
    fillName(path,name_list_path)
    shutil.make_archive('output', 'zip', 'out')
    shutil.rmtree('out', ignore_errors=True)

if __name__ == "__main__":
    certificateGen(PATH, NAME_LIST_PATH)

