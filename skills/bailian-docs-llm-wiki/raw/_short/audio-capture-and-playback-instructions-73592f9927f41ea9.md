# 音频采集和播放说明

本文主要介绍多模交互开发套件中的输入输出语音格式，以及格式不符合要求时的常见问题及解决方法。

<a id="音频格式说明"></a>

<a id="599c760251e7t"></a>

## 音频格式说明

<table><thead><tr><th><p><strong>类型</strong></p></th><th><p><strong>可选参数设置</strong></p></th><th><p><strong>语音格式说明</strong></p></th></tr></thead><tbody><tr><td><p>语音识别</p></td><td><ul><li><p>upstream.audio_format</p></li></ul></td><td><ul><li><p>支持的输入格式：</p><ul><li><p>&quot;pcm&quot;：PCM编码（无压缩的PCM或WAV），16bit 采样深度，单通道。</p></li><li><p>&quot;raw-opus&quot;：裸 OPUS 数据，以定长发送</p></li></ul></li><li><p>音频采样率：默认16000 Hz。</p></li></ul></td></tr><tr><td><p>语音合成</p></td><td><ul><li><p>downstream.audio_format</p></li><li><p>downstream.sample_rate</p></li><li><p>downstream.frame_size</p></li></ul></td><td><ul><li><p>支持的输出格式：</p><ul><li><p>&quot;pcm&quot;：PCM编码（无压缩的PCM或WAV），16bit 采样深度，单通道。</p></li><li><p>&quot;opus&quot;：OGG封装的OPUS格式单声道（mono）音频</p></li><li><p>&quot;raw-opus&quot;：裸 OPUS 数据，以定长发送</p></li><li><p>&quot;mp3&quot;：MP3 音频格式</p></li></ul></li><li><p>支持的音频采样率：8000 Hz、16000 Hz、24000Hz、48000Hz。默认采样率为 24000Hz。</p></li><li><p>支持的帧长度：10,20,40,60,100,120，默认值为60，单位ms，只在合成音频格式为opus或raw-opus时生效</p></li></ul></td></tr><tr><td></td><td></td><td></td></tr></tbody></table>

<a id="查看语音格式"></a>

<a id="8be1981eae3tu"></a>

## 查看语音格式

<a id="基本说明"></a>

<a id="6eb7933de3j3r"></a>

### 基本说明

常见语音格式名词说明：

-   采样率：比如 8000 Hz（8K Hz）、16000 Hz (16K Hz) 代表每秒8000个或16000个采样点。
-   采样位数：比如 16 bit 代表每个采样点的音频信息用16 bit（2个字节）保存。
-   声道：有两种声道：Mono单声道、Stereo立体声。

语音时长与文件大小转换：

-   语音文件Size大小（单位MiB）=（采样率×采样位数×声道数×语音时长（单位s））/（8_1024_1024）
    
    -   例如：16000（Hz）\*16（bit）_1（声道）_60（s）/（8_1024_1024）=1.83 MiB（近似值）

<a id="linux操作系统下查看语音格式"></a>

<a id="cfee47f97b82w"></a>

### Linux操作系统下查看语音格式

1.  使用如下命令查看

<a id="code-block"></a>

```javascript
file input.wav
```

1.  预期结果
    
    -   16000 Hz采样率、16 bit采样位数、单声道（mono）的无压缩WAV格式如下所示：

<a id="code-block-2"></a>

```bash
$file test-16000.wav
test-16000.wav: RIFF (little-endian) data, WAVE audio, Microsoft PCM, 16 bit, mono 16000 Hz
```

<a id="windows操作系统下查看语音格式"></a>

<a id="bca8cf0c1ae8l"></a>

### Windows操作系统下查看语音格式

1.  在Windows操作系统中，您可以选中目标语音，单击鼠标右键，选择**属性**，可以查看更多信息。
    
2.  预期结果
    
    -   16000 Hz采样率、16 bit采样位数、单声道（mono）的无压缩WAV格式：音频文件属性显示：持续时间为 00:05，音频声道为单声道，采样速率为 16 kHz，每个样本的位数为 16。

<a id="如何进行语音格式转换"></a>

<a id="868e843a78h7t"></a>

## 如何进行语音格式转换

若输入语音采样率、采样位数、声道、编码等不符合语音识别格式要求时会报错，测试语音可先进行语音格式转换。

<a id="linux操作系统下转换语音格式"></a>

<a id="2fbb17480aj0t"></a>

### Linux操作系统下转换语音格式

使用如下常见的FFmpeg命令进行转换。更多操作，请参见[下载FFmpeg](http://ffmpeg.org/download.html)。

<a id="code-block-3"></a>

```powershell
#查询语音格式如采样率、声道、编码等
ffmpeg -i input.mp3
#将某个wav文件转化为8K、16bit、单声道的wav文件
ffmpeg -i input.wav  -ar 8000 -ac 1 -acodec pcm_s16le -f s16le output.wav
#将某个wav文件转化为16K、16bit、单声道的wav文件
ffmpeg -i input.wav  -ar 16000 -ac 1 -acodec pcm_s16le -f s16le output.wav
#将某个pcm文件转化为16K、16bit、单声道的wav文件
ffmpeg -i input.pcm -f s16le -ar 16000 -ac 1 -acodec pcm_s16le  output.wav
#将某个wav文件转化为16K、16bit、单声道的pcm文件
ffmpeg -y -i input.wav -acodec pcm_s16le -f s16le -ac 1 -ar 16000 output.pcm
#将某个Mp3文件转换为转化为16K、16bit、单声道的wav文件
ffmpeg -y -i input.mp3 -acodec pcm_s16le -f s16le -ac 1 -ar 16000 output.wav
#将某个44.1KHz、16bit的wav文件转化为16K、16bit、单声道的wav文件
ffmpeg -y -f s16le -ar 44100 -ac 1 -i input.wav -acodec pcm_s16le -f s16le -ac 1 -ar 16000 output.wav
#将某个8K的alaw文件转化为8K、16bit、单声道的wav文件
ffmpeg -f alaw -ar 8000 -i input.wav -ar 8000 -ac 1 -acodec pcm_s16le -f s16le output.wav
#将某个8K的mulaw文件转化为8K、16bit、单声道的wav文件
ffmpeg -f mulaw -ar 8000 -i input.wav -ar 8000 -ac 1 -acodec pcm_s16le -f s16le output.wav
#将某个amr文件转化为16K、16bit、单声道的wav文件
ffmpeg -i input.wav -ar 16000 -ac 1 -acodec pcm_s16le -f s16le output.wav
```

<a id="windows操作系统下转换语音格式"></a>

<a id="e45aa4e5d1t1t"></a>

### Windows操作系统下转换语音格式

Windows系统下语音转换格式可使用转换工具，常见工具Adobe Audition、CoolEdit或其他在线、离线语音转换工具。

使用转换工具，优先打开语音，修改**导出设置**的格式后运行即可，以下是以输出16K数据为例。以Adobe Audition为例，打开**批处理**面板，单击文件夹图标添加待转换的音频文件（如test.wav）。单击底部**导出设置...**按钮，在弹出的**导出设置**对话框中设置导出位置，将**格式**选择为**Wave PCM (\*.wav, \*.bwf, \*.rf64, \*.amb)**，将**新建采样类型**设置为**16000 Hz 单声道，16 位**，单击**确定**后单击**运行**按钮执行批处理导出。

<a id="raw-opus格式数据使用"></a>

<a id="4e61b0bdf6h0n"></a>

## raw-opus格式数据使用

Opus 是一种广泛使用的开源压缩音频格式。尤其是在 **RTOS**设备上，Opus 经常作为一种默认音频编码集成。

由于 RTOS 方案上通常只具备核心的 Opus 编解码能力，没有集成 Ogg 容器，故我们开放原始 Opus 音频数据作为输入输出，并将这种音频格式（format）命名为“raw-opus”。

<a id="使用-raw-opus-进行语音识别"></a>

<a id="6e76cea1c7qlt"></a>

#### 使用“raw-opus” 进行语音识别

在您的设备端，通常可以通过操作系统提供的录音工具获取固定间隔的原始音频数据（PCM），您可以将这样一个数据包编码（ encode ）为 raw-opus 数据包，并通过接口流式地发送给多模态交互开发套件。

如果您的设备支持录音直接输出raw-opus 数据，您可以直接将这个数据包依次发送给多模态交互开发套件。

请注意设置对应的音频采样率。

<a id="使用-raw-opus-进行语音合成"></a>

<a id="cacdd65687byi"></a>

#### 使用“raw-opus” 进行语音合成

您可以设置音频格式为“raw-opus”，并设置音频采样率（sample\_rate）、帧长度（frame\_size），以便多模态交互开发套件下发对应的raw-opus 数据。

如果您在播放音频时出现异常，请检查音频合成参数以及解码参数是否对应。

<a id="典型的-raw-opus-配置"></a>

<a id="5222cd5408n58"></a>

#### 典型的“raw-opus”配置

<a id="code-block-4"></a>

```text
1. 上行采样率: upstream.sample_rate:48000
2. 上行格式: upstream.audio_format: raw-opus
3. 下行采样率: downstream.sample_rate
4. 下行格式: downstream.audio_format: raw-opus
5. 下行opus帧长: downstream.frame_size:20
```

<a id="常见问题及解决方法"></a>

<a id="9a55cf67d4zww"></a>

## 常见问题及解决方法

<a id="官网示例语音正常-换成自己待测试的语音就获取不到识别结果"></a>

<a id="15887eda19h3a"></a>

### 官网示例语音正常，换成自己待测试的语音就获取不到识别结果？

-   检查音频文件格式
    
    -   建议您检查待测试的语音格式是否符合语音识别输入格式要求。更多内容，请参见上文音频格式说明。
    -   将待测试语音转换成16K、16 bit采样位数、单声道（mono）无压缩的WAV文件。

<a id="tap2talk-duplex-模式下-发送音频没有最终结果返回"></a>

<a id="a3a1f3b167j9o"></a>

### Tap2Talk/Duplex 模式下，发送音频没有最终结果返回？

-   Tap2Talk/Duplex 模式使用云端 vad 检测音频尾点。 如果是使用音频文件调用，需要音频文件后面至少包含 800-1000ms 静音，否则识别无法结束。

<a id="语音合成的语速和我预期的不一致"></a>

<a id="cb0b47af04z5k"></a>

### 语音合成的语速和我预期的不一致？

-   检查您的播放参数设置
    
    -   请检查您播放的参数，尤其是采样率、采样位数、以及通道数。通常在播放 PCM 数据的时候，错误的设置会造成声音异常。
    -   以 Android 为例。通常客户端使用AudioTrack播放，通常的配置如下。

<a id="code-block-5"></a>

```java
AudioFormat format = new AudioFormat.Builder()
        .setSampleRate(16000)
        .setChannelMask(AudioFormat.CHANNEL_OUT_MONO)
        .setEncoding(AudioFormat.ENCODING_PCM_16BIT)
        .build();
```
