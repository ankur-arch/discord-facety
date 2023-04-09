from models.face_details import FaceDetails
import cv2
from image_utils import ImageInfo
from deepface import DeepFace


def analyzeFace(images: list[ImageInfo]):
    for im in images:
        if im is None:
            yield None
            continue
        result = DeepFace.analyze(img_path=im.numpy_format, actions=[
            'age', 'gender', 'race', 'emotion'], enforce_detection=False)
        if result:
            x = result.get('region').get('x')
            w = result.get('region').get('w')
            y = result.get('region').get('y')
            h = result.get('region').get('h')
            temp = cv2.cvtColor(
                im.numpy_format[y:y+h, x:x+w, :], cv2.COLOR_BGR2RGB)
            _, encoded_image = cv2.imencode('.png', temp)

            im_bytes = encoded_image.tobytes()

            yield FaceDetails(
                region=result.get('region'),
                race=result.get('dominant_race'),
                emotion=result.get('dominant_emotion'),
                age=result.get('age'),
                gender=result.get('gender'),
                face=im_bytes)
        return
