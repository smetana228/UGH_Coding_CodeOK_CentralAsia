import cv2

#pre-trained Haar Cascade Classifier for car detection
car_cascade = cv2.CascadeClassifier('haarcascade_car.xml')
image_path = 'image'
#creates a function to detect cars in an image
def detect_cars(image_path):
    # Load the image
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #detects cars in the image
    cars = car_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(25, 25))
    car_count=0
    is_loaded = False
    #draws rectangles around detected cars
    for (x, y, w, h) in cars:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        car_count+=1

    #displays the image with detected cars
    cv2.imshow('Car Detection', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    if car_count > 20:
        is_loaded = True
detect_cars(image_path)