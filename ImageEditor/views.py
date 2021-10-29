import glob
import os
import shutil
import time
import cv2
import numpy as np
import pandas as pd
import tensorflow as tf

from PIL import Image

Image.LOAD_TRUNCATED_IMAGES = True

from django.shortcuts import render, redirect
from ImageEditor.models import Video, Conner
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import load_model


# Create your views here.


def videoList(request):
    videoList = Video.objects.all()
    if request.method == "POST":
        download_path = "D:/video/"
        files = glob.glob(download_path + '*.ts')
        print(files)

        for idx, file in enumerate(files):
            fname, ext = os.path.splitext(file)
            print(fname)
            filename = os.path.basename(file)
            move_path = fname + "/"
            createFolder(move_path)
            shutil.move(download_path + filename, move_path + filename)
            video = Video(
                title=filename,
                path=fname,
                conner='N'
            )
            videoCapture(video)
            video.save()
        return render(request, 'ImageEditor/videoList.html', context={'videoList': videoList})
    else:

        return render(request, 'ImageEditor/videoList.html', context={'videoList': videoList})


## videoCapture ?초 단위 JPG 생성 저장
def videoCapture(video):
    original_path = video.path + '/' + video.title
    videoObj = cv2.VideoCapture(original_path)
    print(videoObj)
    ## caputre 타이밍
    seconds = 5  # 5초 단위
    fps = videoObj.get(cv2.CAP_PROP_FPS)  # fps : 초당 프레임

    multiplier = fps * seconds

    frameCount = 0
    ret = 1
    startPoint = time.time()
    while ret:
        frameId = int(round(videoObj.get(1)))  # Frame 넘버

        ret, frame = videoObj.read()
        if frameId % multiplier < 1:
            # 파일명 뒤에 frameId 캡쳐 타임 기록해두어 나중에 구간 선정 시 파일명 참고
            frame_path = video.path + '/frame/'
            createFolder(frame_path)
            frame_name = frame_path + str((frameCount * seconds)) + ".jpg"
            extension = os.path.splitext(frame_name)[1]  # 이미지 확장자
            result, encoded_img = cv2.imencode(extension, frame)
            if result:
                with open(frame_name, mode='w+b') as f:
                    encoded_img.tofile(f)
            frameCount += 1
    finishPoint = time.time()

    print('----- Finish Video Capture! -----')
    print('\n', "처리시간은: ", finishPoint - startPoint, "초 입니다.")


def selectVideo(request, id):
    # Video 목록 중 pk(primaryKey)를 이용하여 검색
    video = Video.objects.get(id=id)
    if video.conner == 'Y':
        connerList = Conner.objects.get(video_id=id)
        context = {'video': video, 'connerList': connerList}
    else:
        context = {'video': video}

    if request.method == "POST":
        connerClassification(video)

        return render(request, 'ImageEditor/selectVideo.html', context=context)

    else:
        return render(request, 'ImageEditor/selectVideo.html', context=context)


def connerClassification(video):
    frame_path = video.path + '/frame/'
    crop_path = 'D:/video/crop/'
    createFolder(crop_path)

    # [전처리1] imageCrop
    imageCrop(frame_path, crop_path)
    print("전처리1 : 코너 영역 분리 완료")
    # [전처리2] imageGenerator : rescale
    image_generator = imageGenerator(crop_path)
    print(image_generator)
    #filenames = image_generator.filenames
    #print(filenames)
    print("전처리2 : ImageGenrator Rescale 완료")
    #prediction(crop_path)


# [전처리1] imageCrop (학습 영역 crop_coordinate 수정)
def imageCrop(frame_path, crop_path):
    crop_coordinate = {
        'left': 270,
        'top': 85,
        'right': 560,
        'bottom': 120
    }

    files = glob.glob(frame_path + '/*.jpg')
    for idx, file in enumerate(files):
        fname, ext = os.path.splitext(file)
        img = Image.open(file)
        filename = os.path.basename(file)
        crop_image = img.crop((crop_coordinate['left'], crop_coordinate['top'], crop_coordinate['right'], crop_coordinate['bottom']))
        crop_image.save(crop_path + filename)


# [전처리2] imageGenerator
def imageGenerator(crop_path):
    image_datagen = ImageDataGenerator(rescale=1./255)
    image_generator = image_datagen.flow_from_directory(crop_path, batch_size=128, target_size=(35, 290),
                                                        class_mode='categorical')
    return image_generator


# [예측]
def prediction(image_generator):
    model_path = 'D:/video/model/superman_cnn_model.h5'
    model = load_model(model_path)

    print(model)
    pred = model.predict(image_generator)

    #cl = np.round(pred)
    #filenames = image_generator.filenames
    #print(filenames)
    #print(pred)

    # Data Frame
    #result = pd.DataFrame({"file": filenames, "pr": pred[:, 0], "class": cl[:, 0]})
    #print(result)

    np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})
    print(image_generator.class_indices)
    print(pred)



def createFolder(dir):
    try:
        if not os.path.exists(dir):
            os.makedirs(dir)
    except OSError:
        print('Error: Creating directory. ' + dir)
