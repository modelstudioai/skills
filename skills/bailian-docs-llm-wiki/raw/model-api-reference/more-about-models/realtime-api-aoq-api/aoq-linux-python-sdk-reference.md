# AOQ Client SDK Linux Python API 参考

本文介绍 AOQ Client SDK Linux 版的 Python 接口、回调和数据类型。

> **说明**
>
> AOQ SDK 提供通用视频接口。[Qwen-Audio-Realtime](../../realtime-api-directory/audio-realtime-api-directory/audio-realtime-aoq-access.md) 不支持视频输入或输出；其他模型可使用的媒体能力以对应接入文档为准。

Linux 平台通过 Python 模块 `aoq_client_sdk` 提供 API。所有回调在 native 线程触发，使用者需自行保证线程安全。

<a id="接口目录"></a>

<a id="50f808fe1e25"></a>

<a id="eefa81fce5bc"></a>

## 接口目录

<a id="引擎生命周期"></a>

<a id="9368289c54af"></a>

<a id="3853d5fc7e0a"></a>

### 引擎生命周期

| 接口 | 简介 |
| --- | --- |
| create\_engine | 创建引擎实例（单例模式） |
| destroy | 销毁引擎实例 |
| get\_version | 获取 SDK 版本号 |
| connect | 连接 Relay 服务器 |
| disconnect | 断开服务器连接 |

<a id="音频设备管理"></a>

<a id="d5149fe79ec7"></a>

<a id="b4fb44f6eb28"></a>

### 音频设备管理

| 接口 | 简介 |
| --- | --- |
| start\_audio\_capture | 打开音频采集设备（麦克风） |
| stop\_audio\_capture | 关闭音频采集设备 |
| mute\_audio\_capture | 静音或取消静音音频采集 |
| start\_audio\_player | 开始音频渲染（播放远端音频） |
| stop\_audio\_player | 停止音频渲染 |
| pause\_audio\_player | 暂停音频渲染，支持淡出 |
| resume\_audio\_player | 恢复音频渲染，支持淡入 |
| interrupt\_audio\_player | 打断本轮音频通话 |

<a id="音频编码配置"></a>

<a id="df6d38304341"></a>

<a id="ef974c1ad8ee"></a>

### 音频编码配置

| 接口 | 简介 |
| --- | --- |
| set\_audio\_encoder\_config | 设置音频编码参数 |
| set\_audio\_decoder\_config | 设置音频解码参数 |

<a id="视频设备管理"></a>

<a id="09719abf4c5a"></a>

<a id="49303f7eebef"></a>

### 视频设备管理

| 接口 | 简介 |
| --- | --- |
| start\_video\_capture | 打开视频采集设备（摄像头） |
| stop\_video\_capture | 关闭视频采集设备 |
| set\_local\_view | 设置或移除本地视频渲染窗口 |
| set\_remote\_view | 设置或移除远端视频渲染窗口 |

<a id="视频编解码与外部输入"></a>

<a id="08bbe4646013"></a>

<a id="189dfcd2badb"></a>

### 视频编解码与外部输入

| 接口 | 简介 |
| --- | --- |
| set\_video\_encoder\_config | 设置视频编码参数 |
| set\_video\_decoder\_config | 设置视频解码参数 |
| push\_external\_video\_frame | 推送外部采集视频帧 |
| push\_external\_video\_encoded\_frame | 推送外部已编码视频帧 |

<a id="媒体流发送控制"></a>

<a id="9445c406f734"></a>

<a id="74db1f031e94"></a>

### 媒体流发送控制

| 接口 | 简介 |
| --- | --- |
| enable\_send\_media\_stream | 控制本地媒体流的发送开关 |

<a id="音频文件播放"></a>

<a id="f97765976080"></a>

<a id="28f63a96752c"></a>

### 音频文件播放

| 接口 | 简介 |
| --- | --- |
| start\_audio\_file | 开始推流播放本地音频文件 |
| stop\_audio\_file | 停止音频文件播放 |
| pause\_audio\_file | 暂停音频文件播放 |
| resume\_audio\_file | 恢复音频文件播放 |
| get\_audio\_file\_duration | 获取音频文件总时长 |
| get\_audio\_file\_current\_position | 获取音频文件当前播放位置 |
| set\_audio\_file\_position\_millis | 设置音频文件播放位置（seek） |
| set\_audio\_file\_volume | 设置音频文件音量 |
| get\_audio\_file\_volume | 获取音频文件当前音量 |

<a id="外部音频流"></a>

<a id="a7364ed43671"></a>

<a id="d6b4c13dff30"></a>

### 外部音频流

| 接口 | 简介 |
| --- | --- |
| add\_audio\_external\_stream | 新增一条外部音频流 |
| remove\_audio\_external\_stream | 移除外部音频流 |
| push\_audio\_external\_stream\_data | 输入外部音频 PCM 数据 |
| set\_audio\_external\_stream\_volume | 设置外部音频流音量 |
| get\_audio\_external\_stream\_volume | 获取外部音频流音量 |
| clear\_audio\_external\_stream\_buffer | 清空外部音频流缓存 |

<a id="实时消息"></a>

<a id="b5f5c3d5bc72"></a>

<a id="a66495101cc7"></a>

### 实时消息

| 接口 | 简介 |
| --- | --- |
| send\_data\_msg | 发送实时数据消息 |

<a id="音频帧回调"></a>

<a id="b4f53244f85f"></a>

<a id="b2a326f23d00"></a>

### 音频帧回调

| 接口 | 简介 |
| --- | --- |
| set\_audio\_frame\_observer | 设置音频帧数据回调监听 |
| enable\_audio\_frame\_observer | 开启或关闭指定位置的音频帧回调 |

<a id="视频帧回调"></a>

<a id="47f0dab16306"></a>

<a id="7d6304a9d294"></a>

### 视频帧回调

| 接口 | 简介 |
| --- | --- |
| set\_video\_frame\_observer | 设置视频帧数据回调监听 |
| enable\_video\_frame\_observer | 开启或关闭指定位置的视频帧回调 |

<a id="回调接口"></a>

<a id="bc13be1b47e3"></a>

<a id="c9e559b8e784"></a>

### 回调接口

| 接口 | 简介 |
| --- | --- |
| on\_error | 引擎错误回调 |
| on\_connection\_status\_change | 连接状态变化回调 |
| on\_data\_msg | 收到实时数据消息回调 |

<a id="iaudioframeobserver-回调"></a>

### IAudioFrameObserver 回调

| 接口 | 简介 |
| --- | --- |
| on\_captured\_audio\_frame | 采集到原始音频帧时触发。数据为采集后的原始 PCM，未经任何处理。 |
| on\_process\_captured\_audio\_frame | 3A 处理后的音频帧回调。数据经过 3A（AEC/AGC/ANS）处理。 |
| on\_publish\_audio\_frame | 推流前的音频帧回调。数据为即将编码发送的音频帧。 |
| on\_playback\_audio\_frame | 播放前的远端音频帧回调。数据为远端解码后、即将播放的音频帧。 |

<a id="ivideoframeobserver-回调"></a>

### IVideoFrameObserver 回调

| 接口 | 简介 |
| --- | --- |
| on\_captured\_video\_frame | 采集到原始视频帧时触发（前处理前）。数据为采集后的裸帧，尚未经过前处理。 |
| on\_pre\_encode\_video\_frame | 编码前的视频帧回调（前处理后）。数据为前处理完成、即将编码的裸帧。 |
| on\_remote\_video\_frame | 远端解码后、渲染前的视频帧回调。数据为远端解码完成、即将渲染的裸帧。 |

<a id="工具函数"></a>

<a id="b4f02d8fe512"></a>

<a id="d053f2735f02"></a>

### 工具函数

| 接口 | 简介 |
| --- | --- |
| load\_library | 手动指定并加载 native 共享库 |

<a id="接口详情"></a>

<a id="be91a86f0301"></a>

<a id="dd0f0f808cdb"></a>

## 接口详情

<a id="引擎生命周期-2"></a>

<a id="1f74f37f4c57"></a>

<a id="3853d5fc7e0a-details"></a>

<a id="aoq-api-category-1"></a>

### 引擎生命周期

<a id="create-engine"></a>

<a id="03d2dfbaf224"></a>

<a id="f0964a40e1ed"></a>

#### create\_engine

创建引擎实例（类方法）。SDK 内部以全局单例方式持有引擎，重复调用返回已创建的实例；`destroy` 后需再次 `create_engine` 方可继续使用。

<a id="code-block"></a>

```python
@classmethod
def create_engine(cls, config: AoqCreateConfig, listener: AoqEngineEventListener) -> "AoqClientEngine"
```

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| config | AoqCreateConfig | 引擎创建配置 |
| listener | AoqEngineEventListener | 引擎事件回调监听 |

返回值：AoqClientEngine 引擎实例；创建失败时抛出 RuntimeError。

<a id="destroy"></a>

<a id="8091f9e52b2e"></a>

<a id="3c32463acd34"></a>

#### destroy

销毁引擎实例（类方法），释放所有资源。

<a id="code-block-2"></a>

```python
@classmethod
def destroy(cls) -> int
```

返回值：0 表示成功；非 0 表示失败。

<a id="get-version"></a>

<a id="2eda7465d021"></a>

<a id="2b33409f0268"></a>

#### get\_version

获取 SDK 当前版本号（静态方法）。

<a id="code-block-3"></a>

```python
@staticmethod
def get_version() -> str
```

返回值：版本号字符串，如 "1.0.0"。

<a id="connect"></a>

<a id="ea70c119bd88"></a>

<a id="0e054fb286f7"></a>

#### connect

连接 Relay 服务器。业务 AppServer 应根据所用协议获取临时 AOQ 连接参数并下发给客户端，具体操作请参见Token 鉴权。

<a id="code-block-4"></a>

```python
def connect(self, config: AoqConnectConfig) -> int
```

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| config | AoqConnectConfig | 连接配置，包含 Token、SID、Relay 接入点列表等 |

返回值：0 表示调用已下发（异步执行）；非 0 表示参数校验失败。

<a id="disconnect"></a>

<a id="6a648d0e6ac9"></a>

<a id="22d67fb3d286"></a>

#### disconnect

断开与服务器的连接，释放连接相关资源。

<a id="code-block-5"></a>

```python
def disconnect(self) -> int
```

返回值：0 表示调用已下发（异步执行）；非 0 表示失败。

<a id="音频设备管理-2"></a>

<a id="6642f751be32"></a>

<a id="b4fb44f6eb28-details"></a>

<a id="aoq-api-category-2"></a>

### 音频设备管理

<a id="start-audio-capture"></a>

<a id="1355ab5fc364"></a>

<a id="31c502b94341"></a>

#### start\_audio\_capture

<a id="code-block-6"></a>

```python
def start_audio_capture(self, config: AoqAudioCaptureConfig) -> int
```

Linux 版中该方法为空实现：返回 0，但不会打开声卡或麦克风。音频输入请通过外部音频流接口提供。

<a id="stop-audio-capture"></a>

<a id="4742acf83343"></a>

<a id="ca58b433fc09"></a>

#### stop\_audio\_capture

<a id="code-block-7"></a>

```python
def stop_audio_capture(self) -> int
```

由于 Linux 版不会设置音频采集设备状态，该方法没有实际效果。

<a id="mute-audio-capture"></a>

<a id="de316be2f826"></a>

<a id="8e44294e8c16"></a>

#### mute\_audio\_capture

<a id="code-block-8"></a>

```python
def mute_audio_capture(self, mute: bool) -> int
```

Linux 版不支持麦克风采集，该方法不能控制实际音频采集设备。

<a id="start-audio-player"></a>

<a id="4f32ae8d2c0a"></a>

<a id="d99792fa8ec8"></a>

#### start\_audio\_player

<a id="code-block-9"></a>

```python
def start_audio_player(self, config: AoqAudioPlaybackConfig) -> int
```

Linux 版中该方法为空实现：返回 0，但不会打开声卡或扬声器。音频输出请通过音频帧回调获取数据并自行播放。

<a id="stop-audio-player-pause-audio-player-resume-audio-player"></a>

<a id="9dced9e1fdbe"></a>

<a id="f62e98bc3840"></a>

#### stop\_audio\_player / pause\_audio\_player / resume\_audio\_player

<a id="code-block-10"></a>

```python
def stop_audio_player(self) -> int
def pause_audio_player(self, fade_ms: int = 0) -> int
def resume_audio_player(self, fade_ms: int = 0) -> int
```

Linux 版不支持扬声器播放，以上方法不能控制实际音频播放设备。fade\_ms：淡出或淡入时长（毫秒）；0 表示立即执行。

<a id="interrupt-audio-player"></a>

<a id="af4fe726202a"></a>

<a id="8fb2e9e228e1"></a>

#### interrupt\_audio\_player

<a id="code-block-11"></a>

```python
def interrupt_audio_player(self, track_type: int, fade_ms: int = 0) -> int
```

打断本轮音频通话。

<a id="音频编码配置-2"></a>

<a id="48f996bb17d1"></a>

<a id="ef974c1ad8ee-details"></a>

<a id="aoq-api-category-3"></a>

### 音频编码配置

<a id="code-block-12"></a>

```python
def set_audio_encoder_config(self, config: AoqAudioCodecConfig) -> int
def set_audio_decoder_config(self, config: AoqAudioCodecConfig) -> int
```

<a id="视频设备管理-2"></a>

<a id="e5d0d709f1b0"></a>

<a id="49303f7eebef-details"></a>

<a id="aoq-api-category-4"></a>

### 视频设备管理

<a id="code-block-13"></a>

```python
def start_video_capture(self, config: AoqVideoCaptureConfig) -> int
def stop_video_capture(self) -> int
def set_local_view(self, track_type: int, canvas: Optional[AoqVideoCanvas]) -> int
def set_remote_view(self, track_type: int, canvas: Optional[AoqVideoCanvas]) -> int
```

Linux 版不支持摄像头采集，也没有视频渲染后端。调用 `start_video_capture` 时须将 `is_external` 设为 `True`，并通过 `push_external_video_frame` 提供视频帧；`set_local_view`、`set_remote_view` 及 `AoqVideoCanvas.view` 在 Linux 上无实际用途。如需预览，请通过视频帧回调获取数据并自行渲染。

<a id="视频编解码与外部输入-2"></a>

<a id="9d1888384e52"></a>

<a id="189dfcd2badb-details"></a>

<a id="aoq-api-category-5"></a>

### 视频编解码与外部输入

<a id="set-video-decoder-config"></a>

#### set\_video\_decoder\_config

<a id="code-block-14"></a>

```python
def set_video_decoder_config(self, config: AoqVideoCodecConfig) -> int
```

`config` 为视频解码配置。仅以下字段生效：`track_type`、`codec_type`、`width`、`height`、`fps`、`bitrate`。 其余字段仅用于编码。

在 `connect` 之前调用，作为订阅侧编解码参数提议。

返回值：0 表示成功；非 0 表示失败。

<a id="code-block-15"></a>

```python
def set_video_encoder_config(self, config: AoqVideoCodecConfig) -> int
def set_video_decoder_config(self, config: AoqVideoCodecConfig) -> int
def push_external_video_frame(self, frame: AoqVideoFrame, track_type: AoqTrackType = AoqTrackType.VIDEO) -> int
def push_external_video_encoded_frame(self, track_type: AoqTrackType, frame: AoqVideoEncodedFrame) -> int
```

> **说明**
>
> -   set\_video\_decoder\_config 仅 track\_type/codec\_type/width/height/fps/bitrate 字段生效。
> -   push\_external\_video\_frame 仅在 start\_video\_capture(is\_external=True) 后消费；打包格式（NV12/NV21/BGRA/RGBA）填 `frame.data`，I420 三平面填 `frame.data_y/u/v` 与对应 stride；若缓冲区满返回 AoqErrorCode.VIDEO\_EXTERNAL\_BUFFER\_FULL(210)。
> -   push\_external\_video\_encoded\_frame 要求已调用 set\_video\_encoder\_config(is\_external=True, codec\_type=VIDEO\_JPEG)，否则返回 AoqErrorCode.VIDEO\_EXTERNAL\_ENCODER\_NOT\_ENABLED(212)；直接走旁路通路不做二次编码，**无需依赖** start\_video\_capture。

<a id="媒体流发送控制-2"></a>

<a id="b0fb76de33bc"></a>

<a id="74db1f031e94-details"></a>

<a id="aoq-api-category-6"></a>

### 媒体流发送控制

<a id="code-block-16"></a>

```python
def enable_send_media_stream(self, track_type: AoqTrackType, enable: bool) -> int
```

建议初始化后根据业务需要，分别调用 enable\_send\_media\_stream(AoqTrackType.AUDIO, False) 和 enable\_send\_media\_stream(AoqTrackType.VIDEO, False) 关闭音频、视频轨道发送；待 on\_connection\_status\_change(CONNECTED) 后，再分别开启所需轨道。

<a id="音频文件播放-2"></a>

<a id="e5ee83628fcf"></a>

<a id="28f63a96752c-details"></a>

<a id="aoq-api-category-7"></a>

### 音频文件播放

<a id="code-block-17"></a>

```python
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

<a id="外部音频流-2"></a>

<a id="ae1497519af8"></a>

<a id="d6b4c13dff30-details"></a>

<a id="aoq-api-category-8"></a>

### 外部音频流

<a id="code-block-18"></a>

```python
def add_audio_external_stream(self, stream_id: str, config: AoqAudioExternalStreamConfig) -> int
def remove_audio_external_stream(self, stream_id: str) -> int
def push_audio_external_stream_data(self, stream_id: str, data: AoqAudioFrameData) -> int
def set_audio_external_stream_volume(self, stream_id: str, type_: AoqAudioStreamDirection, volume: int) -> int
def get_audio_external_stream_volume(self, stream_id: str, type_: AoqAudioStreamDirection) -> int
def clear_audio_external_stream_buffer(self, stream_id: str, fadeout_ms: int = -1) -> None
```

> **说明**
>
> push\_audio\_external\_stream\_data 缓冲区满时返回 AoqErrorCode.AUDIO\_EXTERNAL\_BUFFER\_FULL(110)，建议等待约 20ms 后重试同一帧。

<a id="实时消息-2"></a>

<a id="3c161f4619d6"></a>

<a id="a66495101cc7-details"></a>

<a id="aoq-api-category-9"></a>

### 实时消息

<a id="code-block-19"></a>

```python
def send_data_msg(self, msg: AoqDataMsg) -> int
```

<a id="音频帧回调-2"></a>

<a id="ac3a3d59f720"></a>

<a id="b2a326f23d00-details"></a>

<a id="aoq-api-category-10"></a>

### 音频帧回调

<a id="code-block-20"></a>

```python
def set_audio_frame_observer(self, observer: Optional[IAudioFrameObserver]) -> int
def enable_audio_frame_observer(self, enabled: bool, audio_source: AoqAudioSource, config: AoqAudioObserverConfig) -> int
```

set\_audio\_frame\_observer 传 None 表示注销观察者。

<a id="视频帧回调-2"></a>

<a id="f0adde634832"></a>

<a id="7d6304a9d294-details"></a>

<a id="aoq-api-category-11"></a>

### 视频帧回调

<a id="code-block-21"></a>

```python
def set_video_frame_observer(self, observer: Optional[IVideoFrameObserver]) -> int
def enable_video_frame_observer(self, enabled: bool, video_source: AoqVideoSource, config: AoqVideoObserverConfig) -> int
```

set\_video\_frame\_observer 传 None 表示注销观察者。

<a id="回调接口-2"></a>

<a id="445a9f025184"></a>

<a id="c9e559b8e784-details"></a>

<a id="aoq-api-category-12"></a>

### 回调接口

<a id="aoqengineeventlistener"></a>

<a id="90468ac3f329"></a>

<a id="ac3e2ac2122d"></a>

#### AoqEngineEventListener

引擎事件回调基类。所有方法均为可选 override，默认空实现；回调在 native 线程触发，使用者需自行保证线程安全。

<a id="code-block-22"></a>

```python
class AoqEngineEventListener:
    def on_error(self, code: int, message: str) -> None: ...
    def on_connection_status_change(self, status: AoqConnectionStatus) -> None: ...
    def on_data_msg(self, msg: AoqDataMsg) -> None: ...
```

<a id="on-error"></a>

<a id="f92b80f70377"></a>

<a id="9f2f7ce7c173"></a>

#### on\_error

<a id="code-block-23"></a>

```python
def on_error(self, code: int, message: str) -> None
```

引擎错误回调。code 对应 AoqErrorCode 枚举值。

<a id="on-connection-status-change"></a>

<a id="009c0e546b84"></a>

<a id="837f5301307d"></a>

#### on\_connection\_status\_change

<a id="code-block-24"></a>

```python
def on_connection_status_change(self, status: AoqConnectionStatus) -> None
```

连接状态变化回调。状态流转：DISCONNECTED -> CONNECTING -> CONNECTED/FAILED -> DISCONNECTED。

<a id="on-data-msg"></a>

<a id="c20467be7e16"></a>

<a id="4dfd537ac790"></a>

#### on\_data\_msg

<a id="code-block-25"></a>

```python
def on_data_msg(self, msg: AoqDataMsg) -> None
```

收到实时数据消息回调。

<a id="iaudioframeobserver-回调-2"></a>

<a id="6e50e043f473"></a>

<a id="f6a6ab3f2969"></a>

<a id="aoq-api-category-13"></a>

### IAudioFrameObserver 回调

音频帧数据监听基类。所有方法均为可选 override，默认空实现。

<a id="code-block-26"></a>

```python
class IAudioFrameObserver:
    def on_captured_audio_frame(self, data: AoqAudioFrameData) -> None: ...
    def on_process_captured_audio_frame(self, data: AoqAudioFrameData) -> None: ...
    def on_publish_audio_frame(self, track_type: AoqTrackType, data: AoqAudioFrameData) -> None: ...
    def on_playback_audio_frame(self, data: AoqAudioFrameData) -> None: ...
```

回调在 native 音频线程触发，禁止在其中做任何耗时操作。`AoqAudioFrameData.data` 已是 bytes 拷贝，可安全异步使用。

<a id="on-captured-audio-frame"></a>

#### on\_captured\_audio\_frame

采集到原始音频帧时触发。数据为采集后的原始 PCM，未经任何处理。

<a id="code-block-27"></a>

```python
def on_captured_audio_frame(self, data: AoqAudioFrameData) -> None: ...
```

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| data | AoqAudioFrameData | 采集的音频帧数据 |

返回值：无（None）。

> **说明**
>
> 帧数据已是 bytes 拷贝，可安全异步使用。

<a id="on-process-captured-audio-frame"></a>

#### on\_process\_captured\_audio\_frame

3A 处理后的音频帧回调。数据经过 3A（AEC/AGC/ANS）处理。

<a id="code-block-28"></a>

```python
def on_process_captured_audio_frame(self, data: AoqAudioFrameData) -> None: ...
```

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| data | AoqAudioFrameData | 3A 处理后的音频帧数据 |

返回值：无（None）。

> **说明**
>
> 帧数据已是 bytes 拷贝，可安全异步使用。

<a id="on-publish-audio-frame"></a>

#### on\_publish\_audio\_frame

推流前的音频帧回调。数据为即将编码发送的音频帧。

<a id="code-block-29"></a>

```python
def on_publish_audio_frame(self, track_type: AoqTrackType, data: AoqAudioFrameData) -> None: ...
```

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| track\_type | AoqTrackType | 音频轨道类型 |
| data | AoqAudioFrameData | 推流前的音频帧数据 |

返回值：无（None）。

> **说明**
>
> 帧数据已是 bytes 拷贝，可安全异步使用。 此回调仅支持只读模式。

<a id="on-playback-audio-frame"></a>

#### on\_playback\_audio\_frame

播放前的远端音频帧回调。数据为远端解码后、即将播放的音频帧。

<a id="code-block-30"></a>

```python
def on_playback_audio_frame(self, data: AoqAudioFrameData) -> None: ...
```

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| data | AoqAudioFrameData | 播放前的远端音频帧数据 |

返回值：无（None）。

> **说明**
>
> 帧数据已是 bytes 拷贝，可安全异步使用。

<a id="ivideoframeobserver-回调-2"></a>

<a id="6804f6d8c94a"></a>

<a id="2d6140cd723f"></a>

<a id="aoq-api-category-14"></a>

### IVideoFrameObserver 回调

视频帧数据监听基类。所有方法均为可选 override，默认返回 False。

<a id="code-block-31"></a>

```python
class IVideoFrameObserver:
    def on_captured_video_frame(self, track_type: AoqTrackType, frame: AoqVideoFrame) -> bool: ...
    def on_pre_encode_video_frame(self, track_type: AoqTrackType, frame: AoqVideoFrame) -> bool: ...
    def on_remote_video_frame(self, track_type: AoqTrackType, frame: AoqVideoFrame) -> bool: ...
```

回调在 native 视频线程触发，禁止在其中做任何耗时操作。帧中像素数据已是 bytes 拷贝；当前 Python 层为拷贝语义，修改写回暂不支持，建议始终返回 False。

<a id="on-captured-video-frame"></a>

#### on\_captured\_video\_frame

采集到原始视频帧时触发（前处理前）。数据为采集后的裸帧，尚未经过前处理。

<a id="code-block-32"></a>

```python
def on_captured_video_frame(self, track_type: AoqTrackType, frame: AoqVideoFrame) -> bool: ...
```

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| track\_type | AoqTrackType | 帧所属轨道（Video / Screen） |
| frame | AoqVideoFrame | 采集的视频帧数据 |

返回值：True 表示数据已修改需写回 SDK（仅 I420 生效），False 表示只读。当前 Python 层为拷贝语义，建议始终返回 False。

> **说明**
>
> 帧数据已是 bytes 拷贝，可安全异步使用。

<a id="on-pre-encode-video-frame"></a>

#### on\_pre\_encode\_video\_frame

编码前的视频帧回调（前处理后）。数据为前处理完成、即将编码的裸帧。

<a id="code-block-33"></a>

```python
def on_pre_encode_video_frame(self, track_type: AoqTrackType, frame: AoqVideoFrame) -> bool: ...
```

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| track\_type | AoqTrackType | 帧所属轨道（Video / Screen） |
| frame | AoqVideoFrame | 编码前的视频帧数据 |

返回值：True 表示数据已修改需写回 SDK（仅 I420 生效），False 表示只读。当前 Python 层为拷贝语义，建议始终返回 False。

> **说明**
>
> 帧数据已是 bytes 拷贝，可安全异步使用。

<a id="on-remote-video-frame"></a>

#### on\_remote\_video\_frame

远端解码后、渲染前的视频帧回调。数据为远端解码完成、即将渲染的裸帧。

<a id="code-block-34"></a>

```python
def on_remote_video_frame(self, track_type: AoqTrackType, frame: AoqVideoFrame) -> bool: ...
```

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| track\_type | AoqTrackType | 帧所属轨道（Video / Screen） |
| frame | AoqVideoFrame | 远端解码后的视频帧数据 |

返回值：True 表示数据已修改需写回 SDK（仅 I420 生效），False 表示只读。当前 Python 层为拷贝语义，建议始终返回 False。

> **说明**
>
> 帧数据已是 bytes 拷贝，可安全异步使用。

<a id="工具函数-2"></a>

<a id="b6a7b7d502e2"></a>

<a id="d053f2735f02-details"></a>

<a id="aoq-api-category-15"></a>

### 工具函数

<a id="load-library"></a>

<a id="52e69fd9ee8e"></a>

<a id="1ae02fc7beb3"></a>

#### load\_library

<a id="code-block-35"></a>

```python
def load_library(path: Optional[str] = None) -> ctypes.CDLL
```

加载 native 共享库。一般无需手动调用，首次使用引擎时自动加载。path 为空时按以下顺序查找 `libAoqClientSdk.so`：`AOQ_CLIENT_SDK_LIB` 环境变量、模块同目录、同级 lib 目录、系统默认路径。加载失败抛出 OSError（典型原因：依赖库不在 LD\_LIBRARY\_PATH 中）。

<a id="数据类型与枚举"></a>

<a id="9ab211dfe726"></a>

<a id="73575e0c13ff"></a>

## 数据类型与枚举

数据类型均为 Python dataclass，直接构造并按字段赋值即可。

<a id="通用类型"></a>

<a id="68bb54474a1b"></a>

<a id="07322b5db657"></a>

### 通用类型

<a id="aoqcreateconfig"></a>

<a id="29371106460b"></a>

<a id="eed0f444e642"></a>

#### AoqCreateConfig

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| work\_dir | str | "" | SDK 工作目录 |
| enable\_dump\_audio | bool | False | 是否开启音频 dump（调试用） |
| extras | str | "" | 扩展参数字符串 |
| max\_encoded\_video\_frame\_bytes | int | 190 × 1024 | 编码后单帧大小上限（字节），仅用于 SDK 内部 JPEG 编码。 |
| enable\_drop\_oversized\_video\_frame | bool | False | 仅用于 SDK 内部 JPEG 编码：降至最低质量后仍超限时，是否允许丢弃该帧。 |

<a id="aoqconnectconfig"></a>

<a id="5ad996dff9cd"></a>

<a id="3e7902dce8b5"></a>

#### AoqConnectConfig

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| token | str | "" | 连接鉴权 Token |
| sid | str | "" | 会话 ID |
| certificate | str | "" | 服务器证书指纹 |
| relay\_endpoints | List\[AoqRelayEndpoint\] | 空 | Relay 接入点列表 |
| workspace\_id\_hash | str | "" | 工作空间 ID Hash |
| publish\_tracks | List\[AoqTrackParam\] | 空 | 本端发布轨道列表 |
| subscribe\_tracks | List\[AoqTrackParam\] | 空 | 本端订阅轨道列表 |

<a id="aoqrelayendpoint"></a>

<a id="35555e0dc484"></a>

<a id="b58a1473e07b"></a>

#### AoqRelayEndpoint

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| endpoint | str | "" | Relay 服务器域名或 IP |
| port | int | 0 | Relay 服务器端口 |
| route\_index | int | \-1 | 路径序号；<0 时 SDK 按数组下标自动填充 |
| tcp\_port | int | 0 | TCP 降级端口；0 表示使用 SDK 默认端口 443。 |

<a id="aoqtrackparam"></a>

<a id="89c7fafaec2a"></a>

<a id="570fc294b704"></a>

#### AoqTrackParam

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| track\_type | AoqTrackType | AoqTrackType.AUDIO | 轨道类型 |

<a id="aoqdatamsg"></a>

<a id="9b28d3e4eb75"></a>

<a id="e0d8895ec85c"></a>

#### AoqDataMsg

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| data | bytes | b"" | 消息数据（字节串） |

<a id="枚举类型"></a>

<a id="11d39f7fea0f"></a>

<a id="f26ca8671462"></a>

### 枚举类型

<a id="aoqerrorcode"></a>

<a id="bd1a6ae84020"></a>

<a id="a22cd1d8b665"></a>

#### AoqErrorCode

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| OK | 0 | 成功 |
| PARAM\_INVALID | 1 | 参数非法 |
| STATE\_INVALID | 2 | 状态非法 |
| AUDIO | 100 | 音频通用错误 |
| AUDIO\_EXTERNAL\_BUFFER\_FULL | 110 | 外部音频缓冲区满 |
| AUDIO\_DEVICE | 120 | 音频设备通用错误 |
| AUDIO\_DEVICE\_RECORDING\_AUTH\_FAILED | 121 | 录音权限未获取 |
| AUDIO\_DEVICE\_RECORDING\_OCCUPIED | 122 | 录音设备被占用 |
| AUDIO\_DEVICE\_RECORDING\_START\_FAIL | 124 | 录音启动失败 |
| AUDIO\_DEVICE\_PLAYOUT\_OCCUPIED | 125 | 播放设备被占用 |
| AUDIO\_DEVICE\_PLAYOUT\_START\_FAIL | 127 | 播放启动失败 |
| VIDEO | 200 | 视频通用错误 |
| VIDEO\_EXTERNAL\_BUFFER\_FULL | 210 | 外部视频缓冲区满 |

<a id="aoqwarningcode"></a>

#### AoqWarningCode

警告码枚举。

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| OK | 0 | 无警告 |
| AUDIO | 100 | 音频通用警告 |
| AUDIO\_HOWLING | 101 | 音频啸叫检测 |
| AUDIO\_DEVICE | 120 | 音频设备通用警告 |
| AUDIO\_DEVICE\_MIC\_ENUMERATE\_ERROR | 121 | 麦克风枚举错误 |
| AUDIO\_DEVICE\_MIC\_START\_TIMEOUT | 122 | 麦克风启动超时 |
| AUDIO\_DEVICE\_RECORDING\_ERROR | 123 | 录音过程错误 |
| AUDIO\_DEVICE\_SPEAKER\_ENUMERATE\_ERROR | 124 | 扬声器枚举错误 |
| AUDIO\_DEVICE\_SPEAKER\_START\_TIMEOUT | 125 | 扬声器启动超时 |
| AUDIO\_DEVICE\_PLAYOUT\_ERROR | 126 | 播放过程错误 |
| VIDEO | 200 | 视频通用警告 |
| VIDEO\_CAMERA\_ENUMERATE\_ERROR | 201 | 摄像头枚举错误 |
| VIDEO\_ENCODER\_SWITCHED | 202 | 视频编码器已切换 |
| VIDEO\_RENDER\_DOWNGRADE | 203 | 视频渲染降级 |

> **说明**
>
> `AoqEngineEventListener` 基类未声明 `on_warning`，但 C 桥接层会以 `getattr(listener, "on_warning")` 动态转发，业务侧可自行在 listener 上实现该方法接收警告。

<a id="aoqconnectionstatus"></a>

<a id="a728226f8a53"></a>

<a id="1048d0c3e6ee"></a>

#### AoqConnectionStatus

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| DISCONNECTED | 0 | 未连接 |
| CONNECTING | 1 | 连接中 |
| CONNECTED | 2 | 已连接 |
| FAILED | 3 | 连接失败 |

<a id="aoqtracktype"></a>

<a id="1dac9813a4d6"></a>

<a id="47f3d99e128f"></a>

#### AoqTrackType

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| AUDIO | 0 | 音频轨道 |
| VIDEO | 1 | 视频轨道 |
| DATA | 2 | 数据消息轨道 |

<a id="aoqencodertype"></a>

<a id="119cfb21807b"></a>

<a id="8c23a1705af2"></a>

#### AoqEncoderType

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| UNKNOWN | 0 | 未知格式 |
| AUDIO\_PCM | 1 | 音频 PCM |
| AUDIO\_OPUS | 2 | 音频 Opus |
| VIDEO\_H264 | 3 | 视频 H.264 |
| VIDEO\_JPEG | 4 | 视频 JPEG |
| DATA\_TEXT | 5 | 数据文本 |

<a id="aoqmirrormode"></a>

<a id="88fa0beab28b"></a>

<a id="353c6d658a7b"></a>

#### AoqMirrorMode

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| DISABLED | 0 | 关闭镜像 |
| ENABLED | 1 | 开启镜像 |

<a id="aoqorientationmode"></a>

<a id="8c37ace505ad"></a>

<a id="2a6192140564"></a>

#### AoqOrientationMode

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| AUTO | 0 | 自动适应 |
| PORTRAIT | 1 | 竖屏 |
| LANDSCAPE | 2 | 横屏 |

<a id="aoqrendermode"></a>

<a id="11ec7d100c4b"></a>

<a id="dcf4df2c1544"></a>

#### AoqRenderMode

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| AUTO | 0 | 自适应模式 |
| STRETCH | 1 | 拉伸模式 |
| FILL | 2 | 填充模式 |
| CROP | 3 | 裁剪模式 |

<a id="aoqvideopixelformat"></a>

<a id="83f3a5357119"></a>

<a id="1bff63b2d99e"></a>

#### AoqVideoPixelFormat

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| UNKNOWN | 0 | 未知格式 |
| I420 | 1 | I420（YUV 三平面格式） |
| NV12 | 2 | NV12（YUV 半平面格式） |
| NV21 | 3 | NV21（YUV 半平面格式） |
| BGRA | 4 | BGRA（32 位） |
| RGBA | 5 | RGBA（32 位） |
| CV\_PIXEL\_BUFFER | 6 | Apple 平台零拷贝路径，Linux 不使用 |

<a id="aoqcameradirection"></a>

<a id="6a7da0d00af2"></a>

<a id="2c99c2f73af8"></a>

#### AoqCameraDirection

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| FRONT | 0 | 前置摄像头（平台通用枚举；Linux 不支持摄像头采集） |
| BACK | 1 | 后置摄像头（平台通用枚举；Linux 不支持摄像头采集） |

<a id="音频类型"></a>

<a id="73eecbfe4036"></a>

<a id="18fc2abe2aed"></a>

### 音频类型

<a id="aoqaudiocaptureconfig"></a>

<a id="4c2cdeef4941"></a>

<a id="55191a7475de"></a>

#### AoqAudioCaptureConfig

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| is\_external | bool | False | 是否为外部采集模式 |
| channel | int | 1 | 声道数（默认单声道） |

<a id="aoqaudioplaybackconfig"></a>

<a id="b3d0105e8d7a"></a>

<a id="0b30f197ac02"></a>

#### AoqAudioPlaybackConfig

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| is\_external | bool | False | 是否为外部播放模式 |
| channel | int | 1 | 声道数（默认单声道） |

<a id="aoqaudiocodecconfig"></a>

<a id="913d1c29a7f6"></a>

<a id="87b9f458d857"></a>

#### AoqAudioCodecConfig

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| track\_type | AoqTrackType | AUDIO | 轨道类型 |
| codec\_type | AoqEncoderType | AUDIO\_OPUS | 编码格式 |
| sample\_rate | int | 48000 | 采样率（Hz） |
| channel | int | 1 | 声道数 |
| bitrate | int | 32000 | 比特率（bps） |

<a id="aoqaudiofilemixconfig"></a>

<a id="96b85c0ff575"></a>

<a id="ec61543adc99"></a>

#### AoqAudioFileMixConfig

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| file\_name | str | "" | 文件名（含路径），非空 |
| cycles | int | \-1 | 循环次数，-1 表示无限循环 |
| start\_pos\_ms | int | 0 | 起始播放位置（毫秒） |
| publish\_volume | int | 100 | 推流音量，取值范围 \[0-100\] |
| playout\_volume | int | 100 | 播放音量，取值范围 \[0-100\] |

<a id="aoqaudioexternalstreamconfig"></a>

<a id="3eba1dc32e42"></a>

<a id="f4414bef223f"></a>

#### AoqAudioExternalStreamConfig

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| track\_type | AoqTrackType | AUDIO | 音频轨道类型 |
| codec\_type | AoqEncoderType | AUDIO\_PCM | 音频流格式 |
| channels | int | 1 | 声道数 |
| sample\_rate | int | 48000 | 采样率（Hz） |
| playout\_volume | int | 100 | 播放音量 \[0-100\] |
| publish\_volume | int | 100 | 推流音量 \[0-100\] |
| max\_buffer\_duration | int | 1000 | 最大缓冲时长（毫秒） |
| enable\_3a | bool | False | 是否对输入 PCM 进行 3A 处理 |

<a id="aoqaudioframedata"></a>

<a id="f83b4a1c34e5"></a>

<a id="e2449bc9dece"></a>

#### AoqAudioFrameData

音频裸数据，用于外部输入或观察者回调。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| data | bytes | b"" | 音频 PCM 原始数据（回调中为 bytes 拷贝） |
| num\_of\_samples | int | 0 | 采样点数（单声道） |
| bytes\_per\_sample | int | 0 | 每个采样点的字节数 |
| num\_of\_channels | int | 0 | 声道数 |
| samples\_per\_sec | int | 0 | 每秒采样点数（采样率） |
| push\_sequence | int | 0 | PCM 输入轮次 |
| time\_stamp | int | 0 | 时间戳 |
| auto\_gen\_mute | bool | False | True 表示 SDK 生成的静音数据 |

<a id="aoqaudioobserverconfig"></a>

<a id="dd4f5445a9fa"></a>

<a id="b51a6a244111"></a>

#### AoqAudioObserverConfig

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| sample\_rate | int | 48000 | 回调音频采样率（Hz） |
| channels | int | 1 | 回调音频声道数 |
| mode | AoqAudioObserverMode | READ\_ONLY | 读写模式 |

<a id="aoqaudiostreamdirection"></a>

<a id="54a33a803d68"></a>

<a id="e18ec4adeb8a"></a>

#### AoqAudioStreamDirection

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| PUBLISH | 0 | 发布流（推流） |
| PLAYOUT | 1 | 播放流（拉流） |

<a id="aoqaudioexternalstreamtoggle"></a>

<a id="596bcb155f6e"></a>

<a id="8d3a23582ad2"></a>

#### AoqAudioExternalStreamToggle

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| NORMAL | 0 | 正常状态 |
| PAUSE | 1 | 暂停状态 |

<a id="aoqaudiosource"></a>

<a id="220c0e16e643"></a>

<a id="75ec30549522"></a>

#### AoqAudioSource

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| CAPTURED | 0 | 采集的音频数据 |
| PROCESS\_CAPTURED | 1 | 3A 处理后的音频数据 |
| PUBLISH | 2 | 推流的音频数据 |
| PLAYBACK | 3 | 播放的音频数据 |

<a id="aoqaudioobservermode"></a>

<a id="f0439052f53c"></a>

<a id="5a14511da6c5"></a>

#### AoqAudioObserverMode

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| READ\_ONLY | 0 | 只读模式 |
| READ\_WRITE | 1 | 读写模式 |

<a id="视频类型"></a>

<a id="26243e9ba4f4"></a>

<a id="3af61073ee2d"></a>

### 视频类型

<a id="aoqvideocaptureconfig"></a>

<a id="efc45d5b63c8"></a>

<a id="cde328a703a7"></a>

#### AoqVideoCaptureConfig

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| width | int | 1280 | 采集宽度（像素），is\_external=True 时无效 |
| height | int | 720 | 采集高度（像素），is\_external=True 时无效 |
| fps | int | 15 | 采集帧率，is\_external=True 时无效 |
| is\_external | bool | False | 是否使用外部采集。Linux 仅支持 True；调用 start\_video\_capture 后通过 push\_external\_video\_frame 提供视频帧 |
| camera\_direction | AoqCameraDirection | FRONT | 移动端摄像头方向；Linux 无对应能力，保留 FRONT 即可 |

<a id="aoqvideocodecconfig"></a>

<a id="4659aff13cd4"></a>

<a id="9cf96fb66801"></a>

#### AoqVideoCodecConfig

视频编解码参数（编解码共用）。解码时仅 track\_type/codec\_type/width/height/fps/bitrate 生效，其余仅编码使用。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| is\_external | bool | False | 外部编码模式；True 时由调用方推送已编码帧，SDK 不做采集和编码（仅编码生效） |
| track\_type | AoqTrackType | VIDEO | 轨道类型 |
| codec\_type | AoqEncoderType | VIDEO\_H264 | 编码格式 |
| width | int | 540 | 编码宽度（像素） |
| height | int | 960 | 编码高度（像素） |
| fps | int | 5 | 编码帧率 |
| bitrate | int | 500000 | 目标比特率（bps） |
| min\_bitrate | int | 128000 | 最小比特率（bps） |
| keyframe\_interval | int | 2 | 关键帧间隔（秒） |
| mirror\_mode | AoqMirrorMode | DISABLED | 镜像模式 |
| orientation\_mode | AoqOrientationMode | AUTO | 视频方向模式 |

<a id="aoqvideocanvas"></a>

<a id="44010cbde896"></a>

<a id="9edfb857a3a8"></a>

#### AoqVideoCanvas

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| view | int | 0 | 渲染窗口句柄。Linux 无渲染后端，该字段无实际用途，保持 0 即可 |
| render\_mode | AoqRenderMode | AUTO | 渲染模式。Linux 无渲染后端，该字段无实际用途 |

<a id="aoqvideoframe"></a>

<a id="0191874fe308"></a>

<a id="11a8f9fa6709"></a>

#### AoqVideoFrame

外部视频帧 / 视频帧回调数据。使用打包格式（NV12/NV21/BGRA/RGBA）时填 data；使用 I420 三平面时填 data\_y/u/v 与对应 stride（两者互斥）。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| format | AoqVideoPixelFormat | UNKNOWN | 像素格式 |
| width | int | 0 | 视频宽度（像素） |
| height | int | 0 | 视频高度（像素） |
| data | bytes | b"" | 打包格式数据（NV12/NV21/BGRA/RGBA） |
| data\_y | bytes | b"" | I420 Y 平面数据 |
| data\_u | bytes | b"" | I420 U 平面数据 |
| data\_v | bytes | b"" | I420 V 平面数据 |
| stride\_y | int | 0 | Y 平面行跨度 |
| stride\_u | int | 0 | U 平面行跨度 |
| stride\_v | int | 0 | V 平面行跨度 |
| time\_stamp | int | 0 | 时间戳（毫秒）；0 时 SDK 用本地时钟补齐 |
| native\_pixel\_buffer | int | 0 | Apple 零拷贝句柄，Linux 保留为 0 |

<a id="aoqvideoencodedframe"></a>

<a id="97270b6a80d3"></a>

<a id="1613344be8c8"></a>

#### AoqVideoEncodedFrame

外部已编码视频帧（如 JPEG）。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| codec | AoqEncoderType | VIDEO\_JPEG | 编码格式 |
| data | bytes | b"" | 编码后数据 |
| width | int | 0 | 宽度（像素） |
| height | int | 0 | 高度（像素） |
| time\_stamp | int | 0 | 时间戳（毫秒）；0 时 SDK 用本地时钟补齐 |

<a id="aoqvideoobserverconfig"></a>

<a id="a458a6906f02"></a>

<a id="c9ee095b2d9b"></a>

#### AoqVideoObserverConfig

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| format | AoqVideoPixelFormat | I420 | 期望回调像素格式 |
| alignment | AoqVideoObserverAlignment | DEFAULT | 宽度对齐策略 |
| mode | AoqVideoObserverMode | READ\_ONLY | 读写模式 |
| mirror\_applied | bool | False | 是否对回调数据应用镜像 |

<a id="aoqvideosource"></a>

<a id="839deb24c19c"></a>

<a id="04545dfc3641"></a>

#### AoqVideoSource

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| CAPTURED | 0 | 采集后的视频数据（前处理前） |
| PRE\_ENCODE | 1 | 编码前的视频数据（前处理后） |
| REMOTE | 2 | 远端解码后、渲染前的视频数据 |

<a id="aoqvideoobservermode"></a>

<a id="2562c6c47605"></a>

<a id="d2b9c40f7022"></a>

#### AoqVideoObserverMode

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| READ\_ONLY | 0 | 只读模式 |
| READ\_WRITE | 1 | 读写模式 |

<a id="aoqvideoobserveralignment"></a>

<a id="533da038e9ad"></a>

<a id="e34688bb403f"></a>

#### AoqVideoObserverAlignment

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| DEFAULT | 0 | 默认对齐 |
| EVEN | 1 | 偶数对齐 |
| ALIGN\_4 | 2 | 4 字节对齐 |
| ALIGN\_8 | 3 | 8 字节对齐 |
| ALIGN\_16 | 4 | 16 字节对齐 |
