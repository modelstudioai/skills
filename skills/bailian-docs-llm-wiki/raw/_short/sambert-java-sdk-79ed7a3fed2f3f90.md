# Sambert Java SDK

本文介绍语音合成Sambert Java SDK的参数和接口细节。

<a id="7640d5d455ayp"></a>

**用户指南：**关于模型介绍和选型建议请参见[实时语音合成-CosyVoice /Sambert](https://help.aliyun.com/zh/model-studio/text-to-speech)。

**在线体验：**暂不支持。

<a id="前提条件"></a>

<a id="48aab93a6fe63"></a>

## 前提条件

已开通服务并[获取与配置 API Key](../model-api-reference/preparations/get-api-key.md)。请[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)，而非硬编码在代码中，防范因代码泄露导致的安全风险。

-   [安装最新版DashScope SDK](../model-api-reference/preparations/install-sdk.md)。

<a id="接口地址"></a>

<a id="5505671-h2-service-endpoint"></a>

### 接口地址

SDK的接口地址需在初始化前设置为下方地址（包含WorkspaceId）。请修改 `Constants.baseWebsocketApiUrl`为对应地域的URL。

Sambert仅支持在北京地域使用。

`wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference`，调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

**设置方式**：

<a id="code-block"></a>

```java
import com.alibaba.dashscope.utils.Constants;

// 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
Constants.baseWebsocketApiUrl = "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference";
```

> **重要**
>
> 阿里云百炼为华北2（北京）地域推出了业务空间专属域名，能够为推理请求提供卓越的性能和更高的稳定性，建议从 `dashscope.aliyuncs.com` 迁移至 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`。
>
> `{WorkspaceId}`需要替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。现有域名仍可正常使用。

<a id="模型列表"></a>

<a id="57d33631f7doi"></a>

### 模型列表

> **说明**
>
> 默认采样率代表当前模型的最佳采样率，缺省条件下默认按照该采样率输出，同时支持降采样或升采样。如知妙音色，默认采样率16 kHz，使用时可以降采样到8 kHz，但升采样到48 kHz时不会有额外效果提升。

| 音色 | 音频试听（右键保存音频） | model参数 | 时间戳支持 | 适用场景 | 特色 | 语言 | 默认采样率（Hz） |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 知楠 |  | sambert-zhinan-v1 | 是 | 通用场景 | 广告男声 | 中文+英文 | 48k |
| 知琪 |  | sambert-zhiqi-v1 | 是 | 通用场景 | 温柔女声 | 中文+英文 | 48k |
| 知厨 |  | sambert-zhichu-v1 | 是 | 新闻播报 | 舌尖男声 | 中文+英文 | 48k |
| 知德 |  | sambert-zhide-v1 | 是 | 新闻播报 | 新闻男声 | 中文+英文 | 48k |
| 知佳 |  | sambert-zhijia-v1 | 是 | 新闻播报 | 标准女声 | 中文+英文 | 48k |
| 知茹 |  | sambert-zhiru-v1 | 是 | 新闻播报 | 新闻女声 | 中文+英文 | 48k |
| 知倩 |  | sambert-zhiqian-v1 | 是 | 配音解说、新闻播报 | 资讯女声 | 中文+英文 | 48k |
| 知祥 |  | sambert-zhixiang-v1 | 是 | 配音解说 | 磁性男声 | 中文+英文 | 48k |
| 知薇 |  | sambert-zhiwei-v1 | 是 | 阅读产品简介 | 萝莉女声 | 中文+英文 | 48k |
| 知浩 |  | sambert-zhihao-v1 | 是 | 通用场景 | 咨询男声 | 中文+英文 | 16k |
| 知婧 |  | sambert-zhijing-v1 | 是 | 通用场景 | 严厉女声 | 中文+英文 | 16k |
| 知茗 |  | sambert-zhiming-v1 | 是 | 通用场景 | 诙谐男声 | 中文+英文 | 16k |
| 知墨 |  | sambert-zhimo-v1 | 是 | 通用场景 | 情感男声 | 中文+英文 | 16k |
| 知娜 |  | sambert-zhina-v1 | 是 | 通用场景 | 浙普女声 | 中文+英文 | 16k |
| 知树 |  | sambert-zhishu-v1 | 是 | 通用场景 | 资讯男声 | 中文+英文 | 16k |
| 知莎 |  | sambert-zhistella-v1 | 是 | 通用场景 | 知性女声 | 中文+英文 | 16k |
| 知婷 |  | sambert-zhiting-v1 | 是 | 通用场景 | 电台女声 | 中文+英文 | 16k |
| 知笑 |  | sambert-zhixiao-v1 | 是 | 通用场景 | 资讯女声 | 中文+英文 | 16k |
| 知雅 |  | sambert-zhiya-v1 | 是 | 通用场景 | 严厉女声 | 中文+英文 | 16k |
| 知晔 |  | sambert-zhiye-v1 | 是 | 通用场景 | 青年男声 | 中文+英文 | 16k |
| 知颖 |  | sambert-zhiying-v1 | 是 | 通用场景 | 软萌童声 | 中文+英文 | 16k |
| 知媛 |  | sambert-zhiyuan-v1 | 是 | 通用场景 | 知心姐姐 | 中文+英文 | 16k |
| 知悦 |  | sambert-zhiyue-v1 | 是 | 客服 | 温柔女声 | 中文+英文 | 16k |
| 知柜 |  | sambert-zhigui-v1 | 是 | 阅读产品简介 | 直播女声 | 中文+英文 | 16k |
| 知硕 |  | sambert-zhishuo-v1 | 是 | 数字人 | 自然男声 | 中文+英文 | 16k |
| 知妙（多情感） |  | sambert-zhimiao-emo-v1 | 是 | 阅读产品简介、数字人、直播 | 多种情感女声 | 中文+英文 | 16k |
| 知猫 |  | sambert-zhimao-v1 | 是 | 阅读产品简介、配音解说、数字人、直播 | 直播女声 | 中文+英文 | 16k |
| 知伦 |  | sambert-zhilun-v1 | 是 | 配音解说 | 悬疑解说 | 中文+英文 | 16k |
| 知飞 |  | sambert-zhifei-v1 | 是 | 配音解说 | 激昂解说 | 中文+英文 | 16k |
| 知达 |  | sambert-zhida-v1 | 是 | 新闻播报 | 标准男声 | 中文+英文 | 16k |
| Camila |  | sambert-camila-v1 | 否 | 通用场景 | 西班牙语女声 | 西班牙语 | 16k |
| Perla |  | sambert-perla-v1 | 否 | 通用场景 | 意大利语女声 | 意大利语 | 16k |
| Indah |  | sambert-indah-v1 | 否 | 通用场景 | 印尼语女声 | 印尼语 | 16k |
| Clara |  | sambert-clara-v1 | 否 | 通用场景 | 法语女声 | 法语 | 16k |
| Hanna |  | sambert-hanna-v1 | 否 | 通用场景 | 德语女声 | 德语 | 16k |
| Beth |  | sambert-beth-v1 | 是 | 通用场景 | 咨询女声 | 美式英文 | 16k |
| Betty |  | sambert-betty-v1 | 是 | 通用场景 | 客服女声 | 美式英文 | 16k |
| Cally |  | sambert-cally-v1 | 是 | 通用场景 | 自然女声 | 美式英文 | 16k |
| Cindy |  | sambert-cindy-v1 | 是 | 通用场景 | 对话女声 | 美式英文 | 16k |
| Eva |  | sambert-eva-v1 | 是 | 通用场景 | 陪伴女声 | 美式英文 | 16k |
| Donna |  | sambert-donna-v1 | 是 | 通用场景 | 教育女声 | 美式英文 | 16k |
| Brian |  | sambert-brian-v1 | 是 | 通用场景 | 客服男声 | 美式英文 | 16k |
| Waan |  | sambert-waan-v1 | 否 | 通用场景 | 泰语女声 | 泰语 | 16k |

<a id="快速开始"></a>

<a id="97fdd5c2aft1r"></a>

## 快速开始

[SpeechSynthesizer类](sambert-java-sdk-79ed7a3fed2f3f90.md#adcb5e9bddbyq)提供了非流式调用和单向流式调用的接口。请根据业务场景选择合适的调用方式：

-   非流式调用：提交文本后，服务端立即处理并返回完整的语音合成结果。整个过程是阻塞式的，客户端需要等待服务端完成处理后才能继续下一步操作。适合短文本合成场景。
-   单向流式调用：将文本一次发送至服务端并实时接收语音合成结果，不允许将文本分段发送。适用于对实时性要求高的场景。

<a id="非流式调用"></a>

<a id="8341058094tc3"></a>

### 非流式调用

提交单个语音合成任务，无需调用回调方法，进行语音合成（无流式输出中间结果），最终一次性获取完整结果。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6772835871/CAEQURiBgIDHpsn4phkiIDQ0ZGE2OTk3NmY5NTRhNDVhZDQwNWE3ZGZiMzk4Yjk54709861_20241015153444.149.svg)

实例化[SpeechSynthesizer类](sambert-java-sdk-79ed7a3fed2f3f90.md#adcb5e9bddbyq)，调用`call`方法绑定[请求参数](sambert-java-sdk-79ed7a3fed2f3f90.md#a96bfa6340jdd)，进行合成并获取二进制音频数据。

<a id="accordion-点击查看完整示例"></a>

点击查看完整示例

以下示例展示了如何使用同步接口调用发音人模型知厨（sambert-zhichu-v1），将文案”今天天气怎么样”合成采样率为48kHz，音频格式为wav的音频，并保存到名为output.wav的文件中。

<a id="code-block-2"></a>

```java
import com.alibaba.dashscope.audio.tts.SpeechSynthesizer;
import com.alibaba.dashscope.audio.tts.SpeechSynthesisParam;
import com.alibaba.dashscope.audio.tts.SpeechSynthesisAudioFormat;
import com.alibaba.dashscope.utils.Constants;

import java.io.*;
import java.nio.ByteBuffer;

public class Main {
    public static void syncAudioDataToFile() {
        SpeechSynthesizer synthesizer = new SpeechSynthesizer();
        SpeechSynthesisParam param = SpeechSynthesisParam.builder()
                // 若没有将API Key配置到环境变量中，需将下面这行代码注释放开，并将apiKey替换为自己的API Key
                // .apiKey("yourApikey")
                .model("sambert-zhichu-v1")
                .text("今天天气怎么样")
                .sampleRate(48000)
                .format(SpeechSynthesisAudioFormat.WAV)
                .build();

        File file = new File("output.wav");
        // 提交同步合成任务，获取完整的音频数据
        ByteBuffer audio = synthesizer.call(param);
        try (FileOutputStream fos = new FileOutputStream(file)) {
            fos.write(audio.array());
            System.out.println("synthesis done!");
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    public static void main(String[] args) {
        // 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
        Constants.baseWebsocketApiUrl = "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference";
        syncAudioDataToFile();
        System.exit(0);
    }
}
```

<a id="单向流式调用"></a>

<a id="ba023aacfbr84"></a>

### 单向流式调用

提交单个语音合成任务，通过回调的方式流式输出中间结果，合成结果通过`ResultCallback`中的回调方法流式进行获取。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6772835871/CAEQVRiBgMDN2_qhrBkiIGJlMTQ5MDY4YWJlZTQxYWY5ZWEzOTZiNTVjOGEwZjZh4709861_20241015153444.149.svg)

实例化[SpeechSynthesizer类](sambert-java-sdk-79ed7a3fed2f3f90.md#adcb5e9bddbyq)，调用`call`方法绑定[请求参数](sambert-java-sdk-79ed7a3fed2f3f90.md#a96bfa6340jdd)和[回调接口（ResultCallback）](sambert-java-sdk-79ed7a3fed2f3f90.md#3639e1cb40mxi)并开始语音合成，通过[回调接口（ResultCallback）](sambert-java-sdk-79ed7a3fed2f3f90.md#3639e1cb40mxi)的`onEvent`方法实时获取合成结果。

语音合成完成后（[回调接口（ResultCallback）](sambert-java-sdk-79ed7a3fed2f3f90.md#3639e1cb40mxi)的`onComplete`方法被回调之后），还可以调用[SpeechSynthesizer类](sambert-java-sdk-79ed7a3fed2f3f90.md#adcb5e9bddbyq)的`getAudioData`和`getTimestamps`方法，一次性获取完整的音频和时间戳结果。

<a id="accordion-点击查看完整示例-2"></a>

点击查看完整示例

以下示例展示了如何使用流式接口调用发音人模型知厨（sambert-zhichu-v1）将文案”今天天气怎么样”合成采样率为48kHz，默认音频格式（wav）的流式音频，并获取对应时间戳。

<a id="code-block-3"></a>

```java
import com.alibaba.dashscope.audio.tts.SpeechSynthesisParam;
import com.alibaba.dashscope.audio.tts.SpeechSynthesisResult;
import com.alibaba.dashscope.audio.tts.SpeechSynthesizer;
import com.alibaba.dashscope.common.ResultCallback;
import com.alibaba.dashscope.utils.Constants;

import java.util.concurrent.CountDownLatch;

public class Main {
    public static void main(String[] args) {
        // 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
        Constants.baseWebsocketApiUrl = "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference";
        CountDownLatch latch = new CountDownLatch(1);
        SpeechSynthesizer synthesizer = new SpeechSynthesizer();
        SpeechSynthesisParam param = SpeechSynthesisParam.builder()
                // 若没有将API Key配置到环境变量中，需将下面这行代码注释放开，并将apiKey替换为自己的API Key
                // .apiKey("yourApikey")
                .model("sambert-zhichu-v1")
                .text("今天天气怎么样")
                .sampleRate(48000)
                .enableWordTimestamp(true)
                .enablePhonemeTimestamp(true)
                .build();

        class ReactCallback extends ResultCallback<SpeechSynthesisResult> {
            @Override
            public void onEvent(SpeechSynthesisResult result) {
                if (result.getAudioFrame() != null) {
                    // do something with the audio frame
                    System.out.println("audio result length: " + result.getAudioFrame().array().length);
                }
                if (result.getTimestamp() != null) {
                    // do something with the timestamp
                    System.out.println("timestamp: " + result.getTimestamp());
                }
            }

            @Override
            public void onComplete() {
                // do something when the synthesis is done
                System.out.println("onComplete!");
                latch.countDown();
            }

            @Override
            public void onError(Exception e) {
                // do something when an error occurs
                System.out.println("onError:" + e);
                latch.countDown();
            }
        }

        synthesizer.call(param, new ReactCallback());
        try {
            latch.await();
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
        System.exit(0);
    }
}
```

<a id="通过flowable调用"></a>

<a id="b0f81fef83ojo"></a>

### 通过Flowable调用

Flowable是一个用于工作流和业务流程管理的开源框架，它基于Apache 2.0许可证发布。关于Flowable的使用，请参见[Flowable API详情](http://reactivex.io/RxJava/2.x/javadoc/)。

<a id="accordion-点击查看完整示例-3"></a>

点击查看完整示例

以下示例展示了通过`Flowable`对象的`blockingForEach`接口，阻塞式地获取每次流式返回的[音频数据和时间戳信息（SpeechSynthesisResult）](sambert-java-sdk-79ed7a3fed2f3f90.md#a727da82951p6)。

您也可以在Flowable的所有流式数据返回完成后，通过[SpeechSynthesizer类](sambert-java-sdk-79ed7a3fed2f3f90.md#adcb5e9bddbyq)的`getAudioData`和`getTimestamps`方法分别获取完整的合成结果和完整的时间戳。

<a id="code-block-4"></a>

```java
import com.alibaba.dashscope.audio.tts.SpeechSynthesisParam;
import com.alibaba.dashscope.audio.tts.SpeechSynthesisResult;
import com.alibaba.dashscope.audio.tts.SpeechSynthesizer;
import com.alibaba.dashscope.utils.Constants;
import io.reactivex.Flowable;

public class Main {
    public static void main(String[] args) {
        // 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
        Constants.baseWebsocketApiUrl = "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference";
        SpeechSynthesizer synthesizer = new SpeechSynthesizer();
        SpeechSynthesisParam param = SpeechSynthesisParam.builder()
                // 若没有将API Key配置到环境变量中，需将下面这行代码注释放开，并将apiKey替换为自己的API Key
                // .apiKey("yourApikey")
                .model("sambert-zhichu-v1")
                .text("今天天气怎么样")
                .sampleRate(48000)
                .enableWordTimestamp(true)
                .build();

        Flowable<SpeechSynthesisResult> flowable = synthesizer.streamCall(param);
        flowable.blockingForEach(
                msg -> {
                    if (msg.getAudioFrame() != null) {
                        // do something with the audio frame
                        System.out.println("getAudioFrame");
                    }
                    if (msg.getTimestamp() != null) {
                        // do something with the timestamp
                        System.out.println("getTimestamp");
                    }
                }
        );
        System.exit(0);
    }
}
```

<a id="高并发调用"></a>

<a id="e8c4348a9f53z"></a>

### 高并发调用

对象池配置、并发调用完整示例及异常处理请参见[语音合成最佳实践](../model-user-guide/model-experience/speech-and-audio/speech-synthesis/tts-high-concurrency-best-practices.md#sambert-java)。

<a id="请求参数"></a>

<a id="a96bfa6340jdd"></a>

## 请求参数

通过`SpeechSynthesisParam`的链式方法配置模型、待合成文本等参数。配置完成的对象传入[SpeechSynthesizer类](sambert-java-sdk-79ed7a3fed2f3f90.md#adcb5e9bddbyq)的`call`方法中使用。

<a id="accordion-点击查看示例"></a>

点击查看示例

<a id="code-block-5"></a>

```java
SpeechSynthesisParam param = SpeechSynthesisParam.builder()
                .model("sambert-zhichu-v1")
                .text("今天天气怎么样")
                .sampleRate(48000)
                .enableWordTimestamp(true)
                .build();
```

<table><thead><tr><th><strong>参数</strong></th><th><strong>类型</strong></th><th><strong>默认值</strong></th><th><strong>是否必须</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><p>model</p></td><td><p>String</p></td><td><ul><li></li></ul></td><td><p>是</p></td><td><p>指定用于语音合成的音色模型名，完整列表请参见<a href="sambert-java-sdk-79ed7a3fed2f3f90.md#57d33631f7doi">模型列表</a>。</p></td></tr><tr><td><p>text</p></td><td><p>String</p></td><td><ul><li></li></ul></td><td><p>是</p></td><td><p>指定待合成文本，要求采用UTF-8编码且不能为空。</p><p>最高字符限制：1万字符。</p><blockquote><p>字符计算规则：1个汉字、1个英文字母、1个标点或1个句子中间空格均算作1个字符。</p></blockquote><p>支持SSML格式。SSML标记语言的使用请参见<a href="https://help.aliyun.com/zh/isi/developer-reference/ssml-overview">SSML标记语言介绍</a>。</p></td></tr><tr><td><p>format</p></td><td><p>enum</p></td><td><p>WAV</p></td><td><p>否</p></td><td><p>指定合成音频的编码格式，支持下列格式：</p><ul><li>SpeechSynthesisAudioFormat.PCM</li><li>SpeechSynthesisAudioFormat.WAV</li><li>SpeechSynthesisAudioFormat.MP3</li></ul><p><code>SpeechSynthesisAudioFormat</code>通过“<code>import com.alibaba.dashscope.audio.tts.SpeechSynthesisAudioFormat;</code>”的方式引入。</p></td></tr><tr><td><p>sampleRate</p></td><td><p>int</p></td><td><p>16000</p></td><td><p>否</p></td><td><p>指定合成音频的采样率（单位：Hz），建议使用模型默认采样率（参见<a href="sambert-java-sdk-79ed7a3fed2f3f90.md#57d33631f7doi">模型列表</a>），如果不匹配，服务会进行必要的升降采样处理。</p></td></tr><tr><td><p>volume</p></td><td><p>int</p></td><td><p>50</p></td><td><p>否</p></td><td><p>指定合成音频的音量，取值范围是0~100。</p></td></tr><tr><td><p>rate</p></td><td><p>float</p></td><td><p>1.0</p></td><td><p>否</p></td><td><p>指定合成音频的语速，取值范围：0.5~2。</p><ul><li>0.5：表示默认语速的0.5倍速。</li><li>1：表示默认语速。默认语速是指模型默认输出的合成语速，语速会因发音人不同而略有不同。约每秒钟4个字。</li><li>2：表示默认语速的2倍速。</li></ul></td></tr><tr><td><p>pitch</p></td><td><p>float</p></td><td><p>1.0</p></td><td><p>否</p></td><td><p>指定合成音频的语调，取值范围：0.5~2。</p></td></tr><tr><td><p>enableWordTimestamp</p></td><td><p>boolean</p></td><td><p>false</p></td><td><p>否</p></td><td><p>是否开启字级别时间戳。默认不开启。</p></td></tr><tr><td><p>enablePhonemeTimestamp</p></td><td><p>boolean</p></td><td><p>false</p></td><td><p>否</p></td><td><p>是否在开启字级别时间戳（<code>enableWordTimestamp</code>为<code>true</code>）的基础上，进一步显示音素级别时间戳。默认不开启。</p></td></tr><tr><td><p>apiKey</p></td><td><p>String</p></td><td><ul><li></li></ul></td><td><p>否</p></td><td><p>用户API Key。</p></td></tr></tbody></table>

<a id="接口参考"></a>

<a id="843fb17087zct"></a>

<a id="关键接口"></a>

## 接口参考

<a id="speechsynthesizer类"></a>

<a id="adcb5e9bddbyq"></a>

### `SpeechSynthesizer`类

`SpeechSynthesizer`可以通过“`import com.alibaba.dashscope.audio.tts.SpeechSynthesizer;`”方式引入。它的关键接口如下：

<table><thead><tr><th><strong>接口/方法</strong></th><th><strong>参数</strong></th><th><strong>返回值</strong></th><th><strong>描述</strong></th></tr></thead><tbody><tr><td><a id="code-block-6"></a><pre class="language-java"><code>public ByteBuffer call(SpeechSynthesisParam param)
</code></pre></td><td><p><code>param</code>：<a href="sambert-java-sdk-79ed7a3fed2f3f90.md#a96bfa6340jdd">请求参数</a></p></td><td><p>二进制音频</p></td><td><p>发送待合成文本并获取语音合成结果。该方法阻塞当前线程直到所有结果返回。</p></td></tr><tr><td><a id="code-block-7"></a><pre class="language-java"><code>public void call(SpeechSynthesisParam param, ResultCallback&lt;SpeechSynthesisResult&gt; callback)
</code></pre></td><td><ul><li><code>param</code>：<a href="sambert-java-sdk-79ed7a3fed2f3f90.md#a96bfa6340jdd">请求参数</a></li><li><code>callback</code>：<a href="sambert-java-sdk-79ed7a3fed2f3f90.md#3639e1cb40mxi">回调接口（ResultCallback）</a></li></ul></td><td><p>无</p></td><td><p>异步开启语音合成任务。</p><p>任务开启后，服务端会通过回调的方式调用<code>ResultCallback</code>实例的方法，将关键流程信息和数据返回给客户端。</p></td></tr><tr><td><a id="code-block-8"></a><pre class="language-java"><code>public ByteBuffer getAudioData()
</code></pre></td><td><p>无</p></td><td><p>二进制音频</p></td><td><p>获取完整的二进制音频数据。</p><p>单向流式调用时，完成回调后（<code>ResultCallback</code>的<code>onComplete</code>方法被调用之后）可以使用该方法一次性获取完整的音频。</p></td></tr><tr><td><a id="code-block-9"></a><pre class="language-java"><code>public List&lt;Sentence&gt; getTimestamps()
</code></pre></td><td><p>无</p></td><td><p><a href="sambert-java-sdk-79ed7a3fed2f3f90.md#6a6d7363490w6">句子级别时间戳信息（Sentence）</a>的<code>List</code>集合</p></td><td><p>获取完整的<a href="sambert-java-sdk-79ed7a3fed2f3f90.md#6a6d7363490w6">句子级别时间戳信息（Sentence）</a>。</p><p>单向流式调用时，完成回调后（<code>ResultCallback</code>的<code>onComplete</code>方法被调用之后）可以使用该方法一次性获取完整的时间戳。</p></td></tr><tr><td><a id="code-block-10"></a><pre class="language-java"><code>public String getLastRequestId()
</code></pre></td><td><p>无</p></td><td><p>当前任务的request ID</p></td><td><p>获取当前任务的request ID，在调用<code>call</code>开始新任务之后可以使用。</p></td></tr><tr><td><a id="code-block-11"></a><pre class="language-java"><code>public long getFirstPackageDelay()
</code></pre></td><td><p>无</p></td><td><p>当前任务首包延迟</p></td><td><p>获取当前任务的首包延迟，任务结束后使用。</p></td></tr></tbody></table>

<a id="回调接口-resultcallback"></a>

<a id="3639e1cb40mxi"></a>

### 回调接口（`ResultCallback`）

[单向流式调用](sambert-java-sdk-79ed7a3fed2f3f90.md#ba023aacfbr84)时，通过回调接口`ResultCallback`获取合成结果。

<a id="accordion-点击查看示例-2"></a>

点击查看示例

<a id="code-block-12"></a>

```java
ResultCallback<SpeechSynthesisResult> callback = new ResultCallback<SpeechSynthesisResult>() {
    @Override
    public void onEvent(SpeechSynthesisResult result) {
        System.out.println("RequestId为：" + result.getRequestId());
        // 在此实现处理语音合成结果的逻辑
    }

    @Override
    public void onComplete() {
        System.out.println("任务完成");
    }

    @Override
    public void onError(Exception e) {
        System.out.println("任务失败：" + e.getMessage());
    }
};
```

<table><thead><tr><th><strong>接口/方法</strong></th><th><strong>参数</strong></th><th><strong>返回值</strong></th><th><strong>描述</strong></th></tr></thead><tbody><tr><td><a id="code-block-13"></a><pre class="language-java"><code>public void onEvent(SpeechSynthesisResult result)
</code></pre></td><td><p><code>result</code>：<a href="sambert-java-sdk-79ed7a3fed2f3f90.md#a727da82951p6">音频数据和时间戳信息（SpeechSynthesisResult）</a></p></td><td><p>无</p></td><td><p>当服务端返回合成数据时会被回调。</p></td></tr><tr><td><a id="code-block-14"></a><pre class="language-java"><code>public void onComplete()
</code></pre></td><td><p>无</p></td><td><p>无</p></td><td><p>当所有合成数据全部返回后被回调。</p></td></tr><tr><td><a id="code-block-15"></a><pre class="language-java"><code>public void onError(Exception e)
</code></pre></td><td><p><code>e</code>：异常信息</p></td><td><p>无</p></td><td><p>当调用过程出现异常以及服务返回错误后被回调。</p></td></tr></tbody></table>

<a id="响应结果"></a>

<a id="7157e59867m4x"></a>

### 响应结果

[非流式调用](sambert-java-sdk-79ed7a3fed2f3f90.md#8341058094tc3)：响应结果为二进制音频数据。

[单向流式调用](sambert-java-sdk-79ed7a3fed2f3f90.md#ba023aacfbr84)：响应结果为[音频数据和时间戳信息（SpeechSynthesisResult）](sambert-java-sdk-79ed7a3fed2f3f90.md#a727da82951p6)。

<a id="音频数据和时间戳信息-speechsynthesisresult"></a>

<a id="a727da82951p6"></a>

#### 音频数据和时间戳信息（`SpeechSynthesisResult`）

`SpeechSynthesisResult`封装了语音合成结果，常用的接口为`getAudioFrame`和`getTimestamp`。

<table><thead><tr><th><strong>接口/方法</strong></th><th><strong>参数</strong></th><th><strong>返回值</strong></th><th><strong>描述</strong></th></tr></thead><tbody><tr><td><a id="code-block-16"></a><pre class="language-java"><code>public ByteBuffer getAudioFrame()
</code></pre></td><td><p>无</p></td><td><p>二进制音频数据</p></td><td><p>返回一个流式合成片段的增量二进制音频数据，可能为空。</p></td></tr><tr><td><a id="code-block-17"></a><pre class="language-java"><code>public List&lt;Sentence&gt; getTimestamp()
</code></pre></td><td><p>无</p></td><td><p><a href="sambert-java-sdk-79ed7a3fed2f3f90.md#6a6d7363490w6">句子级别时间戳信息（Sentence）</a>的<code>List</code>集合</p></td><td><p>批量获取句子级别时间戳信息，可能为空。</p></td></tr></tbody></table>

<a id="句子级别时间戳信息-sentence"></a>

<a id="6a6d7363490w6"></a>

#### 句子级别时间戳信息（`Sentence`）

`Sentence`封装了句子级别时间戳信息。

<table><thead><tr><th><strong>接口/方法</strong></th><th><strong>参数</strong></th><th><strong>返回值</strong></th><th><strong>描述</strong></th></tr></thead><tbody><tr><td><a id="code-block-18"></a><pre class="language-java"><code>public int getBeginTime()
</code></pre></td><td><p>无</p></td><td><p>句子开始时间，单位为ms</p></td><td><p>返回句子开始时间。</p></td></tr><tr><td><a id="code-block-19"></a><pre class="language-java"><code>public int getEndTime()
</code></pre></td><td><p>无</p></td><td><p>句子结束时间，单位为ms</p></td><td><p>返回句子结束时间。</p></td></tr><tr><td><a id="code-block-20"></a><pre class="language-java"><code>public List&lt;Word&gt; getWords()
</code></pre></td><td><p>无</p></td><td><p><a href="sambert-java-sdk-79ed7a3fed2f3f90.md#216af8dfafag2">字级别时间戳信息（Word）</a>的<code>List</code>集合</p></td><td><p>批量获取字级别时间戳信息，可能为空。</p></td></tr></tbody></table>

<a id="字级别时间戳信息-word"></a>

<a id="216af8dfafag2"></a>

#### 字级别时间戳信息（`Word`）

`Word`封装了字级别时间戳信息。

<table><thead><tr><th><strong>接口/方法</strong></th><th><strong>参数</strong></th><th><strong>返回值</strong></th><th><strong>描述</strong></th></tr></thead><tbody><tr><td><a id="code-block-21"></a><pre class="language-java"><code>public int getBeginTime()
</code></pre></td><td><p>无</p></td><td><p>词开始时间，单位为ms</p></td><td><p>返回词开始时间。</p></td></tr><tr><td><a id="code-block-22"></a><pre class="language-java"><code>public int getEndTime()
</code></pre></td><td><p>无</p></td><td><p>词结束时间，单位为ms</p></td><td><p>返回词结束时间。</p></td></tr><tr><td><a id="code-block-23"></a><pre class="language-java"><code>public String getText()
</code></pre></td><td><p>无</p></td><td><p>文本信息</p></td><td><p>返回文本信息。</p></td></tr><tr><td><a id="code-block-24"></a><pre class="language-java"><code>public List&lt;Phoneme&gt; getPhonemes()
</code></pre></td><td><p>无</p></td><td><p><a href="sambert-java-sdk-79ed7a3fed2f3f90.md#05e7893c08and">音素级别时间戳信息（Phoneme）</a>的<code>List</code>集合</p></td><td><p>批量获取音素级别时间戳信息，可能为空。</p></td></tr></tbody></table>

<a id="音素级别时间戳信息-phoneme"></a>

<a id="05e7893c08and"></a>

#### 音素级别时间戳信息（`Phoneme`）

`Phoneme`封装了音素级别时间戳信息。

<table><thead><tr><th><strong>接口/方法</strong></th><th><strong>参数</strong></th><th><strong>返回值</strong></th><th><strong>描述</strong></th></tr></thead><tbody><tr><td><a id="code-block-25"></a><pre class="language-java"><code>public int getBeginTime()
</code></pre></td><td><p>无</p></td><td><p>音素开始时间，单位为ms</p></td><td><p>返回音素开始时间。</p></td></tr><tr><td><a id="code-block-26"></a><pre class="language-java"><code>public int getEndTime()
</code></pre></td><td><p>无</p></td><td><p>音素结束时间，单位为ms</p></td><td><p>返回音素结束时间。</p></td></tr><tr><td><a id="code-block-27"></a><pre class="language-java"><code>public String getText()
</code></pre></td><td><p>无</p></td><td><p>文本信息</p></td><td><p>返回文本信息。</p></td></tr><tr><td><a id="code-block-28"></a><pre class="language-java"><code>public String getTone()
</code></pre></td><td><p>无</p></td><td><p>音调</p></td><td><p>返回音调。</p><ul><li>英文中，0、1、2分别代表轻音、重音和次重音。</li><li>拼音中，1、2、3、4、5分别代表一声、二声、三声、四声和轻声。</li></ul></td></tr></tbody></table>

<a id="更多示例"></a>

<a id="4b46ba65680pp"></a>

## 更多示例

更多示例，请参见[GitHub](https://github.com/aliyun/alibabacloud-bailian-speech-demo)。

<a id="错误码"></a>

<a id="a370386972oa4"></a>

## 错误码

在使用API过程中，如果调用失败并返回错误信息，请参见[错误码](../model-api-reference/preparations/error-code.md)进行解决。
