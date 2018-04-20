import boto3
import json
import PIL
from PIL import Image, ImageDraw

if __name__ == "__main__":

    imageFile='input5.jpg'
    client=boto3.client('rekognition','us-west-2')
   
    with open(imageFile, 'rb') as image:
        response = client.detect_faces(Image={'Bytes': image.read()},Attributes=['ALL'])
    
    #print(json.dumps(response['FaceDetails'][0], indent=4, sort_keys=True))
    print('Detected faces for ' + imageFile)
    for faceDetail in response['FaceDetails']:
        boundingBox = faceDetail['BoundingBox']


        print('The detected face is between ' + str(faceDetail['AgeRange']['Low'])
              + ' and ' + str(faceDetail['AgeRange']['High']) + ' years old')
        print('Here are the other attributes:')
        print(json.dumps(faceDetail, indent=4, sort_keys=True))
    

    mayorConfidence = response['FaceDetails'][0]['Emotions'][0]
    for emotion in response['FaceDetails'][0]['Emotions']:
        if emotion['Confidence'] >= mayorConfidence['Confidence']:
            mayorConfidence = emotion

    print(emotion, " mayor: ", mayorConfidence)

    height = response['FaceDetails'][0]['BoundingBox']['Height']
    left = response['FaceDetails'][0]['BoundingBox']['Left']
    top = response['FaceDetails'][0]['BoundingBox']['Top']
    width = response['FaceDetails'][0]['BoundingBox']['Width']
    
    '''if mayorConfidence['Type'] == "DISGUSTED":
        imageName = "DISGUSTED.png"
    elif mayorConfidence['Type'] == "HAPPY":
        imageName = "HAPPY.png"
    elif mayorConfidence['Type'] == "SAD":
        imageName = "SAD.png"
    elif mayorConfidence['Type'] == "ANGRY":
        imageName = "ANGRY.png"
    elif mayorConfidence['Type'] == "CONFUSED":
        imageName = "CONFUSED.png"
    elif mayorConfidence['Type'] == "SURPRISED":
        imageName = "SURPRISED.png"
    elif mayorConfidence['Type'] == "CALM":
        imageName = "CALM.png"
    elif mayorConfidence['Type'] == "UNKNOWN":
        imageName = "UNKNOWN.png"'''

    
    originalImage = Image.open(imageFile)
    oX, oY = originalImage.size

    imageName = "images/" + mayorConfidence['Type'] + ".png"
    im = Image.open(imageName)
    x, y = im.size

    newHeight = oY * height
    newTop = oY * top

    newWidth = oX * width
    newLeft = oX * left

    newSize = newHeight, newWidth

    newCoords = int(newTop), int(newLeft), int(newSize[0]), int(newSize[1])
    print(newCoords)

    print("New height", oY, height)
    print("New width", oX, width)

    im = im.resize((int(newSize[0]), int(newSize[1])), PIL.Image.ANTIALIAS)
    print(newSize)

    #im.save("RESIZED.png", "PNG")

    originalImage.paste(im,(int(newLeft),int(newTop)),im)

    originalImage.save("MODIFIED.jpg", "JPEG")

    #print(newCoords)

def pasteImage():
    return None