import boto3
import json
if __name__ == "__main__":

    imageFile='input.jpg'
    client=boto3.client('rekognition','us-west-2')
   
    with open(imageFile, 'rb') as image:
        response = client.detect_faces(Image={'Bytes': image.read()},Attributes=['ALL'])
    
    #print(json.dumps(response['FaceDetails'][0], indent=4, sort_keys=True))
    print('Detected faces for ' + imageFile)
    for faceDetail in response['FaceDetails']:
        print('The detected face is between ' + str(faceDetail['AgeRange']['Low'])
              + ' and ' + str(faceDetail['AgeRange']['High']) + ' years old')
        print('Here are the other attributes:')
        print(json.dumps(faceDetail, indent=4, sort_keys=True))
    

    mayorConfidence = response['FaceDetails'][0]['Emotions'][0]
    for emotion in response['FaceDetails'][0]['Emotions']:
        if emotion['Confidence'] >= mayorConfidence['Confidence']:
            mayorConfidence = emotion

        print(emotion, " mayor: ", mayorConfidence)
                        
    