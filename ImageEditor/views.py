import glob
import os
import shutil
import time
from PIL import Image
import cv2

Image.LOAD_TRUNCATED_IMAGES = True

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from ImageEditor.models import ImageCrop, VideoList, ConnerList


def videoList(request):
    if request.method == "POST":
        download_path = "D:/video/"
        files = glob.glob(download_path + '*.ts')
        print(files)

        for idx, file in enumerate(files):
            print(idx)
            fname, ext = os.path.splitext(file)

            filename = os.path.basename(file)
            move_path = fname + "/"
            createFolder(move_path)
            shutil.move(download_path + filename, move_path + filename)
            video = VideoList(
                title=filename,
                path=fname,
                conner='N'
            )
            video.save()
            videoCapture(video)
            return redirect('/ImageEditor/videoList/')

        # return HttpResponseRedirect('/ImageEditor/videoList/')
    else:
        videoList = VideoList.objects.all()
        return render(request, 'ImageEditor/videoList.html', context={'videoList': videoList})


## videoCapture ?초 단위 JPG 생성 저장
def videoCapture(video):
    original_path = video.path + '/' + video.title
    videoObj = cv2.VideoCapture(original_path)

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
            frame_path = video.path + '/frame'
            createFolder(frame_path)
            filename = os.path.basename(video.title)
            cv2.imwrite(frame_path + "/%d.jpg" % (frameCount * seconds), frame)
            frameCount += 1
    finishPoint = time.time()

    print('----- Finish Video Capture! -----')
    print('\n', "처리시간은: ", finishPoint - startPoint, "초 입니다.")


def selectVideo(request, pk):
    # Video 목록 중 pk(primaryKey)를 이용하여 검색
    video = VideoList.objects.get(pk=pk)

    if request.method == "POST":
        connerClassification(video)
        video.path

        return redirect('ImageEditor/selectVideo/', context={'video':video})

    else:
        connerList = ConnerList.objects.all()
        return render(request, 'ImageEditor/selectVideo.html', context={'video': video, 'connerList': connerList})


def connerClassification(video):

    frame_path = video.path + '/frame'
    crop_path = video.path + '/crop'
    createFolder(crop_path)

    # [전처리1] imageCrop
    imageCrop(frame_path, crop_path)
    # [전처리2] imageGenerator : rescale


# [전처리1] imageCrop (학습 영역 crop_coordinate 수정)
def imageCrop(frame_path, crop_path):
    crop_coordinate = {
        'left': 270,
        'top': 85,
        'right': 560,
        'bottom': 120
    }
    print(crop_coordinate)

    files = glob.glob(frame_path + '/*.jpg')
    for idx, file in enumerate(files):
        fname, ext = os.path.splitext(file)
        print(ext)
        img = Image.open(file)
        filename = os.path.basename(file)
        crop_image = img.crop(
            (crop_coordinate['left'], crop_coordinate['top'], crop_coordinate['right'], crop_coordinate['bottom']))
        crop_image.save(crop_path + '/' + filename)


def createFolder(dir):
    try:
        if not os.path.exists(dir):
            os.makedirs(dir)
    except OSError:
        print('Error: Creating directory. ' + dir)
