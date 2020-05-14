from flaskblog import app,loginmanager,detector,model,face_net,in_encoder
from flaskblog.models import User,DriverInfo,BookingInfo
from flask_login import login_required,logout_user,login_user,current_user
from flask import render_template,url_for,redirect
from flaskblog.forms import LoginForm,RegistrationForm,BookingForm,DriverLoginForm
from flaskblog import db
# from basics import graph
# from basics import detector,face_net,model,in_encoder
# from PIL import Image
# from numpy import asarray
# from tensorflow import keras
# import cv2
#from mtcnn.mtcnn import MTCNN
# from numpy import expand_dims
#from datetime import datetime
import datetime
import tensorflow as tf
#graph = tf.get_default_graph()


from PIL import Image
from numpy import asarray
from numpy import load
from numpy import expand_dims
from numpy import asarray
import numpy as np
from numpy import load
import cv2

from sklearn.svm import SVC
import joblib







@app.route('/home')
@login_required
def home():
    print(current_user)

    return render_template('home.html')


@app.route('/face_prediction')
@login_required
def face_prediction():
    recog = 0
    b = BookingInfo.query.filter_by(driver_email=current_user.email).first()
    if b is not None:
        if b.verified == 'yes':
            return redirect(url_for('after_recognition'))
        bookt = b.date
        print(datetime.datetime.now())
        time = datetime.datetime.now().time()
        booktime = datetime.time(int(bookt[:2]),int(bookt[3:5]),int(bookt[6:]))
        dateTimeA = datetime.datetime.combine(datetime.date.today(), booktime)
        dateTimeB = datetime.datetime.combine(datetime.date.today(), time)
        print(dateTimeA,dateTimeB)
        if dateTimeA >= dateTimeB:
            print("inside")
            dif = str(dateTimeA - dateTimeB)
            print(dif)
            if dif[:1] == '0' and int(dif[2:4]) <= 30:
                recog = 1
                print(recog)
            else:
                print("shashi")
                return redirect(url_for('driver_profile'))
        else:
            return redirect(url_for('driver_profile'))
        if recog == 1:

            sh = un = su = 0

            def draw_face(filename, name, required_size=(160, 160)):
                #    image = Image.open(filename)

                #   image = image.convert('RGB')

                # pixels = asarray(filename)
                #with graph.as_default():
                results = detector.detect_faces(filename)
                # print("results:{}".format(results))

                for face in results:
                    x, y, wi, he = face['box']
                    cv2.rectangle(filename, (x, y), (x + wi, y + he), (255, 0, 0), 2, cv2.LINE_AA)
                    cv2.putText(filename, name, (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
                image2 = cv2.cvtColor(filename, cv2.COLOR_RGB2BGR)
                return image2

            def extract_face(filename, required_size=(160, 160)):
                #    image = Image.open(filename)

                #   image = image.convert('RGB')

                pixels = asarray(filename)
                #with graph.as_default():
                results = detector.detect_faces(filename)
                # print("results:{}".format(results))

                image2 = cv2.cvtColor(filename, cv2.COLOR_RGB2BGR)
                if len(results) != 0:
                    x1, y1, width, height = results[0]['box']
                    x1, y1 = abs(x1), abs(y1)
                    x2, y2 = x1 + width, y1 + height
                    face = pixels[y1:y2, x1:x2]
                    image = Image.fromarray(face)
                    image = image.resize(required_size)
                    face_array = asarray(image)

                    return [face_array, image2]
                else:
                    return [0, image2]

            import cv2

            # face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

            def get_embedding(model, face_pixels):
                # scale pixel values
                face_pixels = face_pixels.astype('float32')
                # standardize pixel values across channels (global)
                mean, std = face_pixels.mean(), face_pixels.std()
                face_pixels = (face_pixels - mean) / std
                # transform face into one sample
                samples = expand_dims(face_pixels, axis=0)
                # make prediction to get embedding
                #with graph.as_default():
                yhat = face_net.predict(samples)
                return yhat[0]

            cap = cv2.VideoCapture(0)
            count = 0

            while cap.isOpened():
                ret, frame = cap.read()
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                face_array, frame = extract_face(image)
                if type(face_array) != type(0):
                    # print(type(face_array))
                    # print(face_array.shape)
                    # m,n,o = face_array.shape
                    # face_array = np.reshape(face_array,(1,m,n,o))
                    # print(type(face_array))
                    newTrainX = list()
                    # face_array = face_array.astype('float32')

                    embedding = get_embedding(model, face_array)
                    # print(type(face_array))
                    # print(face_array.shape)
                    newTrainX.append(embedding)
                    newTrainX = asarray(newTrainX)
                    trainX = in_encoder.transform(newTrainX)
                    # print(type(trainX))
                    # print(trainX.shape)
                    # print(len(trainX))
                    # print("hello")
                    # print("shape:{}:{}".format(trainX.shape,type(trainX)))

                    # samples = expand_dims(trainX, axis=0)
                    #        print("shape:{}:{}".format(samples.shape,type(samples)))
                    y_class = model.predict(trainX)
                    # print(y_class)
                    y_prob = model.predict_proba(trainX)
                    # print(y_prob)
                    class_index = y_class[0]
                    print(class_index)
                    class_probability = y_prob[0, class_index] * 100
                    print(class_probability)
                    if class_probability < 96.00:
                        name = "Unknown"
                        un += 1
                    else:
                        if class_index == 0:
                            name = "shashank"
                            sh += 1
                        else:
                            name = "sumanth"
                            su += 1

                    frame = draw_face(image, name)

                cv2.imshow('shashank', frame)
                if (cv2.waitKey(1) & 0xff == ord('q')):
                    break
                if (sh == 25) or (su == 25) or (un == 25):
                    break
            cap.release()
            cv2.destroyAllWindows()
            if sh == 25:
               # print("The person is Shashank")
                fin_name = "shashank"
            elif su == 25:
                fin_name = "sumanth"
                #print("The person is Shamala")
            else:
                fin_name = "unknown"
                #print("Unknown person")
            if fin_name == current_user.name:
                b = BookingInfo.query.filter_by(driver_email=current_user.email).first()
                b.verified = "yes"
                db.session.commit()
            else:
                b.verified = "no"
                db.session.commit()



            return redirect(url_for('after_recognition'))
    else:
        return redirect(url_for('driver_profile'))

    #return render_template('recognition.html')

@app.route('/after_recognition')
@login_required
def after_recognition():
    b = BookingInfo.query.filter_by(driver_email = current_user.email).first()
    if b.verified != 'yes':
        return redirect('driver_profile')
    return render_template('recognition.html')




@app.route('/driver_profile')
@login_required
def driver_profile():

#    print(current_user)
    print(current_user.is_authenticated)
    book_info = BookingInfo.query.filter_by(driver_email = current_user.email).first()
    if book_info is not None:
        user = User.query.filter_by(id=book_info.user_id).first()
        return render_template('driver_profile.html',book_info=book_info,user=user)
    else:
        return render_template('No_register.html')
    return render_template('driver_profile.html')

@app.route('/driver_login',methods=['GET','POST'])

def driver_login():
    @loginmanager.user_loader
    def load_user(id):
        return DriverInfo.query.get(int(id))
    form_d = DriverLoginForm()
    if form_d.validate_on_submit():
        driver = DriverInfo.query.filter_by(email=form_d.email.data).first()
        if driver is not None:
            login_user(driver)
            print(driver)
            return redirect(url_for('driver_profile'))
    return render_template('driver_login.html',form_d=form_d)

@app.route('/delete_booking',methods=['GET','POST'])
def delete_booking():
    b = BookingInfo.query.filter_by(user_id=current_user.id).first()
    if b is not None:
        if b.verified == 'yes':
            return redirect(url_for('booking'))
        driver_email = b.driver_email
        driver = DriverInfo.query.filter_by(email=driver_email).first()
        driver.about = 'free'
        db.session.delete(b)
        db.session.commit()
    return redirect(url_for('booking'))

@app.route("/", methods=['GET', 'POST'])
def register():
    @loginmanager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    form_l = LoginForm()
    form = RegistrationForm()
    #form_d = DriverLoginForm()

    if form.validate_on_submit():
        #flash(f'Account created for {form.username.data}!', 'success')
        user = User(username = form.username.data,email=form.email.data,password=form.password.data )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        #if current_user.is_authenticated:
         #   return redirect(url_for('home'))
        return redirect(url_for('booking'))



    if form_l.validate_on_submit():
        user = User.query.filter_by(email=form_l.email.data).first()
        if user and user.password == form_l.password.data:
            login_user(user)
            return redirect(url_for('booking'))



    return render_template('signup.html', title='Register', form=form,form_l=form_l)

@app.route("/booking",methods=['GET','POST'])
@login_required
def booking():
    form = BookingForm()
    if form.validate_on_submit():
        d = DriverInfo.query.filter_by(about="free").first()
        #print("{}".format(d))
        if d is None:
            return redirect(url_for('login'))
            print(d)
        else:
            b = BookingInfo.query.filter_by(user_id = current_user.id).first()
            if b is not None:
                return redirect(url_for('booking'))
            d.about = "Book"
            name = d.password
            print(current_user)
            print(dir(current_user))
            print(current_user.id)
            print(current_user.get_id())
            print(form.date.data)
            date = str(form.date.data)
            print(date)
            book_info = BookingInfo(pickup=form.pickup.data,verified="not yet",destination=form.destination.data,driver_email=d.email,date=date,user_id=current_user.id)
            db.session.add(book_info)
            image = url_for('static',filename='images/'+d.image)
            driver_info = d
            dl_image = url_for('static',filename='images/'+d.dl)

            db.session.commit()

            return render_template('booking_secess.html',image=image,driver = driver_info,dl_image=dl_image)

        print(form.date.data)
        #return redirect(url_for('home'))
    return render_template('booking.html',form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    #return redirect(url_for('check'))
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            #flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            print("hello")
            #flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)



@app.route('/check_driver')
@login_required
def check_driver():
    b = BookingInfo.query.filter_by(user_id=current_user.id).first()
    if b is not None:
        if b.verified == "yes":
            message = "Driver Face has been Reconised"
        elif b.verified == "no":
            message = "Please Contact the authority.Since we are having some Trouble recognizing Driver's Face"
        else:
            message = ''
        d = DriverInfo.query.filter_by(email=b.driver_email).first()
        image = url_for('static', filename='images/' + d.image)
        driver_info = d
        dl_image = url_for('static', filename='images/' + d.dl)

        #db.session.commit()

        return render_template('booking_secess.html', image=image, driver=driver_info, dl_image=dl_image,message=message)
    d = DriverInfo.query.filter_by(about="free").first()
    if d is None:
        message = "All Drivers are booked"
    else:
        message = "You Haven't Booked the Cab"
    print(message)
    return render_template('login.html', message=message)

@app.route('/logout')
@login_required
def logout():
    logout_user()

    return redirect(url_for('register'))


@app.route("/sucess_booking")
def sucess_booking():

    return render_template('booking_secess.html')




@app.route('/reached_destination')
def reached_destination():
    b = BookingInfo.query.filter_by(driver_email=current_user.email).first()
    current_user.about = "free"
    db.session.delete(b)
    db.session.commit()
    return redirect(url_for('driver_profile'))