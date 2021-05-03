# firebase-admin == 4.5.2
import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin import _http_client
from firebase_admin import db

from matplotlib import pyplot as plt
from datetime import datetime

dictionary = {
    "type": "service_account",
    "project_id": "pmss-7fd59",
    "private_key_id": "199a4cd81485e884d7938143af85028f9689a8df",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEuwIBADANBgkqhkiG9w0BAQEFAASCBKUwggShAgEAAoIBAQCZUKErbMesMnMs\nZhDlOv6q2h6I3khe1odXSEuIIJ3EJtzff4ZdKwYzg+9qZ4oT3rE0tgcQfPJfAy4E\nPi9w3crcTOJzshSTUJxTlChezd6PxJAa//hsJbOHhfEUYxX7A2aaQ28azjk9pp7p\ns3DTYhCWX07B154ufy9KU83uPI+uAbj4GVTMSPROgsJLCA3QLejXUr0Q2UbFX8tr\nbus4auFrMGIXRu2k21HU/TSVVli6niOP9WH14YLtPU+GUxKwVaDFczOnQDO96ih1\nJB9KBR9XWqeyDqYCmCv04QNtqPFJqGNk5ljE5Qdcp8d3qA0hOdDt9I48ATCqPQ4k\nfMAm+q4pAgMBAAECgf9NzAoVCzZfmI9rTYQgtZ47vuzkPc71XSPilDqbIiKjTgj3\nL77mY4Dy0+fN5eDuG+HoY5pvDJabPm+JDPjtcYYRUC9P228ns0YaL11ZH7CTKytK\nJpmfhCy6HnqADqMYvLlsOMvGtgNJpvoIwWb5GaVphBf477n/fKLLv1lSTcpqH5P1\niOVyjJZXFqsHc7r7zQ6OijI5XBiVUXuJZIS+rdrBsiU2wlzv4Uh4a/Y2kINcWPHL\nnCGyxFoYXIH4W/qekO/ZeOLjyB0O30iolZafEO6iEjaka7IRuKxXAE55T3WGK3Md\nJlWNhe0o0AbMxhkgT95lLjmNIDTW35zgagpAnAECgYEA0A+xUQIK/HEyVeXlVCRh\n3MJWzx4wB9XiHJhhus/Kyko8sIThLvxawca9i5bGOiVbw2Pmobgp8/8gC8PdvoqY\nm312FXhv3cG9JGV3QqctqXNwCbVzi2WIjgl/2Ue23fSe0HBYFVrrqLyj1bHS9QJl\njD9MzHXyb/SgXWtPKfGTA1ECgYEAvKPGDC1OOm236hlDMv6M5+eb2mzHlTHFb5RU\nZmDShaj4TB6A2qiWFn9Ar3AzSVWgveuHMycc/veYIqMYhpUWGyv36gtWzfLp5vTo\nnyPN1IMowt5D6oogvAQLbu+1lgEfrbRQGg2KKUqqJZYVw6wY4GEjiDbSO7XsgMsk\nde1eV1kCgYEAsKaSOyBL6ZfGT+4YLr+RI1kRUVrlFtH+3551Y6InIGe1bX30nur9\nt4agyhKijR3I8nUwjOALJrHXKIYNEEkmVuZHyuTtvc9PYsaPYlUEzNlJJ8UarCDx\ntv7TwMxFs9+Ms5afAsqmSSaYx8fqP8HgLBpWf0YpJ+r/+TEyDn+f/XECgYBfEpOQ\nM41HuWCF5bGOk+hkQMC19zknomwFblaTOp0frCdoBb+fdHQgZoYtZXkTrspSrc/4\nIfBlOFg+rMCBo8X+b8yE8q4PIixssGZFPoBQaMI0ZF0Kag9RcyBoCvwT3AEhRM1S\nNBy77tuOEfRqJ+RpwctsrWSLn4bQ6pE3tihkEQKBgBA9EYb4sDysH3mWkq1LxjIt\n01ozm+JK6Jz4i323Iur87LFZ0g+anxjcin6J3iDoNGbJbcL8njhbv8ZFODiL7NiK\nZlWUKkHDxIym3Y8Sen0M9/U4C+3uv7aWJON6w0mTKqKhYguIrEwSN6tU/uk6ULE7\nc/mxatnmvph99xIM6Gqm\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-7r2n5@pmss-7fd59.iam.gserviceaccount.com",
    "client_id": "111322646092052715365",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-7r2n5%40pmss-7fd59.iam.gserviceaccount.com"
}


# initializing the credentials of the app
# after creating app project settings>service account> generate new private key
cred = credentials.Certificate(dictionary)
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://pmss-7fd59-default-rtdb.firebaseio.com/'
})

doctor_id = "d1"
patient_id = "p1"

abs_path = "Doctors/" + doctor_id + "/Patients/" + patient_id


def get_values(abs_path):
    ecg = []
    hr = []
    spo2 = []

    ref = db.reference(abs_path)
    data = ref.order_by_child("timestamp").limit_to_last(1).get()
    data = dict(data).values()
    data = list(data)
    # print(data)
    for i in data:
        hr.append(i.get("hr"))
        ecg += (i.get("ecg"))
        spo2.append(i.get("spo2"))

    return(ecg, hr, spo2)


def get_range_values(abs_path, start_date=0, start_hour=0, start_min=0, end_date=0, end_hour=0, end_min=0):
    ecg = []
    hr = []
    spo2 = []

    ref = db.reference(abs_path)

    def convert_timestamp(date, hour, mins):
        sec = "0"
        input_datetime = date + " " + hour+":" + mins + ":" + sec
        date_time_obj = datetime.strptime(input_datetime, '%d/%m/%y %H:%M:%S')
        #print("python date time object: ",date_time_obj)
        timestamp = str(int(datetime.timestamp(date_time_obj)))
        # print(timestamp)
        return timestamp
    start_time = convert_timestamp(
        date=start_date, hour=start_hour, mins=start_min)
    end_time = convert_timestamp(date=end_date, hour=end_hour, mins=end_min)

    data = ref.order_by_child("timestamp").start_at(
        start_time).end_at(end_time).get()

    data = dict(data).values()
    data = list(data)
    # print(data)
    for i in data:
        hr.append(i.get("hr"))
        ecg += (i.get("ecg"))
        spo2.append(i.get("spo2"))
    return(ecg, hr, spo2)









last_val = get_values(abs_path)
# print("ECG :", last_val[0])
# print("hr :", last_val[1])
# print("spo2 :", last_val[2])
# print("")


range_val = get_range_values(abs_path,
                             start_date="15/04/21", start_hour='23', start_min='4',
                             end_date="15/04/21", end_hour="23", end_min="5")

# print("ECG :" ,range_val[0])
# print("hr :" , range_val[1])
# print("spo2 :" , range_val[2])
# print("")



# plt.figure(1)
# plt.plot(last_val[0])
# plt.grid()
# plt.show()
# plt.savefig("ecg.png")


    

    


# plt.figure(2)
# plt.plot(range_val[1])
# plt.grid()
# plt.show()
# plt.savefig("hr.png")


# plt.figure(3)
# plt.plot(range_val[2])
# plt.grid()
# plt.show()
# plt.savefig("spo2.png")
