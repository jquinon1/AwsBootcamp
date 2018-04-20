import boto3
import json
import PIL
from PIL import Image, ImageDraw

if __name__ == "__main__":

    imageFile='input.jpg'
    originalImage = Image.open(imageFile) # Imagen completa
    client=boto3.client('rekognition','us-west-2')
   
    with open(imageFile, 'rb') as image:
        response = client.detect_faces(Image={'Bytes': image.read()},Attributes=['ALL'])
    
    #print(json.dumps(response['FaceDetails'][0], indent=4, sort_keys=True))
    print('Detected faces for ' + imageFile + ' Size' , len(response['FaceDetails']))
    
    #for faceDetail in response['FaceDetails']:
        
        
        #boundingBox = faceDetail['BoundingBox']
        #print('The detected face is between ' + str(faceDetail['AgeRange']['Low'])
        #      + ' and ' + str(faceDetail['AgeRange']['High']) + ' years old')
        #print('Here are the other attributes:')
        #print(json.dumps(faceDetail, indent=4, sort_keys=True))

    for i in range(0,len(response['FaceDetails'])):
        faceDetails = response['FaceDetails'][i]

        mayorConfidence = faceDetails['Emotions'][0]
        for emotion in faceDetails['Emotions']:
            if emotion['Confidence'] >= mayorConfidence['Confidence']:
                mayorConfidence = emotion

        print(emotion, " mayor: ", mayorConfidence)

        height = faceDetails['BoundingBox']['Height']
        left = faceDetails['BoundingBox']['Left']
        top = faceDetails['BoundingBox']['Top']
        width = faceDetails['BoundingBox']['Width']

        
        
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