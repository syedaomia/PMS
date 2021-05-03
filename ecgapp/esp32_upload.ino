
#include <Wire.h>
#include "MAX30105.h"
#include "spo2_algorithm.h"

#include "ESPDateTime.h"
#include "config.h"

MAX30105 particleSensor;

#define MAX_BRIGHTNESS 255

#include <WiFi.h>
#include <Firebase_ESP_Client.h>

/* 1. Define the WiFi credentials */
#define WIFI_SSID "Finally!!!"
#define WIFI_PASSWORD "alubokhara32"

/* 2. Define the Firebase project host name and API Key */
#define FIREBASE_HOST "pmss-7fd59-default-rtdb.firebaseio.com"
#define API_KEY "AIzaSyD9InLOfFAP9QruzyvtYRT8sJs99xHDcAw"

/* 3. Define the user Email and password that alreadey registerd or added in your project */
#define USER_EMAIL "farhanishti32@gmail.com"
#define USER_PASSWORD "alubokhara32"

//Define Firebase Data object
FirebaseData fbdo;

FirebaseAuth auth;
FirebaseConfig config;

void printResult(FirebaseData &data);

uint16_t ecg[150];
uint32_t irBuffer[50]; //infrared LED sensor data
uint32_t redBuffer[50];  //red LED sensor data
String unq_id = "d1" ;
float x ;

int32_t bufferLength = 50; //data length
int32_t spo2; //SPO2 value
int8_t validSPO2; //indicator to show if the SPO2 calculation is valid
int32_t heartRate; //heart rate value
int8_t validHeartRate; //indicator to show if the heart rate calculation is valid

int spo2_v = 0;
int hr_v = 0;

void setupDateTime() {
  DateTime.setServer("ntp.aliyun.com");
  DateTime.setTimeZone("UTC-6");
  DateTime.begin();
  if (!DateTime.isTimeValid()) {
    Serial.println("Failed to get time from server.");
  }
}

void setup()
{
 
  Serial.begin(2400); // initialize serial communication at 115200 bits per second:


  Serial.println("Begin");
  while (!Serial) continue;
    Serial.println();
    Serial.println();

    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    Serial.print("Connecting to Wi-Fi");
    while (WiFi.status() != WL_CONNECTED)
    {
        Serial.print(".");
        delay(300);
    }
    Serial.println();
    Serial.print("Connected with IP: ");
    Serial.println(WiFi.localIP());
    Serial.println();

    /* Assign the project host and api key (required) */
    config.host = FIREBASE_HOST;
    config.api_key = API_KEY;

    /* Assign the user sign in credentials */
    auth.user.email = USER_EMAIL;
    auth.user.password = USER_PASSWORD;

    Firebase.begin(&config, &auth);
    Firebase.reconnectWiFi(true);


    fbdo.setResponseSize(1024);

setupDateTime();

////////////////////////////////ECG////////////////////////////////
  pinMode(35, INPUT); // Setup for leads off detection LO +
  pinMode(32, INPUT); // Setup for leads off detection LO -

  // Initialize sensor
  if (!particleSensor.begin(Wire, I2C_SPEED_FAST)) //Use default I2C port, 400kHz speed
  {
    Serial.println(F("MAX30105 was not found. Please check wiring/power."));
    while (1);
  }

//  Serial.println(F("Attach sensor to finger with rubber band. Press any key to start conversion"));
//  while (Serial.available() == 0) ; //wait until user presses a key
//  Serial.read();

  byte ledBrightness = 50; //Options: 0=Off to 255=50mA
  byte sampleAverage = 4; //Options: 1, 2, 4, 8, 16, 32
  byte ledMode = 2; //Options: 1 = Red only, 2 = Red + IR, 3 = Red + IR + Green
  byte sampleRate = 100; //Options: 50, 100, 200, 400, 800, 1000, 1600, 3200
  int pulseWidth = 411; //Options: 69, 118, 215, 411
  int adcRange = 4096; //Options: 2048, 4096, 8192, 16384

  particleSensor.setup(ledBrightness, sampleAverage, ledMode, sampleRate, pulseWidth, adcRange); //Configure sensor with these settings

////////////////////////////////////////////////

  //read the first 100 samples, and determine the signal range
  for (byte i = 0 ; i < bufferLength ; i++)
  {
    while (particleSensor.available() == false) //do we have new data?
      particleSensor.check(); //Check the sensor for new data

    redBuffer[i] = particleSensor.getRed();
    irBuffer[i] = particleSensor.getIR();
    particleSensor.nextSample(); //We're finished with this sample so move to next sample
  }

  //calculate heart rate and SpO2 after first 100 samples (first 4 seconds of samples)
  maxim_heart_rate_and_oxygen_saturation(irBuffer, bufferLength, redBuffer, &spo2, &validSPO2, &heartRate, &validHeartRate);

}

void loop()
{
  String jsonStr = "";
  String time_stamp = String(DateTime.now()) ;
  //Serial.println(time_stamp);
  String path ="/Doctors/" + unq_id + "/Patients/p1/" + time_stamp;
  
  FirebaseJson json1;
   
  Serial.print("Loop started");
  Serial.println(String(DateTime.now()));
  
  for (byte i = 0; i < 150 ; i = i + 1) 
    {
      /////////////ECG////////////////
      x = analogRead(34);
      json1.set("ecg/[" + String(i) + "]", x);
    ///////////////SPO2///////////////////
      for (byte i = 1; i < 50; i++)
      {
        redBuffer[i - 1] = redBuffer[i];
        irBuffer[i - 1] = irBuffer[i];
      }

        while (particleSensor.available() == false) //do we have new data?
          particleSensor.check(); //Check the sensor for new data
 
  
        redBuffer[49] = particleSensor.getRed();
        irBuffer[49] = particleSensor.getIR();
        particleSensor.nextSample(); //We're finished with this sample so move to next sample
  
      maxim_heart_rate_and_oxygen_saturation(irBuffer, bufferLength, redBuffer, &spo2, &validSPO2, &heartRate, &validHeartRate);
     spo2_v = spo2 ;
     hr_v   = heartRate;
        
    }
    json1.set("spo2/",spo2_v );
    json1.set("hr/",hr_v );
    json1.set("timestamp/", time_stamp );

//   json1.toString(jsonStr, true);
//   Serial.println(jsonStr);

    Firebase.RTDB.set(&fbdo, path.c_str(), &json1);

    
}
