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
            print(file)
            move_path = fname + "/"
            createFolder(move_path)
            shutil.move(download_path + filename, move_path + filename)
            video = Video(
                title=filename,
                path=fname,
                conner='N'
            )
            # videoCapture(video)
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
    connerList = Conner.objects.filter(video_id=id)
    if video.conner == 'Y':
        context = {'video': video, 'connerList': connerList}
    else:
        context = {'video': video}

    if request.method == "POST":
        conner_result = connerClassification(video)
        print(len(conner_result))
        for i in range(0, len(conner_result)):
            thumbnailMake(video, conner_result.iloc[i, 1])
            conner = Conner(
                frame_img="/media/" + video.path + "/" + str(conner_result.iloc[i, 1]) + ".jpg",
                video_id=video.id,
                conner_name=conner_result.iloc[i, 0],
                conner_start=conner_result.iloc[i, 1],
                conner_end=conner_result.iloc[i, 2],
            )

            conner.save()
        video.conner = 'Y'
        video.save()
        context = {'video': video, 'connerList': connerList}

        return render(request, 'ImageEditor/selectVideo.html', context=context)

    else:
        return render(request, 'ImageEditor/selectVideo.html', context=context)


def thumbnailMake(video, conner_start):
    frame = video.path + "/frame/" + str(conner_start) + ".jpg"
    frame_name = os.path.basename(frame)
    print(frame)
    print(frame_name)
    thumbnail_path = "C:/project/META21/MediaProject/media/" + os.path.splitext(video.title)[0]
    print(thumbnail_path)
    createFolder(thumbnail_path)
    thumbnail = thumbnail_path + "/" + frame_name

    shutil.copy(frame, thumbnail)



def connerClassification(video):
    frame_path = video.path + '/frame/'
    crop_path = video.path + '/pred/crop/'
    pred_path = video.path + '/pred'
    createFolder(crop_path)

    # [전처리1] imageCrop
    imageCrop(frame_path, crop_path)

    # [전처리2] imageGenerator : rescale
    image_generator = imageGenerator(pred_path)

    # [예측] CNN 모델
    pred = prediction(image_generator)

    # [결과] 코너 구간 분류 알고리즘

    pred['conner'] = pred.apply(connerName, axis=1)
    # print(pred_result[500:510])

    group = pred.groupby('conner').agg(['min', 'max'])['time']
    group.drop(['untitled'], inplace=True)
    conner_result = group.sort_values(by=['min'], axis=0)
    conner_result = conner_result.rename_axis('conner').reset_index()

    return conner_result


def connerName(pred):
    connerList = ['hyunbin', 'juho', 'jung', 'sam', 'sauri', 'yoon']

    if pred['hyunbin'] > 0.9:
        val = 'hyunbin'
    elif pred['juho'] > 0.9:
        val = 'juho'
    elif pred['jung'] > 0.9:
        val = 'jung'
    elif pred['sam'] > 0.9:
        val = 'sam'
    elif pred['sauri'] > 0.9:
        val = 'sauri'
    elif pred['yoon'] > 0.9:
        val = 'yoon'
    else:
        val = 'untitled'

    return val


# [전처리1] imageCrop 학습 영역 crop_coordinate 수정)
def imageCrop(frame_path, crop_path):
    print("전처리1 : 코너 영역 이미지 분리 시작")
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
        crop_image = img.crop(
            (crop_coordinate['left'], crop_coordinate['top'], crop_coordinate['right'], crop_coordinate['bottom']))
        file_numbering = '0' * (10 - len(filename))
        crop_image.save(crop_path + file_numbering + filename)
    print("전처리1 : 코너 영역 이미지 분리 완료")


# [전처리2] imageGenerator
def imageGenerator(crop_path):
    print("전처리2 : ImageGenrator Rescale 시작")
    image_datagen = ImageDataGenerator(rescale=1. / 255)
    image_generator = image_datagen.flow_from_directory(crop_path, batch_size=128, target_size=(35, 290), shuffle=False,
                                                        class_mode="categorical")
    image_generator.reset()
    print("전처리2 : ImageGenrator Rescale 완료")
    return image_generator


# [예측]
def prediction(image_generator):
    print("예측 : CNN 모델 예측 시작")
    model_path = 'D:/video/model/project_pilot.h5'
    model = load_model(model_path)

    conner_map = {
        0: 'hyunbin',
        1: 'juho',
        2: 'jung',
        3: 'sam',
        4: 'sauri',
        5: 'yoon'
    }

    pred = model.predict_generator(image_generator)
    df_pred = pd.DataFrame(pred)
    df_pred.rename(columns=conner_map, inplace=True)
    pd.options.display.float_format = '{:.2f}'.format

    file_names = image_generator.filenames
    time = []
    for i in range(0, len(file_names)):
        time.append(i * 5)
    df_file = pd.DataFrame({"file": file_names, "time": time})

    result = pd.concat([df_file, df_pred], axis=1)

    print("예측 : CNN 모델 예측 종료")
    return result
    # Data Frame


def createFolder(dir):
    try:
        if not os.path.exists(dir):
            os.makedirs(dir)
    except OSError:
        print('Error: Creating directory. ' + dir)
