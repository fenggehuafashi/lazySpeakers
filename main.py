import pyaudio
import wave
import os
from threading import Timer



# import sys
# 定义数据流块
CHUNK = 1024

# if len(sys.argv) < 2:
#     # print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
#     sys.exit(-1)

# 只读方式打开wav文件
wav_path = os.getcwd() + '\\slient.wav'

# 输入判断,自定义输入时间间隔.
while True:
    play_interval = input("请输入播放间隔时间(min), 默认15min:")
    # 默认时间间隔
    if play_interval=='':
        play_interval = 15 * 60
        break

    if  play_interval.isdigit()==False:
        print("必须输入数字,范围为0-1440!!!")
        continue

    play_interval= int((float(play_interval)))

    if play_interval>0 and play_interval<=1440:
        play_interval*=60
        break
    else:
        print("必须输入数字,范围为0-1440!!!")

# play_interval = 15 * 60

# 使用pyaudio播放音频文件
def waker():
    print("播放 slient.wav")
    wf = wave.open(wav_path, 'rb')
    p = pyaudio.PyAudio()

    # 打开数据流
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # 读取数据
    data = wf.readframes(CHUNK)

    # 播放
    while data != b'':
        stream.write(data)
        data = wf.readframes(CHUNK)

    # 停止数据流
    stream.stop_stream()
    stream.close()

    # 关闭 PyAudio
    p.terminate()


class RepeatingTimer(Timer):
    def run(self):
        while not self.finished.is_set():
            self.function(*self.args, **self.kwargs)
            self.finished.wait(self.interval)

t = RepeatingTimer(play_interval, waker)
t.start()

# 关闭 timer
input()
t.cancel()



