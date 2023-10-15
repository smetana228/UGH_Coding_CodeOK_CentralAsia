import cv2

#pre-trained Haar Cascade Classifier for car detection
car_cascade = cv2.CascadeClassifier('haarcascade_car.xml')
video_path = 'video'

def detect_cars(video_path):
    video = cv2.VeideoCapture(video_path)
    gray = cv2.cvtColor(video, cv2.COLOR_BGR2GRAY)

    cars = car_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(25, 25))
    car_count=0
    is_loaded = False
    #draws rectangles around detected cars
    for (x, y, w, h) in cars:
        cv2.rectangle(vid, (x, y), (x + w, y + h), (0, 0, 255), 2)
        car_count+=1

    cv2.release('Car Detection', video)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    if car_count > 20:
        is_loaded = True
detect_cars(video_path)
