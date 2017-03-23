from naoqi import ALProxy
import vision_definitions
import time
import sys
import Image# Python Image Library

def getGyrometersValue(IP, PORT):
	# Create proxy to ALMemory
    try:
        memoryProxy = ALProxy("ALMemory", IP, PORT)
    except Exception, e:
        print "Could not create proxy to ALMemory"
        print "Error was: ", e

    #Get the Gyrometer X, Y, Z values
    Gyro_X = memoryProxy.getData("Device/SubDeviceList/InertialSensor/AccelerometerX/Sensor/Value")
    Gyro_Y = memoryProxy.getData("Device/SubDeviceList/InertialSensor/AccelerometerY/Sensor/Value")
    Gyro_Z = memoryProxy.getData("Device/SubDeviceList/InertialSensor/AccelerometerZ/Sensor/Value")
    Gyrometer_Val = (Gyro_X, Gyro_Y, Gyro_Z)
    return Gyrometer_Val

def getImage(IP, PORT):
	print "Creating ALVideoDevice proxy to ", IP

	camProxy = ALProxy("ALVideoDevice", IP, PORT)

	####
	# Register a Generic Video Module

	resolution = vision_definitions.kQQVGA
	colorSpace = vision_definitions.kYUVColorSpace
	fps = 20

	nameId = camProxy.subscribe("python_GVM", resolution, colorSpace, fps)

	print 'getting images in remote'
	print "getting image " + str(i)
	camProxy.getImageRemote(nameId)
	time.sleep(0.05)

	camProxy.unsubscribe(nameId)

def showNaoImage(IP, PORT):
  """
  First get an image from Nao, then show it on the screen with PIL.
  """

  camProxy = ALProxy("ALVideoDevice", IP, PORT)
  resolution = 2    # VGA
  colorSpace = 11   # RGB

  videoClient = camProxy.subscribe("python_client", resolution, colorSpace, 5)

  t0 = time.time()

  # Get a camera image.
  # image[6] contains the image data passed as an array of ASCII chars.
  naoImage = camProxy.getImageRemote(videoClient)

  t1 = time.time()

  # Time the image transfer.
  print "acquisition delay ", t1 - t0

  camProxy.unsubscribe(videoClient)

  # Now we work with the image returned and save it as a PNG  using ImageDraw
  # package.

  # Get the image size and pixel array.
  imageWidth = naoImage[0]
  imageHeight = naoImage[1]
  array = naoImage[6]

  # Create a PIL Image from our pixel array.
  im = Image.fromstring("RGB", (imageWidth, imageHeight), array)

  # Save the image.
  im.save("camImage.png", "PNG")

  im.show()

if __name__ == '__main__':
	port = 9559
	IP_address = "nao.local"

	motion = ALProxy("ALMotion", IP_address, port)
	motion.setStiffnesses("Body", 1.0)
	tts = ALProxy("ALTextToSpeech", IP_address, port)
	tts.say("I am awake!")

	motion.moveInit()
	for i in range(4):
		motion.post.moveTo(0, 0, -1)
		tts.say("I'm keeping truning right!")
		#getImage()
		tts.say("Now I see the world around!")
	getGyrometersValue(IP_address, port)
	print(getGyrometersValue(IP_address, port))
	if (getGyrometersValue(IP_address, port)[0] !=0)or(getGyrometersValue(IP_address, port)[1] !=0)or(getGyrometersValue(IP_address, port)[2] !=0):
		tts.say("I am a little dizzy!")
	
	tts.say(" Here is waht I see.")
	showNaoImage(IP_address, port)
