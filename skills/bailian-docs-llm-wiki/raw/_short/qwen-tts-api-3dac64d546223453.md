# 非实时语音合成（Qwen-TTS）API参考

非实时语音合成（Qwen-TTS）API 的请求参数与返回字段说明。

<table><tbody><tr><td><a id="58f39efa90jby"></a><h2>请求体</h2></td><td rowspan="3"><div><a id="sec-tabs"></a><section><a id="非流式输出"></a><section><a id="非流式输出-h4"></a><h4>非流式输出</h4><a id="sec-tabs-2"></a><section><a id="python"></a><section><a id="python-h4"></a><h4>Python</h4><blockquote><p>DashScope Python SDK 2.0 中，非实时语音合成通过<code>client.audio.tts.http</code>资源调用。</p></blockquote><a id="code-block"></a><pre class="language-python"><code># 请安装 DashScope SDK 的最新版本
import os
import dashscope

# 以下为华北2（北京）地域的配置，调用时请将&quot;{WorkspaceId}&quot;替换为真实的业务空间ID，各地域的配置不同。
client = dashscope.Client(
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    workspace=&quot;{WorkspaceId}&quot;,
    region=&quot;cn-beijing&quot;,
)

text = &quot;那我来给大家推荐一款T恤，这款呢真的是超级好看，这个颜色呢很显气质，而且呢也是搭配的绝佳单品，大家可以闭眼入，真的是非常好看，对身材的包容性也很好，不管啥身材的宝宝呢，穿上去都是很好看的。推荐宝宝们下单哦。&quot;
result = client.audio.tts.http.synthesize(
    text,
    model=&quot;qwen3-tts-flash&quot;,
    voice=&quot;Cherry&quot;
)
print(result.audio_url, result.audio_id, result.expires_at)
</code></pre></section><a id="java"></a><section><a id="java-h4"></a><h4>Java</h4><a id="code-block-2"></a><pre class="language-java"><code>// 请安装 DashScope SDK 的最新版本
import com.alibaba.dashscope.aigc.multimodalconversation.AudioParameters;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.JsonUtils;
import com.alibaba.dashscope.utils.Constants;

public class Main {
    private static final String MODEL = &quot;qwen3-tts-flash&quot;;
    public static void call() throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                .model(MODEL)
                // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：apiKey(&quot;sk-xxx&quot;)
                .apiKey(System.getenv(&quot;DASHSCOPE_API_KEY&quot;))
                .text(&quot;Today is a wonderful day to build something people love!&quot;)
                .voice(AudioParameters.Voice.CHERRY)
                .parameter(&quot;language_type&quot;, &quot;English&quot;)
                .build();
        MultiModalConversationResult result = conv.call(param);
        System.out.println(JsonUtils.toJson(result));
    }
    public static void main(String[] args) {
        // 以下为华北2（北京）地域的配置。
        Constants.baseHttpApiUrl = &quot;https://dashscope.aliyuncs.com/api/v1&quot;;
        try {
            call();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
</code></pre></section><a id="curl"></a><section><a id="curl-h4"></a><h4>curl</h4><a id="code-block-3"></a><pre class="language-bash"><code># ======= 重要提示 =======
# 以下为华北2（北京）地域的配置。
# 新加坡地域和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 若没有配置环境变量，请用阿里云百炼API Key将$DASHSCOPE_API_KEY替换为：sk-xxx。
# === 执行时请删除该注释 ===

curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
-H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
-H 'Content-Type: application/json' \
-d '{
    &quot;model&quot;: &quot;qwen3-tts-flash&quot;,
    &quot;input&quot;: {
        &quot;text&quot;: &quot;那我来给大家推荐一款T恤，这款呢真的是超级好看，这个颜色呢很显气质，而且呢也是搭配的绝佳单品，大家可以闭眼入，真的是非常好看，对身材的包容性也很好，不管啥身材的宝宝呢，穿上去都是很好看的。推荐宝宝们下单哦。&quot;,
        &quot;voice&quot;: &quot;Cherry&quot;,
        &quot;language_type&quot;: &quot;Chinese&quot;
    }
}'
</code></pre></section></section></section><a id="流式输出"></a><section><a id="流式输出-h4"></a><h4>流式输出</h4><a id="sec-tabs-3"></a><section><a id="python-2"></a><section><a id="python-2-h4"></a><h4>Python</h4><blockquote><p>DashScope Python SDK 2.0 中，非实时语音合成通过<code>client.audio.tts.http</code>资源调用。</p></blockquote><a id="code-block-4"></a><pre class="language-python"><code># DashScope SDK 版本不低于 2.0.1
import os
import dashscope

# 以下为华北2（北京）地域的配置，调用时请将&quot;{WorkspaceId}&quot;替换为真实的业务空间ID，各地域的配置不同。
client = dashscope.Client(
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    workspace=&quot;{WorkspaceId}&quot;,
    region=&quot;cn-beijing&quot;,
)

text = &quot;那我来给大家推荐一款T恤，这款呢真的是超级好看，这个颜色呢很显气质，而且呢也是搭配的绝佳单品，大家可以闭眼入，真的是非常好看，对身材的包容性也很好，不管啥身材的宝宝呢，穿上去都是很好看的。推荐宝宝们下单哦。&quot;
for chunk in client.audio.tts.http.stream(
    text,
    model=&quot;qwen3-tts-flash&quot;,
    voice=&quot;Cherry&quot;,
):
    # chunk.audio 为已解码的音频字节（bytes），chunk.is_final 为 True 时携带整段音频 URL
    print(chunk)
</code></pre></section><a id="java-2"></a><section><a id="java-2-h4"></a><h4>Java</h4><a id="code-block-5"></a><pre class="language-java"><code>// DashScope SDK 版本需要不低于 2.19.0
import com.alibaba.dashscope.aigc.multimodalconversation.AudioParameters;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.JsonUtils;
import com.alibaba.dashscope.utils.Constants;
import io.reactivex.Flowable;

public class Main {
    private static final String MODEL = &quot;qwen3-tts-flash&quot;;
    public static void streamCall() throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                .model(MODEL)
                // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：apiKey(&quot;sk-xxx&quot;)
                .apiKey(System.getenv(&quot;DASHSCOPE_API_KEY&quot;))
                .text(&quot;Today is a wonderful day to build something people love!&quot;)
                .voice(AudioParameters.Voice.CHERRY)
                .parameter(&quot;language_type&quot;, &quot;English&quot;)
                .build();
        Flowable&lt;MultiModalConversationResult&gt; result = conv.streamCall(param);
        result.blockingForEach(r -&gt; {System.out.println(JsonUtils.toJson(r));
        });
    }
    public static void main(String[] args) {
        // 以下为华北2（北京）地域的配置。
        Constants.baseHttpApiUrl = &quot;https://dashscope.aliyuncs.com/api/v1&quot;;
        try {
            streamCall();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
</code></pre></section><a id="curl-2"></a><section><a id="curl-2-h4"></a><h4>curl</h4><a id="code-block-6"></a><pre class="language-bash"><code># ======= 重要提示 =======
# 以下为华北2（北京）地域的配置。
# 新加坡地域和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 若没有配置环境变量，请用阿里云百炼API Key将$DASHSCOPE_API_KEY替换为：sk-xxx。
# === 执行时请删除该注释 ===

curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
-H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
-H 'Content-Type: application/json' \
-H 'X-DashScope-SSE: enable' \
-d '{
    &quot;model&quot;: &quot;qwen3-tts-flash&quot;,
    &quot;input&quot;: {
        &quot;text&quot;: &quot;那我来给大家推荐一款T恤，这款呢真的是超级好看，这个颜色呢很显气质，而且呢也是搭配的绝佳单品，大家可以闭眼入，真的是非常好看，对身材的包容性也很好，不管啥身材的宝宝呢，穿上去都是很好看的。推荐宝宝们下单哦。&quot;,
        &quot;voice&quot;: &quot;Cherry&quot;,
        &quot;language_type&quot;: &quot;Chinese&quot;
    }
}'
</code></pre></section></section><p>实时播放 Base64 音频的方法请参见<a href="qwen-tts-api-3dac64d546223453.md#qwen-tts-streaming-playback">流式播放</a>。</p></section></section></div></td></tr><tr><td><p><strong>model</strong><code>string</code><strong>（必选）</strong></p><p>模型名称，详情请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-synthesis/non-realtime-tts-user-guide.md#4a43cc1bb7kxg">支持的模型</a>。</p></td></tr><tr><td><p><strong>input</strong><code>object</code><strong>（必选）</strong></p><p>输入参数<strong>。</strong></p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>text</strong> <code>string</code> <strong>（必选）</strong></p><p>要合成的文本，支持多语种混合输入。最大输入长度为 600 字符。</p><p><strong>voice</strong> <code>string</code> <strong>（必选）</strong></p><p>使用的音色，参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-synthesis/non-realtime-tts-user-guide.md#bac280ddf5a1u">支持的系统音色</a>。</p><p><strong>language_type</strong> <code>string</code> （可选）</p><p>合成音频的语种。默认为 <code>Auto</code>。</p><ul><li><p><code>Auto</code>：适用于文本包含多种语言或语种不确定的场景。模型自动为不同语言片段匹配发音，但无法保证完全精准。</p></li><li><p>指定语种：适用于单一语种文本。指定具体语种能显著提升合成质量，效果通常优于 <code>Auto</code>。可选值：</p><ul><li><code>Chinese</code></li><li><code>English</code></li><li><code>German</code></li><li><code>Italian</code></li><li><code>Portuguese</code></li><li><code>Spanish</code></li><li><code>Japanese</code></li><li><code>Korean</code></li><li><code>French</code></li><li><code>Russian</code></li></ul></li></ul></div></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="cd3063363egdc"></a><h2>返回对象（流式与非流式输出格式一致）</h2></td><td rowspan="7"><div><a id="fig-code-group"></a><div><a id="fig-code-group-千问3-tts-flash-tab"></a>千问3-TTS-Flash<div><a id="code-code-group-千问3-tts-flash"></a><pre class="language-json"><code>{
    &quot;status_code&quot;: 200,
    &quot;request_id&quot;: &quot;5c63c65c-cad8-4bf4-959d-xxxxxxxxxxxx&quot;,
    &quot;code&quot;: &quot;&quot;,
    &quot;message&quot;: &quot;&quot;,
    &quot;output&quot;: {
        &quot;text&quot;: null,
        &quot;finish_reason&quot;: &quot;stop&quot;,
        &quot;choices&quot;: null,
        &quot;audio&quot;: {
            &quot;data&quot;: &quot;&quot;,
            &quot;url&quot;: &quot;http://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/1d/ab/20251218/d2033070/39b6d8f2-c0db-4daa-9073-5d27bfb66b78.wav?Expires=1766113409&amp;OSSAccessKeyId=YOUR_ACCESS_KEY_ID&amp;Signature=YOUR_SIGNATURE&quot;,
            &quot;id&quot;: &quot;audio_5c63c65c-cad8-4bf4-959d-xxxxxxxxxxxx&quot;,
            &quot;expires_at&quot;: 1766113409
        }
    },
    &quot;usage&quot;: {
        &quot;input_tokens&quot;: 0,
        &quot;output_tokens&quot;: 0,
        &quot;characters&quot;: 195
    }
}
</code></pre></div></div></div></td></tr><tr><td><p><strong>status_code</strong> <code>integer</code></p><p>HTTP状态码。遵循 <a href="https://www.rfc-editor.org/rfc/rfc9110.html#name-status-codes">RFC 9110</a>标准定义。例如：<br>• <code>200</code>：请求成功，正常返回结果<br>• <code>400</code>：客户端请求参数错误<br>• <code>401</code>：未授权访问<br>• <code>404</code>：资源未找到<br>• <code>500</code>：服务器内部错误。<br></p></td></tr><tr><td><p><strong>request_id</strong> <code>string</code></p><p>本次请求的唯一标识，可用于问题排查。</p></td></tr><tr><td><p><strong>code</strong> <code>string</code></p><p>请求失败时展示错误码（参见<a href="../model-api-reference/preparations/error-code.md">错误码</a>）。</p></td></tr><tr><td><p><strong>message</strong> <code>string</code></p><p>请求失败时展示错误信息（参见<a href="../model-api-reference/preparations/error-code.md">错误码</a>）。</p></td></tr><tr><td><p><strong>output</strong><code>object</code></p><p>模型的输出。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>text</strong><code>string</code></p><p>始终为null，无需关注该参数。</p><p><strong>choices</strong><code>string</code></p><p>始终为null，无需关注该参数。</p><p><strong>finish_reason</strong><code>string</code></p><p>生成状态标识：</p><ul><li>正在生成时为&quot;null&quot;；</li><li>模型输出自然结束或触发了停止条件时为 &quot;stop&quot;。</li></ul><p><strong>audio</strong> <code>object</code></p><p>模型输出的音频信息。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>url</strong> <code>string</code></p><p>完整音频文件的 URL，有效期 24 小时。</p><div><div><p><strong>说明</strong>流式输出说明：流式模式下，API 返回多个 chunk。中间 chunk 的 audio.data 包含 Base64 编码的音频片段，audio.url 为空；最后一个 chunk 的 audio.data 为空字符串，audio.url 包含完整音频文件的 <strong>OSS</strong> 地址。开发者可在最后一个 chunk 中通过 url 字段下载完整音频。非流式模式下，该字段直接返回完整音频文件 URL。</p></div></div><p><strong>data</strong> <code>string</code></p><p>Base64 编码的音频数据。非流式输出和流式输出的中间 chunk 中返回 Base64 编码的音频片段；流式输出的最后一个 chunk 中该字段为空字符串，音频通过同级的 url 字段获取。</p><p><strong>id</strong> <code>string</code></p><p>音频的唯一标识。</p><p><strong>expires_at</strong> <code>integer</code></p><p>URL 过期时间的 UNIX 时间戳。</p></div></section></div></section></td></tr><tr><td><p><strong>usage</strong> <code>object</code></p><p>本次请求的字符消耗信息。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>output_tokens</strong> <code>integer</code></p><p>输出音频的 Token 消耗量。对于千问3-TTS-Flash模型，该字段固定为0。</p><p><strong>input_tokens</strong> <code>integer</code></p><p>输入文本的 Token 消耗量。对于千问3-TTS-Flash模型，该字段固定为0。</p><p><strong>characters</strong> <code>integer</code></p><p>输入文本的字符数。仅千问3-TTS-Flash模型返回该字段。</p></div></section></td></tr><tr><td><p><strong>request_id</strong> <code>string</code></p><p>本次请求的 ID。</p></td><td></td></tr></tbody></table>

<a id="音频下载与播放"></a>

<a id="qwen-tts-audio-examples"></a>

## 音频下载与播放

运行示例前，请先[获取并配置 API Key](../model-api-reference/preparations/get-api-key.md)，并[安装 DashScope SDK](../model-api-reference/preparations/install-sdk.md)。Python 播放示例还依赖 PyAudio 和 NumPy；PyAudio 的安装方式见代码注释，NumPy 可通过 `pip install numpy` 安装。

<a id="下载音频-java"></a>

<a id="qwen-tts-audio-download"></a>

### 下载音频（Java）

需要导入 Gson 依赖，Maven 或 Gradle 添加方式如下：

<a id="sec-tabs-4"></a>

<a id="maven"></a>

<a id="maven-h4"></a>

#### Maven

在`pom.xml`中添加：

<a id="code-block-7"></a>

```xml
<!-- https://mvnrepository.com/artifact/com.google.code.gson/gson -->
<dependency>
    <groupId>com.google.code.gson</groupId>
    <artifactId>gson</artifactId>
    <version>2.13.1</version>
</dependency>
```

<a id="gradle"></a>

<a id="gradle-h4"></a>

#### Gradle

在`build.gradle`中添加：

<a id="code-block-8"></a>

```groovy
// https://mvnrepository.com/artifact/com.google.code.gson/gson
implementation("com.google.code.gson:gson:2.13.1")
```

<a id="code-block-9"></a>

```java
import com.alibaba.dashscope.aigc.multimodalconversation.AudioParameters;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.net.URL;

public class Main {
    private static final String MODEL = "qwen3-tts-flash";
    public static void call() throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model(MODEL)
                .text("Today is a wonderful day to build something people love!")
                .voice(AudioParameters.Voice.CHERRY)
                .parameter("language_type", "English") // 建议与文本语种一致，以获得正确的发音和自然的语调。
                .build();
        MultiModalConversationResult result = conv.call(param);
        String audioUrl = result.getOutput().getAudio().getUrl();
        System.out.print(audioUrl);

        // 下载音频文件到本地
        try (InputStream in = new URL(audioUrl).openStream();
             FileOutputStream out = new FileOutputStream("downloaded_audio.wav")) {
            byte[] buffer = new byte[1024];
            int bytesRead;
            while ((bytesRead = in.read(buffer)) != -1) {
                out.write(buffer, 0, bytesRead);
            }
            System.out.println("\n音频文件已下载到本地：downloaded_audio.wav");
        } catch (Exception e) {
            System.out.println("\n下载音频文件时出错：" + e.getMessage());
        }
    }
    public static void main(String[] args) {
        try {
            // 以下为华北2（北京）地域的配置。
            Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
            call();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

<a id="流式播放"></a>

<a id="qwen-tts-streaming-playback"></a>

### 流式播放

<a id="sec-tabs-5"></a>

<a id="python-3"></a>

<a id="python-3-h4"></a>

#### Python

<a id="code-block-10"></a>

```python
# coding=utf-8
#
# Installation instructions for pyaudio:
# APPLE Mac OS X
#   brew install portaudio
#   pip install pyaudio
# Debian/Ubuntu
#   sudo apt-get install python-pyaudio python3-pyaudio
#   or
#   pip install pyaudio
# CentOS
#   sudo yum install -y portaudio portaudio-devel && pip install pyaudio
# Microsoft Windows
#   python -m pip install pyaudio

import os
import dashscope
import pyaudio
import time

# 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
client = dashscope.Client(
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

p = pyaudio.PyAudio()
# 创建音频流
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=24000,
                output=True)

text = "你好啊，我是千问"

for chunk in client.audio.tts.http.stream(
    text,
    model="qwen3-tts-flash",
    voice="Cherry",
    language_type="Chinese",  # 建议与文本语种一致，以获得正确的发音和自然的语调。
):
    if chunk.audio:
        # 直接播放音频数据（chunk.audio 已是解码后的音频字节）
        stream.write(chunk.audio)
    if chunk.is_final:
        print(f"finish at: {chunk.expires_at}")
time.sleep(0.8)
# 清理资源
stream.stop_stream()
stream.close()
p.terminate()
```

<a id="java-3"></a>

<a id="java-3-h4"></a>

#### Java

需要导入 Gson 依赖，Maven 或 Gradle 添加方式如下：

<a id="sec-tabs-6"></a>

<a id="maven-2"></a>

<a id="maven-2-h4"></a>

#### Maven

在`pom.xml`中添加：

<a id="code-block-11"></a>

```xml
<!-- https://mvnrepository.com/artifact/com.google.code.gson/gson -->
<dependency>
    <groupId>com.google.code.gson</groupId>
    <artifactId>gson</artifactId>
    <version>2.13.1</version>
</dependency>
```

<a id="gradle-2"></a>

<a id="gradle-2-h4"></a>

#### Gradle

在`build.gradle`中添加：

<a id="code-block-12"></a>

```groovy
// https://mvnrepository.com/artifact/com.google.code.gson/gson
implementation("com.google.code.gson:gson:2.13.1")
```

<a id="code-block-13"></a>

```java
import com.alibaba.dashscope.aigc.multimodalconversation.AudioParameters;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;
import io.reactivex.Flowable;
import javax.sound.sampled.*;
import java.util.Base64;

public class Main {
    private static final String MODEL = "qwen3-tts-flash";
    public static void streamCall() throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model(MODEL)
                .text("Today is a wonderful day to build something people love!")
                .voice(AudioParameters.Voice.CHERRY)
                .parameter("language_type", "English") // 建议与文本语种一致，以获得正确的发音和自然的语调。
                .build();
        Flowable<MultiModalConversationResult> result = conv.streamCall(param);
        result.blockingForEach(r -> {
            try {
                // 1. 获取Base64编码的音频数据
                String base64Data = r.getOutput().getAudio().getData();
                byte[] audioBytes = Base64.getDecoder().decode(base64Data);

                // 2. 配置音频格式（根据API返回的音频格式调整）
                AudioFormat format = new AudioFormat(
                        AudioFormat.Encoding.PCM_SIGNED,
                        24000, // 采样率（需与API返回格式一致）
                        16,    // 采样位数
                        1,     // 声道数
                        2,     // 帧大小（字节数）
                        24000, // 帧率（需与采样率一致）
                        false  // 大端序
                );

                // 3. 实时播放音频数据
                DataLine.Info info = new DataLine.Info(SourceDataLine.class, format);
                try (SourceDataLine line = (SourceDataLine) AudioSystem.getLine(info)) {
                    if (line != null) {
                        line.open(format);
                        line.start();
                        line.write(audioBytes, 0, audioBytes.length);
                        line.drain();
                    }
                }
            } catch (LineUnavailableException e) {
                e.printStackTrace();
            }
        });
    }
    public static void main(String[] args) {
        // 以下为华北2（北京）地域的配置。
        Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
        try {
            streamCall();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```
