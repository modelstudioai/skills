# 非实时语音合成CosyVoice Java SDK参考

本文介绍非实时语音合成CosyVoice的Java SDK调用方法，支持非流式和流式两种调用模式。

**用户指南**：参见[非实时语音合成](https://help.aliyun.com/zh/model-studio/non-realtime-tts-user-guide)。

**重要**

该功能仅在[中国内地部署范围](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)（北京地域）下可用。

## **前提条件**

-   已[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)并将其[配置到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)
    
-   已安装符合版本要求的DashScope Java SDK，建议[安装最新版](https://help.aliyun.com/zh/model-studio/install-sdk)，SDK版本需≥2.22.15
    

## **HttpSpeechSynthesizer 类**

**包路径**：`com.alibaba.dashscope.audio.http_tts.HttpSpeechSynthesizer`

**功能**：基于HTTP的语音合成，支持非流式和流式两种调用方式。

### **构造方法**

```
public HttpSpeechSynthesizer()
```

创建HttpSpeechSynthesizer实例，使用默认配置。SDK会自动从环境变量`DASHSCOPE_API_KEY`或`Constants.apiKey`获取API Key。

### **callAndReturnAudio() - 非流式调用（返回音频数据）**

**方法签名**：

```
public ByteBuffer callAndReturnAudio(HttpSpeechSynthesisParam param) throws ApiException, NoApiKeyException, InputRequiredException
```

**参数说明**：

**参数**

**类型**

**说明**

param

[HttpSpeechSynthesisParam](#h2-cv3a4b5c)

语音合成参数对象，包含模型、文本、音色等配置。

**返回值**：`ByteBuffer`，包含完整的音频数据。可通过`remaining()`获取音频大小（字节）。

### **call() - 非流式调用（返回音频URL）**

**方法签名**：

```
public HttpSpeechSynthesisResult call(HttpSpeechSynthesisParam param) throws ApiException, NoApiKeyException, InputRequiredException
```

**参数说明**：

**参数**

**类型**

**说明**

param

[HttpSpeechSynthesisParam](#h2-cv3a4b5c)

语音合成参数对象。

**返回值**：`HttpSpeechSynthesisResult`对象，通过`getAudioInfo().getUrl()`获取音频下载URL，URL有效期有限，可通过`getAudioInfo().getExpiresAt()`获取过期时间。

### **streamCall() - 流式调用**

**方法签名**：

```
public void streamCall(HttpSpeechSynthesisParam param, ResultCallback<HttpSpeechSynthesisResult> callback) throws ApiException, NoApiKeyException, InputRequiredException
```

**参数说明**：

**参数**

**类型**

**说明**

param

[HttpSpeechSynthesisParam](#h2-cv3a4b5c)

语音合成参数对象。

callback

ResultCallback<HttpSpeechSynthesisResult>

回调对象，需实现`onEvent`（接收音频分片）、`onComplete`（合成完成）、`onError`（错误处理）三个方法。

该方法为异步调用，音频数据通过回调函数分片返回，适用于对首包延迟有要求的场景。

**ResultCallback 回调方法**：

`com.alibaba.dashscope.common.ResultCallback`是DashScope SDK提供的通用回调接口，需实现以下三个方法：

**方法**

**参数**

**说明**

onEvent

HttpSpeechSynthesisResult result

每接收到一个音频分片时触发。通过`result.hasAudioData()`判断是否包含音频数据，通过`result.getAudioDataSize()`获取分片大小。

onComplete

无

语音合成完成时触发，表示所有音频分片已接收完毕。

onError

Exception e

合成过程中发生错误时触发，可通过`e.getMessage()`获取错误信息。

## **HttpSpeechSynthesisParam 类**

**包路径**：`com.alibaba.dashscope.audio.http_tts.HttpSpeechSynthesisParam`

通过Builder模式构建参数对象。

部分参数没有专用的Builder方法，需要通过继承自父类的`parameter(String key, Object value)`方法或`parameters(Map<String, Object>)`方法进行设置，详见下表中的说明。

**方法**

**类型**

**必填**

**说明**

model(String)

String

是

语音合成模型。

取值范围：

-   cosyvoice-v3.5-plus
    
-   cosyvoice-v3.5-flash
    
-   cosyvoice-v3-plus
    
-   cosyvoice-v3-flash
    
-   cosyvoice-v2
    

text(String)

String

是

待合成文本。

支持 SSML 和 LaTeX 格式输入。将待合成文本替换为对应格式即可。

-   使用 SSML 时，需同时将 `enable_ssml` 设置为 `true`。支持的 SSML 标签及用法，请参见[SSML标记语言介绍](https://help.aliyun.com/zh/model-studio/introduction-to-cosyvoice-ssml-markup-language)。
    
-   使用 LaTeX 时，将待合成文本替换为 LaTeX 格式即可，无需额外配置。支持的 LaTeX 语法及用法，请参见[LaTeX 公式转语音](https://help.aliyun.com/zh/model-studio/latex-capability-support-description)。
    

voice(String)

String

是

音色。

取值范围：

-   系统音色：参见[音色列表](https://help.aliyun.com/zh/model-studio/cosyvoice-voice-list)
    
-   声音复刻音色：如何创建音色请参见[CosyVoice声音复刻/设计API](https://help.aliyun.com/zh/model-studio/cosyvoice-clone-design-api)
    
-   声音设计音色：如何创建音色请参见[CosyVoice声音复刻/设计API](https://help.aliyun.com/zh/model-studio/cosyvoice-clone-design-api)
    

format(String)

String

否

音频编码格式。

默认值：mp3。

取值范围：

-   mp3
    
-   pcm
    
-   wav
    
-   opus
    

sampleRate(int)

int

否

音频采样率（Hz）。

取值范围：8000, 16000, 22050（默认）, 24000, 44100, 48000。

volume(int)

int

否

音量。

默认值：50。

取值范围：\[0, 100\]。

rate(float)

float

否

语速。

默认值：1.0。

取值范围：\[0.5, 2.0\]。

pitch(float)

float

否

音调。

默认值：1.0。

取值范围：\[0.5, 2.0\]。

enable\_ssml

boolean

否

是否开启SSML功能。设置为`true`时，`text`参数需传入SSML格式文本。支持的SSML标签及用法，请参见[SSML标记语言介绍](https://help.aliyun.com/zh/model-studio/introduction-to-cosyvoice-ssml-markup-language)。

默认值：false。

**说明**

`enable_ssml`需要通过`HttpSpeechSynthesisParam`实例的`parameter`方法或者`parameters`方法进行设置：

## 通过parameter设置

```
HttpSpeechSynthesisParam param = HttpSpeechSynthesisParam.builder()
    .model("cosyvoice-v3-flash")
    .text("<speak>你好</speak>")
    .voice("longanyang")
    .parameter("enable_ssml", true)
    .build();
```

## 通过parameters设置

```
HttpSpeechSynthesisParam param = HttpSpeechSynthesisParam.builder()
    .model("cosyvoice-v3-flash")
    .text("<speak>你好</speak>")
    .voice("longanyang")
    .parameters(Collections.singletonMap("enable_ssml", true))
    .build();
```

word\_timestamp\_enabled

boolean

否

是否开启字级别时间戳。

默认值：false。

适用范围：仅适用于cosyvoice-v3-flash、cosyvoice-v3-plus和cosyvoice-v2模型的复刻音色，以及[音色列表](https://help.aliyun.com/zh/model-studio/cosyvoice-voice-list)中标记为支持的系统音色。

**说明**

`word_timestamp_enabled`需要通过`HttpSpeechSynthesisParam`实例的`parameter`方法或者`parameters`方法进行设置：

## 通过parameter设置

```
HttpSpeechSynthesisParam param = HttpSpeechSynthesisParam.builder()
    .model("cosyvoice-v3-flash")
    .text("我家的后面有一个很大的花园。")
    .voice("longanyang")
    .parameter("word_timestamp_enabled", true)
    .build();
```

## 通过parameters设置

```
HttpSpeechSynthesisParam param = HttpSpeechSynthesisParam.builder()
    .model("cosyvoice-v3-flash")
    .text("我家的后面有一个很大的花园。")
    .voice("longanyang")
    .parameters(Collections.singletonMap("word_timestamp_enabled", true))
    .build();
```

seed

int

否

生成时使用的随机数种子，使合成的效果产生变化。在模型版本、文本、音色及其他参数均相同的前提下，使用相同的seed可复现相同的合成结果。

默认值0。

取值范围：\[0, 65535\]。

**说明**

`seed`需要通过`HttpSpeechSynthesisParam`实例的`parameter`方法或者`parameters`方法进行设置：

## 通过parameter设置

```
HttpSpeechSynthesisParam param = HttpSpeechSynthesisParam.builder()
    .model("cosyvoice-v3-flash")
    .text("我家的后面有一个很大的花园。")
    .voice("longanyang")
    .parameter("seed", 1234)
    .build();
```

## 通过parameters设置

```
HttpSpeechSynthesisParam param = HttpSpeechSynthesisParam.builder()
    .model("cosyvoice-v3-flash")
    .text("我家的后面有一个很大的花园。")
    .voice("longanyang")
    .parameters(Collections.singletonMap("seed", 1234))
    .build();
```

language\_hints

List

否

**重要**

-   此参数为数组，但当前版本仅处理第一个元素，因此建议只传入一个值。
    
-   此参数用于指定语音合成的目标语言，该设置与声音复刻时的样本音频的语种无关。如需设置复刻任务的源语言，请参见声音复刻API参考。
    

指定语音合成的目标语言，提升合成效果。

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
    

**说明**

`language_hints`需要通过`HttpSpeechSynthesisParam`实例的`parameter`方法或者`parameters`方法进行设置：

## 通过parameter设置

```
HttpSpeechSynthesisParam param = HttpSpeechSynthesisParam.builder()
    .model("cosyvoice-v3-flash")
    .text("我家的后面有一个很大的花园。")
    .voice("longanyang")
    .parameter("language_hints", Arrays.asList("zh"))
    .build();
```

## 通过parameters设置

```
HttpSpeechSynthesisParam param = HttpSpeechSynthesisParam.builder()
    .model("cosyvoice-v3-flash")
    .text("我家的后面有一个很大的花园。")
    .voice("longanyang")
    .parameters(Collections.singletonMap("language_hints", Arrays.asList("zh")))
    .build();
```

instruction

String

否

设置指令，用于控制方言、情感或角色等合成效果。

具体用法请参见[非实时语音合成](https://help.aliyun.com/zh/model-studio/non-realtime-tts-user-guide)。

**说明**

`instruction`需要通过`HttpSpeechSynthesisParam`实例的`parameter`方法或者`parameters`方法进行设置：

## 通过parameter设置

```
HttpSpeechSynthesisParam param = HttpSpeechSynthesisParam.builder()
    .model("cosyvoice-v3-flash")
    .text("我家的后面有一个很大的花园。")
    .voice("longanyang")
    .parameter("instruction", "请用非常开心的语气说话。")
    .build();
```

## 通过parameters设置

```
HttpSpeechSynthesisParam param = HttpSpeechSynthesisParam.builder()
    .model("cosyvoice-v3-flash")
    .text("我家的后面有一个很大的花园。")
    .voice("longanyang")
    .parameters(Collections.singletonMap("instruction", "请用非常开心的语气说话。"))
    .build();
```

bit\_rate

int

否

音频码率（单位：kbps）。

默认值：32。

取值范围：\[6, 510\]。

**重要**

仅在`format`为`opus`时支持使用该参数。

**说明**

`bit_rate`需要通过`HttpSpeechSynthesisParam`实例的`parameter`方法或者`parameters`方法进行设置：

## 通过parameter设置

```
HttpSpeechSynthesisParam param = HttpSpeechSynthesisParam.builder()
    .model("cosyvoice-v3-flash")
    .text("我家的后面有一个很大的花园。")
    .voice("longanyang")
    .format("opus")
    .parameter("bit_rate", 32)
    .build();
```

## 通过parameters设置

```
HttpSpeechSynthesisParam param = HttpSpeechSynthesisParam.builder()
    .model("cosyvoice-v3-flash")
    .text("我家的后面有一个很大的花园。")
    .voice("longanyang")
    .format("opus")
    .parameters(Collections.singletonMap("bit_rate", 32))
    .build();
```

enable\_aigc\_tag

boolean

否

是否在生成的音频中添加AIGC隐性标识。设置为true时，会将隐性标识嵌入到支持格式（wav/mp3/opus）的音频中。

默认值：false。

仅cosyvoice-v3-flash、cosyvoice-v3-plus、cosyvoice-v2支持该功能。

**说明**

`enable_aigc_tag`需要通过`HttpSpeechSynthesisParam`实例的`parameter`方法或者`parameters`方法进行设置：

## 通过parameter设置

```
HttpSpeechSynthesisParam param = HttpSpeechSynthesisParam.builder()
    .model("cosyvoice-v3-flash")
    .text("我家的后面有一个很大的花园。")
    .voice("longanyang")
    .parameter("enable_aigc_tag", true)
    .build();
```

## 通过parameters设置

```
HttpSpeechSynthesisParam param = HttpSpeechSynthesisParam.builder()
    .model("cosyvoice-v3-flash")
    .text("我家的后面有一个很大的花园。")
    .voice("longanyang")
    .parameters(Collections.singletonMap("enable_aigc_tag", true))
    .build();
```

aigc\_propagator

String

否

设置AIGC隐性标识中的 `ContentPropagator` 字段，用于标识内容的传播者。仅在 `enable_aigc_tag` 为 `true` 时生效。

默认值：阿里云UID。

仅cosyvoice-v3-flash、cosyvoice-v3-plus、cosyvoice-v2支持该功能。

**说明**

`aigc_propagator`需要通过`HttpSpeechSynthesisParam`实例的`parameter`方法或者`parameters`方法进行设置：

## 通过parameter设置

```
HttpSpeechSynthesisParam param = HttpSpeechSynthesisParam.builder()
    .model("cosyvoice-v3-flash")
    .text("我家的后面有一个很大的花园。")
    .voice("longanyang")
    .parameter("enable_aigc_tag", true)
    .parameter("aigc_propagator", "xxxx")
    .build();
```

## 通过parameters设置

```
Map<String, Object> map = new HashMap<>();
map.put("enable_aigc_tag", true);
map.put("aigc_propagator", "xxxx");

HttpSpeechSynthesisParam param = HttpSpeechSynthesisParam.builder()
    .model("cosyvoice-v3-flash")
    .text("我家的后面有一个很大的花园。")
    .voice("longanyang")
    .parameters(map)
    .build();
```

aigc\_propagate\_id

String

否

设置AIGC隐性标识中的 `PropagateID` 字段，用于唯一标识一次具体的传播行为。仅在 `enable_aigc_tag` 为 `true` 时生效。

默认值：本次语音合成请求Request ID。

仅cosyvoice-v3-flash、cosyvoice-v3-plus、cosyvoice-v2支持该功能。

**说明**

`aigc_propagate_id`需要通过`HttpSpeechSynthesisParam`实例的`parameter`方法或者`parameters`方法进行设置：

## 通过parameter设置

```
HttpSpeechSynthesisParam param = HttpSpeechSynthesisParam.builder()
    .model("cosyvoice-v3-flash")
    .text("我家的后面有一个很大的花园。")
    .voice("longanyang")
    .parameter("enable_aigc_tag", true)
    .parameter("aigc_propagate_id", "xxxx")
    .build();
```

## 通过parameters设置

```
Map<String, Object> map = new HashMap<>();
map.put("enable_aigc_tag", true);
map.put("aigc_propagate_id", "xxxx");

HttpSpeechSynthesisParam param = HttpSpeechSynthesisParam.builder()
    .model("cosyvoice-v3-flash")
    .text("我家的后面有一个很大的花园。")
    .voice("longanyang")
    .parameters(map)
    .build();
```

hot\_fix

Map

否

文本热修复配置，用于自定义指定词语的发音或对待合成文本进行替换。

cosyvoice-v2不支持该功能。

参数介绍：

-   pronunciation：自定义发音。指定词语的拼音标注，用于纠正默认发音不准确的情况。
    
-   replace：文本替换。在语音合成前将指定词语替换为目标文本，替换后的文本将作为实际合成内容。
    

示例：

```
"hot_fix": {
  "pronunciation": [
    {"天气": "tian1 qi4"}
  ],
  "replace": [
    {"今天": "金天"}
  ]
}
```

**说明**

`hot_fix`需要通过`HttpSpeechSynthesisParam`实例的`parameter`方法或者`parameters`方法进行设置：

## 通过parameter设置

```
Map<String, Object> hotFix = new HashMap<>();

List<Map<String, String>> pronunciation = new ArrayList<>();
Map<String, String> pronItem = new HashMap<>();
pronItem.put("天气", "tian1 qi4");
pronunciation.add(pronItem);
hotFix.put("pronunciation", pronunciation);

List<Map<String, String>> replace = new ArrayList<>();
Map<String, String> replaceItem = new HashMap<>();
replaceItem.put("今天", "金天");
replace.add(replaceItem);
hotFix.put("replace", replace);

HttpSpeechSynthesisParam param = HttpSpeechSynthesisParam.builder()
    .model("cosyvoice-v3-flash")
    .text("今天天气真好。")
    .voice("longanyang")
    .parameter("hot_fix", hotFix)
    .build();
```

## 通过parameters设置

```
// 构建hotFix对象同上
HttpSpeechSynthesisParam param = HttpSpeechSynthesisParam.builder()
    .model("cosyvoice-v3-flash")
    .text("今天天气真好。")
    .voice("longanyang")
    .parameters(Collections.singletonMap("hot_fix", hotFix))
    .build();
```

enable\_markdown\_filter

boolean

否

**重要**

仅cosyvoice-v3-flash复刻音色支持该功能。

是否启用 Markdown 过滤。启用该功能后，系统在合成语音前自动过滤输入文本中的 Markdown 标记符号，避免将其朗读为文字内容。

默认值：false。

取值范围：

-   true：启用Markdown过滤
    
-   false：禁用Markdown过滤
    

**说明**

`enable_markdown_filter`需要通过`HttpSpeechSynthesisParam`实例的`parameter`方法或者`parameters`方法进行设置：

## 通过parameter设置

```
HttpSpeechSynthesisParam param = HttpSpeechSynthesisParam.builder()
    .model("cosyvoice-v3-flash")
    .text("# 标题\n正文内容")
    .voice("longanyang")
    .parameter("enable_markdown_filter", true)
    .build();
```

## 通过parameters设置

```
HttpSpeechSynthesisParam param = HttpSpeechSynthesisParam.builder()
    .model("cosyvoice-v3-flash")
    .text("# 标题\n正文内容")
    .voice("longanyang")
    .parameters(Collections.singletonMap("enable_markdown_filter", true))
    .build();
```

## **示例代码**

以下示例展示CosyVoice语音合成的非流式和流式调用方式。运行前请确保已设置环境变量`DASHSCOPE_API_KEY`。

**重要**

不同模型版本需使用对应版本的音色。例如`cosyvoice-v3-flash`和`cosyvoice-v3-plus`使用`longanyang`等音色，`cosyvoice-v2`使用`longxiaochun_v2`等音色。更换模型时请同步更换为对应版本的音色。此外，每个音色支持的语言不同，合成非中文语言时，需选择支持对应语言的音色。具体的模型与音色对应关系，请参见[音色列表](https://help.aliyun.com/zh/model-studio/cosyvoice-voice-list)。

### **非流式调用**

非流式调用会等待服务端合成完成后一次性返回结果。根据返回类型的不同，提供以下两种方式：

-   `callAndReturnAudio()`：返回音频二进制数据（ByteBuffer），适用于直接保存或处理音频的场景。
    
-   `call()`：返回音频URL，适用于需要通过URL下载音频的场景。
    

```
import com.alibaba.dashscope.audio.http_tts.AudioInfo;
import com.alibaba.dashscope.audio.http_tts.HttpSpeechSynthesisParam;
import com.alibaba.dashscope.audio.http_tts.HttpSpeechSynthesisResult;
import com.alibaba.dashscope.audio.http_tts.HttpSpeechSynthesizer;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;

import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.ByteBuffer;

public class CosyVoiceSyncExample {

    /**
     * 非流式调用示例一：返回音频数据（ByteBuffer）
     * 调用callAndReturnAudio方法，阻塞等待合成完成后返回完整音频数据。
     */
    public static void syncCallReturnAudio() {
        HttpSpeechSynthesizer synthesizer = new HttpSpeechSynthesizer();

        HttpSpeechSynthesisParam param =
            HttpSpeechSynthesisParam.builder()
                .model("cosyvoice-v3-flash")  // 更换模型时，需同步更换为对应版本的音色
                .text("我家的后面有一个很大的花园。")
                .voice("longanyang")  // 该音色适用于cosyvoice-v3系列，cosyvoice-v2请使用longxiaochun_v2等v2音色
                .format("wav")
                .sampleRate(24000)
                // 未配置环境变量时，将下行替换为：apiKey("sk-xxx")，即替换为实际的API Key
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                // 通过parameter方法设置额外参数
                // .parameter("seed", 1234)
                // .parameter("enable_ssml", true)
                .build();

        try {
            ByteBuffer audioData = synthesizer.callAndReturnAudio(param);
            if (audioData != null && audioData.hasRemaining()) {
                byte[] bytes = new byte[audioData.remaining()];
                audioData.get(bytes);

                try (FileOutputStream fos = new FileOutputStream("sync_output.wav")) {
                    fos.write(bytes);
                    System.out.println("Audio saved to sync_output.wav, size: " + bytes.length + " bytes");
                } catch (IOException e) {
                    System.err.println("Failed to save audio: " + e.getMessage());
                }
            }
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.err.println("Synthesis failed: " + e.getMessage());
        }
        System.exit(0);
    }

    /**
     * 非流式调用示例二：返回音频URL
     * 调用call方法，返回包含音频URL的结果对象，可通过URL下载音频文件。
     */
    public static void syncCallReturnUrl() {
        HttpSpeechSynthesizer synthesizer = new HttpSpeechSynthesizer();

        HttpSpeechSynthesisParam param =
            HttpSpeechSynthesisParam.builder()
                .model("cosyvoice-v3-flash")  // 更换模型时，需同步更换为对应版本的音色
                .text("我家的后面有一个很大的花园。")
                .voice("longanyang")  // 该音色适用于cosyvoice-v3系列，cosyvoice-v2请使用longxiaochun_v2等v2音色
                .format("wav")
                .sampleRate(24000)
                // 未配置环境变量时，将下行替换为：apiKey("sk-xxx")，即替换为实际的API Key
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .build();

        try {
            HttpSpeechSynthesisResult result = synthesizer.call(param);
            System.out.println("Request ID: " + result.getRequestId());

            if (result.hasAudioUrl()) {
                AudioInfo audioInfo = result.getAudioInfo();
                System.out.println("Audio URL: " + audioInfo.getUrl());
                System.out.println("Expires At: " + audioInfo.getExpiresAt());
                System.out.println("Remaining Time: " + audioInfo.getRemainingSeconds() + " seconds");
            }
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.err.println("Synthesis failed: " + e.getMessage());
        }
    }

    public static void main(String[] args) {
        // 非流式调用示例一：返回音频数据（ByteBuffer）
        // syncCallReturnAudio();
        // 非流式调用示例二：返回音频URL
        syncCallReturnUrl();
    }
}
```

### **流式调用**

流式调用通过回调函数分片返回音频数据，无需等待合成完成即可开始处理，适用于对首包延迟有要求的实时播放场景。

```
import com.alibaba.dashscope.audio.http_tts.HttpSpeechSynthesisParam;
import com.alibaba.dashscope.audio.http_tts.HttpSpeechSynthesisResult;
import com.alibaba.dashscope.audio.http_tts.HttpSpeechSynthesizer;
import com.alibaba.dashscope.common.ResultCallback;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;

import java.io.FileOutputStream;
import java.io.IOException;
import java.util.concurrent.CountDownLatch;

public class CosyVoiceStreamExample {

    public static void streamCallWithCallback() {
        HttpSpeechSynthesizer synthesizer = new HttpSpeechSynthesizer();

        HttpSpeechSynthesisParam param =
                HttpSpeechSynthesisParam.builder()
                        .model("cosyvoice-v3-flash")  // 更换模型时，需同步更换为对应版本的音色
                        .text("今天天气真好，适合出去玩。")
                        .voice("longanyang")  // 该音色适用于cosyvoice-v3系列，cosyvoice-v2请使用longxiaochun_v2等v2音色
                        .format("wav")
                        .sampleRate(24000)
                        // 未配置环境变量时，将下行替换为：apiKey("sk-xxx")，即替换为实际的API Key
                        .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                        .build();

        CountDownLatch latch = new CountDownLatch(1);

        // 新增：创建输出文件流
        try (FileOutputStream fos = new FileOutputStream("output.wav")) {

            synthesizer.streamCall(param,
                    new ResultCallback<HttpSpeechSynthesisResult>() {
                        private int chunkCount = 0;

                        @Override
                        public void onEvent(HttpSpeechSynthesisResult result) {
                            chunkCount++;
                            if (result.hasAudioData()) {
                                System.out.println("Received chunk #" + chunkCount
                                        + ", size: " + result.getAudioDataSize() + " bytes");
                                try {
                                    fos.write(result.getAudioData());
                                } catch (IOException e) {
                                    System.err.println("Failed to write audio data: " + e.getMessage());
                                }
                            }
                            if (result.getRequestId() != null) {
                                System.out.println("Request ID: " + result.getRequestId());
                            }
                        }

                        @Override
                        public void onComplete() {
                            System.out.println("Synthesis completed, total chunks: " + chunkCount);
                            System.out.println("Audio saved to output.wav");
                            latch.countDown();
                        }

                        @Override
                        public void onError(Exception e) {
                            System.err.println("Error during synthesis: " + e.getMessage());
                            latch.countDown();
                        }
                    });

            latch.await();

        } catch (ApiException | NoApiKeyException | InputRequiredException | InterruptedException e) {
            System.err.println("Failed: " + e.getMessage());
        } catch (IOException e) {
            System.err.println("Failed to create output file: " + e.getMessage());
        }
    }

    public static void main(String[] args) {
        streamCallWithCallback();
        System.exit(0);
    }
}
```
