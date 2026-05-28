# 实时语音合成CosyVoice Java SDK

通过DashScope Java SDK进行CosyVoice语音合成。

**用户指南：**关于模型介绍和选型建议请参见[语音合成](https://help.aliyun.com/zh/model-studio/tts-model/)。

## **服务端点**

SDK默认使用**北京地域**的服务端点。如需切换到其他地域，需在初始化前修改 `Constants.baseWebsocketApiUrl`。

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

`wss://dashscope.aliyuncs.com/api-ws/v1/inference`

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

`wss://dashscope-intl.aliyuncs.com/api-ws/v1/inference`

**切换到新加坡地域**：

```
import com.alibaba.dashscope.common.Constants;

// 在代码开头设置
Constants.baseWebsocketApiUrl = "wss://dashscope-intl.aliyuncs.com/api-ws/v1/inference";
```

## **SpeechSynthesizer**

**包路径**：`com.alibaba.dashscope.audio.ttsv2.SpeechSynthesizer`

### **构造方法**

```
public SpeechSynthesizer(SpeechSynthesisParam param, ResultCallback<SpeechSynthesisResult> callback)
```

**参数说明**：

-   `param`：语音合成参数，通过`[SpeechSynthesisParam](#sec-5k9m2p7r).builder()`构建
    
-   `callback`：回调函数，用于流式调用。非流式调用时传入null
    

### **call() - 非流式/单向流式合成**

**方法签名**：

```
public ByteBuffer call(String text)
```

**参数说明**：

**参数**

**类型**

**必填**

**说明**

text

String

是

待合成的文本，长度不得超过20000字符。

**返回值**：`ByteBuffer` 或 null。非流式调用时返回完整音频数据；单向流式调用时音频通过回调返回，此方法返回null。

### **streamingCall() - 双向流式合成**

**方法签名**：

```
public void streamingCall(String text)
```

**参数说明**：

**参数**

**类型**

**必填**

**说明**

text

String

是

待合成的文本，长度不得超过20000字符。可多次调用追加文本。

### **streamingComplete() - 结束双向流式调用**

**方法签名**：

```
public void streamingComplete()
```

结束双向流式调用，通知服务端所有文本已发送完毕。

### **callAsFlowable() - 单向流式合成（响应式）**

**方法签名**：

```
public Flowable<SpeechSynthesisResult> callAsFlowable(String text)
```

**参数说明**：

**参数**

**类型**

**必填**

**说明**

text

String

是

待合成的文本。

**返回值**：`Flowable<[SpeechSynthesisResult](#sec-7m5k9p2r)>` 响应式流。

### **streamingCallAsFlowable() - 双向流式合成（响应式）**

**方法签名**：

```
public Flowable<SpeechSynthesisResult> streamingCallAsFlowable(Flowable<String> textStream)
```

**参数说明**：

**参数**

**类型**

**必填**

**说明**

textStream

Flowable<String>

是

文本的响应式流。

**返回值**：`Flowable<[SpeechSynthesisResult](#sec-7m5k9p2r)>` 响应式流。

### **getDuplexApi().close() - 关闭WebSocket连接**

**方法签名**：

```
public boolean getDuplexApi().close(int code, String reason)
```

**参数说明**：

**参数**

**类型**

**必填**

**说明**

code

int

是

关闭码。

reason

String

是

关闭原因。

**返回值**：`boolean`，是否成功关闭。

### **getLastRequestId() - 获取请求ID**

**方法签名**：

```
public String getLastRequestId()
```

**返回值**：`String`，请求ID。

### **getFirstPackageDelay() - 获取首包延迟**

**方法签名**：

```
public long getFirstPackageDelay()
```

**返回值**：`long`，首包延迟（ms），从发送第一包到收到首包结果。

## **SpeechSynthesisParam**

**包路径**：`com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisParam`

**示例**：

```
SpeechSynthesisParam param = SpeechSynthesisParam.builder()
    .model("cosyvoice-v3-flash") // 模型
    .voice("longanyang") // 音色
    .format(SpeechSynthesisAudioFormat.WAV_8000HZ_MONO_16BIT) // 音频编码格式、采样率
    .volume(50) // 音量，取值范围：[0, 100]
    .speechRate(1.0f) // 语速，取值范围：[0.5, 2]
    .pitchRate(1.0f) // 语调，取值范围：[0.5, 2]
    .build();
```

### Builder 方法

**方法**

**参数类型**

**必填**

**说明**

`model(String)`

String

是

模型名称。

`voice(String)`

String

是

**voice** `_string_` **（必选）**

语音合成所使用的音色。

-   **系统音色**：参见[音色列表](https://help.aliyun.com/zh/model-studio/cosyvoice-voice-list)
    
-   **复刻音色**：通过声音复刻功能定制
    
-   **声音设计音色**：通过声音设计功能定制
    

`format(SpeechSynthesisAudioFormat)`

enum

否

音频编码格式及采样率。

`cosyvoice-v1`不支持opus格式。

默认值：SpeechSynthesisAudioFormat.MP3\_22050HZ\_MONO\_256KBPS。

SpeechSynthesisAudioFormat包路径：`com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisAudioFormat`。

`volume(int)`

int

否

音量。

默认值：50。

取值范围：\[0, 100\]。

`speechRate(float)`

float

否

语速。

默认值：1.0。

取值范围：\[0.5, 2.0\]。

`pitchRate(float)`

float

否

音调。

默认值：1.0。

取值范围：\[0.5, 2.0\]。

`enableWordTimestamp(boolean)`

boolean

否

是否开启字级别时间戳。

默认值：false。

适用范围：仅适用于cosyvoice-v3-flash、cosyvoice-v3-plus和cosyvoice-v2模型的复刻音色，以及[音色列表](https://help.aliyun.com/zh/model-studio/cosyvoice-voice-list)中标记为支持的系统音色。

`seed(int)`

int

否

生成时使用的随机数种子，使合成的效果产生变化。在模型版本、文本、音色及其他参数均相同的前提下，使用相同的seed可复现相同的合成结果。

默认值0。

取值范围：\[0, 65535\]。

cosyvoice-v1不支持该参数。

SDK版本低于2.21.7时，`seed`需要通过扩展参数进行设置。

`languageHints(List<String>)`

List<String>

否

**重要**

-   此参数为数组，但当前版本仅处理第一个元素，因此建议只传入一个值。
    
-   此参数用于指定语音合成的目标语言，该设置与声音复刻时的样本音频的语种无关。如需设置复刻任务的源语言，请参见声音复刻API参考。
    

指定语音合成的目标语言，提升合成效果。cosyvoice-v1不支持该功能。

当数字、缩写、符号等朗读方式或者小语种合成效果不符合预期时使用，例如：

-   数字朗读方式不符合预期，“hello, this is 110”读成“hello, this is one one zero”而非“hello, this is 幺幺零”
    
-   符号朗读不准确，“@”读成“艾特”而非“at”
    
-   小语种合成效果差，合成不自然
    

取值范围：

-   zh：中文
    
-   en：英文
    
-   fr：法语
    
-   de：德语
    
-   ja：日语
    
-   ko：韩语
    
-   ru：俄语
    
-   pt：葡萄牙语
    
-   th：泰语
    
-   id：印尼语
    
-   vi：越南语
    

`instruction(String)`

String

否

设置指令，用于控制方言、情感或角色等合成效果。

使用说明请参见[指令控制](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#12884a10929p9)。

`hotFix(ParamHotFix)`

ParamHotFix

否

文本热修复配置，用于自定义指定词语的发音或对待合成文本进行替换。

cosyvoice-v2、cosyvoice-v1不支持该功能。

参数介绍：

-   pronunciation：自定义发音。指定词语的拼音标注，用于纠正默认发音不准确的情况。
    
-   replace：文本替换。在语音合成前将指定词语替换为目标文本，替换后的文本将作为实际合成内容。
    

示例：

```
List<ParamHotFix.PronunciationItem> pronunciationItems = new ArrayList<>();
pronunciationItems.add(new ParamHotFix.PronunciationItem("天气", "tian1 qi4"));

List<ParamHotFix.ReplaceItem> replaceItems = new ArrayList<>();
replaceItems.add(new ParamHotFix.ReplaceItem("今天", "金天"));

ParamHotFix paramHotFix = new ParamHotFix();
paramHotFix.setPronunciation(pronunciationItems);
paramHotFix.setReplace(replaceItems);

SpeechSynthesisParam param = SpeechSynthesisParam.builder()
                        .model("cosyvoice-v3-flash") // 模型
                        .voice("your_voice") // 替换成cosyvoice-v3-flash复刻音色
                        .hotFix(paramHotFix)
                        .build();
```

`parameter(String key, Object value)`

String, Object

否

设置[扩展参数](#8135356d13pvn)。

`parameters(Map<String, Object>)`

Map

否

设置[扩展参数](#8135356d13pvn)。

### 扩展参数

通过 `parameter()` 或 `parameters()` 设置。

**示例**：

```
SpeechSynthesisParam param = SpeechSynthesisParam.builder()
  .model("cosyvoice-v3-flash")
  .voice("longanyang")
  .parameter("enable_markdown_filter", true)
  .build();
```

**参数名**

**类型**

**必填**

**说明**

`bit_rate`

integer

否

音频码率（kbps）。音频格式为opus时，支持通过`bit_rate`参数调整码率。

默认值：32。

取值范围：\[6, 510\]。

`cosyvoice-v1`模型不支持该参数。

`enable_aigc_tag`

boolean

否

是否在生成的音频中添加AIGC隐性标识。设置为true时，会将隐性标识嵌入到支持格式（wav/mp3/opus）的音频中。

默认值：false。

仅cosyvoice-v3-flash、cosyvoice-v3-plus、cosyvoice-v2支持该功能。

`aigc_propagator`

String

否

设置AIGC隐性标识中的 `ContentPropagator` 字段，用于标识内容的传播者。仅在 `enable_aigc_tag` 为 `true` 时生效。

默认值：阿里云UID。

仅cosyvoice-v3-flash、cosyvoice-v3-plus、cosyvoice-v2支持该功能。

`aigc_propagate_id`

String

否

设置AIGC隐性标识中的 `PropagateID` 字段，用于唯一标识一次具体的传播行为。仅在 `enable_aigc_tag` 为 `true` 时生效。

默认值：本次语音合成请求Request ID。

仅cosyvoice-v3-flash、cosyvoice-v3-plus、cosyvoice-v2支持该功能。

`enable_markdown_filter`

boolean

否

**重要**

仅cosyvoice-v3-flash复刻音色支持该功能。

是否启用 Markdown 过滤。启用该功能后，系统在合成语音前自动过滤输入文本中的 Markdown 标记符号，避免将其朗读为文字内容。

默认值：false。

取值范围：

-   true：启用Markdown过滤
    
-   false：禁用Markdown过滤
    

## **ResultCallback**

**包路径**：`com.alibaba.dashscope.common.ResultCallback`

### **onEvent() - 接收音频数据**

**方法签名**：

```
public void onEvent(SpeechSynthesisResult result)
```

**参数说明**：

**参数**

**类型**

**必填**

**说明**

result

[SpeechSynthesisResult](#sec-7m5k9p2r)

是

接收到合成事件时触发，包含音频帧、时间戳信息和输出信息（事件类型、原始文本等）。

### **onComplete() - 合成完成**

**方法签名**：

```
public void onComplete()
```

语音合成完成时触发。

### **onError() - 错误处理**

**方法签名**：

```
public void onError(Exception e)
```

**参数说明**：

**参数**

**类型**

**必填**

**说明**

e

Exception

是

发生错误时触发，包含异常信息。

## **SpeechSynthesisResult**

**包路径**：`com.alibaba.dashscope.audio.tts.SpeechSynthesisResult`

### **getAudioFrame() - 获取音频数据帧**

**方法签名**：

```
public ByteBuffer getAudioFrame()
```

**返回值**：`ByteBuffer`，音频数据帧。

### **getTimestamp() - 获取时间戳信息**

**方法签名**：

```
public Sentence getTimestamp()
```

**返回值**：`[Sentence](#sec-sentence-ts)`，时间戳信息。

### **getOutput() - 获取输出信息**

**方法签名**：

```
public JsonObject getOutput()
```

**返回值**：`com.google.gson.JsonObject`，合成事件的[输出信息](#sec-output-info)，包含事件类型和文本内容。需要SDK版本 >= 2.22.0。

### 句子级别时间戳信息（`Sentence`）

`Sentence`封装了句子级别时间戳信息。

#### **getBeginTime() - 获取句子开始时间**

**方法签名**：

```
public int getBeginTime()
```

**返回值**：句子开始时间，单位为ms。

#### **getEndTime() - 获取句子结束时间**

**方法签名**：

```
public int getEndTime()
```

**返回值**：句子结束时间，单位为ms。

#### **getWords() - 获取字级别时间戳**

**方法签名**：

```
public List<Word> getWords()
```

**返回值**：[Word](#h4-word-ts)的`List`集合，批量获取字级别时间戳信息，可能为空。

### 字级别时间戳信息（`Word`）

`Word`封装了字级别时间戳信息。

#### **getBeginTime() - 获取词开始时间**

**方法签名**：

```
public int getBeginTime()
```

**返回值**：词开始时间，单位为ms。

#### **getEndTime() - 获取词结束时间**

**方法签名**：

```
public int getEndTime()
```

**返回值**：词结束时间，单位为ms。

#### **getText() - 获取文本信息**

**方法签名**：

```
public String getText()
```

**返回值**：`String`，文本信息。

#### **getPhonemes() - 获取音素级别时间戳**

**方法签名**：

```
public List<Phoneme> getPhonemes()
```

**返回值**：[Phoneme](#h4-phoneme-ts)的`List`集合，批量获取音素级别时间戳信息，可能为空。

### 音素级别时间戳信息（`Phoneme`）

`Phoneme`封装了音素级别时间戳信息。

#### **getBeginTime() - 获取音素开始时间**

**方法签名**：

```
public int getBeginTime()
```

**返回值**：音素开始时间，单位为ms。

#### **getEndTime() - 获取音素结束时间**

**方法签名**：

```
public int getEndTime()
```

**返回值**：音素结束时间，单位为ms。

#### **getText() - 获取文本信息**

**方法签名**：

```
public String getText()
```

**返回值**：`String`，文本信息。

#### **getTone() - 获取音调**

**方法签名**：

```
public int getTone()
```

**返回值**：音调。

-   英文中，0、1、2分别代表轻音、重音和次重音。
    
-   拼音中，1、2、3、4、5分别代表一声、二声、三声、四声和轻声。
    

### 输出信息（`output`）

`getOutput()`返回`JsonObject`，封装了合成事件的输出信息。在`onEvent`回调或Flowable流中获取。包含以下字段：

**字段**

**类型**

**说明**

type

String

事件类型。取值：`sentence-begin`（句子开始，返回待合成的文本内容）、`sentence-synthesis`（标识音频数据块，表示当前正在合成音频）、`sentence-end`（句子结束，返回文本内容和字级别时间戳）。

original\_text

String

当前句子的原始文本内容。在`sentence-begin`和`sentence-end`事件中返回。

sentence

JsonObject

句子信息，包含句子编号（`index`）和字级别时间戳（`words`）。在`sentence-end`事件中包含完整的字级别时间戳信息。

## **示例代码**

SDK提供了语音合成的关键接口，支持以下几种调用方式：

-   非流式调用：阻塞式，一次性发送完整文本，直接返回完整音频。适合短文本语音合成场景。
    
-   单向流式调用：非阻塞式，一次性发送完整文本，通过回调函数接收音频数据（可能分片）。适用于对实时性要求高的短文本语音合成场景。
    
-   双向流式调用：非阻塞式，可分多次发送文本片段，通过回调函数实时接收增量合成的音频流。适合实时性要求高的长文本语音合成场景。
    

更多示例，请参见[GitHub](https://github.com/aliyun/alibabacloud-bailian-speech-demo)。

### **非流式调用**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9933679771/CAEQURiBgIDHpsn4phkiIDQ0ZGE2OTk3NmY5NTRhNDVhZDQwNWE3ZGZiMzk4Yjk54709861_20241015153444.149.svg)

发送的文本长度不得超过20000字符。

**重要**

每次调用`call`方法前，需要重新初始化`SpeechSynthesizer`实例。

```
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisParam;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesizer;
import com.alibaba.dashscope.utils.Constants;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.ByteBuffer;

public class Main {
    // 模型
    private static String model = "cosyvoice-v3-flash";
    // 音色
    private static String voice = "longanyang";

    public static void streamAudioDataToSpeaker() {
        // 请求参数
        SpeechSynthesisParam param =
                SpeechSynthesisParam.builder()
                        // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                        // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                        .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                        .model(model) // 模型
                        .voice(voice) // 音色
                        .build();

        // 同步模式：禁用回调（第二个参数为null）
        SpeechSynthesizer synthesizer = new SpeechSynthesizer(param, null);
        ByteBuffer audio = null;
        try {
            // 阻塞直至音频返回
            audio = synthesizer.call("今天天气怎么样？");
        } catch (Exception e) {
            throw new RuntimeException(e);
        } finally {
            // 任务结束关闭websocket连接
            synthesizer.getDuplexApi().close(1000, "bye");
        }
        if (audio != null) {
            // 将音频数据保存到本地文件"output.mp3"中
            File file = new File("output.mp3");
            // 首次发送文本时需建立 WebSocket 连接，因此首包延迟会包含连接建立的耗时
            System.out.println(
                    "[Metric] requestId为："
                            + synthesizer.getLastRequestId()
                            + "首包延迟（毫秒）为："
                            + synthesizer.getFirstPackageDelay());
            try (FileOutputStream fos = new FileOutputStream(file)) {
                fos.write(audio.array());
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        }
    }

    public static void main(String[] args) {
        // 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：wss://dashscope-intl.aliyuncs.com/api-ws/v1/inference
        Constants.baseWebsocketApiUrl = "wss://dashscope.aliyuncs.com/api-ws/v1/inference";
        streamAudioDataToSpeaker();
        System.exit(0);
    }
}
```

### **单向流式调用**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9933679771/CAEQVRiBgMCfo..hrBkiIGEyMjNkZjVlMWZiYzRhZDU4ZjEyZjdjMmMzYjM1YzMz4709861_20241015153444.149.svg)

发送的文本长度不得超过20000字符。

**重要**

每次调用`call`方法前，需要重新初始化`SpeechSynthesizer`实例。

```
import com.alibaba.dashscope.audio.tts.SpeechSynthesisResult;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisParam;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesizer;
import com.alibaba.dashscope.common.ResultCallback;
import com.alibaba.dashscope.utils.Constants;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.concurrent.CountDownLatch;

class TimeUtils {
    private static final DateTimeFormatter formatter =
            DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss.SSS");

    public static String getTimestamp() {
        return LocalDateTime.now().format(formatter);
    }
}

public class Main {
    // 模型
    private static String model = "cosyvoice-v3-flash";
    // 音色
    private static String voice = "longanyang";

    public static void streamAudioDataToSpeaker() {
        CountDownLatch latch = new CountDownLatch(1);

        // 实现回调接口ResultCallback
        ResultCallback<SpeechSynthesisResult> callback = new ResultCallback<SpeechSynthesisResult>() {
            @Override
            public void onEvent(SpeechSynthesisResult result) {
                if (result.getAudioFrame() != null) {
                    // 此处实现保存音频数据到本地的逻辑
                    System.out.println(TimeUtils.getTimestamp() + " 收到音频");
                }
                // 获取输出信息，包含事件类型和原始文本
                if (result.getOutput() != null && result.getOutput().has("type")) {
                    System.out.println("事件类型: " + result.getOutput().get("type").getAsString()
                            + ", 原始文本: " + (result.getOutput().has("original_text") ? result.getOutput().get("original_text").getAsString() : ""));
                }
            }

            @Override
            public void onComplete() {
                System.out.println(TimeUtils.getTimestamp() + " 收到Complete，语音合成结束");
                latch.countDown();
            }

            @Override
            public void onError(Exception e) {
                System.out.println("出现异常：" + e.toString());
                latch.countDown();
            }
        };

        // 请求参数
        SpeechSynthesisParam param =
                SpeechSynthesisParam.builder()
                        // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                        // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                        .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                        .model(model) // 模型
                        .voice(voice) // 音色
                        .build();
        // 第二个参数"callback"传入回调即启用异步模式
        SpeechSynthesizer synthesizer = new SpeechSynthesizer(param, callback);
        // 非阻塞调用，立即返回null（实际结果通过回调接口异步传递），在回调接口的onEvent方法中实时获取二进制音频
        try {
            synthesizer.call("今天天气怎么样？");
            // 等待合成完成
            latch.await();
            // 等待播放线程全部播放完
        } catch (Exception e) {
            throw new RuntimeException(e);
        } finally {
            // 任务结束后关闭websocket连接
            synthesizer.getDuplexApi().close(1000, "bye");
        }
        // 首次发送文本时需建立 WebSocket 连接，因此首包延迟会包含连接建立的耗时
        System.out.println(
                "[Metric] requestId为："
                        + synthesizer.getLastRequestId()
                        + "，首包延迟（毫秒）为："
                        + synthesizer.getFirstPackageDelay());
    }

    public static void main(String[] args) {
        // 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：wss://dashscope-intl.aliyuncs.com/api-ws/v1/inference
        Constants.baseWebsocketApiUrl = "wss://dashscope.aliyuncs.com/api-ws/v1/inference";
        streamAudioDataToSpeaker();
        System.exit(0);
    }
}
```

### 双向流式调用

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0043679771/CAEQVRiBgICHxPGhrBkiIGE3ZTVmMzY0YzI3NzQxYTFiYWE2MmU2NTBhMDgzZGM14709861_20241015153444.149.svg)

单次发送文本长度不得超过 20000 字符，且累计发送文本总长度不得超过 20 万字符。

-   流式输入时可多次调用`streamingCall`按顺序提交文本片段。服务端接收文本片段后自动进行分句：
    
    -   完整语句立即合成
        
    -   不完整语句缓存至完整后合成
        
    
    调用 `streamingComplete` 时，服务端会强制合成所有已接收但未处理的文本片段（包括未完成的句子）。
    
-   发送文本片段的间隔不得超过23秒，否则触发“request timeout after 23 seconds”异常。
    
    若无待发送文本，需及时调用 `streamingComplete`结束任务。
    
    **重要**
    
    请务必确保调用`streamingComplete`方法，否则可能会导致结尾部分的文本无法成功转换为语音。
    
    > 服务端强制设定23秒超时机制，客户端无法修改该配置。
    

```
import com.alibaba.dashscope.audio.tts.SpeechSynthesisResult;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisAudioFormat;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisParam;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesizer;
import com.alibaba.dashscope.common.ResultCallback;
import com.alibaba.dashscope.utils.Constants;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

class TimeUtils {
    private static final DateTimeFormatter formatter =
            DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss.SSS");

    public static String getTimestamp() {
        return LocalDateTime.now().format(formatter);
    }
}

public class Main {
    private static String[] textArray = {"流式文本语音合成SDK，",
            "可以将输入的文本", "合成为语音二进制数据，", "相比于非流式语音合成，",
            "流式合成的优势在于实时性", "更强。用户在输入文本的同时",
            "可以听到接近同步的语音输出，", "极大地提升了交互体验，",
            "减少了用户等待时间。", "适用于调用大规模", "语言模型（LLM），以",
            "流式输入文本的方式", "进行语音合成的场景。"};
    private static String model = "cosyvoice-v3-flash"; // 模型
    private static String voice = "longanyang"; // 音色

    public static void streamAudioDataToSpeaker() {
        // 配置回调函数
        ResultCallback<SpeechSynthesisResult> callback = new ResultCallback<SpeechSynthesisResult>() {
            @Override
            public void onEvent(SpeechSynthesisResult result) {
                // System.out.println("收到消息: " + result);
                if (result.getAudioFrame() != null) {
                    // 此处实现处理音频数据的逻辑
                    System.out.println(TimeUtils.getTimestamp() + " 收到音频");
                }
            }

            @Override
            public void onComplete() {
                System.out.println(TimeUtils.getTimestamp() + " 收到Complete，语音合成结束");
            }

            @Override
            public void onError(Exception e) {
                System.out.println("出现异常：" + e.toString());
            }
        };

        // 请求参数
        SpeechSynthesisParam param =
                SpeechSynthesisParam.builder()
                        // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                        // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                        .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                        .model(model)
                        .voice(voice)
                        .format(SpeechSynthesisAudioFormat
                                .PCM_22050HZ_MONO_16BIT) // 流式合成使用PCM或者MP3
                        .build();
        SpeechSynthesizer synthesizer = new SpeechSynthesizer(param, callback);
        // 带Callback的call方法将不会阻塞当前线程
        try {
            for (String text : textArray) {
                // 发送文本片段，在回调接口的onEvent方法中实时获取二进制音频
                synthesizer.streamingCall(text);
            }
            // 等待结束流式语音合成
            synthesizer.streamingComplete();
        } catch (Exception e) {
            throw new RuntimeException(e);
        } finally {
            // 任务结束关闭websocket连接
            synthesizer.getDuplexApi().close(1000, "bye");
        }

        // 首次发送文本时需建立 WebSocket 连接，因此首包延迟会包含连接建立的耗时
        System.out.println(
                "[Metric] requestId为："
                        + synthesizer.getLastRequestId()
                        + "，首包延迟（毫秒）为："
                        + synthesizer.getFirstPackageDelay());
    }

    public static void main(String[] args) {
        // 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：wss://dashscope-intl.aliyuncs.com/api-ws/v1/inference
        Constants.baseWebsocketApiUrl = "wss://dashscope.aliyuncs.com/api-ws/v1/inference";
        streamAudioDataToSpeaker();
        System.exit(0);
    }
}
```

### **通过Flowable调用**

Flowable是一个用于工作流和业务流程管理的开源框架，它基于Apache 2.0许可证发布。关于Flowable的使用，请参见[Flowable API详情](http://reactivex.io/RxJava/2.x/javadoc/)。

使用Flowable前需确保已集成RxJava库，并了解响应式编程基础概念。

单次发送文本长度不得超过 20000 字符，且累计发送文本总长度不得超过 20 万字符。

## 单向流式调用

以下示例展示了通过Flowable对象的`blockingForEach`接口，阻塞式地获取每次流式返回的`SpeechSynthesisResult`类型数据。

```
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisParam;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesizer;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.Constants;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

class TimeUtils {
    private static final DateTimeFormatter formatter =
            DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss.SSS");

    public static String getTimestamp() {
        return LocalDateTime.now().format(formatter);
    }
}

public class Main {
    private static String model = "cosyvoice-v3-flash"; // 模型
    private static String voice = "longanyang"; // 音色

    public static void streamAudioDataToSpeaker() throws NoApiKeyException {
        // 请求参数
        SpeechSynthesisParam param =
                SpeechSynthesisParam.builder()
                        // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                        // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                        .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                        .model(model) // 模型
                        .voice(voice) // 音色
                        .build();
        SpeechSynthesizer synthesizer = new SpeechSynthesizer(param, null);
        synthesizer.callAsFlowable("今天天气怎么样?").blockingForEach(result -> {
            if (result.getAudioFrame() != null) {
                // 此处实现处理音频数据的逻辑
                System.out.println(TimeUtils.getTimestamp() + " 收到音频");
            }
            // 获取输出信息，包含事件类型和原始文本
            if (result.getOutput() != null && result.getOutput().has("type")) {
                System.out.println("事件类型: " + result.getOutput().get("type").getAsString()
                        + ", 原始文本: " + (result.getOutput().has("original_text") ? result.getOutput().get("original_text").getAsString() : ""));
            }
        });
        // 任务结束关闭 WebSocket 连接
        synthesizer.getDuplexApi().close(1000, "bye");
        // 首次发送文本时需建立 WebSocket 连接，因此首包延迟会包含连接建立的耗时
        System.out.println(
                "[Metric] requestId为："
                        + synthesizer.getLastRequestId()
                        + "首包延迟（毫秒）为："
                        + synthesizer.getFirstPackageDelay());
    }

    public static void main(String[] args) throws NoApiKeyException {
        // 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：wss://dashscope-intl.aliyuncs.com/api-ws/v1/inference
        Constants.baseWebsocketApiUrl = "wss://dashscope.aliyuncs.com/api-ws/v1/inference";
        streamAudioDataToSpeaker();
        System.exit(0);
    }
}
```

## 双向流式调用

以下示例展示了通过Flowable对象作为输入参数，输入文本流。并通过Flowable对象作为返回值，利用的`blockingForEach`接口，阻塞式地获取每次流式返回的`SpeechSynthesisResult`类型数据。

```
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisParam;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesizer;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.Constants;
import io.reactivex.BackpressureStrategy;
import io.reactivex.Flowable;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

class TimeUtils {
    private static final DateTimeFormatter formatter =
            DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss.SSS");

    public static String getTimestamp() {
        return LocalDateTime.now().format(formatter);
    }
}

public class Main {
    private static String[] textArray = {"流式文本语音合成SDK，",
            "可以将输入的文本", "合成为语音二进制数据，", "相比于非流式语音合成，",
            "流式合成的优势在于实时性", "更强。用户在输入文本的同时",
            "可以听到接近同步的语音输出，", "极大地提升了交互体验，",
            "减少了用户等待时间。", "适用于调用大规模", "语言模型（LLM），以",
            "流式输入文本的方式", "进行语音合成的场景。"};
    private static String model = "cosyvoice-v3-flash";
    private static String voice = "longanyang";

    public static void streamAudioDataToSpeaker() throws NoApiKeyException {
        // 模拟流式输入
        Flowable<String> textSource = Flowable.create(emitter -> {
            new Thread(() -> {
                for (int i = 0; i < textArray.length; i++) {
                    emitter.onNext(textArray[i]);
                    try {
                        Thread.sleep(1000);
                    } catch (InterruptedException e) {
                        throw new RuntimeException(e);
                    }
                }
                emitter.onComplete();
            }).start();
        }, BackpressureStrategy.BUFFER);

        // 请求参数
        SpeechSynthesisParam param =
                SpeechSynthesisParam.builder()
                        // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                        // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                        .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                        .model(model) // 模型
                        .voice(voice) // 音色
                        .build();
        SpeechSynthesizer synthesizer = new SpeechSynthesizer(param, null);
        synthesizer.streamingCallAsFlowable(textSource).blockingForEach(result -> {
            if (result.getAudioFrame() != null) {
                // 此处实现播放音频的逻辑
                System.out.println(
                        TimeUtils.getTimestamp() +
                                " 二进制音频大小为：" + result.getAudioFrame().capacity());
            }
            // 获取输出信息，包含事件类型和原始文本
            if (result.getOutput() != null && result.getOutput().has("type")) {
                System.out.println("事件类型: " + result.getOutput().get("type").getAsString()
                        + ", 原始文本: " + (result.getOutput().has("original_text") ? result.getOutput().get("original_text").getAsString() : ""));
            }
        });
        synthesizer.getDuplexApi().close(1000, "bye");
        // 首次发送文本时需建立 WebSocket 连接，因此首包延迟会包含连接建立的耗时
        System.out.println(
                "[Metric] requestId为："
                        + synthesizer.getLastRequestId()
                        + "，首包延迟（毫秒）为："
                        + synthesizer.getFirstPackageDelay());
    }

    public static void main(String[] args) throws NoApiKeyException {
        // 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：wss://dashscope-intl.aliyuncs.com/api-ws/v1/inference
        Constants.baseWebsocketApiUrl = "wss://dashscope.aliyuncs.com/api-ws/v1/inference";
        streamAudioDataToSpeaker();
        System.exit(0);
    }
}
```

### **高并发调用**

在DashScope Java SDK中，采用了OkHttp3的连接池技术，以减少重复建立连接的开销。详情请参见[高并发最佳实践](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#ug-hc-h3)。
