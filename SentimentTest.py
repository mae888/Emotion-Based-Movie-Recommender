import cv2
from deepface import DeepFace
from PyMovieDb import IMDB
import random
from deepface.commons import functions


def captureImage():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        cv2.imshow('Press Space to Capture Image', frame)
        if cv2.waitKey(1) & 0xFF == ord(' '):
            cv2.imwrite('user_image.jpg', frame)
            break

    cap.release()
    cv2.destroyAllWindows()


def analyzeEmotion(image_path):
    result = DeepFace.analyze(img_path=image_path, actions=['emotion'])
    return result


def getMovie(genre):
    imdb = IMDB()
    res = imdb.popular_movies(genre=genre, start_id=1, sort_by=None)
    movieStrings = res.split('},')
    movieList = [movie.strip() + '}' for movie in movieStrings]
    movieList[-1] = movieList[-1].rstrip('}')
    choice = random.choice(movieList).replace(
        '{', '').replace('}', '').replace('[', '').replace(']', '')
    return choice


def recommendMovie(emotion):
    emotionGenreMap = {
        'happy': ['Romance', 'Drama'],
        'sad': ['Comedy'],
        'angry': ['Comedy'],
        'fear': ['Comedy'],
        'surprise': ['Adventure'],
        'disgust': ['Romance'],
        'neutral': ['Comedy', 'Action', 'Adventure', 'Documentary'],
    }

    genres = emotionGenreMap.get(emotion, ['Drama'])
    return random.choice(genres)


def main():
    #Input from User's camera
    captureImage()
    results = analyzeEmotion('user_image.jpg')
    #Test Case from existing image#results = analyzeEmotion('Test Case 3 - Happy.jpg')
    #Test Case from existing image#results = analyzeEmotion('Test Case 2 - Sad.jpg')
    #Test Case from existing image#results = analyzeEmotion('Test Case 3 - Happy.jpg')
    for i, result in enumerate(results):
        domEmotion = result['dominant_emotion']
        if i == 0:
            print(f'Dominant emotion: {domEmotion}')
    print(getMovie(recommendMovie(domEmotion)))

if __name__ == '__main__':
    main()
