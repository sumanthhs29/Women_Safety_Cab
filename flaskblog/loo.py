import cv2
from mtcnn.mtcnn import MTCNN
detector = MTCNN()

def detect(frame,image):
    faces = detector.detect_faces(image)
    for face in faces:
        x,y,wi,he = face['box']
        cv2.rectangle(frame,(x,y),(x+wi,y+he),(255,0,0),2,cv2.LINE_AA)
    return frame

cap = cv2.VideoCapture(0)

while cap.isOpened():
    _,frame = cap.read()
    image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    print("hello")
    frame = detect(frame,image)
    print("shashank")
    cv2.imshow("shashank",frame)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()