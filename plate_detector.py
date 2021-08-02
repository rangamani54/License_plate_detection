import cv2


def read_image(path):
  photo = cv2.imread(path)
  photo = cv2.cvtColor(photo, cv2.COLOR_BGR2RGB)
  return photo

def plate_detector(path, size=0.5):
    model_plate = cv2.CascadeClassifier(r"C:\Users\ranga\OneDrive\Desktop\ml_projects\character_number_plate_detection\haarcascade_russian_plate_number (1).xml")
    img = read_image(path)
    plate = model_plate.detectMultiScale(img, 1.1, 4)
    for (x,y,w,h) in plate:
        p = int(0.06*img.shape[0])
        d = int(0.025*img.shape[1])
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,255),5)
        plate_cropped = img[y+d:y+h-d, x+p:x+w-d]

    return img, plate_cropped
