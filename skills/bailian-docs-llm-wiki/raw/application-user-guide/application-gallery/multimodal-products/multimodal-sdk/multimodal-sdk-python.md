# 服务端Python SDK

本文介绍了如何使用阿里云百炼大模型服务提供的实时多模交互服务端 Python SDK，包括SDK下载安装、关键接口及代码示例。

## **多模态实时交互服务架构**

![多模态实时交互服务接入架构-通用-流程图](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7227370571/p976841.jpg)

## **前提条件**

开通服务并获取必要参数。

开通阿里云百炼实时多模交互应用，获取[Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)、[APP ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#2612f896detsz)和[API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。

## **音频格式说明**

服务端接入方式只支持 websocket 传输协议。

-   WS 链路音频格式说明：
    
    -   上行：支持 pcm （16k 采样率 16bit 单通道）和 opus 音频流。
        
    -   下行：支持 pcm 和 mp3 音频流。
        

## **环境依赖**

**运行环境要求**：Python 3.9及以上版本。

**依赖安装方式**：

您可以通过pip 导入Dashscope依赖， 版本号>=1.24.2。

```
dashscope>=1.24.2
```

完整示例请参考：[Github示例代码](https://github.com/aliyun/alibabacloud-bailian-speech-demo/tree/master/samples/conversation/multimodal_dialog)。

## **接口说明**

### dashscope.multimodal.MultiModalDialog

服务入口

**方法说明：**

#### **1**、MultiModalDialog

创建交互，设置回调。

```
"""
创建一个语音对话会话。

此方法用于初始化一个新的会话，设置必要的参数以准备开始与模型的交互。
:param workspace_id: 客户的workspace_id
:param app_id: 客户在管控台创建的应用id，可以根据值规律确定使用哪个对话系统
:param request_params: 请求参数集合
:param url: (str) API的URL地址。
:param multimodal_callback: (MultimodalCallback) 回调对象，用于处理来自服务器的消息。
:param api_key: (str) 应用程序接入的唯一key
:param dialog_id:对话id，如果传入表示承接上下文继续聊
:param model: 模型
"""
def __init__(self,
                 workspace_id: str,
                 app_id: str,
                 request_params: RequestParameters,
                 multimodal_callback: MultiModalCallback,
                 url: str = None,
                 api_key: str = None,
                 dialog_id: str = None,
                 model: str = None
                 ):
```

#### **2**、**start**

启动voice\_chat对话服务，返回on\_started回调。注意on\_started会回调dialog\_id。

```
"""
初始化WebSocket连接并发送启动请求       
:param dialog_id: 对话ID，用于标识特定的对话会话
"""
def start(self, dialog_id):
```

#### **3**、**start\_speech**

通知服务端开始上传音频，注意需要在LISTENING状态才可以调用。

```
"""
开始上传语音数据
"""
def start_speech(self):
```

#### **4**、**send\_audio\_data**

通知服务端上传音频。

```
"""
上传语音数据
:param speechData: bytes 语音数据
"""
def send_audio_data(self, speechData):
```

#### **5**、**stop\_speech**

通知服务端结束上传音频。

```
"""
结束上传语音数据
"""
def stop_speech(self):
```

#### **6**、**interrupt**

通知服务端，客户端需要打断当前交互，开始说话。

```
"""
结束交互，发送RequestToSpeak给服务端
"""
def interrupt(self):
```

#### **7**、**local\_responding\_started**

通知服务端，客户端开始播放tts音频。

```
"""
通知服务端客户端开始播放tts音频
"""
def local_responding_started(self):
```

#### **8**、**local\_responding\_ended**

通知服务端，客户端结束播放tts音频。

```
"""
通知服务端客户端播放tts音频结束
"""
def local_responding_ended(self):
```

#### **9**、**stop**

结束当前轮次voice\_chat对话。

```
"""
结束当前轮次voice_chat对话       
"""
def stop(self):
```

#### **10**、**get\_dialog\_state**

获得当前对话服务状态。DialogState枚举。

```
"""
:return dialog_id: dialog_state.DialogState
"""
get_dialog_state(self)
```

#### **11**、**request\_to\_respond**

请求服务端直接文本合成语音，或者发送指令给服务端。

```
def request_to_respond(self,
                       request_type: str,
                       text: str,
                       parameters: RequestToRespondParameters = None):
```

#### **12**、**class** MultiModalCallback。

回调函数

```
class MultiModalCallback:
    """
    语音聊天回调类，用于处理语音聊天过程中的各种事件。
    """

    def on_started(self, dialog_id: str) -> None:
        """
        通知对话开始

        :param dialog_id: 回调对话ID
        """
        pass

    def on_stopped(self) -> None:
        """
        通知对话停止
        """
        pass

    def on_state_changed(self, state: 'dialog_state.DialogState') -> None:
        """
        对话状态改变

        :param state: 新的对话状态
        """
        pass

    def on_speech_audio_data(self, data: bytes) -> None:
        """
        合成音频数据回调

        :param data: 音频数据
        """
        pass

    def on_error(self, error) -> None:
        """
        发生错误时调用此方法。

        :param error: 错误信息
        """
        pass

    def on_connected(self) -> None:
        """
        成功连接到服务器后调用此方法。
        """
        pass

    def on_responding_started(self):
        """
        回复开始回调
        """
        pass

    def on_responding_ended(self):
        """
        回复结束
        """
        pass

    def on_speech_content(self, payload):
        """
        语音识别文本

        :param payload: text
        """
        pass

    def on_responding_content(self, payload):
        """
        大模型回复文本。

        :param payload: text
        """
        pass

    def on_request_accepted(self):
        """
        打断请求被接受。
        """
        pass

    def on_close(self, close_status_code, close_msg):
        """
        连接关闭时调用此方法。

        :param close_status_code: 关闭状态码
        :param close_msg: 关闭消息
        """
        pass
```

### **对话状态说明（**DialogState**）**

多模对话服务有LISTENING、THINKING、RESPONDING三个状态：

-   LISTENING (str): 表示机器人正在监听用户输入。用户可以发送音频。
    
-   THINKING (str): 表示机器人正在思考。
    
-   RESPONDING (str): 表示机器人正在生成语音或语音回复中。
    

### **调用说明**

#### **参数设置**

多模交互通过RequestParameters 类设置参数，包含up\_stream、down\_stream、client\_info等多个参数段。具体如下表：

一级参数

二级参数

三级参数

四级参数

类型

是否必选

说明

task\_group

任务组名称，固定为"aigc"

task

任务名称，固定为"multimodal-generation"

function

调用功能，固定为"generation"

model

服务名称，固定为"multimodal-dialog"

input

workspace\_id

string

是

用户业务空间ID

app\_id

string

是

客户在管控台创建的应用ID，可以根据值规律确定使用哪个对话系统

sandbox

boolean

否

是否使用测试配置，默认false

directive

string

是

指令名称：Start

dialog\_id

string

否

对话ID，如果传入表示接着聊

parameters

upstream

type

string

是

上行类型：

-   AudioOnly：仅语音通话
    
-   AudioAndVideo：上传视频
    

mode

string

否

客户端使用的模式，可选项：

-   push2talk
    
-   tap2talk
    
-   duplex
    

默认tap2talk

audio\_format

string

否

音频格式，支持pcm，opus，默认为pcm

downstream

voice

string

否

合成语音的音色

sample\_rate

int

否

合成语音的采样率，默认采样率24000Hz

intermediate\_text

string

否

控制返回给用户那些中间文本：

-   transcript：返回用户语音识别结果
    
-   dialog：返回对话系统回答中间结果
    

可以设置多种，以逗号分割，默认为transcript

debug

boolean

否

是否下发debug信息，默认false

audio\_format

string

否

音频格式，支持pcm，mp3，默认为pcm

client\_info

user\_id

string

是

终端用户ID，用来做用户相关的处理

device

uuid

string

否

客户端全局唯一的ID，需要用户自己生成，传入SDK

network

ip

string

否

调用方公网IP

location

latitude

string

否

调用方维度信息

longitude

string

否

调用方经度信息

city\_name

string

否

调用方所在城市

biz\_params

user\_defined\_params

object

否

其他需要透传给agent的参数

user\_defined\_tokens

object

否

透传agent所需鉴权信息

tool\_prompts

object

否

透传agent所需prompt

user\_query\_params

object

否

透传用户请求自定义参数

user\_prompt\_params

object

否

透传用户prompt自定义参数

#### **调用示例**

```
up_stream = Upstream(type="AudioOnly", mode="push2talk", audio_format="pcm")
# down_stream = Downstream(voice="longxiaochun_v2", sample_rate=16000)

client_info = ClientInfo(user_id="aabb", device=Device(uuid="1234567890"))
request_params = RequestParameters(upstream=up_stream,downstream=Downstream(sample_rate=48000), client_info=client_info)
```

## **调用交互时序图**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5621377471/p957919.png)

### **更多SDK接口使用说明**

#### **VQA（图片问答）交互**

VQA 是对话过程中通过发送图片实现图片+语音的多模交互的功能。

核心过程是通过输入类似"看一下xxx"意图的语音，或者直接输入请求文本的方式触发VQA，返回基于图片内容的问答结果。

-   通过语音请求的流程为：
    
    1.  语音说："看一下前面有什么" 。
        
    2.  通过回调函数`on_responding_content`返回拍照意图**"visual\_qa"**。
        
    3.  客户端收到上述意图后，调用request\_to\_respond接口提交图片内容触发问答回复。
        
    
    ```
    # callback visual_qa 
    def on_responding_content(self, payload: Dict[str, Any]):
            if payload:
                logger.debug(f"Response content: {payload}")
                try:
                    commands_str = payload["output"]["extra_info"]["commands"]
                    if "visual_qa" in commands_str:
                        if self.vqa_handler_func:
                            self.vqa_handler_func() #send_image_vqa 
                        logger.debug("handle visual_qa command>>>>")
                except:
                    return
    ...
    
    # request VQA
    def send_image_vqa(self):
        image1 = {"type": "base64",
             "value": CONST_TEST_IMAGE_BASE64}
        # 或者使用下发url方式调用
        image2 = {"type": "url", "value": image_url}
    
        images = [image1]
        images_params = RequestToRespondParameters(images=images)
    
        # 使用语音调用VQA，text传""即可
        self.conversation.request_to_respond("prompt", "", parameters=images_params)
    ```
    
-   直接通过文本请求流程为：
    
    1.  客户端直接调用request\_to\_respond接口提交图片内容和请求文本，触发问答回复。
        
    
    ```
    image1 = {"type": "base64",
             "value": CONST_TEST_IMAGE_BASE64}
    # 或者使用下发url方式调用
    image2 = {"type": "url", "value": image_url}
    
    images = [image1]
    images_params = RequestToRespondParameters(images=images)
    
    # 使用文本直接请求图片回复，text填入文本请求
    self.conversation.request_to_respond("prompt", "这张图片里面有什么", parameters=images_params)
    ```
    

注意：VQA 支持发送图片链接或者base64数据（支持小于180KB的图片）。

### **通过Websocket请求LiveAI（视频通话）**

LiveAI （视频通话）是百炼多模交互提供的官方Agent。通过Python SDK发送图片序列的方式，可以实现视频通话的功能。 我们推荐您的服务端和客户端（网页或者APP）通过RTC传输视频和音频，然后将服务端采集到的视频帧以 500ms/张 的速度发送给SDK，同时保持实时的音频输入。

注意：LiveAI发送图片只支持base64编码，每张图片的大小在180K以下。

-   LiveAI调用时序
    

#### ![截屏2025-06-20 11](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1903140571/p975541.png)

-   关键代码示例
    

完整代码请参考 [Github示例代码](https://github.com/aliyun/alibabacloud-bailian-speech-demo/tree/master/samples/conversation/multimodal_dialog)。

```
# 1. 设置请求模式为AudioAndVideo
up_stream = Upstream(type="AudioAndVideo", mode="duplex", audio_format="pcm")
...

# 2. 发送连接到视频对话Agent请求
# {"action":"connect", "type":"voicechat_video_channel"}
def send_connect_video_command(self):
    """发送切换到视频模式的指令"""
    logger.info("Sending connect video command")
    try:
        video_connect_command = [{"action":"connect", "type":"voicechat_video_channel"}]

        self.conversation.request_to_respond("prompt","", RequestToRespondParameters(biz_params=BizParams(videos=video_connect_command)))
        # 标记视频模式已激活
        self.video_mode_active = True
        logger.info("Video mode activated")

    except Exception as e:
        logger.error(f"Failed to send connect video command: {e}")
 
 
 # 3. 间隔500ms 发送一张180KB以下的视频帧图片
 def send_video_frame_data_loop(self):
    """循环发送视频帧数据"""
    logger.info("Starting video frame data loop")
    self.video_thread_running = True

    # 获取示例图片数据
    image_data = self._get_sample_images()

    try:
        while self.video_thread_running and self.video_mode_active:
            # 发送图片数据
            self._send_video_frame(image_data) 
            logger.debug(f"Sent video frame, sleeping for {VIDEO_FRAME_INTERVAL}s")

            # 等待500ms
            time.sleep(VIDEO_FRAME_INTERVAL)
...
# 其他调用过程省略，可参考完整示例。
```

### **文本合成TTS**

SDK支持通过文本直接请求服务端合成音频。

您需要在客户端处于Listening状态下发送`request_to_respond`请求。

若当前状态非Listening，需要先调用`interrupt` 接口打断当前播报。

```
conversation.request_to_respond("transcript", "今天天气不错", parameters=None)
```

### **自定义提示词变量和传值**

-   在管控台项目【提示词】配置自定义变量。
    

如下图示例，定义了一个`user_name`字段代表用户昵称。并将变量`user_name`以占位符形式${user\_name} 插入到Prompt 中。

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1903140571/p975545.png)

-   在代码中设置变量。
    

如下示例，设置`"user_name" = "大米"`。

```
# 在请求参数构建中传入biz_params.user_prompt_params
biz_params = BizParams(user_prompt_params={"user_name": "大米"})
request_params = RequestParameters(upstream=up_stream, downstream=down_stream,
                                           client_info=client_info, biz_params=biz_params)
```

-   请求回复
    

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1903140571/p975544.png)

### **使用文本请求对话结果**

SDK支持通过文本直接请求服务端返回 LLM 结果和语音合成数据。

您需要在客户端处于Listening状态下发送`request_to_respond`请求。

```
conversation.request_to_respond("prompt", "今天天气不错", parameters=None)
```

### **更多使用示例**

请参考 [Github示例代码](https://github.com/aliyun/alibabacloud-bailian-speech-demo/tree/master/samples/conversation/multimodal_dialog)。
