# UDP communication for streaming :https://www.aipacommander.com/entry/2017/12/27/155711
# カメラからの画像の読み込み、画像処理、機械学習、UDPで画像と答えの文字を送信

import socket
import numpy as np
import cv2
import time
import multiprocessing as mp
from multiprocessing import  Queue,Process
from queue import Empty
import sys
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image,ImageFile
import time
import copy
import time

#　機械学習による判断と　答え　画像の送信
class Proc(Process):
    def __init__(self,frame,ip):#
        super(Proc, self).__init__()
        # self.queue = queue
        self.frame = frame
        self.ip    = ip #ip address

    def run(self):
        # 通信方法の設定
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        to_send_addr = (self.ip, 8080)

        img = self.frame#cv2.imread("./image_data/test1.jpg")
 
        # <judge by AI　モデルを使用して答えの出力>
        # 答えのクラス名
        classes=["model1-base","model1-controlroom","model1-cover","model1-joint1","model1-joint2","model1-patrollight","model1-rot","model1-shorel","model1-shuft","model1-wheel"]
        num_classes=len(classes)
        image_size=100
        # モデルファイルのディレクトリ
        MODEL_FILE_PATH='./ml_models/final_model.h5'

        ImageFile.LOAD_TRUNCATED_IMAGES = True
        # 取得エラーが出た場合は、Image.open()で行う。んで、＊１で書き込む
        image= img#Image.open("./image_data/test2.jpg")　
        model=load_model(MODEL_FILE_PATH)

        image=image.convert('RGB')
        image=image.resize((image_size,image_size))
        data=np.asarray(image)
        X=[]
        X.append(data)
        X=np.array(X)

        result=model.predict([X])[0]
        predicted=result.argmax()
        percentage=int(result[predicted]*100)

        answer = classes[predicted]


        frame = cv2.resize(img, (640,480))
        # フレームをJPEG形式にエンコード
        _, img_encode = cv2.imencode('.jpeg', frame)

        # 念の為５回送信？しておく
        for j in range(3):
            # 画像を分割する
            for i in np.array_split(img_encode, 26):
                # 画像の送信
                udp.sendto(i.tostring(), to_send_addr)
            if(j==2):
                answer_byte = answer.encode()
                udp.sendto(b'__end__', to_send_addr)
                udp.sendto(answer_byte,to_send_addr)
            else:
                udp.sendto(b'__end__', to_send_addr)
                udp.sendto(b'__THE__',to_send_addr)

        print("send\n")

    
# 画像のトリミング関数
def crop_minAreaRect(img, rect):
    angle     = rect[2]
    rows,cols = img.shape[0], img.shape[1]
    h,w = img.shape[:2]

    wi = int(w/2)-rect[0][0]
    hi = int(h/2)-rect[0][1]
    mv_mat = np.float32([[1, 0,wi],[0, 1,hi]])
    img = cv2.warpAffine(img, mv_mat, (w, h),1)

    rect__ = ((int(w/2),int(h/2)),(rect[1][0],rect[1][1]),rect[2])
    box = cv2.boxPoints(rect__)
    matrix    = cv2.getRotationMatrix2D((cols/2,rows/2),angle,1)
    img_rot   = cv2.warpAffine(img,matrix,(cols,rows))
    
    pts = np.int0(cv2.transform(np.array([box]), matrix))[0]
    pts[pts < 0] = 0
    return img_rot[pts[1][1]-30:pts[0][1]+30, pts[1][0]-30:pts[2][0]+30]






def main():
    host = socket.gethostname()
    print(host)

    # ipアドレスを取得、表示
    # 処理されていない動画の送信先IPアドレス
    ip1 = socket.gethostbyname(host)
    print(ip1) # 192.168.○○○.○○○
    #　画像処理後の動画送信先のIPアドレスポート
    ip2 = ip1
    print(ip2)

    # 送信スタイルの設定
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    to_send_addr = (ip1, 8008)

    # カメラの起動
    cap = cv2.VideoCapture(0)
    if cap.isOpened()== False:
        sys.exit()
    #　カメラのFPS値など
    cap.set(cv2.CAP_PROP_FPS, 15)
    ret,frame = cap.read()

    # 物体を置いてもらう指示線　範囲設定
    h,w = frame.shape[:2]
    frame_s= (int(w/6),int(h/6))
    frame_e= (int(w*5/6),int(h*5/6))

    count_in = 0
    inside = 0
    co = 0
    img_pre = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    ab = 0
    while True:


        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(gray,img_pre)

        if(len(diff[diff>33]) > 0):#moveing now
                count_in = 0 #中に入った回数
                move = 1

        else:
            move = 0

            if(count_in == 0):
                count_in = 1
                ret, c1img = cv2.threshold(gray, 37, 255, cv2.THRESH_BINARY)
                contours, h_= cv2.findContours(c1img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
                mx_area = 0
                
                for cont in contours:
                    area = cv2.contourArea(cont)

                    if area > mx_area:
                        mx_cont, mx_area = cont, area

                mx_rect = cv2.minAreaRect(mx_cont)  # 四角く括れるエリアを探す//角度のついた長方形の値が戻る
                
                hi = mx_rect[1][1]
                wi = mx_rect[1][0]


                box = cv2.boxPoints(mx_rect)# 上記エリアを長方形座標に変換する
                box = np.int0(box)

                M = cv2.moments(mx_cont) # COM

                xcom,ycom = int(M["m10"]/M["m00"]) , int(M["m01"]/M["m00"])

                (xcen, ycen), radius = cv2.minEnclosingCircle(mx_cont)
                center = (int(xcen), int(ycen))
        
                if(w//6<int(mx_rect[0][0])<w*5//6) & (h//6<int(mx_rect[0][1])<h*5//6) :
                    inout = 1 #中
                    co+=1
                    roi = crop_minAreaRect(frame, mx_rect)

        
                    deltax = xcen-xcom
                    if deltax < 0: # always left COM
                        roi = cv2.rotate(roi, cv2.ROTATE_180)

                    hi, wi = roi.shape[:2]
            

                    if hi > wi:
                        roi = cv2.rotate(roi, cv2.ROTATE_90_CLOCKWISE)

                    roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                    hi,wi = roi.shape[:2]
                    mask = np.zeros((hi,wi))
                    mask[roi_gray<1] = 255
                    mask[roi_gray>0] = 0
                    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
                    mask = cv2.dilate(mask, kernel)
                    mask = cv2.inRange(mask,100, 255)
                    pick = cv2.inpaint(roi,mask,10,cv2.INPAINT_NS)
                    box = cv2.boxPoints(mx_rect)
                    box = np.int0(box)
                    # *1 ここで書き込む
                    # fname = "./image_data/dashboard/test2.jpg"
                    # cv2.imwrite(fname,pick)#ppick
                    inside = inside + 1
                    p = Proc(pick,ip2).start()
             
                else:
                    inout = 0 #外


        cv2.rectangle(frame,frame_s,frame_e,(0,255,0),2)
        img_pre = copy.deepcopy(gray)
        current_time = time.time()
# 並列処理、送信などのチェックイに使用する<
        # if(ab>150):
        #     # fname = "./image_data/dashboard/test1.jpg"
        #     # cv2.imwrite(fname,frame)
        #     inside = inside + 1
        #     p = Proc(frame,ip2).start()# # # # # #
        #     ab = 0
        # ab += 1

        # if cv2.waitKey(10) == 27:
        #     break
# ここまで>

        #　送信できるサイズにリサイズ
        frame = cv2.resize(frame, (640,480))

        # フレームをJPEG形式にエンコード
        _, img_encode = cv2.imencode('.jpeg', frame)

        # 画像を分割する　
        for i in np.array_split(img_encode, 26):
            # 画像の送信
            udp.sendto(i.tostring(), to_send_addr)
        udp.sendto(b'__end__', to_send_addr)
        message = "main"
        message_byte = message.encode()
        udp.sendto(message_byte,to_send_addr)

    # リソースを解放
    cap.release()
    udp.close()



if __name__ == '__main__':
    mp.freeze_support() #　multi processを使う際に、必要なコード
    main()
