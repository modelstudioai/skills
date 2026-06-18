# Paraformer实时语音识别Python SDK

本文介绍Paraformer实时语音识别Python SDK的参数和接口细节。

**用户指南：**关于模型介绍和选型建议请参见[实时语音识别-Fun-ASR/Gummy/Paraformer](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition)。

**在线体验**：仅paraformer-realtime-v2、paraformer-realtime-8k-v2和paraformer-realtime-v1支持[在线体验](https://bailian.console.aliyun.com/?tab=model#/efm/model_experience_center/voice)。

## **前提条件**

-   已开通服务并[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。请[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)，而非硬编码在代码中，防范因代码泄露导致的安全风险。
    
    **说明**
    
    当您需要为第三方应用或用户提供临时访问权限，或者希望严格控制敏感数据访问、删除等高风险操作时，建议使用[临时鉴权Token](https://help.aliyun.com/zh/model-studio/generate-temporary-api-key)。
    
    与长期有效的 API Key 相比，临时鉴权 Token 具备时效性短（60秒）、安全性高的特点，适用于临时调用场景，能有效降低API Key泄露的风险。
    
    使用方式：在代码中，将原本用于鉴权的 API Key 替换为获取到的临时鉴权 Token 即可。
    
-   [安装最新版DashScope SDK](https://help.aliyun.com/zh/model-studio/install-sdk)。
    

## **模型列表**

**paraformer-realtime-v2（推荐）**

**paraformer-realtime-8k-v2（推荐）**

**paraformer-realtime-v1**

**paraformer-realtime-8k-v1**

**适用场景**

直播、会议等场景

电话客服、语音信箱等 8kHz 音频的识别场景

直播、会议等场景

电话客服、语音信箱等 8kHz 音频的识别场景

**采样率**

任意

8kHz

16kHz

8kHz

**语种**

中文（包含中文普通话和各种方言）、英文、日语、韩语、德语、法语、俄语

支持的中文方言：上海话、吴语、闽南语、东北话、甘肃话、贵州话、河南话、湖北话、湖南话、江西话、宁夏话、山西话、陕西话、山东话、四川话、天津话、云南话、粤语

中文

中文

中文

**标点符号预测**

✅ 默认支持，无需配置

✅ 默认支持，无需配置

✅ 默认支持，无需配置

✅ 默认支持，无需配置

**逆文本正则化（ITN）**

✅ 默认支持，无需配置

✅ 默认支持，无需配置

✅ 默认支持，无需配置

✅ 默认支持，无需配置

**定制热词**

✅ 参见[定制热词](https://help.aliyun.com/zh/model-studio/custom-hot-words/)

✅ 参见[定制热词](https://help.aliyun.com/zh/model-studio/custom-hot-words/)

✅ 参见[Paraformer语音识别热词定制与管理](https://help.aliyun.com/zh/model-studio/paraformer-asr-phrase-manager)

✅ 参见[Paraformer语音识别热词定制与管理](https://help.aliyun.com/zh/model-studio/paraformer-asr-phrase-manager)

**指定待识别语种**

✅ 通过`language_hints`参数指定

❌

❌

❌

**情感识别**

❌

✅ （点击查看使用方式）

情感识别遵循如下约束：

-   仅限`paraformer-realtime-8k-v2`模型。
    
-   必须关闭语义断句（可通过[请求参数](#555007db2033f)`semantic_punctuation_enabled`控制）。语义断句默认为关闭状态。
    
-   只有在[识别结果（RecognitionResult）](#bc3e1a43d6hhy)的`is_sentence_end`方法返回结果为`True`时才显示情感识别结果。
    

情感识别结果获取方式：通过[单句信息（Sentence）](#f28f50b035qtn)的`emo_tag`和`emo_confidence`字段分别获取当前句子的情感和情感置信度。

❌

❌

## **快速开始**

[Recognition类](#d6bc1f133f871)提供了非流式调用和双向流式调用接口。请根据实际需求选择合适的调用方式：

-   非流式调用：针对本地文件进行识别，并一次性返回完整的处理结果。适合处理录制好的音频。
    
-   双向流式调用：可直接对音频流进行识别，并实时输出结果。音频流可以来自外部设备（如麦克风）或从本地文件读取。适合需要即时反馈的场景。
    

### **非流式调用**

提交单个语音实时转写任务，通过传入本地文件的方式同步阻塞地拿到转写结果。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7413285771/CAEQURiBgMDS0c2RpxkiIDNmYjBlMTE3ODQxYTQ3Nzk4MGMxNTc5MjY3OWVjZjlj4709861_20241015153444.149.svg)

实例化[Recognition类](#d6bc1f133f871)绑定[请求参数](#555007db2033f)，调用`call`进行识别/翻译并最终获取[识别结果（RecognitionResult）](#bc3e1a43d6hhy)。

点击查看完整示例

示例中用到的音频为：[asr\_example.wav](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250210/iwaouc/asr_example.wav)。

```
from http import HTTPStatus
from dashscope.audio.asr import Recognition

# 若没有将API Key配置到环境变量中，需将下面这行代码注释放开，并将apiKey替换为自己的API Key
# import dashscope
# dashscope.api_key = "apiKey"

recognition = Recognition(model='paraformer-realtime-v2',
                          format='wav',
                          sample_rate=16000,
                          # “language_hints”只支持paraformer-realtime-v2模型
                          language_hints=['zh', 'en'],
                          callback=None)
result = recognition.call('asr_example.wav')
if result.status_code == HTTPStatus.OK:
    print('识别结果：')
    print(result.get_sentence())
else:
    print('Error: ', result.message)
    
print(
    '[Metric] requestId: {}, first package delay ms: {}, last package delay ms: {}'
    .format(
        recognition.get_last_request_id(),
        recognition.get_first_package_delay(),
        recognition.get_last_package_delay(),
    ))
```

### **双向流式调用**

提交单个语音实时转写任务，通过实现回调接口的方式流式输出实时识别结果。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7413285771/CAEQURiBgIDvi..2pxkiIGE4NTc3Njg4ZGM2YzQ2NzVhZGI3MzE2YWUwYTA3OGEy4709861_20241015153444.149.svg)

1.  启动流式语音识别
    
    实例化[Recognition类](#d6bc1f133f871)绑定[请求参数](#555007db2033f)和[回调接口（RecognitionCallback）](#85d698b9f9g8s)，调用`start`方法启动流式语音识别。
    
2.  流式传输
    
    循环调用[Recognition类](#d6bc1f133f871)的`send_audio_frame`方法，将从本地文件或设备（如麦克风）读取的二进制音频流分段发送至服务端。
    
    在发送音频数据的过程中，服务端会通过[回调接口（RecognitionCallback）](#85d698b9f9g8s)的`on_event`方法，将识别结果实时返回给客户端。
    
    建议每次发送的音频时长约为100毫秒，数据大小保持在1KB至16KB之间。
    
3.  结束处理
    
    调用[Recognition类](#d6bc1f133f871)的`stop`方法结束语音识别。
    
    该方法会阻塞当前线程，直到[回调接口（RecognitionCallback）](#85d698b9f9g8s)的`on_complete`或者`on_error`回调触发后才会释放线程阻塞。
    

点击查看完整示例

## 识别传入麦克风的语音

```
import os
import signal  # for keyboard events handling (press "Ctrl+C" to terminate recording)
import sys

import dashscope
import pyaudio
from dashscope.audio.asr import *

mic = None
stream = None

# Set recording parameters
sample_rate = 16000  # sampling rate (Hz)
channels = 1  # mono channel
dtype = 'int16'  # data type
format_pcm = 'pcm'  # the format of the audio data
block_size = 3200  # number of frames per buffer

def init_dashscope_api_key():
    """
        Set your DashScope API-key. More information:
        https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/PREREQUISITES.md
    """

    if 'DASHSCOPE_API_KEY' in os.environ:
        dashscope.api_key = os.environ[
            'DASHSCOPE_API_KEY']  # load API-key from environment variable DASHSCOPE_API_KEY
    else:
        dashscope.api_key = '<your-dashscope-api-key>'  # set API-key manually

# Real-time speech recognition callback
class Callback(RecognitionCallback):
    def on_open(self) -> None:
        global mic
        global stream
        print('RecognitionCallback open.')
        mic = pyaudio.PyAudio()
        stream = mic.open(format=pyaudio.paInt16,
                          channels=1,
                          rate=16000,
                          input=True)

    def on_close(self) -> None:
        global mic
        global stream
        print('RecognitionCallback close.')
        stream.stop_stream()
        stream.close()
        mic.terminate()
        stream = None
        mic = None

    def on_complete(self) -> None:
        print('RecognitionCallback completed.')  # recognition completed

    def on_error(self, message) -> None:
        print('RecognitionCallback task_id: ', message.request_id)
        print('RecognitionCallback error: ', message.message)
        # Stop and close the audio stream if it is running
        if 'stream' in globals() and stream.active:
            stream.stop()
            stream.close()
        # Forcefully exit the program
        sys.exit(1)

    def on_event(self, result: RecognitionResult) -> None:
        sentence = result.get_sentence()
        if 'text' in sentence:
            print('RecognitionCallback text: ', sentence['text'])
            if RecognitionResult.is_sentence_end(sentence):
                print(
                    'RecognitionCallback sentence end, request_id:%s, usage:%s'
                    % (result.get_request_id(), result.get_usage(sentence)))

def signal_handler(sig, frame):
    print('Ctrl+C pressed, stop recognition ...')
    # Stop recognition
    recognition.stop()
    print('Recognition stopped.')
    print(
        '[Metric] requestId: {}, first package delay ms: {}, last package delay ms: {}'
        .format(
            recognition.get_last_request_id(),
            recognition.get_first_package_delay(),
            recognition.get_last_package_delay(),
        ))
    # Forcefully exit the program
    sys.exit(0)

# main function
if __name__ == '__main__':
    init_dashscope_api_key()
    print('Initializing ...')

    # Create the recognition callback
    callback = Callback()

    # Call recognition service by async mode, you can customize the recognition parameters, like model, format,
    # sample_rate
    recognition = Recognition(
        model='paraformer-realtime-v2',
        format=format_pcm,
        # 'pcm'、'wav'、'opus'、'speex'、'aac'、'amr', you can check the supported formats in the document
        sample_rate=sample_rate,
        # support 8000, 16000
        semantic_punctuation_enabled=False,
        callback=callback)

    # Start recognition
    recognition.start()

    signal.signal(signal.SIGINT, signal_handler)
    print("Press 'Ctrl+C' to stop recording and recognition...")
    # Create a keyboard listener until "Ctrl+C" is pressed

    while True:
        if stream:
            data = stream.read(3200, exception_on_overflow=False)
            recognition.send_audio_frame(data)
        else:
            break

    recognition.stop()
```

## 识别本地语音文件

示例中用到的音频为：[asr\_example.wav](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250210/acoict/asr_example.wav)。

```
import os
import time
from dashscope.audio.asr import *

# 若没有将API Key配置到环境变量中，需将下面这行代码注释放开，并将apiKey替换为自己的API Key
# import dashscope
# dashscope.api_key = "apiKey"

from datetime import datetime

def get_timestamp():
    now = datetime.now()
    formatted_timestamp = now.strftime("[%Y-%m-%d %H:%M:%S.%f]")
    return formatted_timestamp

class Callback(RecognitionCallback):
    def on_complete(self) -> None:
        print(get_timestamp() + ' Recognition completed')  # recognition complete

    def on_error(self, result: RecognitionResult) -> None:
        print('Recognition task_id: ', result.request_id)
        print('Recognition error: ', result.message)
        exit(0)

    def on_event(self, result: RecognitionResult) -> None:
        sentence = result.get_sentence()
        if 'text' in sentence:
            print(get_timestamp() + ' RecognitionCallback text: ', sentence['text'])
            if RecognitionResult.is_sentence_end(sentence):
                print(get_timestamp() + 
                    'RecognitionCallback sentence end, request_id:%s, usage:%s'
                    % (result.get_request_id(), result.get_usage(sentence)))

callback = Callback()

recognition = Recognition(model='paraformer-realtime-v2',
                          format='wav',
                          sample_rate=16000,
                          # “language_hints”只支持paraformer-realtime-v2模型
                          language_hints=['zh', 'en'],
                          callback=callback)

recognition.start()

try:
    audio_data: bytes = None
    f = open("asr_example.wav", 'rb')
    if os.path.getsize("asr_example.wav"):
        while True:
            audio_data = f.read(3200)
            if not audio_data:
                break
            else:
                recognition.send_audio_frame(audio_data)
            time.sleep(0.1)
    else:
        raise Exception(
            'The supplied file was empty (zero bytes long)')
    f.close()
except Exception as e:
    raise e

recognition.stop()

print(
    '[Metric] requestId: {}, first package delay ms: {}, last package delay ms: {}'
    .format(
        recognition.get_last_request_id(),
        recognition.get_first_package_delay(),
        recognition.get_last_package_delay(),
    ))
```

### **并发调用**

在Python中，由于存在[全局解释器锁](https://docs.python.org/zh-cn/3/glossary.html#term-global-interpreter-lock)，同一时刻只有一个线程可以执行Python代码（虽然某些性能导向的库可能会去除此限制）。如果您想更好地利用多核心计算机的计算资源，推荐您使用[multiprocessing](https://docs.python.org/zh-cn/3.11/library/multiprocessing.html#module-multiprocessing)或[concurrent.futures.ProcessPoolExecutor](https://docs.python.org/zh-cn/3.11/library/concurrent.futures.html#concurrent.futures.ProcessPoolExecutor)。 多线程在较高并发下会显著增加SDK调用延迟。

## **请求参数**

请求参数通过[Recognition类](#d6bc1f133f871)的构造方法（\_init\_）进行设置。

**参数**

**类型**

**默认值**

**是否必须**

**说明**

model

str

\-

是

用于实时语音识别的模型（参见[模型列表](#1e173d999c1th)）。

sample\_rate

int

\-

是

设置待识别音频采样率（单位Hz）。

因模型而异：

-   paraformer-realtime-v2支持任意采样率。
    
-   paraformer-realtime-v1仅支持16000Hz采样。
    
-   paraformer-realtime-8k-v2仅支持8000Hz采样率。
    
-   paraformer-realtime-8k-v1仅支持8000Hz采样率。
    

format

str

\-

是

设置待识别音频格式。

支持的音频格式：pcm、wav、mp3、opus、speex、aac、amr。

**重要**

opus/speex：必须使用Ogg封装；

wav：必须为PCM编码；

amr：仅支持AMR-NB类型。

vocabulary\_id

str

\-

否

设置热词ID，若未设置则不生效。v2及更高版本模型设置热词ID时使用该字段。

在本次语音识别中，将应用与该热词ID对应的热词信息。具体使用方法请参见[定制热词](https://help.aliyun.com/zh/model-studio/custom-hot-words/)。

phrase\_id

str

\-

否

设置热词ID，若未设置则不生效。v1系列模型设置热词ID时使用该字段。

在本次语音识别中，将应用与该热词ID对应的热词信息。具体使用方法请参见[Paraformer语音识别热词定制与管理](https://help.aliyun.com/zh/model-studio/paraformer-asr-phrase-manager)。

disfluency\_removal\_enabled

bool

False

否

设置是否过滤语气词：

-   true：过滤语气词
    
-   false（默认）：不过滤语气词
    

language\_hints

list\[str\]

\["zh", "en"\]

否

设置待识别语言代码。如果无法提前确定语种，可不设置，模型会自动识别语种。

目前支持的语言代码：

-   zh: 中文
    
-   en: 英文
    
-   ja: 日语
    
-   yue: 粤语
    
-   ko: 韩语
    
-   de：德语
    
-   fr：法语
    
-   ru：俄语
    

该参数仅对支持多语言的模型生效（参见[模型列表](#1e173d999c1th)）。

semantic\_punctuation\_enabled

bool

False

否

设置是否开启语义断句，默认关闭。

-   true：开启语义断句，关闭VAD（Voice Activity Detection，语音活动检测）断句。
    
-   false（默认）：开启VAD（Voice Activity Detection，语音活动检测）断句，关闭语义断句。
    

语义断句准确性更高，适合会议转写场景；VAD（Voice Activity Detection，语音活动检测）断句延迟较低，适合交互场景。

通过调整`semantic_punctuation_enabled`参数，可以灵活切换语音识别的断句方式以适应不同场景需求。

该参数仅在模型为v2及更高版本时生效。

max\_sentence\_silence

int

800

否

设置VAD（Voice Activity Detection，语音活动检测）断句的静音时长阈值（单位为ms）。

当一段语音后的静音时长超过该阈值时，系统会判定该句子已结束。

参数范围为200ms至6000ms，默认值为800ms。

该参数仅在`semantic_punctuation_enabled`参数为false（VAD断句）且模型为v2及更高版本时生效。

multi\_threshold\_mode\_enabled

bool

False

否

该开关打开时（true）可以防止VAD断句切割过长。默认关闭。

该参数仅在`semantic_punctuation_enabled`参数为false（VAD断句）且模型为v2及更高版本时生效。

punctuation\_prediction\_enabled

bool

True

否

设置是否在识别结果中自动添加标点：

-   true（默认）：是
    
-   false：否
    

该参数仅在模型为v2及更高版本时生效。

heartbeat

bool

False

否

当需要与服务端保持长连接时，可通过该开关进行控制：

-   true：在持续发送静音音频的情况下，可保持与服务端的连接不中断。
    
-   false（默认）：即使持续发送静音音频，连接也将在60秒后因超时而断开。
    
    静音音频指的是在音频文件或数据流中没有声音信号的内容。静音音频可以通过多种方法生成，例如使用音频编辑软件如Audacity或Adobe Audition，或者通过命令行工具如FFmpeg。
    

该参数仅在模型为v2及更高版本时生效。

使用该字段时，SDK版本不能低于1.23.1。

inverse\_text\_normalization\_enabled

bool

True

否

设置是否开启ITN（Inverse Text Normalization，逆文本正则化）。

默认开启（true）。开启后，中文数字将转换为阿拉伯数字。

该参数仅在模型为v2及更高版本时生效。

callback

RecognitionCallback

\-

否

[回调接口（RecognitionCallback）](#85d698b9f9g8s)。

## **关键接口**

### `Recognition`类

`Recognition`通过“`from dashscope.audio.asr import *`”方式引入。

**成员方法**

**方法签名**

**说明**

call

```
def call(self, file: str, phrase_id: str = None, **kwargs) -> RecognitionResult
```

基于本地文件的非流式调用，该方法会阻塞当前线程直到全部音频读完，该方法要求所识别文件具有可读权限。

识别结果以`RecognitionResult`类型数据返回。

start

```
def start(self, phrase_id: str = None, **kwargs)
```

开始语音识别。

基于回调形式的流式实时识别，该方法不会阻塞当前线程。需要配合`send_audio_frame`和`stop`使用。

send\_audio\_frame

```
def send_audio_frame(self, buffer: bytes)
```

推送音频。每次推送的音频流不宜过大或过小，建议每包音频时长为100ms左右，大小在1KB~16KB之间。

识别结果通过[回调接口（RecognitionCallback）](#85d698b9f9g8s)的on\_event方法获取。

stop

```
def stop(self)
```

停止语音识别，阻塞到服务将收到的音频都识别后结束任务。

get\_last\_request\_id

```
def get_last_request_id(self)
```

获取request\_id，在构造函数调用（创建对象）后可以使用。

get\_first\_package\_delay

```
def get_first_package_delay(self)
```

获取首包延迟，从发送第一包音频到收到首包识别结果延迟，在任务完成后使用。

get\_last\_package\_delay

```
def get_last_package_delay(self)
```

获得尾包延迟，发送`stop`指令到最后一包识别结果下发耗时，在任务完成后使用。

### **回调接口（**`RecognitionCallback`）

[双向流式调用](#9d1e5f6852jr8)时，服务端会通过回调的方式，将关键流程信息和数据返回给客户端。您需要实现回调方法，处理服务端返回的信息或者数据。

点击查看示例

```
class Callback(RecognitionCallback):
    def on_open(self) -> None:
        print('连接成功')

    def on_event(self, result: RecognitionResult) -> None:
        # 实现接收识别结果的逻辑

    def on_complete(self) -> None:
        print('任务完成')

    def on_error(self, result: RecognitionResult) -> None:
        print('出现异常：', result)

    def on_close(self) -> None:
        print('连接关闭')

callback = Callback()
```

**方法**

**参数**

**返回值**

**描述**

```
def on_open(self) -> None
```

无

无

当和服务端建立连接完成后，该方法立刻被回调。

```
def on_event(self, result: RecognitionResult) -> None
```

`result`：[识别结果（RecognitionResult）](#bc3e1a43d6hhy)

无

当服务有回复时会被回调。

```
def on_complete(self) -> None
```

无

无

当所有识别结果全部返回后进行回调。

```
def on_error(self, result: RecognitionResult) -> None
```

`result`：[识别结果（RecognitionResult）](#bc3e1a43d6hhy)

无

发生异常时该方法被回调。

```
def on_close(self) -> None
```

无

无

当服务已经关闭连接后进行回调。

## **响应结果**

### **识别结果（**`**RecognitionResult**`**）**

`RecognitionResult`代表[双向流式调用](#9d1e5f6852jr8)中一次实时识别或[非流式调用](#8341058094tc3)的识别结果。

**成员方法**

**方法签名**

**说明**

get\_sentence

```
def get_sentence(self) -> Union[Dict[str, Any], List[Any]]
```

获取当前识别的句子及时间戳信息。回调中返回的是单句信息，所以此方法返回类型为Dict\[str, Any\]。

详情请参见[单句信息（Sentence）](#f28f50b035qtn)。

get\_request\_id

```
def get_request_id(self) -> str
```

获取请求的request\_id。

is\_sentence\_end

```
@staticmethod
def is_sentence_end(sentence: Dict[str, Any]) -> bool
```

判断给定句子是否已经结束。

### 单句信息（`Sentence`）

Sentence类成员如下：

**参数**

**类型**

**说明**

begin\_time

int

句子开始时间，单位为ms。

end\_time

int

句子结束时间，单位为ms。

text

str

识别文本。

words

[字时间戳信息（Word）](#b55a7391caxxe)的list集合

字时间戳信息。

emo\_tag

str

当前句子的情感：

-   positive：正面情感，如开心、满意
    
-   negative：负面情感，如愤怒、沉闷
    
-   neutral：无明显情感
    

情感识别遵循如下约束：

-   仅限`paraformer-realtime-8k-v2`模型。
    
-   必须关闭语义断句（可通过[请求参数](#555007db2033f)`semantic_punctuation_enabled`控制）。语义断句默认为关闭状态。
    
-   只有在[识别结果（RecognitionResult）](#bc3e1a43d6hhy)的`is_sentence_end`方法返回结果为`True`时才显示情感识别结果。
    

emo\_confidence

float

当前句子识别情感的置信度，取值范围：\[0.0,1.0\]。值越大表示置信度越高。

情感识别遵循如下约束：

-   仅限`paraformer-realtime-8k-v2`模型。
    
-   必须关闭语义断句（可通过[请求参数](#555007db2033f)`semantic_punctuation_enabled`控制）。语义断句默认为关闭状态。
    
-   只有在[识别结果（RecognitionResult）](#bc3e1a43d6hhy)的`is_sentence_end`方法返回结果为`True`时才显示情感识别结果。
    

### **字时间戳信息（**`**Word**`**）**

Word类成员如下：

**参数**

**类型**

**说明**

begin\_time

int

字开始时间，单位为ms。

end\_time

int

字结束时间，单位为ms。

text

str

字。

punctuation

str

标点。

## **错误码**

如遇报错问题，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行排查。

若问题仍未解决，请加入[开发者群](https://github.com/aliyun/alibabacloud-bailian-speech-demo)反馈遇到的问题，并提供Request ID，以便进一步排查问题。

## **更多示例**

更多示例，请参见[GitHub](https://github.com/aliyun/alibabacloud-bailian-speech-demo)。

## **常见问题**

### **功能特性**

#### **Q：在长时间静默的情况下，如何保持与服务端长连接？**

将请求参数`heartbeat`设置为true，并持续向服务端发送静音音频。

静音音频指的是在音频文件或数据流中没有声音信号的内容。静音音频可以通过多种方法生成，例如使用音频编辑软件如Audacity或Adobe Audition，或者通过命令行工具如FFmpeg。

#### **Q：如何将音频格式转换为满足要求的格式？**

可使用[FFmpeg工具](https://ffmpeg.en.lo4d.com/download)，更多用法请参见FFmpeg官网。

```
# 基础转换命令（万能模板）
# -i，作用：输入文件路径，常用值示例：audio.wav
# -c:a，作用：音频编码器，常用值示例：aac, libmp3lame, pcm_s16le
# -b:a，作用：比特率（音质控制），常用值示例：192k, 320k
# -ar，作用：采样率，常用值示例：44100 (CD), 48000, 16000
# -ac，作用：声道数，常用值示例：1(单声道), 2(立体声)
# -y，作用：覆盖已存在文件(无需值)
ffmpeg -i input_audio.ext -c:a 编码器名 -b:a 比特率 -ar 采样率 -ac 声道数 output.ext

# 例如：WAV → MP3（保持原始质量）
ffmpeg -i input.wav -c:a libmp3lame -q:a 0 output.mp3
# 例如：MP3 → WAV（16bit PCM标准格式）
ffmpeg -i input.mp3 -c:a pcm_s16le -ar 44100 -ac 2 output.wav
# 例如：M4A → AAC（提取/转换苹果音频）
ffmpeg -i input.m4a -c:a copy output.aac  # 直接提取不重编码
ffmpeg -i input.m4a -c:a aac -b:a 256k output.aac  # 重编码提高质量
# 例如：FLAC无损 → Opus（高压缩）
ffmpeg -i input.flac -c:a libopus -b:a 128k -vbr on output.opus
```

##### **Q：**是否支持查看每句话对应的时间范围？

支持。语音识别结果中会包含每句话的开始时间戳和结束时间戳，可通过它们确定每句话的时间范围。

#### **Q：如何识别本地文件（录音文件）？**

识别本地文件有两种方式：

-   直接传入本地文件路径：此种方式在最终识别结束后获取完整识别结果，不适合即时反馈的场景。
    
    参见[非流式调用](#8341058094tc3)，在[Recognition类](#d6bc1f133f871)的`call`方法中传入文件路径对录音文件直接进行识别。
    
-   将本地文件转成二进制流进行识别：此种方式一边识别文件一边流式获取识别结果，适合即时反馈的场景。
    
    参见[双向流式调用](#9d1e5f6852jr8)，通过[Recognition类](#d6bc1f133f871)的`send_audio_frame`方法向服务端发送二进制流对其进行识别。
    

### **故障排查**

#### **Q：无法识别语音（无识别结果）是什么原因？**

1.  请检查请求参数中的音频格式（`format`）和采样率（`sampleRate`/`sample_rate`）设置是否正确且符合参数约束。以下为常见错误示例：
    
    -   音频文件扩展名为 .wav，但实际为 MP3 格式，而请求参数 `format` 设置为 mp3（参数设置错误）。
        
    -   音频采样率为 3600Hz，但请求参数 `sampleRate`/`sample_rate` 设置为 48000（参数设置错误）。
        
    
    可以使用[ffprobe](https://ffmpeg.org/ffprobe.html)工具获取音频的容器、编码、采样率、声道等信息：
    
    ```
    ffprobe -v error -show_entries format=format_name -show_entries stream=codec_name,sample_rate,channels -of default=noprint_wrappers=1 input.xxx
    ```
    
2.  使用`paraformer-realtime-v2`模型时，请检查`language_hints`设置的语言是否与音频实际语言一致。
    
    例如：音频实际为中文，但`language_hints`设置为`en`（英文）。
    
3.  若以上检查均无问题，可通过定制热词提升对特定词语的识别效果。
