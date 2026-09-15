# AOQ Client SDK Linux Python API 参考

本文介绍 AOQ Client SDK Linux 版的 Python 接口、回调和数据类型。

Linux 平台通过 Python 模块 `aoq_client_sdk` 提供 API。所有回调在 native 线程触发，使用者需自行保证线程安全。

## 接口目录

### 引擎生命周期

**接口**

**简介**

create\_engine

创建引擎实例（单例模式）

destroy

销毁引擎实例

get\_version

获取 SDK 版本号

connect

连接 Relay 服务器

disconnect

断开服务器连接

### 音频设备管理

**接口**

**简介**

start\_audio\_capture

启动音频采集（Linux 为空实现，不会打开麦克风）

stop\_audio\_capture

停止音频采集（Linux 无实际效果）

mute\_audio\_capture

静音或取消静音音频采集（Linux 无设备采集能力）

start\_audio\_player

启动音频播放（Linux 为空实现，不会打开扬声器）

stop\_audio\_player

停止音频播放（Linux 无实际效果）

pause\_audio\_player

暂停音频播放（Linux 无设备播放能力）

resume\_audio\_player

恢复音频播放（Linux 无设备播放能力）

interrupt\_audio\_player

打断本轮音频通话

### 音频编码配置

**接口**

**简介**

set\_audio\_encoder\_config

设置音频编码参数

set\_audio\_decoder\_config

设置音频解码参数

### 视频设备管理

**接口**

**简介**

start\_video\_capture

启动视频采集（Linux 仅支持外部采集模式）

stop\_video\_capture

停止视频采集（Linux 仅适用于外部采集模式）

set\_local\_view

设置或移除本地视频渲染窗口（Linux 无渲染实现）

set\_remote\_view

设置或移除远端视频渲染窗口（Linux 无渲染实现）

### 视频编解码与外部输入

**接口**

**简介**

set\_video\_encoder\_config

设置视频编码参数

set\_video\_decoder\_config

设置视频解码参数

push\_external\_video\_frame

推送外部采集视频帧

push\_external\_video\_encoded\_frame

推送外部已编码视频帧

### 媒体流发送控制

**接口**

**简介**

enable\_send\_media\_stream

控制本地媒体流的发送开关

### 音频文件播放

**接口**

**简介**

start\_audio\_file

开始推流播放本地音频文件

stop\_audio\_file

停止音频文件播放

pause\_audio\_file

暂停音频文件播放

resume\_audio\_file

恢复音频文件播放

get\_audio\_file\_duration

获取音频文件总时长

get\_audio\_file\_current\_position

获取音频文件当前播放位置

set\_audio\_file\_position\_millis

设置音频文件播放位置（seek）

set\_audio\_file\_volume

设置音频文件音量

get\_audio\_file\_volume

获取音频文件当前音量

### 外部音频流

**接口**

**简介**

add\_audio\_external\_stream

新增一条外部音频流

remove\_audio\_external\_stream

移除外部音频流

push\_audio\_external\_stream\_data

输入外部音频 PCM 数据

set\_audio\_external\_stream\_volume

设置外部音频流音量

get\_audio\_external\_stream\_volume

获取外部音频流音量

clear\_audio\_external\_stream\_buffer

清空外部音频流缓存

### 实时消息

**接口**

**简介**

send\_data\_msg

发送实时数据消息

### 音频帧回调

**接口**

**简介**

set\_audio\_frame\_observer

设置音频帧数据回调监听

enable\_audio\_frame\_observer

开启或关闭指定位置的音频帧回调

### 视频帧回调

**接口**

**简介**

set\_video\_frame\_observer

设置视频帧数据回调监听

enable\_video\_frame\_observer

开启或关闭指定位置的视频帧回调

### 回调接口

**回调**

**简介**

on\_error

引擎错误回调

on\_connection\_status\_change

连接状态变化回调

on\_data\_msg

收到实时数据消息回调

IAudioFrameObserver

音频帧数据监听基类

IVideoFrameObserver

视频帧数据监听基类

### 工具函数

**接口**

**简介**

load\_library

手动指定并加载 native 共享库

## 接口详情

### 引擎生命周期

#### create\_engine

创建引擎实例（类方法）。SDK 内部以全局单例方式持有引擎，重复调用返回已创建的实例；`destroy` 后需再次 `create_engine` 方可继续使用。

```
@classmethod
def create_engine(cls, config: AoqCreateConfig, listener: AoqEngineEventListener) -> "AoqClientEngine"
```

**参数**

**类型**

**说明**

config

AoqCreateConfig

引擎创建配置

listener

AoqEngineEventListener

引擎事件回调监听

返回值：AoqClientEngine 引擎实例；创建失败时抛出 RuntimeError。

#### destroy

销毁引擎实例（类方法），释放所有资源。

```
@classmethod
def destroy(cls) -> int
```

返回值：0 表示成功；非 0 表示失败。

#### get\_version

获取 SDK 当前版本号（静态方法）。

```
@staticmethod
def get_version() -> str
```

返回值：版本号字符串，如 "1.0.0"。

#### connect

连接 Relay 服务器。业务 AppServer 应根据所用协议获取临时 AOQ 连接参数并下发给客户端，具体操作请参见Token 鉴权。

```
def connect(self, config: AoqConnectConfig) -> int
```

**参数**

**类型**

**说明**

config

AoqConnectConfig

连接配置，包含 Token、SID、Relay 接入点列表等

返回值：0 表示调用已下发（异步执行）；非 0 表示参数校验失败。

#### disconnect

断开与服务器的连接，释放连接相关资源。

```
def disconnect(self) -> int
```

返回值：0 表示调用已下发（异步执行）；非 0 表示失败。

### 音频设备管理

#### start\_audio\_capture

```
def start_audio_capture(self, config: AoqAudioCaptureConfig) -> int
```

Linux 版中该方法为空实现：返回 0，但不会打开声卡或麦克风。音频输入请通过外部音频流接口提供。

#### stop\_audio\_capture

```
def stop_audio_capture(self) -> int
```

由于 Linux 版不会设置音频采集设备状态，该方法没有实际效果。

#### mute\_audio\_capture

```
def mute_audio_capture(self, mute: bool) -> int
```

Linux 版不支持麦克风采集，该方法不能控制实际音频采集设备。

#### start\_audio\_player

```
def start_audio_player(self, config: AoqAudioPlaybackConfig) -> int
```

Linux 版中该方法为空实现：返回 0，但不会打开声卡或扬声器。音频输出请通过音频帧回调获取数据并自行播放。

#### stop\_audio\_player / pause\_audio\_player / resume\_audio\_player

```
def stop_audio_player(self) -> int
def pause_audio_player(self, fade_ms: int = 0) -> int
def resume_audio_player(self, fade_ms: int = 0) -> int
```

Linux 版不支持扬声器播放，以上方法不能控制实际音频播放设备。fade\_ms：淡出或淡入时长（毫秒）；0 表示立即执行。

#### interrupt\_audio\_player

```
def interrupt_audio_player(self, track_type: int, fade_ms: int = 0) -> int
```

打断本轮音频通话。

### 音频编码配置

```
def set_audio_encoder_config(self, config: AoqAudioCodecConfig) -> int
def set_audio_decoder_config(self, config: AoqAudioCodecConfig) -> int
```

### 视频设备管理

```
def start_video_capture(self, config: AoqVideoCaptureConfig) -> int
def stop_video_capture(self) -> int
def set_local_view(self, track_type: int, canvas: Optional[AoqVideoCanvas]) -> int
def set_remote_view(self, track_type: int, canvas: Optional[AoqVideoCanvas]) -> int
```

Linux 版不支持摄像头采集，也没有视频渲染后端。调用 `start_video_capture` 时须将 `is_external` 设为 `True`，并通过 `push_external_video_frame` 提供视频帧；`set_local_view`、`set_remote_view` 及 `AoqVideoCanvas.view` 在 Linux 上无实际用途。如需预览，请通过视频帧回调获取数据并自行渲染。

### 视频编解码与外部输入

```
def set_video_encoder_config(self, config: AoqVideoCodecConfig) -> int
def set_video_decoder_config(self, config: AoqVideoCodecConfig) -> int
def push_external_video_frame(self, frame: AoqVideoFrame, track_type: AoqTrackType = AoqTrackType.VIDEO) -> int
def push_external_video_encoded_frame(self, track_type: AoqTrackType, frame: AoqVideoEncodedFrame) -> int
```

注意：

-   set\_video\_decoder\_config 仅 track\_type/codec\_type/width/height/fps/bitrate 字段生效。
-   push\_external\_video\_frame 仅在 start\_video\_capture(is\_external=True) 后消费；打包格式（NV12/NV21/BGRA/RGBA）填 `frame.data`，I420 三平面填 `frame.data_y/u/v` 与对应 stride；若缓冲区满返回 AoqErrorCode.VIDEO\_EXTERNAL\_BUFFER\_FULL(210)。
-   push\_external\_video\_encoded\_frame 要求 start\_video\_capture(is\_external=True) 且 set\_video\_encoder\_config(codec\_type=VIDEO\_JPEG)，直接走旁路通路不做二次编码。

### 媒体流发送控制

```
def enable_send_media_stream(self, track_type: AoqTrackType, enable: bool) -> int
```

建议初始化后根据业务需要，分别调用 enable\_send\_media\_stream(AoqTrackType.AUDIO, False) 和 enable\_send\_media\_stream(AoqTrackType.VIDEO, False) 关闭音频、视频轨道发送；待 on\_connection\_status\_change(CONNECTED) 后，再分别开启所需轨道。

### 音频文件播放

```
def start_audio_file(self, file_id: str, config: AoqAudioFileMixConfig) -> int
def stop_audio_file(self, file_id: str) -> int
def pause_audio_file(self, file_id: str) -> int
def resume_audio_file(self, file_id: str) -> int
def get_audio_file_duration(self, file_id: str) -> int
def get_audio_file_current_position(self, file_id: str) -> int
def set_audio_file_position_millis(self, file_id: str, position_ms: int) -> int
def set_audio_file_volume(self, file_id: str, type_: AoqAudioStreamDirection, volume: int) -> int
def get_audio_file_volume(self, file_id: str, type_: AoqAudioStreamDirection) -> int
```

### 外部音频流

```
def add_audio_external_stream(self, stream_id: str, config: AoqAudioExternalStreamConfig) -> int
def remove_audio_external_stream(self, stream_id: str) -> int
def push_audio_external_stream_data(self, stream_id: str, data: AoqAudioFrameData) -> int
def set_audio_external_stream_volume(self, stream_id: str, type_: AoqAudioStreamDirection, volume: int) -> int
def get_audio_external_stream_volume(self, stream_id: str, type_: AoqAudioStreamDirection) -> int
def clear_audio_external_stream_buffer(self, stream_id: str, fadeout_ms: int = -1) -> None
```

注意：push\_audio\_external\_stream\_data 缓冲区满时返回 AoqErrorCode.AUDIO\_EXTERNAL\_BUFFER\_FULL(110)，建议等待约 20ms 后重试同一帧。

### 实时消息

```
def send_data_msg(self, msg: AoqDataMsg) -> int
```

### 音频帧回调

```
def set_audio_frame_observer(self, observer: Optional[IAudioFrameObserver]) -> int
def enable_audio_frame_observer(self, enabled: bool, audio_source: AoqAudioSource, config: AoqAudioObserverConfig) -> int
```

set\_audio\_frame\_observer 传 None 表示注销观察者。

### 视频帧回调

```
def set_video_frame_observer(self, observer: Optional[IVideoFrameObserver]) -> int
def enable_video_frame_observer(self, enabled: bool, video_source: AoqVideoSource, config: AoqVideoObserverConfig) -> int
```

set\_video\_frame\_observer 传 None 表示注销观察者。

### 回调接口

#### AoqEngineEventListener

引擎事件回调基类。所有方法均为可选 override，默认空实现；回调在 native 线程触发，使用者需自行保证线程安全。

```
class AoqEngineEventListener:
    def on_error(self, code: int, message: str) -> None: ...
    def on_connection_status_change(self, status: AoqConnectionStatus) -> None: ...
    def on_data_msg(self, msg: AoqDataMsg) -> None: ...
```

#### on\_error

```
def on_error(self, code: int, message: str) -> None
```

引擎错误回调。code 对应 AoqErrorCode 枚举值。

#### on\_connection\_status\_change

```
def on_connection_status_change(self, status: AoqConnectionStatus) -> None
```

连接状态变化回调。状态流转：DISCONNECTED -> CONNECTING -> CONNECTED/FAILED -> DISCONNECTED。

#### on\_data\_msg

```
def on_data_msg(self, msg: AoqDataMsg) -> None
```

收到实时数据消息回调。

#### IAudioFrameObserver

音频帧数据监听基类。所有方法均为可选 override，默认空实现。

```
class IAudioFrameObserver:
    def on_captured_audio_frame(self, data: AoqAudioFrameData) -> None: ...
    def on_process_captured_audio_frame(self, data: AoqAudioFrameData) -> None: ...
    def on_publish_audio_frame(self, track_type: AoqTrackType, data: AoqAudioFrameData) -> None: ...
    def on_playback_audio_frame(self, data: AoqAudioFrameData) -> None: ...
```

回调在 native 音频线程触发，禁止在其中做任何耗时操作。`AoqAudioFrameData.data` 已是 bytes 拷贝，可安全异步使用。

#### IVideoFrameObserver

视频帧数据监听基类。所有方法均为可选 override，默认返回 False。

```
class IVideoFrameObserver:
    def on_captured_video_frame(self, frame: AoqVideoFrame) -> bool: ...
    def on_pre_encode_video_frame(self, track_type: AoqTrackType, frame: AoqVideoFrame) -> bool: ...
    def on_remote_video_frame(self, track_type: AoqTrackType, frame: AoqVideoFrame) -> bool: ...
```

回调在 native 视频线程触发，禁止在其中做任何耗时操作。帧中像素数据已是 bytes 拷贝；当前 Python 层为拷贝语义，修改写回暂不支持，建议始终返回 False。

### 工具函数

#### load\_library

```
def load_library(path: Optional[str] = None) -> ctypes.CDLL
```

加载 native 共享库。一般无需手动调用，首次使用引擎时自动加载。path 为空时按以下顺序查找 `libAoqClientSdk.so`：`AOQ_CLIENT_SDK_LIB` 环境变量、模块同目录、同级 lib 目录、系统默认路径。加载失败抛出 OSError（典型原因：依赖库不在 LD\_LIBRARY\_PATH 中）。

## 数据类型与枚举

数据类型均为 Python dataclass，直接构造并按字段赋值即可。

### 通用类型

#### AoqCreateConfig

**字段**

**类型**

**默认值**

**说明**

work\_dir

str

""

SDK 工作目录

enable\_dump\_audio

bool

False

是否开启音频 dump（调试用）

extras

str

""

扩展参数字符串

#### AoqConnectConfig

**字段**

**类型**

**默认值**

**说明**

token

str

""

连接鉴权 Token

sid

str

""

会话 ID

certificate

str

""

服务器证书指纹

relay\_endpoints

List\[AoqRelayEndpoint\]

空

Relay 接入点列表

workspace\_id\_hash

str

""

工作空间 ID Hash

publish\_tracks

List\[AoqTrackParam\]

空

本端发布轨道列表

subscribe\_tracks

List\[AoqTrackParam\]

空

本端订阅轨道列表

#### AoqRelayEndpoint

**字段**

**类型**

**默认值**

**说明**

endpoint

str

""

Relay 服务器域名或 IP

port

int

0

Relay 服务器端口

route\_index

int

\-1

路径序号，与其他平台 SDK 的 routeIndex 对齐；<0 时 SDK 按数组下标自动填充

#### AoqTrackParam

**字段**

**类型**

**默认值**

**说明**

track\_type

AoqTrackType

AoqTrackType.AUDIO

轨道类型

#### AoqDataMsg

**字段**

**类型**

**默认值**

**说明**

data

bytes

b""

消息数据（字节串）

### 枚举类型

#### AoqErrorCode

**枚举值**

**值**

**说明**

OK

0

成功

PARAM\_INVALID

1

参数非法

STATE\_INVALID

2

状态非法

AUDIO

100

音频通用错误

AUDIO\_EXTERNAL\_BUFFER\_FULL

110

外部音频缓冲区满

AUDIO\_DEVICE

120

音频设备通用错误

AUDIO\_DEVICE\_RECORDING\_AUTH\_FAILED

121

录音权限未获取

AUDIO\_DEVICE\_RECORDING\_OCCUPIED

122

录音设备被占用

AUDIO\_DEVICE\_RECORDING\_START\_FAIL

124

录音启动失败

AUDIO\_DEVICE\_PLAYOUT\_OCCUPIED

125

播放设备被占用

AUDIO\_DEVICE\_PLAYOUT\_START\_FAIL

127

播放启动失败

VIDEO

200

视频通用错误

VIDEO\_EXTERNAL\_BUFFER\_FULL

210

外部视频缓冲区满

#### AoqConnectionStatus

**枚举值**

**值**

**说明**

DISCONNECTED

0

未连接

CONNECTING

1

连接中

CONNECTED

2

已连接

FAILED

3

连接失败

#### AoqTrackType

**枚举值**

**值**

**说明**

AUDIO

0

音频轨道

VIDEO

1

视频轨道

DATA

2

数据消息轨道

#### AoqEncoderType

**枚举值**

**值**

**说明**

UNKNOWN

0

未知格式

AUDIO\_PCM

1

音频 PCM

AUDIO\_OPUS

2

音频 Opus

VIDEO\_H264

3

视频 H.264

VIDEO\_JPEG

4

视频 JPEG

DATA\_TEXT

5

数据文本

#### AoqMirrorMode

**枚举值**

**值**

**说明**

DISABLED

0

关闭镜像

ENABLED

1

开启镜像

#### AoqOrientationMode

**枚举值**

**值**

**说明**

AUTO

0

自动适应

PORTRAIT

1

竖屏

LANDSCAPE

2

横屏

#### AoqRenderMode

**枚举值**

**值**

**说明**

AUTO

0

自适应模式

STRETCH

1

拉伸模式

FILL

2

填充模式

CROP

3

裁剪模式

#### AoqVideoPixelFormat

**枚举值**

**值**

**说明**

UNKNOWN

0

未知格式

I420

1

I420（YUV 三平面格式）

NV12

2

NV12（YUV 半平面格式）

NV21

3

NV21（YUV 半平面格式）

BGRA

4

BGRA（32 位）

RGBA

5

RGBA（32 位）

#### AoqCameraDirection

**枚举值**

**值**

**说明**

FRONT

0

前置摄像头（平台通用枚举；Linux 不支持摄像头采集）

BACK

1

后置摄像头（平台通用枚举；Linux 不支持摄像头采集）

### 音频类型

#### AoqAudioCaptureConfig

**字段**

**类型**

**默认值**

**说明**

is\_external

bool

False

是否为外部采集模式

channel

int

1

声道数（默认单声道）

#### AoqAudioPlaybackConfig

**字段**

**类型**

**默认值**

**说明**

is\_external

bool

False

是否为外部播放模式

channel

int

1

声道数（默认单声道）

#### AoqAudioCodecConfig

**字段**

**类型**

**默认值**

**说明**

track\_type

AoqTrackType

AUDIO

轨道类型

codec\_type

AoqEncoderType

AUDIO\_PCM

编码格式

sample\_rate

int

48000

采样率（Hz）

channel

int

1

声道数

bitrate

int

32000

比特率（bps）

#### AoqAudioFileMixConfig

**字段**

**类型**

**默认值**

**说明**

file\_name

str

""

文件名（含路径），非空

cycles

int

\-1

循环次数，-1 表示无限循环

start\_pos\_ms

int

0

起始播放位置（毫秒）

publish\_volume

int

100

推流音量，取值范围 \[0-100\]

playout\_volume

int

100

播放音量，取值范围 \[0-100\]

#### AoqAudioExternalStreamConfig

**字段**

**类型**

**默认值**

**说明**

track\_type

AoqTrackType

AUDIO

音频轨道类型

codec\_type

AoqEncoderType

AUDIO\_PCM

音频流格式

channels

int

1

声道数

sample\_rate

int

48000

采样率（Hz）

playout\_volume

int

100

播放音量 \[0-100\]

publish\_volume

int

100

推流音量 \[0-100\]

max\_buffer\_duration

int

1000

最大缓冲时长（毫秒）

enable\_3a

bool

False

是否对输入 PCM 进行 3A 处理

#### AoqAudioFrameData

音频裸数据，用于外部输入或观察者回调。

**字段**

**类型**

**默认值**

**说明**

data

bytes

b""

音频 PCM 原始数据（回调中为 bytes 拷贝）

num\_of\_samples

int

0

采样点数（单声道）

bytes\_per\_sample

int

0

每个采样点的字节数

num\_of\_channels

int

0

声道数

samples\_per\_sec

int

0

每秒采样点数（采样率）

push\_sequence

int

0

PCM 输入轮次

time\_stamp

int

0

时间戳

auto\_gen\_mute

bool

False

True 表示 SDK 生成的静音数据

#### AoqAudioObserverConfig

**字段**

**类型**

**默认值**

**说明**

sample\_rate

int

48000

回调音频采样率（Hz）

channels

int

1

回调音频声道数

mode

AoqAudioObserverMode

READ\_ONLY

读写模式

#### AoqAudioStreamDirection

**枚举值**

**值**

**说明**

PUBLISH

0

发布流（推流）

PLAYOUT

1

播放流（拉流）

#### AoqAudioExternalStreamToggle

**枚举值**

**值**

**说明**

NORMAL

0

正常状态

PAUSE

1

暂停状态

#### AoqAudioSource

**枚举值**

**值**

**说明**

CAPTURED

0

采集的音频数据

PROCESS\_CAPTURED

1

3A 处理后的音频数据

PUBLISH

2

推流的音频数据

PLAYBACK

3

播放的音频数据

#### AoqAudioObserverMode

**枚举值**

**值**

**说明**

READ\_ONLY

0

只读模式

READ\_WRITE

1

读写模式

### 视频类型

#### AoqVideoCaptureConfig

**字段**

**类型**

**默认值**

**说明**

width

int

1280

采集宽度（像素），is\_external=True 时无效

height

int

720

采集高度（像素），is\_external=True 时无效

fps

int

15

采集帧率，is\_external=True 时无效

is\_external

bool

False

是否使用外部采集。Linux 仅支持 True；调用 start\_video\_capture 后通过 push\_external\_video\_frame 提供视频帧

camera\_direction

AoqCameraDirection

FRONT

移动端摄像头方向；Linux 无对应能力，保留 FRONT 即可

#### AoqVideoCodecConfig

视频编解码参数（编解码共用）。解码时仅 track\_type/codec\_type/width/height/fps/bitrate 生效，其余仅编码使用。

**字段**

**类型**

**默认值**

**说明**

track\_type

AoqTrackType

VIDEO

轨道类型

codec\_type

AoqEncoderType

VIDEO\_H264

编码格式

width

int

540

编码宽度（像素）

height

int

960

编码高度（像素）

fps

int

5

编码帧率

bitrate

int

500000

目标比特率（bps）

min\_bitrate

int

128000

最小比特率（bps）

keyframe\_interval

int

2

关键帧间隔（秒）

mirror\_mode

AoqMirrorMode

DISABLED

镜像模式

orientation\_mode

AoqOrientationMode

AUTO

视频方向模式

#### AoqVideoCanvas

**字段**

**类型**

**默认值**

**说明**

view

int

0

渲染窗口句柄。Linux 无渲染后端，该字段无实际用途，保持 0 即可

render\_mode

AoqRenderMode

AUTO

渲染模式。Linux 无渲染后端，该字段无实际用途

#### AoqVideoFrame

外部视频帧 / 视频帧回调数据。使用打包格式（NV12/NV21/BGRA/RGBA）时填 data；使用 I420 三平面时填 data\_y/u/v 与对应 stride（两者互斥）。

**字段**

**类型**

**默认值**

**说明**

format

AoqVideoPixelFormat

UNKNOWN

像素格式

width

int

0

视频宽度（像素）

height

int

0

视频高度（像素）

data

bytes

b""

打包格式数据（NV12/NV21/BGRA/RGBA）

data\_y

bytes

b""

I420 Y 平面数据

data\_u

bytes

b""

I420 U 平面数据

data\_v

bytes

b""

I420 V 平面数据

stride\_y

int

0

Y 平面行跨度

stride\_u

int

0

U 平面行跨度

stride\_v

int

0

V 平面行跨度

time\_stamp

int

0

时间戳（毫秒）；0 时 SDK 用本地时钟补齐

#### AoqVideoEncodedFrame

外部已编码视频帧（如 JPEG）。

**字段**

**类型**

**默认值**

**说明**

codec

AoqEncoderType

VIDEO\_JPEG

编码格式

data

bytes

b""

编码后数据

width

int

0

宽度（像素）

height

int

0

高度（像素）

time\_stamp

int

0

时间戳（毫秒）；0 时 SDK 用本地时钟补齐

#### AoqVideoObserverConfig

**字段**

**类型**

**默认值**

**说明**

format

AoqVideoPixelFormat

I420

期望回调像素格式

alignment

AoqVideoObserverAlignment

DEFAULT

宽度对齐策略

mode

AoqVideoObserverMode

READ\_ONLY

读写模式

mirror\_applied

bool

False

是否对回调数据应用镜像

#### AoqVideoSource

**枚举值**

**值**

**说明**

CAPTURED

0

采集后的视频数据（前处理前）

PRE\_ENCODE

1

编码前的视频数据（前处理后）

REMOTE

2

远端解码后、渲染前的视频数据

#### AoqVideoObserverMode

**枚举值**

**值**

**说明**

READ\_ONLY

0

只读模式

READ\_WRITE

1

读写模式

#### AoqVideoObserverAlignment

**枚举值**

**值**

**说明**

DEFAULT

0

默认对齐

EVEN

1

偶数对齐

ALIGN\_4

2

4 字节对齐

ALIGN\_8

3

8 字节对齐

ALIGN\_16

4

16 字节对齐
