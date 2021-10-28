import glob
import os
import shutil
import time

from PIL import Image
import cv2

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from ImageEditor.models import ImageCrop, VideoList, ConnerList


def index(request):
    return render(request, '/ImageEditor/videoList.html')


def videoList(request):
    if request.method == "POST":
        downloadPath = "D:/video/"
        files = glob.glob(downloadPath + '*.ts')
        print(files)

        for idx, file in enumerate(files):
            print(idx)
            fname, ext = os.path.splitext(file)

            filename = os.path.basename(file)
            movePath = fname + "/"
            createFolder(movePath)
            shutil.move(downloadPath + filename, movePath + filename)
            video = VideoList(
                title=filename,
                path=fname,
                conner='N'
            )
            video.save()

        return HttpResponseRedirect('/ImageEditor/videoList/')
    else:
        videoList = VideoList.objects.all()
        return render(request, 'ImageEditor/videoList.html', context={'videoList': videoList})


def selectVideo(request, pk):
    # Video 목록 중 pk(primaryKey)를 이용하여 검색
    video = VideoList.objects.get(pk=pk)
    print(video.title)
    connerList = ConnerList.objects.all()

    return render(request, 'ImageEditor/selectVideo.html', context={'video': video, 'connerList': connerList})


def connerClassification(request):
    if request.method == "POST":
        framePath = "C:/Users/User/image/video/TheReturnofSuperman_210808/test/sam/"
        files = glob.glob(framePath + '*.jpg')
        conner = ConnerList(
            frame_img=framePath + "filename_0.jpg",
            video_title="TheReturnofSuperman_210808.mp4",
            frame_path=framePath,
            conner_name='sam',
            conner_start=0,
            conner_last=390
        )
        conner.save()
        print(conner.video_title)
    return render(request, 'ImageEditor/connerClassification.html')


## videoCapture 1초 단위 JPG 생성 저장
def videoCapture(request, pk):
    video = VideoList.objects.get(pk=pk)

    original_path = video.path + '/' + video.title
    videoObj = cv2.VideoCapture(original_path)

    seconds = 5  # 1초 단위
    fps = videoObj.get(cv2.CAP_PROP_FPS)  # fps : 초당 프레임

    multiplier = fps * seconds

    frameCount = 1
    ret = 1
    startPoint = time.time()
    while ret:
        frameId = int(round(videoObj.get(1)))  # current frame number

        ret, frame = videoObj.read()
        if frameId % multiplier < 1:
            # 파일명 뒤에 frameId 캡쳐 타임 기록해두어 나중에 구간 선정 시 파일명 참고
            framePath = video.path + '/frame'
            createFolder(framePath)
            filename = os.path.basename(video.title)
            cv2.imwrite(framePath + "/" + filename + "_%d.jpg" % frameId, frame)
            frameCount += 1
    finishPoint = time.time()

    print('----- Finish Video Capture! -----')
    print('\n', "처리시간은: ", finishPoint - startPoint, "초 입니다.")

    return render(request, 'ImageEditor/selectVideo.html', context={'video': video})


def imageCrop(request):
    originalPath = "D:/video/superman2/frame/"
    cropPath = "D:/video/superman2/crop/"
    createFolder(cropPath)

    if request.method == "POST":
        left = int(request.POST.get('left'))
        top = int(request.POST.get('top'))
        right = int(request.POST.get('right'))
        bottom = int(request.POST.get('bottom'))
        # left : 270, top : 85, right : 560, bottom : 120

        print(left, top, right, bottom)

        files = glob.glob(originalPath + '/*')
        for idx, file in enumerate(files):
            fname, ext = os.path.splitext(file)
            print(ext)
            if ext in ['.JPG', '.PNG', '.GIF', '.jpg', '.png', '.gif']:  # 뒷 이미지 파일 명
                img = Image.open(file)
                filename = os.path.basename(file)
                print(file)
                crop_image = img.crop((left, top, right, bottom))
                crop_image.save(cropPath + 'crop_' + filename)

        return render(request, 'ImageEditor/imageCrop.html', context={'path': cropPath})

    else:
        return render(request, 'ImageEditor/imageCrop.html', context={'path': ''})


def createFolder(dir):
    try:
        if not os.path.exists(dir):
            os.makedirs(dir)
    except OSError:
        print('Error: Creating directory. ' + dir)


