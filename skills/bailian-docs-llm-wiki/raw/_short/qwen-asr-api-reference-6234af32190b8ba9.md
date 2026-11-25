# 非实时语音识别（Qwen-ASR）API参考

本文介绍 Qwen-ASR 模型的输入与输出参数。可通过OpenAI 兼容或DashScope协议调用 API。

<a id="模型接入方式"></a>

<a id="6560a479ca3lm"></a>

## 模型接入方式

不同[模型](../model-user-guide/model-experience/speech-and-audio/speech-recognition/non-realtime-speech-recognition-user-guide.md)支持的接入方式不同，请根据下表选择正确的方式进行集成。

| 模型 | 接入方式 |
| --- | --- |
| 千问3-ASR-Flash-Filetrans | 仅支持[DashScope异步调用](qwen-asr-api-reference-6234af32190b8ba9.md#9937e8884002q)方式 |
| 千问3-ASR-Flash | [OpenAI 兼容](qwen-asr-api-reference-6234af32190b8ba9.md#d397bcc41eu3q)和[DashScope同步调用](qwen-asr-api-reference-6234af32190b8ba9.md#1afc6b20a29ie)两种方式 |

<a id="openai-兼容"></a>

<a id="d397bcc41eu3q"></a>

## OpenAI 兼容

> **重要**
>
> 美国地域不支持OpenAI兼容模式。

<a id="url"></a>

<a id="57aa8161d39we"></a>

### URL

<a id="sec-tabs"></a>

<a id="华北2-北京"></a>

<a id="华北2-北京-h4"></a>

#### 华北2（北京）

HTTP请求地址：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions`

SDK调用配置的base\_url：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

HTTP请求地址：`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1/chat/completions`

SDK调用配置的base\_url：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

> **重要**
>
> 阿里云百炼为华北2（北京）、新加坡地域推出了业务空间专属域名，能够为推理请求提供卓越的性能和更高的稳定性，建议迁移至新域名：
>
> -   华北2（北京）地域：从 `dashscope.aliyuncs.com` 迁移至 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
> -   新加坡地域：从 `dashscope-intl.aliyuncs.com` 迁移至 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`

<table><tbody><tr><td><a id="0eed3f701cd4j"></a><h3>请求参数</h3><p><strong>model</strong><code>string</code><strong>（必选）</strong></p><p><a href="../model-user-guide/model-experience/speech-and-audio/speech-recognition/non-realtime-speech-recognition-user-guide.md">模型</a>名称。仅适用于千问3-ASR-Flash模型。</p><p><strong>messages</strong><code>array</code><strong>（必选）</strong></p><p>消息列表。</p><a id="accordion-消息类型"></a><section><p>消息类型</p><div><p>System Message<code>object</code>（可选）</p><p>用于为语音识别提供上下文（Context），如背景文本和实体词表等参考信息，不支持设置模型角色等传统系统提示词。如果设置系统消息，请放在messages列表的第一位。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>role</strong><code>string</code><strong>（必选）</strong></p><p>固定为<code>system</code>。</p></div></section><p>User Message<code>object</code><strong>（必选）</strong></p><p>用户发送给模型的消息。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>content</strong><code>array</code><strong>（必选）</strong></p><p>用户消息的内容。仅允许设置一组消息。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>type</strong><code>string</code><strong>（必选）</strong></p><p>固定为<code>input_audio</code>，代表输入的是音频。</p><p><strong>input_audio</strong><code>object</code><strong>（必选）</strong></p><p>待识别音频。具体用法请参见<a href="qwen-asr-api-reference-6234af32190b8ba9.md#qwen-asr-openai-examples">调用示例</a>。</p><p><code>input_audio.data</code> 支持公网可访问的音频文件 URL 和 Base64 Data URI，不支持直接传入本地文件绝对路径。本地音频文件需先读取并编码为 Data URI。</p><p>使用SDK时，若录音文件存储在<a href="https://help.aliyun.com/zh/oss/user-guide/simple-upload#a632b50f190j8">阿里云OSS</a>，不支持使用以 <code>oss://</code>为前缀的临时 URL。</p><p>使用RESTful API时，若录音文件存储在<a href="https://help.aliyun.com/zh/oss/user-guide/simple-upload#a632b50f190j8">阿里云OSS</a>，支持使用以 <code>oss://</code>为前缀的临时 URL。但需注意：</p><div><div><p><strong>重要</strong></p><ul><li>临时 URL 有效期48小时，过期后无法使用，<strong>请勿用于生产环境。</strong></li><li>文件上传凭证接口限流为 100 QPS 且不支持扩容，<strong>请勿用于生产环境、高并发及压测场景。</strong></li><li>生产环境建议使用<a href="https://help.aliyun.com/zh/oss/user-guide/what-is-oss">阿里云OSS</a> 等稳定存储，确保文件长期可用并规避限流问题。</li></ul></div></div></div></section><p><strong>role</strong><code>string</code><strong>（必选）</strong></p><p>用户消息的角色，固定为<code>user</code>。</p></div></section></div></section><p><strong>asr_options</strong><code>object</code>（可选）</p><p>用来指定某些功能是否启用。</p><div><div><p><strong>说明</strong><code>asr_options</code> 非 OpenAI 标准参数。使用 OpenAI Python SDK 时，通过 <code>extra_body</code> 传入；使用 Node.js SDK 时，将 <code>asr_options</code> 作为请求体的顶层参数传入。</p></div></div><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>language</strong> <em>string</em>（可选）无默认值</p><p>若已知音频的语种，可通过该参数指定待识别语种，以提升识别准确率。</p><p>只能指定一个语种。</p><p>若音频语种不确定，或包含多种语种（例如中英日韩混合），请勿指定该参数。</p><a id="accordion-取值范围"></a><section><p>取值范围</p><div><ul><li>zh：中文（普通话、四川话、闽南语、吴语）</li><li>yue：粤语</li><li>en：英文</li><li>ja：日语</li><li>de：德语</li><li>ko：韩语</li><li>ru：俄语</li><li>fr：法语</li><li>pt：葡萄牙语</li><li>ar：阿拉伯语</li><li>it：意大利语</li><li>es：西班牙语</li><li>hi：印地语</li><li>id：印尼语</li><li>th：泰语</li><li>tr：土耳其语</li><li>uk：乌克兰语</li><li>vi：越南语</li><li>cs：捷克语</li><li>da：丹麦语</li><li>fil：菲律宾语</li><li>fi：芬兰语</li><li>is：冰岛语</li><li>ms：马来语</li><li>no：挪威语</li><li>pl：波兰语</li><li>sv：瑞典语</li></ul></div></section><p><strong>enable_itn</strong><code>boolean</code>（可选）默认值为<code>false</code></p><p>是否启用ITN（Inverse Text Normalization，逆文本标准化）。该功能仅适用于中文和英文音频。</p><p>开启后，语音识别结果中的中文数字（如&quot;一百二十三&quot;）或英文数字（如&quot;one hundred&quot;）将自动转换为阿拉伯数字（如&quot;123&quot;）。</p><p>参数值：</p><ul><li>true：开启；</li><li>false：关闭。</li></ul></div></section><p><strong>stream</strong><code>boolean</code>（可选）默认值为<code>false</code></p><p>是否以流式输出方式回复。相关文档：<a href="../model-user-guide/model-experience/text-generation-model/stream.md">流式输出</a></p><p>可选值：</p><ul><li><code>false</code>：模型生成全部内容后一次性返回；</li><li><code>true</code>：边生成边输出，每生成一部分内容即返回一个数据块（chunk）。需实时逐个读取这些块以拼接完整回复。</li></ul><p>推荐设置为<code>true</code>，可提升阅读体验并降低超时风险。</p><p><strong>stream_options</strong><code>object</code>（可选）</p><p>流式输出的配置项，仅在 <code>stream</code> 为 <code>true</code> 时生效。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>include_usage</strong><code>boolean</code>（可选）默认值为<code>false</code></p><p>是否在响应的最后一个数据块包含Token消耗信息。</p><p>可选值：</p><ul><li><code>true</code>：包含；</li><li><code>false</code>：不包含。</li></ul><div><div><p><strong>说明</strong>流式输出时，Token 消耗信息仅可出现在响应的最后一个数据块。</p></div></div></div></section></td><td><a id="qwen-asr-openai-examples"></a><h3>调用示例</h3><div><div><p><strong>说明</strong>OpenAI Python SDK 版本需不低于 <code>1.52.0</code>，Node.js SDK 版本需不低于 <code>4.68.0</code>。</p></div></div><a id="sec-tabs-2"></a><section><a id="输入内容-音频文件url"></a><section><a id="输入内容-音频文件url-h4"></a><h4>输入内容：音频文件URL</h4><a id="sec-tabs-3"></a><section><a id="python-sdk"></a><section><a id="python-sdk-h4"></a><h4>Python SDK</h4><a id="code-block"></a><pre class="language-python"><code>from openai import OpenAI
import os

try:
    client = OpenAI(
        # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key = &quot;sk-xxx&quot;,
        api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
        # 以下为华北2（北京）地域的配置，调用时请将&quot;{WorkspaceId}&quot;替换为真实的业务空间ID，各地域的配置不同。
        base_url=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,
    )

    stream_enabled = False  # 是否开启流式输出
    completion = client.chat.completions.create(
        model=&quot;qwen3-asr-flash&quot;,
        messages=[
            {
                &quot;content&quot;: [
                    {
                        &quot;type&quot;: &quot;input_audio&quot;,
                        &quot;input_audio&quot;: {
                            &quot;data&quot;: &quot;{YOUR_AUDIO_URL}&quot;
                        }
                    }
                ],
                &quot;role&quot;: &quot;user&quot;
            }
        ],
        stream=stream_enabled,
        # stream设为False时，不能设置stream_options参数
        # stream_options={&quot;include_usage&quot;: True},
        extra_body={
            &quot;asr_options&quot;: {
                # &quot;language&quot;: &quot;zh&quot;,
                &quot;enable_itn&quot;: False
            }
        }
    )
    if stream_enabled:
        full_content = &quot;&quot;
        print(&quot;流式输出内容为：&quot;)
        for chunk in completion:
            # 如果stream_options.include_usage为True，则最后一个chunk的choices字段为空列表，需要跳过（可以通过chunk.usage获取 Token 使用量）
            print(chunk)
            if chunk.choices and chunk.choices[0].delta.content:
                full_content += chunk.choices[0].delta.content
        print(f&quot;完整内容为：{full_content}&quot;)
    else:
        print(f&quot;非流式输出内容为：{completion.choices[0].message.content}&quot;)
except Exception as e:
    print(f&quot;错误信息：{e}&quot;)
</code></pre></section><a id="node-js-sdk"></a><section><a id="node-js-sdk-h4"></a><h4>Node.js SDK</h4><a id="code-block-2"></a><pre class="language-javascript"><code>// 运行前的准备工作:
// Windows/Mac/Linux 通用:
// 1. 确保已安装 Node.js (建议版本 &gt;= 14)
// 2. 运行以下命令安装必要的依赖: npm install openai

import OpenAI from &quot;openai&quot;;

const client = new OpenAI({
  // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
  // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：apiKey: &quot;sk-xxx&quot;,
  apiKey: process.env.DASHSCOPE_API_KEY,
  // 以下为华北2（北京）地域的配置，调用时请将&quot;{WorkspaceId}&quot;替换为真实的业务空间ID，各地域的配置不同。
  baseURL: &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,
});

async function main() {
  try {
    const streamEnabled = false; // 是否开启流式输出
    const completion = await client.chat.completions.create({
      model: &quot;qwen3-asr-flash&quot;,
      messages: [
        {
          role: &quot;user&quot;,
          content: [
            {
              type: &quot;input_audio&quot;,
              input_audio: {
                data: &quot;{YOUR_AUDIO_URL}&quot;
              }
            }
          ]
        }
      ],
      stream: streamEnabled,
      // stream设为False时，不能设置stream_options参数
      // stream_options: {
      //   &quot;include_usage&quot;: true
      // },
      asr_options: {
        // language: &quot;zh&quot;,
        enable_itn: false
      }
    });

    if (streamEnabled) {
      let fullContent = &quot;&quot;;
      console.log(&quot;流式输出内容为：&quot;);
      for await (const chunk of completion) {
        console.log(JSON.stringify(chunk));
        if (chunk.choices &amp;&amp; chunk.choices.length &gt; 0) {
          const delta = chunk.choices[0].delta;
          if (delta &amp;&amp; delta.content) {
            fullContent += delta.content;
          }
        }
      }
      console.log(`完整内容为：${fullContent}`);
    } else {
      console.log(`非流式输出内容为：${completion.choices[0].message.content}`);
    }
  } catch (err) {
    console.error(`错误信息：${err}`);
  }
}

main();
</code></pre></section><a id="curl"></a><section><a id="curl-h4"></a><h4>cURL</h4><p>以下为华北2（北京）地域的配置，调用时请将<code>{WorkspaceId}</code>替换为真实的<a href="../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain">Workspace ID</a>，各地域的配置不同。</p><a id="code-block-3"></a><pre class="language-bash"><code>curl -X POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions' \
-H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
-H &quot;Content-Type: application/json&quot; \
-d '{
    &quot;model&quot;: &quot;qwen3-asr-flash&quot;,
    &quot;messages&quot;: [
        {
            &quot;content&quot;: [
                {
                    &quot;type&quot;: &quot;input_audio&quot;,
                    &quot;input_audio&quot;: {
                        &quot;data&quot;: &quot;{YOUR_AUDIO_URL}&quot;
                    }
                }
            ],
            &quot;role&quot;: &quot;user&quot;
        }
    ],
    &quot;stream&quot;:false,
    &quot;asr_options&quot;: {
        &quot;enable_itn&quot;: false
    }
}'
</code></pre></section></section></section><a id="输入内容-base64编码的音频文件"></a><section><a id="输入内容-base64编码的音频文件-h4"></a><h4>输入内容：Base64编码的音频文件</h4><p>可输入Base64编码数据（<a href="https://www.rfc-editor.org/rfc/rfc2397">Data URL</a>），格式为：<code>data:&lt;mediatype&gt;;base64,&lt;data&gt;</code>。</p><ul><li><p><code>&lt;mediatype&gt;</code>：MIME类型</p><p>因音频格式而异，例如：</p><ul><li>WAV：<code>audio/wav</code></li><li>MP3：<code>audio/mpeg</code></li></ul></li><li><p><code>&lt;data&gt;</code>：音频转成的Base64编码的字符串</p><p>Base64编码会增大体积，请控制原文件大小，确保编码后仍符合输入音频大小限制（10MB）</p></li><li><p>示例：<code>data:audio/wav;base64,SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU4LjI5LjEwMAAAAAAAAAAAAAAA//PAxABQ/BXRbMPe4IQAhl9</code></p><a id="accordion-点击查看示例代码"></a><section><p>点击查看示例代码</p><div><a id="fig-code-group"></a><div><a id="fig-code-group-python-tab"></a>python<div><a id="code-code-group-python"></a><pre class="language-python"><code>import base64, pathlib

# 将文件路径替换为待识别的本地音频文件路径，并确保文件符合音频要求。
file_path = pathlib.Path(&quot;{YOUR_AUDIO_FILE}&quot;)
base64_str = base64.b64encode(file_path.read_bytes()).decode()
data_uri = f&quot;data:audio/mpeg;base64,{base64_str}&quot;
</code></pre></div><a id="fig-code-group-java-tab"></a>java<div><a id="code-code-group-java"></a><pre class="language-java"><code>import java.nio.file.*;
import java.util.Base64;

public class Main {
    /**
     * 将文件路径替换为待识别的本地音频文件路径，并确保文件符合音频要求。
     */
    public static String toDataUrl(String filePath) throws Exception {
        byte[] bytes = Files.readAllBytes(Paths.get(filePath));
        String encoded = Base64.getEncoder().encodeToString(bytes);
        return &quot;data:audio/mpeg;base64,&quot; + encoded;
    }

    // 使用示例
    public static void main(String[] args) throws Exception {
        System.out.println(toDataUrl(&quot;{YOUR_AUDIO_FILE}&quot;));
    }
}
</code></pre></div></div></div></section></li></ul><a id="fig-code-group-2"></a><div><a id="fig-code-group-2-python-sdk-tab"></a>Python SDK<div><a id="code-code-group-2-python-sdk"></a><pre class="language-python"><code>import base64
from openai import OpenAI
import os
import pathlib

try:
    # 请替换为实际的音频文件路径
    file_path = &quot;{YOUR_AUDIO_FILE}&quot;
    # 请替换为实际的音频文件MIME类型
    audio_mime_type = &quot;audio/mpeg&quot;

    file_path_obj = pathlib.Path(file_path)
    if not file_path_obj.exists():
        raise FileNotFoundError(f&quot;音频文件不存在: {file_path}&quot;)

    base64_str = base64.b64encode(file_path_obj.read_bytes()).decode()
    data_uri = f&quot;data:{audio_mime_type};base64,{base64_str}&quot;

    client = OpenAI(
        # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key = &quot;sk-xxx&quot;,
        api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
        # 以下为华北2（北京）地域的配置，调用时请将&quot;{WorkspaceId}&quot;替换为真实的业务空间ID，各地域的配置不同。
        base_url=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,
    )

    stream_enabled = False  # 是否开启流式输出
    completion = client.chat.completions.create(
        model=&quot;qwen3-asr-flash&quot;,
        messages=[
            {
                &quot;content&quot;: [
                    {
                        &quot;type&quot;: &quot;input_audio&quot;,
                        &quot;input_audio&quot;: {
                            &quot;data&quot;: data_uri
                        }
                    }
                ],
                &quot;role&quot;: &quot;user&quot;
            }
        ],
        stream=stream_enabled,
        # stream设为False时，不能设置stream_options参数
        # stream_options={&quot;include_usage&quot;: True},
        extra_body={
            &quot;asr_options&quot;: {
                # &quot;language&quot;: &quot;zh&quot;,
                &quot;enable_itn&quot;: False
            }
        }
    )
    if stream_enabled:
        full_content = &quot;&quot;
        print(&quot;流式输出内容为：&quot;)
        for chunk in completion:
            # 如果stream_options.include_usage为True，则最后一个chunk的choices字段为空列表，需要跳过（可以通过chunk.usage获取 Token 使用量）
            print(chunk)
            if chunk.choices and chunk.choices[0].delta.content:
                full_content += chunk.choices[0].delta.content
        print(f&quot;完整内容为：{full_content}&quot;)
    else:
        print(f&quot;非流式输出内容为：{completion.choices[0].message.content}&quot;)
except Exception as e:
    print(f&quot;错误信息：{e}&quot;)
</code></pre></div><a id="fig-code-group-2-node-js-sdk-tab"></a>Node.js SDK<div><a id="code-code-group-2-node-js-sdk"></a><pre class="language-javascript"><code>// 运行前的准备工作:
// Windows/Mac/Linux 通用:
// 1. 确保已安装 Node.js (建议版本 &gt;= 14)
// 2. 运行以下命令安装必要的依赖: npm install openai

import OpenAI from &quot;openai&quot;;
import { readFileSync } from 'fs';

const client = new OpenAI({
  // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
  // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：apiKey: &quot;sk-xxx&quot;,
  apiKey: process.env.DASHSCOPE_API_KEY,
  // 以下为华北2（北京）地域的配置，调用时请将&quot;{WorkspaceId}&quot;替换为真实的业务空间ID，各地域的配置不同。
  baseURL: &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,
});

const encodeAudioFile = (audioFilePath) =&gt; {
    const audioFile = readFileSync(audioFilePath);
    return audioFile.toString('base64');
};

// 请替换为实际的音频文件路径
const dataUri = `data:audio/mpeg;base64,${encodeAudioFile(&quot;{YOUR_AUDIO_FILE}&quot;)}`;

async function main() {
  try {
    const streamEnabled = false; // 是否开启流式输出
    const completion = await client.chat.completions.create({
      model: &quot;qwen3-asr-flash&quot;,
      messages: [
        {
          role: &quot;user&quot;,
          content: [
            {
              type: &quot;input_audio&quot;,
              input_audio: {
                data: dataUri
              }
            }
          ]
        }
      ],
      stream: streamEnabled,
      // stream设为False时，不能设置stream_options参数
      // stream_options: {
      //   &quot;include_usage&quot;: true
      // },
      asr_options: {
        // language: &quot;zh&quot;,
        enable_itn: false
      }
    });

    if (streamEnabled) {
      let fullContent = &quot;&quot;;
      console.log(&quot;流式输出内容为：&quot;);
      for await (const chunk of completion) {
        console.log(JSON.stringify(chunk));
        if (chunk.choices &amp;&amp; chunk.choices.length &gt; 0) {
          const delta = chunk.choices[0].delta;
          if (delta &amp;&amp; delta.content) {
            fullContent += delta.content;
          }
        }
      }
      console.log(`完整内容为：${fullContent}`);
    } else {
      console.log(`非流式输出内容为：${completion.choices[0].message.content}`);
    }
  } catch (err) {
    console.error(`错误信息：${err}`);
  }
}

main();
</code></pre></div></div></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="8c9faf146399l"></a><h3>响应参数</h3><div><div><p><strong>说明</strong>Qwen3-ASR-Flash 通过 OpenAI 兼容接口调用时不返回时间戳。如需时间戳，请使用 Qwen-Audio-ASR-Filetrans 系列模型，调用方式请参见 <a href="qwen-audio-asr-filetrans-http-api-e0184f38f9d98459.md">HTTP API</a>。</p></div></div><p>流式输出的情感标签位于 <code>choices[].delta.annotations[].emotion</code>，非流式输出位于 <code>choices[].message.annotations[].emotion</code>。</p><p><strong>id</strong><code>string</code></p><p>本次调用的唯一标识符。</p><p><strong>choices</strong><code>array</code></p><p>模型的输出信息。</p><a id="accordion-属性-6"></a><section><p>属性</p><div><p><strong>finish_reason</strong><code>string</code></p><p>有三种情况：</p><ul><li>正在生成时为null；</li><li>因模型输出自然结束，或触发输入参数中的stop条件而结束时为stop；</li><li>因生成长度过长而结束为length。</li></ul><p><strong>index</strong><code>integer</code></p><p>当前对象在<code>choices</code>数组中的索引。</p><p><strong>message</strong><code>object</code></p><p>模型输出的消息对象。</p><a id="accordion-属性-7"></a><section><p>属性</p><div><p><strong>role</strong><code>string</code></p><p>输出消息的角色，固定为assistant。</p><p><strong>content</strong><code>string</code></p><p>语音识别结果。</p><p><strong>annotations</strong><code>array</code></p><p>输出标注信息（如语种）</p><a id="accordion-属性-8"></a><section><p>属性</p><div><p><strong>language</strong><code>string</code></p><p>被识别音频的语种。当请求参数<code>language</code>已指定语种时，该值与所指定的参数一致。</p><a id="accordion-取值范围-2"></a><section><p>取值范围</p><div><ul><li>zh：中文（普通话、四川话、闽南语、吴语）</li><li>yue：粤语</li><li>en：英文</li><li>ja：日语</li><li>de：德语</li><li>ko：韩语</li><li>ru：俄语</li><li>fr：法语</li><li>pt：葡萄牙语</li><li>ar：阿拉伯语</li><li>it：意大利语</li><li>es：西班牙语</li><li>hi：印地语</li><li>id：印尼语</li><li>th：泰语</li><li>tr：土耳其语</li><li>uk：乌克兰语</li><li>vi：越南语</li><li>cs：捷克语</li><li>da：丹麦语</li><li>fil：菲律宾语</li><li>fi：芬兰语</li><li>is：冰岛语</li><li>ms：马来语</li><li>no：挪威语</li><li>pl：波兰语</li><li>sv：瑞典语</li></ul></div></section><p><strong>type</strong><code>string</code></p><p>固定为<code>audio_info</code>，表示音频信息。</p><p><strong>emotion</strong><code>string</code></p><p>被识别音频的情感。情感识别固定开启，无需额外配置。支持的情感如下：</p><ul><li><code>surprised</code>：惊讶</li><li><code>neutral</code>：平静</li><li><code>happy</code>：愉快</li><li><code>sad</code>：悲伤</li><li><code>disgusted</code>：厌恶</li><li><code>angry</code>：愤怒</li><li><code>fearful</code>：恐惧</li></ul></div></section></div></section></div></section><p><strong>created</strong><code>integer</code></p><p>请求创建时的 Unix 时间戳（秒）。</p><p><strong>model</strong><code>string</code></p><p>本次请求使用的模型。</p><p><strong>object</strong><code>string</code></p><p>始终为<code>chat.completion</code>。</p><p><strong>usage</strong><code>object</code></p><p>本次请求的Token消耗信息。</p><a id="accordion-属性-9"></a><section><p>属性</p><div><p><strong>completion_tokens</strong> <code>integer</code></p><p>模型输出的 Token 数。</p><p><strong>completion_tokens_details</strong> <code>object</code></p><p>模型输出的 Token 细粒度详情。</p><a id="accordion-属性-10"></a><section><p>属性</p><div><p><strong>text_tokens</strong> <code>integer</code></p><p>模型输出文本的Token数。</p></div></section><p><strong>prompt_tokens</strong> <code>object</code></p><p>输入的Token数。</p><p><strong>prompt_tokens_details</strong> <code>object</code></p><p>输入的 Token 细粒度详情。</p><a id="accordion-属性-11"></a><section><p>属性</p><div><p><strong>audio_tokens</strong> <code>integer</code></p><p>输入音频长度（Token）。音频转换Token规则：每秒音频转换为25个Token，不足1秒按1秒计算。</p><p><strong>text_tokens</strong> <code>integer</code></p><p>无需关注该参数。</p></div></section><p><strong>seconds</strong> <code>integer</code></p><p>音频时长（秒）。</p><p><strong>total_tokens</strong> <code>integer</code></p><p>输入和输出总Token数（<code>total_tokens = completion_tokens + prompt_tokens</code>）。</p></div></section></td><td><a id="fig-code-group-3"></a><div><a id="fig-code-group-3-非流式输出-tab"></a>非流式输出<div><a id="code-code-group-3-非流式输出"></a><pre class="language-json"><code>{
    &quot;choices&quot;: [
        {
            &quot;finish_reason&quot;: &quot;stop&quot;,
            &quot;index&quot;: 0,
            &quot;message&quot;: {
                &quot;annotations&quot;: [
                    {
                        &quot;emotion&quot;: &quot;neutral&quot;,
                        &quot;language&quot;: &quot;zh&quot;,
                        &quot;type&quot;: &quot;audio_info&quot;
                    }
                ],
                &quot;content&quot;: &quot;欢迎使用阿里云。&quot;,
                &quot;role&quot;: &quot;assistant&quot;
            }
        }
    ],
    &quot;created&quot;: 1767683986,
    &quot;id&quot;: &quot;chatcmpl-487abe5f-d4f2-9363-a877-xxxxxxx&quot;,
    &quot;model&quot;: &quot;qwen3-asr-flash&quot;,
    &quot;object&quot;: &quot;chat.completion&quot;,
    &quot;usage&quot;: {
        &quot;completion_tokens&quot;: 12,
        &quot;completion_tokens_details&quot;: {
            &quot;text_tokens&quot;: 12
        },
        &quot;prompt_tokens&quot;: 42,
        &quot;prompt_tokens_details&quot;: {
            &quot;audio_tokens&quot;: 42,
            &quot;text_tokens&quot;: 0
        },
        &quot;seconds&quot;: 1,
        &quot;total_tokens&quot;: 54
    }
}
</code></pre></div><a id="fig-code-group-3-流式输出-tab"></a>流式输出<div><a id="code-code-group-3-流式输出"></a><pre class="language-json"><code>data: {&quot;model&quot;:&quot;qwen3-asr-flash&quot;,&quot;id&quot;:&quot;chatcmpl-3fb97803-d27f-9289-8889-xxxxx&quot;,&quot;created&quot;:1767685989,&quot;object&quot;:&quot;chat.completion.chunk&quot;,&quot;usage&quot;:null,&quot;choices&quot;:[{&quot;logprobs&quot;:null,&quot;index&quot;:0,&quot;delta&quot;:{&quot;content&quot;:&quot;&quot;,&quot;role&quot;:&quot;assistant&quot;}}]}

data: {&quot;model&quot;:&quot;qwen3-asr-flash&quot;,&quot;id&quot;:&quot;chatcmpl-3fb97803-d27f-9289-8889-xxxxx&quot;,&quot;choices&quot;:[{&quot;delta&quot;:{&quot;annotations&quot;:[{&quot;type&quot;:&quot;audio_info&quot;,&quot;language&quot;:&quot;zh&quot;,&quot;emotion&quot;:&quot;neutral&quot;}],&quot;content&quot;:&quot;欢迎&quot;,&quot;role&quot;:null},&quot;index&quot;:0}],&quot;created&quot;:1767685989,&quot;object&quot;:&quot;chat.completion.chunk&quot;,&quot;usage&quot;:null}

data: {&quot;model&quot;:&quot;qwen3-asr-flash&quot;,&quot;id&quot;:&quot;chatcmpl-3fb97803-d27f-9289-8889-xxxxx&quot;,&quot;choices&quot;:[{&quot;delta&quot;:{&quot;annotations&quot;:[{&quot;type&quot;:&quot;audio_info&quot;,&quot;language&quot;:&quot;zh&quot;,&quot;emotion&quot;:&quot;neutral&quot;}],&quot;content&quot;:&quot;使用&quot;,&quot;role&quot;:null},&quot;index&quot;:0}],&quot;created&quot;:1767685989,&quot;object&quot;:&quot;chat.completion.chunk&quot;,&quot;usage&quot;:null}

data: {&quot;model&quot;:&quot;qwen3-asr-flash&quot;,&quot;id&quot;:&quot;chatcmpl-3fb97803-d27f-9289-8889-xxxxx&quot;,&quot;choices&quot;:[{&quot;delta&quot;:{&quot;annotations&quot;:[{&quot;type&quot;:&quot;audio_info&quot;,&quot;language&quot;:&quot;zh&quot;,&quot;emotion&quot;:&quot;neutral&quot;}],&quot;content&quot;:&quot;阿里&quot;,&quot;role&quot;:null},&quot;index&quot;:0}],&quot;created&quot;:1767685989,&quot;object&quot;:&quot;chat.completion.chunk&quot;,&quot;usage&quot;:null}

data: {&quot;model&quot;:&quot;qwen3-asr-flash&quot;,&quot;id&quot;:&quot;chatcmpl-3fb97803-d27f-9289-8889-xxxxx&quot;,&quot;choices&quot;:[{&quot;delta&quot;:{&quot;annotations&quot;:[{&quot;type&quot;:&quot;audio_info&quot;,&quot;language&quot;:&quot;zh&quot;,&quot;emotion&quot;:&quot;neutral&quot;}],&quot;content&quot;:&quot;云&quot;,&quot;role&quot;:null},&quot;index&quot;:0}],&quot;created&quot;:1767685989,&quot;object&quot;:&quot;chat.completion.chunk&quot;,&quot;usage&quot;:null}

data: {&quot;model&quot;:&quot;qwen3-asr-flash&quot;,&quot;id&quot;:&quot;chatcmpl-3fb97803-d27f-9289-8889-xxxxx&quot;,&quot;choices&quot;:[{&quot;delta&quot;:{&quot;annotations&quot;:[{&quot;type&quot;:&quot;audio_info&quot;,&quot;language&quot;:&quot;zh&quot;,&quot;emotion&quot;:&quot;neutral&quot;}],&quot;content&quot;:&quot;。&quot;,&quot;role&quot;:null},&quot;index&quot;:0}],&quot;created&quot;:1767685989,&quot;object&quot;:&quot;chat.completion.chunk&quot;,&quot;usage&quot;:null}

data: {&quot;model&quot;:&quot;qwen3-asr-flash&quot;,&quot;id&quot;:&quot;chatcmpl-3fb97803-d27f-9289-8889-xxxxx&quot;,&quot;choices&quot;:[{&quot;delta&quot;:{&quot;role&quot;:null},&quot;index&quot;:0,&quot;finish_reason&quot;:&quot;stop&quot;}],&quot;created&quot;:1767685989,&quot;object&quot;:&quot;chat.completion.chunk&quot;,&quot;usage&quot;:null}

data: [DONE]
</code></pre></div></div></td></tr></tbody></table>

<a id="dashscope同步调用"></a>

<a id="1afc6b20a29ie"></a>

## DashScope同步调用

<a id="url-2"></a>

<a id="fe508c8badxjg"></a>

### URL

<a id="sec-tabs-4"></a>

<a id="华北2-北京-2"></a>

<a id="华北2-北京-2-h4"></a>

#### 华北2（北京）

HTTP请求地址：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

SDK调用配置的base\_url：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="新加坡-2"></a>

<a id="新加坡-2-h4"></a>

#### 新加坡

HTTP请求地址：`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

SDK调用配置的base\_url：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="美国-弗吉尼亚"></a>

<a id="美国-弗吉尼亚-h4"></a>

#### 美国（弗吉尼亚）

HTTP请求地址：`POST https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

SDK调用配置的base\_url：`https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v1`

> **重要**
>
> 阿里云百炼为华北2（北京）、新加坡地域推出了业务空间专属域名，能够为推理请求提供卓越的性能和更高的稳定性，建议迁移至新域名：
>
> -   华北2（北京）地域：从 `dashscope.aliyuncs.com` 迁移至 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
> -   新加坡地域：从 `dashscope-intl.aliyuncs.com` 迁移至 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`

<table><tbody><tr><td><a id="2a1c410015otp"></a><h3>请求参数</h3><p><strong>model</strong><code>string</code><strong>（必选）</strong></p><p><a href="../model-user-guide/model-experience/speech-and-audio/speech-recognition/non-realtime-speech-recognition-user-guide.md">模型</a>名称。仅适用于千问3-ASR-Flash模型。</p><p><strong>messages</strong><code>array</code><strong>（必选）</strong></p><p>消息列表。</p><div><div><p><strong>说明</strong>通过HTTP调用时，请将<code>messages</code>放入 <code>input</code> 对象中。</p></div></div><a id="accordion-消息类型-2"></a><section><p>消息类型</p><div><p>System Message<code>object</code>（可选）</p><p>用于为语音识别提供上下文（Context），如背景文本和实体词表等参考信息，不支持设置模型角色等传统系统提示词。如果设置系统消息，请放在messages列表的第一位。</p><p>仅千问3-ASR-Flash支持该参数。</p><a id="accordion-属性-12"></a><section><p>属性</p><div><p><strong>role</strong><code>string</code><strong>（必选）</strong></p><p>固定为<code>system</code>。</p></div></section><p>User Message<code>object</code><strong>（必选）</strong></p><p>用户发送给模型的消息。</p><a id="accordion-属性-13"></a><section><p>属性</p><div><p><strong>content</strong><code>array</code><strong>（必选）</strong></p><p>用户消息的内容。仅允许设置一组消息。</p><a id="accordion-属性-14"></a><section><p>属性</p><div><p><strong>audio</strong><code>string</code><strong>（必选）</strong></p><p>待识别音频。具体用法请参见<a href="qwen-asr-api-reference-6234af32190b8ba9.md#qwen-asr-sync-examples">调用示例</a>。</p><p>千问3-ASR-Flash模型在DashScope调用方式下支持三种输入形式：Base64编码的文件、本地文件绝对路径、公网可访问的待识别文件URL。</p><p>使用SDK时，若录音文件存储在<a href="https://help.aliyun.com/zh/oss/user-guide/simple-upload#a632b50f190j8">阿里云OSS</a>，不支持使用以 <code>oss://</code>为前缀的临时 URL。</p><p>使用RESTful API时，若录音文件存储在<a href="https://help.aliyun.com/zh/oss/user-guide/simple-upload#a632b50f190j8">阿里云OSS</a>，支持使用以 <code>oss://</code>为前缀的临时 URL。但需注意：</p><div><div><p><strong>重要</strong></p><ul><li>临时 URL 有效期48小时，过期后无法使用，<strong>请勿用于生产环境。</strong></li><li>文件上传凭证接口限流为 100 QPS 且不支持扩容，<strong>请勿用于生产环境、高并发及压测场景。</strong></li><li>生产环境建议使用<a href="https://help.aliyun.com/zh/oss/user-guide/what-is-oss">阿里云OSS</a> 等稳定存储，确保文件长期可用并规避限流问题。</li></ul></div></div></div></section><p><strong>role</strong><code>string</code><strong>（必选）</strong></p><p>用户消息的角色，固定为<code>user</code>。</p></div></section></div></section><p><strong>asr_options</strong><code>object</code>（可选）</p><p>用来指定某些功能是否启用。</p><p>仅千问3-ASR-Flash支持该参数。</p><a id="accordion-属性-15"></a><section><p>属性</p><div><p><strong>language</strong> <em>string</em>（可选）无默认值</p><p>若已知音频的语种，可通过该参数指定待识别语种，以提升识别准确率。</p><p>只能指定一个语种。</p><p>若音频语种不确定，或包含多种语种（例如中英日韩混合），请勿指定该参数。</p><a id="accordion-取值范围-3"></a><section><p>取值范围</p><div><ul><li>zh：中文（普通话、四川话、闽南语、吴语）</li><li>yue：粤语</li><li>en：英文</li><li>ja：日语</li><li>de：德语</li><li>ko：韩语</li><li>ru：俄语</li><li>fr：法语</li><li>pt：葡萄牙语</li><li>ar：阿拉伯语</li><li>it：意大利语</li><li>es：西班牙语</li><li>hi：印地语</li><li>id：印尼语</li><li>th：泰语</li><li>tr：土耳其语</li><li>uk：乌克兰语</li><li>vi：越南语</li><li>cs：捷克语</li><li>da：丹麦语</li><li>fil：菲律宾语</li><li>fi：芬兰语</li><li>is：冰岛语</li><li>ms：马来语</li><li>no：挪威语</li><li>pl：波兰语</li><li>sv：瑞典语</li></ul></div></section><p><strong>enable_itn</strong><code>boolean</code>（可选）默认值为<code>false</code></p><p>是否启用ITN（Inverse Text Normalization，逆文本标准化）。该功能仅适用于中文和英文音频。</p><p>开启后，语音识别结果中的中文数字（如&quot;一百二十三&quot;）或英文数字（如&quot;one hundred&quot;）将自动转换为阿拉伯数字（如&quot;123&quot;）。</p><p>参数值：</p><ul><li>true：开启；</li><li>false：关闭。</li></ul></div></section></td><td><a id="qwen-asr-sync-examples"></a><h3>调用示例</h3><p>Qwen3-ASR-Flash 支持最长 5 分钟录音，输入支持公网音频文件 URL 或本地文件上传，可流式返回识别结果。</p><a id="sec-tabs-5"></a><section><a id="输入内容-音频文件url-2"></a><section><a id="输入内容-音频文件url-2-h4"></a><h4>输入内容：音频文件URL</h4><a id="fig-code-group-4"></a><div><a id="fig-code-group-4-code-1-tab"></a>Code 1<div><a id="code-code-group-4-code-1"></a><pre class="language-text"><code>curl -X POST &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation&quot; \
-H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
-H &quot;Content-Type: application/json&quot; \
-d '{
    &quot;model&quot;: &quot;qwen3-asr-flash&quot;,
    &quot;input&quot;: {
        &quot;messages&quot;: [
            {
                &quot;content&quot;: [
                    {
                        &quot;audio&quot;: &quot;{YOUR_AUDIO_URL}&quot;
                    }
                ],
                &quot;role&quot;: &quot;user&quot;
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;asr_options&quot;: {
            &quot;enable_itn&quot;: false
        }
    }
}'
</code></pre></div><a id="fig-code-group-4-code-2-tab"></a>Code 2<div><a id="code-code-group-4-code-2"></a><pre class="language-text"><code>import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;

public class Main {
    public static void simpleMultiModalConversationCall()
            throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage userMessage = MultiModalMessage.builder()
                .role(Role.USER.getValue())
                .content(Arrays.asList(
                        Collections.singletonMap(&quot;audio&quot;, &quot;{YOUR_AUDIO_URL}&quot;)))
                .build();

        Map&lt;String, Object&gt; asrOptions = new HashMap&lt;&gt;();
        asrOptions.put(&quot;enable_itn&quot;, false);
        // asrOptions.put(&quot;language&quot;, &quot;zh&quot;); // 可选，若已知音频的语种，可通过该参数指定待识别语种，以提升识别准确率
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 新加坡/美国地域和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：.apiKey(&quot;sk-xxx&quot;)
                .apiKey(System.getenv(&quot;DASHSCOPE_API_KEY&quot;))
                .model(&quot;qwen3-asr-flash&quot;)
                .message(userMessage)
                .parameter(&quot;asr_options&quot;, asrOptions)
                .build();
        MultiModalConversationResult result = conv.call(param);
        System.out.println(JsonUtils.toJson(result));
    }
    public static void main(String[] args) {
        try {
            // 以下为华北2（北京）地域的配置，调用时请将&quot;{WorkspaceId}&quot;替换为真实的业务空间ID，各地域的配置不同。
            Constants.baseHttpApiUrl = &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1&quot;;
            simpleMultiModalConversationCall();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
</code></pre></div><a id="fig-code-group-4-python-sdk-tab"></a>Python SDK<div><a id="code-code-group-4-python-sdk"></a><pre class="language-python"><code>import os
import dashscope

client = dashscope.Client(
    # 新加坡/美国地域和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    # 若没有配置环境变量，请将下行替换为自己的API Key：api_key=&quot;sk-xxx&quot;
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    # 以下为华北2（北京）地域的配置，调用时请将&quot;{WorkspaceId}&quot;替换为真实的业务空间ID，各地域的配置不同。
    workspace=&quot;{WorkspaceId}&quot;,
    region=&quot;cn-beijing&quot;,
)

messages = [
    {&quot;role&quot;: &quot;user&quot;, &quot;content&quot;: [{&quot;audio&quot;: &quot;{YOUR_AUDIO_URL}&quot;}]}
]

response = client.multimodal.chat.create(
    model=&quot;qwen3-asr-flash&quot;,
    messages=messages,
    parameters={
        &quot;asr_options&quot;: {
            # &quot;language&quot;: &quot;zh&quot;, # 可选，若已知音频的语种，可通过该参数指定待识别语种，以提升识别准确率
            &quot;enable_itn&quot;: False
        }
    }
)
print(response)
</code></pre></div></div></section><a id="输入内容-base64编码的音频文件-2"></a><section><a id="输入内容-base64编码的音频文件-2-h4"></a><h4>输入内容：Base64编码的音频文件</h4><p>可输入Base64编码数据（<a href="https://www.rfc-editor.org/rfc/rfc2397">Data URL</a>），格式为：<code>data:&lt;mediatype&gt;;base64,&lt;data&gt;</code>。</p><ul><li><p><code>&lt;mediatype&gt;</code>：MIME类型</p><p>因音频格式而异，例如：</p><ul><li>WAV：<code>audio/wav</code></li><li>MP3：<code>audio/mpeg</code></li></ul></li><li><p><code>&lt;data&gt;</code>：音频转成的Base64编码的字符串</p><p>Base64编码会增大体积，请控制原文件大小，确保编码后仍符合输入音频大小限制（10MB）</p></li><li><p>示例：<code>data:audio/mpeg;base64,SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU4LjI5LjEwMAAAAAAAAAAAAAAA//PAxABQ/BXRbMPe4IQAhl9</code></p><a id="accordion-点击查看示例代码-2"></a><section><p>点击查看示例代码</p><div><a id="fig-code-group-5"></a><div><a id="fig-code-group-5-python-tab"></a>python<div><a id="code-code-group-5-python"></a><pre class="language-python"><code>import base64, pathlib

# input.mp3为待识别的本地音频文件，请替换为自己的音频文件路径，确保其符合音频要求
file_path = pathlib.Path(&quot;{YOUR_AUDIO_FILE}&quot;)
base64_str = base64.b64encode(file_path.read_bytes()).decode()
data_uri = f&quot;data:audio/mpeg;base64,{base64_str}&quot;
</code></pre></div><a id="fig-code-group-5-java-tab"></a>java<div><a id="code-code-group-5-java"></a><pre class="language-java"><code>import java.nio.file.*;
import java.util.Base64;

public class Main {
    /**
     * filePath为待识别的本地音频文件，请替换为自己的音频文件路径，确保其符合音频要求
     */
    public static String toDataUrl(String filePath) throws Exception {
        byte[] bytes = Files.readAllBytes(Paths.get(filePath));
        String encoded = Base64.getEncoder().encodeToString(bytes);
        return &quot;data:audio/mpeg;base64,&quot; + encoded;
    }

    // 使用示例
    public static void main(String[] args) throws Exception {
        System.out.println(toDataUrl(&quot;{YOUR_AUDIO_FILE}&quot;));
    }
}
</code></pre></div></div></div></section></li></ul><a id="fig-code-group-6"></a><div><a id="fig-code-group-6-python-sdk-tab"></a>Python SDK<div><a id="code-code-group-6-python-sdk"></a><pre class="language-python"><code>import base64
import dashscope
import os
import pathlib

client = dashscope.Client(
    # 新加坡/美国地域和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    # 若没有配置环境变量，请将下行替换为自己的API Key：api_key=&quot;sk-xxx&quot;
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    # 以下为华北2（北京）地域的配置，调用时请将&quot;{WorkspaceId}&quot;替换为真实的业务空间ID，各地域的配置不同。
    workspace=&quot;{WorkspaceId}&quot;,
    region=&quot;cn-beijing&quot;,
)

# 请替换为实际的音频文件路径
file_path = &quot;{YOUR_AUDIO_FILE}&quot;
# 请替换为实际的音频文件MIME类型
audio_mime_type = &quot;audio/mpeg&quot;

file_path_obj = pathlib.Path(file_path)
if not file_path_obj.exists():
    raise FileNotFoundError(f&quot;音频文件不存在: {file_path}&quot;)

base64_str = base64.b64encode(file_path_obj.read_bytes()).decode()
data_uri = f&quot;data:{audio_mime_type};base64,{base64_str}&quot;

messages = [
    {&quot;role&quot;: &quot;user&quot;, &quot;content&quot;: [{&quot;audio&quot;: data_uri}]}
]
response = client.multimodal.chat.create(
    model=&quot;qwen3-asr-flash&quot;,
    messages=messages,
    parameters={
        &quot;asr_options&quot;: {
            # &quot;language&quot;: &quot;zh&quot;, # 可选，若已知音频的语种，可通过该参数指定待识别语种，以提升识别准确率
            &quot;enable_itn&quot;: False
        }
    }
)
print(response.output_text)
</code></pre></div><a id="fig-code-group-6-java-sdk-tab"></a>Java SDK<div><a id="code-code-group-6-java-sdk"></a><pre class="language-java"><code>import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;

public class Main {
    // 请替换为实际的音频文件路径
    private static final String AUDIO_FILE = &quot;{YOUR_AUDIO_FILE}&quot;;
    // 请替换为实际的音频文件MIME类型
    private static final String AUDIO_MIME_TYPE = &quot;audio/mpeg&quot;;

    public static void simpleMultiModalConversationCall()
            throws ApiException, NoApiKeyException, UploadFileException, IOException {
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage userMessage = MultiModalMessage.builder()
                .role(Role.USER.getValue())
                .content(Arrays.asList(
                        Collections.singletonMap(&quot;audio&quot;, toDataUrl())))
                .build();

        Map&lt;String, Object&gt; asrOptions = new HashMap&lt;&gt;();
        asrOptions.put(&quot;enable_itn&quot;, false);
        // asrOptions.put(&quot;language&quot;, &quot;zh&quot;); // 可选，若已知音频的语种，可通过该参数指定待识别语种，以提升识别准确率
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 新加坡/美国地域和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：.apiKey(&quot;sk-xxx&quot;)
                .apiKey(System.getenv(&quot;DASHSCOPE_API_KEY&quot;))
                .model(&quot;qwen3-asr-flash&quot;)
                .message(userMessage)
                .parameter(&quot;asr_options&quot;, asrOptions)
                .build();
        MultiModalConversationResult result = conv.call(param);
        System.out.println(JsonUtils.toJson(result));
    }

    public static void main(String[] args) {
        try {
            // 以下为华北2（北京）地域的配置，调用时请将&quot;{WorkspaceId}&quot;替换为真实的业务空间ID，各地域的配置不同。
            Constants.baseHttpApiUrl = &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1&quot;;
            simpleMultiModalConversationCall();
        } catch (ApiException | NoApiKeyException | UploadFileException | IOException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }

    // 生成 data URI
    public static String toDataUrl() throws IOException {
        byte[] bytes = Files.readAllBytes(Paths.get(AUDIO_FILE));
        String encoded = Base64.getEncoder().encodeToString(bytes);
        return &quot;data:&quot; + AUDIO_MIME_TYPE + &quot;;base64,&quot; + encoded;
    }
}
</code></pre></div></div></section><a id="输入内容-本地音频文件绝对路径"></a><section><a id="输入内容-本地音频文件绝对路径-h4"></a><h4>输入内容：本地音频文件绝对路径</h4><p>使用 DashScope SDK 处理本地音频文件时需传入文件路径。请参考下表，结合调用方式与操作系统创建对应路径。</p><table><thead><tr><th><p><strong>系统</strong></p></th><th><p><strong>SDK</strong></p></th><th><p><strong>传入的文件路径</strong></p></th><th><p><strong>示例</strong></p></th></tr></thead><tbody><tr><td rowspan="2"><p>Linux或macOS系统</p></td><td><p>Python SDK</p></td><td rowspan="2"><p>file://{文件的绝对路径}</p></td><td rowspan="2"><p>file:///home/images/test.png</p></td></tr><tr><td><p>Java SDK</p></td></tr><tr><td rowspan="2"><p>Windows系统</p></td><td><p>Python SDK</p></td><td><p>file://{文件的绝对路径}</p></td><td><p>file://D:/images/test.png</p></td></tr><tr><td><p>Java SDK</p></td><td><p>file:///{文件的绝对路径}</p></td><td><p>file:///D:/images/test.png</p></td></tr></tbody></table><div><div><p><strong>重要</strong>本地文件调用上限 100 QPS，不支持扩容，不适合生产环境、高并发或压测场景；如需更高并发，请将文件上传至 OSS 并通过 URL 方式调用。</p></div></div><a id="fig-code-group-7"></a><div><a id="fig-code-group-7-python-sdk-tab"></a>Python SDK<div><a id="code-code-group-7-python-sdk"></a><pre class="language-python"><code>import os

import dashscope

client = dashscope.Client(
    # 新加坡/美国地域和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    # 若没有配置环境变量，请将下行替换为自己的API Key：api_key=&quot;sk-xxx&quot;
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    # 以下为华北2（北京）地域的配置，调用时请将&quot;{WorkspaceId}&quot;替换为真实的业务空间ID，各地域的配置不同。
    workspace=&quot;{WorkspaceId}&quot;,
    region=&quot;cn-beijing&quot;,
)

# 请用您的本地音频的绝对路径替换 ABSOLUTE_PATH/{YOUR_AUDIO_FILE}
audio_file_path = &quot;file://ABSOLUTE_PATH/{YOUR_AUDIO_FILE}&quot;

messages = [
    {&quot;role&quot;: &quot;user&quot;, &quot;content&quot;: [{&quot;audio&quot;: audio_file_path}]}
]
response = client.multimodal.chat.create(
    model=&quot;qwen3-asr-flash&quot;,
    messages=messages,
    parameters={
        &quot;asr_options&quot;: {
            # &quot;language&quot;: &quot;zh&quot;, # 可选，若已知音频的语种，可通过该参数指定待识别语种，以提升识别准确率
            &quot;enable_itn&quot;: False
        }
    }
)
print(response.output_text)
</code></pre></div><a id="fig-code-group-7-java-sdk-tab"></a>Java SDK<div><a id="code-code-group-7-java-sdk"></a><pre class="language-java"><code>import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;

public class Main {
    public static void simpleMultiModalConversationCall()
            throws ApiException, NoApiKeyException, UploadFileException {
        // 请用您本地文件的绝对路径替换掉ABSOLUTE_PATH/{YOUR_AUDIO_FILE}
        String localFilePath = &quot;file://ABSOLUTE_PATH/{YOUR_AUDIO_FILE}&quot;;
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage userMessage = MultiModalMessage.builder()
                .role(Role.USER.getValue())
                .content(Arrays.asList(
                        Collections.singletonMap(&quot;audio&quot;, localFilePath)))
                .build();

        Map&lt;String, Object&gt; asrOptions = new HashMap&lt;&gt;();
        asrOptions.put(&quot;enable_itn&quot;, false);
        // asrOptions.put(&quot;language&quot;, &quot;zh&quot;); // 可选，若已知音频的语种，可通过该参数指定待识别语种，以提升识别准确率
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 新加坡/美国地域和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：.apiKey(&quot;sk-xxx&quot;)
                .apiKey(System.getenv(&quot;DASHSCOPE_API_KEY&quot;))
                .model(&quot;qwen3-asr-flash&quot;)
                .message(userMessage)
                .parameter(&quot;asr_options&quot;, asrOptions)
                .build();
        MultiModalConversationResult result = conv.call(param);
        System.out.println(JsonUtils.toJson(result));
    }
    public static void main(String[] args) {
        try {
            // 以下为华北2（北京）地域的配置，调用时请将&quot;{WorkspaceId}&quot;替换为真实的业务空间ID，各地域的配置不同。
            Constants.baseHttpApiUrl = &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1&quot;;
            simpleMultiModalConversationCall();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
</code></pre></div></div></section><a id="流式输出"></a><section><a id="流式输出-h4"></a><h4>流式输出</h4><a id="qwen-asr-streaming-examples"></a><p>模型逐步生成中间结果，最终结果由其拼接而成。非流式调用需等待全部结果生成后一次性返回；流式调用边生成边返回，可显著降低首字延迟。根据调用方式选择对应的流式参数：</p><ul><li>DashScope Python SDK方式：设置<code>stream</code>参数为true。</li><li>DashScope Java SDK方式：需要通过<code>streamCall</code>接口调用。</li><li>DashScope HTTP方式：需要在Header中指定<code>X-DashScope-SSE</code>为<code>enable</code>。</li></ul><a id="sec-tabs-6"></a><section><a id="python-sdk-2"></a><section><a id="python-sdk-2-h4"></a><h4>Python SDK</h4><a id="code-block-4"></a><pre class="language-python"><code>import os

import dashscope

client = dashscope.Client(
    # 新加坡/美国地域和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    # 若没有配置环境变量，请将下行替换为自己的API Key：api_key=&quot;sk-xxx&quot;
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    # 以下为华北2（北京）地域的配置，调用时请将&quot;{WorkspaceId}&quot;替换为真实的业务空间ID，各地域的配置不同。
    workspace=&quot;{WorkspaceId}&quot;,
    region=&quot;cn-beijing&quot;,
)

messages = [
    {&quot;role&quot;: &quot;user&quot;, &quot;content&quot;: [{&quot;audio&quot;: &quot;{YOUR_AUDIO_URL}&quot;}]}
]
stream = client.multimodal.chat.create(
    model=&quot;qwen3-asr-flash&quot;,
    messages=messages,
    parameters={
        &quot;asr_options&quot;: {
            # &quot;language&quot;: &quot;zh&quot;, # 可选，若已知音频的语种，可通过该参数指定待识别语种，以提升识别准确率
            &quot;enable_itn&quot;: False
        }
    },
    stream=True
)

for chunk in stream:
    try:
        print(chunk.choices[0].delta.content or &quot;&quot;)
    except Exception as e:
        print(f&quot;解析响应失败：{e}&quot;)
</code></pre></section><a id="java-sdk"></a><section><a id="java-sdk-h4"></a><h4>Java SDK</h4><a id="code-block-5"></a><pre class="language-java"><code>import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;
import io.reactivex.Flowable;

public class Main {
    public static void simpleMultiModalConversationCall()
            throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage userMessage = MultiModalMessage.builder()
                .role(Role.USER.getValue())
                .content(Arrays.asList(
                        Collections.singletonMap(&quot;audio&quot;, &quot;{YOUR_AUDIO_URL}&quot;)))
                .build();

        Map&lt;String, Object&gt; asrOptions = new HashMap&lt;&gt;();
        asrOptions.put(&quot;enable_itn&quot;, false);
        // asrOptions.put(&quot;language&quot;, &quot;zh&quot;); // 可选，若已知音频的语种，可通过该参数指定待识别语种，以提升识别准确率
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 新加坡/美国地域和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：.apiKey(&quot;sk-xxx&quot;)
                .apiKey(System.getenv(&quot;DASHSCOPE_API_KEY&quot;))
                .model(&quot;qwen3-asr-flash&quot;)
                .message(userMessage)
                .parameter(&quot;asr_options&quot;, asrOptions)
                .build();
        Flowable&lt;MultiModalConversationResult&gt; resultFlowable = conv.streamCall(param);
        resultFlowable.blockingForEach(item -&gt; {
            try {
                System.out.println(item.getOutput().getChoices().get(0).getMessage().getContent().get(0).get(&quot;text&quot;));
            } catch (Exception e){
                System.out.println(&quot;解析响应失败：&quot; + e.getMessage());
                System.exit(1);
            }
        });
    }

    public static void main(String[] args) {
        try {
            // 以下为华北2（北京）地域的配置，调用时请将&quot;{WorkspaceId}&quot;替换为真实的业务空间ID，各地域的配置不同。
            Constants.baseHttpApiUrl = &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1&quot;;
            simpleMultiModalConversationCall();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
</code></pre></section><a id="curl-2"></a><section><a id="curl-2-h4"></a><h4>cURL</h4><p>以下为华北2（北京）地域的配置，调用时请将<code>{WorkspaceId}</code>替换为真实的<a href="../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain">Workspace ID</a>，各地域的配置不同。</p><a id="code-block-6"></a><pre class="language-bash"><code>curl -X POST &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation&quot; \
-H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
-H &quot;Content-Type: application/json&quot; \
-H &quot;X-DashScope-SSE: enable&quot; \
-d '{
    &quot;model&quot;: &quot;qwen3-asr-flash&quot;,
    &quot;input&quot;: {
        &quot;messages&quot;: [
            {
                &quot;content&quot;: [
                    {
                        &quot;audio&quot;: &quot;{YOUR_AUDIO_URL}&quot;
                    }
                ],
                &quot;role&quot;: &quot;user&quot;
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;incremental_output&quot;: true,
        &quot;asr_options&quot;: {
            &quot;enable_itn&quot;: false
        }
    }
}'
</code></pre></section></section></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="0e1c44902ea1e"></a><h3>响应参数</h3><p><strong>request_id</strong><code>string</code></p><p>本次调用的唯一标识符。</p><div><div><p><strong>说明</strong>Java SDK返回参数为<code>requestId</code>。</p></div></div><p><strong>output</strong><code>object</code></p><p>调用结果信息。</p><a id="accordion-属性-16"></a><section><p>属性</p><div><p><strong>choices</strong><code>array</code></p><p>模型的输出信息。当result_format为message时返回choices参数。</p><a id="accordion-属性-17"></a><section><p>属性</p><div><p><strong>finish_reason</strong><code>string</code></p><p>有三种情况：</p><ul><li>正在生成时为null；</li><li>因模型输出自然结束，或触发输入参数中的stop条件而结束时为stop；</li><li>因生成长度过长而结束为length。</li></ul><p><strong>message</strong><code>object</code></p><p>模型输出的消息对象。</p><a id="accordion-属性-18"></a><section><p>属性</p><div><p><strong>role</strong><code>string</code></p><p>输出消息的角色，固定为assistant。</p><p><strong>content</strong><code>array</code></p><p>输出消息的内容。</p><a id="accordion-属性-19"></a><section><p>属性</p><div><p><strong>text</strong><code>string</code></p><p>语音识别结果。</p></div></section><p><strong>annotations</strong><code>array</code></p><p>输出标注信息（如语种）</p><a id="accordion-属性-20"></a><section><p>属性</p><div><p><strong>language</strong><code>string</code></p><p>被识别音频的语种。当请求参数<code>language</code>已指定语种时，该值与所指定的参数一致。</p><a id="accordion-取值范围-4"></a><section><p>取值范围</p><div><ul><li>zh：中文（普通话、四川话、闽南语、吴语）</li><li>yue：粤语</li><li>en：英文</li><li>ja：日语</li><li>de：德语</li><li>ko：韩语</li><li>ru：俄语</li><li>fr：法语</li><li>pt：葡萄牙语</li><li>ar：阿拉伯语</li><li>it：意大利语</li><li>es：西班牙语</li><li>hi：印地语</li><li>id：印尼语</li><li>th：泰语</li><li>tr：土耳其语</li><li>uk：乌克兰语</li><li>vi：越南语</li><li>cs：捷克语</li><li>da：丹麦语</li><li>fil：菲律宾语</li><li>fi：芬兰语</li><li>is：冰岛语</li><li>ms：马来语</li><li>no：挪威语</li><li>pl：波兰语</li><li>sv：瑞典语</li></ul></div></section><p><strong>type</strong><code>string</code></p><p>固定为<code>audio_info</code>，表示音频信息。</p><p><strong>emotion</strong><code>string</code></p><p>被识别音频的情感。情感识别固定开启，无需额外配置。支持的情感如下：</p><ul><li><code>surprised</code>：惊讶</li><li><code>neutral</code>：平静</li><li><code>happy</code>：愉快</li><li><code>sad</code>：悲伤</li><li><code>disgusted</code>：厌恶</li><li><code>angry</code>：愤怒</li><li><code>fearful</code>：恐惧</li></ul></div></section></div></section></div></section></div></section><p><strong>usage</strong><code>object</code></p><p>本次请求的Token消耗信息。</p><a id="accordion-属性-21"></a><section><p>属性</p><div><p><strong>input_tokens_details</strong> <code>object</code></p><p>千问3-ASR-Flash输入内容长度（Token）。</p><a id="accordion-属性-22"></a><section><p>属性</p><div><p><strong>text_tokens</strong> <code>integer</code></p><p>无需关注该参数。</p></div></section><p><strong>output_tokens_details</strong> <code>object</code></p><p>千问3-ASR-Flash输出内容长度（Token）。</p><a id="accordion-属性-23"></a><section><p>属性</p><div><p><strong>text_tokens</strong> <code>integer</code></p><p>千问3-ASR-Flash输出的识别结果文本长度（Token）。</p></div></section><p><strong>seconds</strong> <code>integer</code></p><p>千问3-ASR-Flash音频时长（秒）。</p></div></section></td><td><a id="code-block-7"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;choices&quot;: [
            {
                &quot;finish_reason&quot;: &quot;stop&quot;,
                &quot;message&quot;: {
                    &quot;annotations&quot;: [
                        {
                            &quot;language&quot;: &quot;zh&quot;,
                            &quot;type&quot;: &quot;audio_info&quot;,
                            &quot;emotion&quot;: &quot;neutral&quot;
                        }
                    ],
                    &quot;content&quot;: [
                        {
                            &quot;text&quot;: &quot;欢迎使用阿里云。&quot;
                        }
                    ],
                    &quot;role&quot;: &quot;assistant&quot;
                }
            }
        ]
    },
    &quot;usage&quot;: {
        &quot;input_tokens_details&quot;: {
            &quot;text_tokens&quot;: 0
        },
        &quot;output_tokens_details&quot;: {
            &quot;text_tokens&quot;: 6
        },
        &quot;seconds&quot;: 1
    },
    &quot;request_id&quot;: &quot;568e2bf0-d6f2-97f8-9f15-a57b11dc6977&quot;
}
</code></pre></td></tr></tbody></table>

<a id="dashscope异步调用"></a>

<a id="9937e8884002q"></a>

## DashScope异步调用

<a id="流程说明"></a>

<a id="4a1eca9360nd1"></a>

### 流程说明

与OpenAI兼容模式或DashScope同步调用（均为一次请求、立即返回结果）不同，异步调用专为处理长音频文件或耗时较长的任务设计，该模式采用“提交-轮询”的两步式流程，避免了因长时间等待而导致的请求超时：

1.  第一步：提交任务
    
    -   客户端发起一个异步处理请求。
    -   服务器验证请求后，不会立即执行任务，而是返回一个唯一的 `task_id`，表示任务已成功创建。
2.  第二步：获取结果
    
    -   客户端使用获取到的 `task_id`，通过轮询方式反复调用结果查询接口。
    -   当任务处理完成后，结果查询接口将返回最终的识别结果。

您可以根据集成环境选择使用SDK或直接调用RESTful API。

-   使用 SDK（示例代码请参见[调用示例](qwen-asr-api-reference-6234af32190b8ba9.md#qwen-asr-async-examples)，请求参数请参见[提交任务](qwen-asr-api-reference-6234af32190b8ba9.md#88657039c4x0g)的请求参数[请求参数](qwen-asr-api-reference-6234af32190b8ba9.md#1a2369eebaueh)，返回结果请参见[异步调用识别结果说明](qwen-asr-api-reference-6234af32190b8ba9.md#2c27ad3e80p4y)）
    
    SDK封装了底层的API调用细节，提供了更便捷的编程体验。
    
    1.  提交任务：Python SDK 调用 `client.audio.asr.jobs.create` 创建任务，此方法将返回一个包含 `task_id` 的任务对象；Java SDK 调用 `asyncCall()` 方法提交任务。
    2.  获取结果：Python SDK 调用 `client.audio.asr.jobs.fetch` 查询任务执行结果，或调用 `client.audio.asr.jobs.wait` 等待任务结束（内部自动处理轮询逻辑，直到任务完成或超时）；Java SDK 使用上一步返回的任务对象或 `task_id`，调用 `fetch()` 方法获取结果。
-   2.  使用 RESTful API
    
    直接调用HTTP接口提供了最大的灵活性。
    
    1.  [提交任务](qwen-asr-api-reference-6234af32190b8ba9.md#88657039c4x0g)，如果请求成功，响应参数[响应参数](qwen-asr-api-reference-6234af32190b8ba9.md#eca6c7d3f35hn)中将包含一个 `task_id`。
    2.  使用上一步获取的 `task_id`，[获取任务执行结果](qwen-asr-api-reference-6234af32190b8ba9.md#f9109f6ea3di2)。

<a id="完整示例"></a>

<a id="qwen-asr-async-examples"></a>

### 完整示例

<a id="sec-tabs-7"></a>

<a id="http"></a>

<a id="http-h4"></a>

#### HTTP

<a id="fig-code-group-8"></a>

<a id="fig-code-group-8-java-tab"></a>

Java

<a id="code-code-group-8-java"></a>

```java
import com.google.gson.Gson;
import com.google.gson.annotations.SerializedName;
import okhttp3.*;

import java.io.IOException;
import java.util.concurrent.TimeUnit;

public class Main {
    // 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
    private static final String API_URL_SUBMIT = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/asr/transcription";
    // 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
    private static final String API_URL_QUERY = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/";
    private static final Gson gson = new Gson();

    public static void main(String[] args) {
        // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：String apiKey = "sk-xxx"
        String apiKey = System.getenv("DASHSCOPE_API_KEY");

        OkHttpClient client = new OkHttpClient();

        // 1. 提交任务
        String payloadJson = """
                {
                    "model": "qwen3-asr-flash-filetrans",
                    "input": {
                        "file_url": "{YOUR_AUDIO_URL}"
                    },
                    "parameters": {
                        "channel_id": [0],
                        "enable_itn": false,
                        "enable_words": true
                    }
                }
                """;

        RequestBody body = RequestBody.create(payloadJson, MediaType.get("application/json; charset=utf-8"));
        Request submitRequest = new Request.Builder()
                .url(API_URL_SUBMIT)
                .addHeader("Authorization", "Bearer " + apiKey)
                .addHeader("Content-Type", "application/json")
                .addHeader("X-DashScope-Async", "enable")
                .post(body)
                .build();

        String taskId = null;

        try (Response response = client.newCall(submitRequest).execute()) {
            if (response.isSuccessful() && response.body() != null) {
                String respBody = response.body().string();
                ApiResponse apiResp = gson.fromJson(respBody, ApiResponse.class);
                if (apiResp.output != null) {
                    taskId = apiResp.output.taskId;
                    System.out.println("任务已提交，task_id: " + taskId);
                } else {
                    System.out.println("提交返回内容: " + respBody);
                    return;
                }
            } else {
                System.out.println("任务提交失败! HTTP code: " + response.code());
                if (response.body() != null) {
                    System.out.println(response.body().string());
                }
                return;
            }
        } catch (IOException e) {
            e.printStackTrace();
            return;
        }

        // 2. 轮询任务状态
        boolean finished = false;
        while (!finished) {
            try {
                TimeUnit.SECONDS.sleep(2);  // 等待 2 秒再查询
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                return;
            }

            String queryUrl = API_URL_QUERY + taskId;
            Request queryRequest = new Request.Builder()
                    .url(queryUrl)
                    .addHeader("Authorization", "Bearer " + apiKey)
                    .addHeader("Content-Type", "application/json")
                    .get()
                    .build();

            try (Response response = client.newCall(queryRequest).execute()) {
                if (response.body() != null) {
                    String queryResponse = response.body().string();
                    ApiResponse apiResp = gson.fromJson(queryResponse, ApiResponse.class);

                    if (apiResp.output != null && apiResp.output.taskStatus != null) {
                        String status = apiResp.output.taskStatus;
                        System.out.println("当前任务状态: " + status);
                        if ("SUCCEEDED".equalsIgnoreCase(status)
                                || "FAILED".equalsIgnoreCase(status)
                                || "UNKNOWN".equalsIgnoreCase(status)) {
                            finished = true;
                            System.out.println("任务完成，最终结果: ");
                            System.out.println(queryResponse);
                        }
                    } else {
                        System.out.println("查询返回内容: " + queryResponse);
                    }
                }
            } catch (IOException e) {
                e.printStackTrace();
                return;
            }
        }
    }

    static class ApiResponse {
        @SerializedName("request_id")
        String requestId;
        Output output;
    }

    static class Output {
        @SerializedName("task_id")
        String taskId;
        @SerializedName("task_status")
        String taskStatus;
    }
}
```

<a id="fig-code-group-8-python-tab"></a>

Python

<a id="code-code-group-8-python"></a>

```python
import os
import time
import requests
import json

# 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
API_URL_SUBMIT = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/asr/transcription"
# 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
API_URL_QUERY_BASE = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/"

def main():
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key = "sk-xxx"
    api_key = os.getenv("DASHSCOPE_API_KEY")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "X-DashScope-Async": "enable"
    }

    # 1. 提交任务
    payload = {
        "model": "qwen3-asr-flash-filetrans",
        "input": {
            "file_url": "{YOUR_AUDIO_URL}"
        },
        "parameters": {
            "channel_id": [0],
            # "language": "zh",
            "enable_itn": False,
            "enable_words": True
        }
    }

    print("提交 ASR 转写任务...")
    try:
        submit_resp = requests.post(API_URL_SUBMIT, headers=headers, data=json.dumps(payload))
    except requests.RequestException as e:
        print(f"请求提交任务失败: {e}")
        return

    if submit_resp.status_code != 200:
        print(f"任务提交失败! HTTP code: {submit_resp.status_code}")
        print(submit_resp.text)
        return

    resp_data = submit_resp.json()
    output = resp_data.get("output")
    if not output or "task_id" not in output:
        print("提交返回内容异常:", resp_data)
        return

    task_id = output["task_id"]
    print(f"任务已提交，task_id: {task_id}")

    # 2. 轮询任务状态
    finished = False
    while not finished:
        time.sleep(2)  # 等待 2 秒再查询

        query_url = API_URL_QUERY_BASE + task_id
        try:
            query_resp = requests.get(query_url, headers={"Authorization": f"Bearer {api_key}"})
        except requests.RequestException as e:
            print(f"请求查询任务失败: {e}")
            return

        if query_resp.status_code != 200:
            print(f"查询任务失败! HTTP code: {query_resp.status_code}")
            print(query_resp.text)
            return

        query_data = query_resp.json()
        output = query_data.get("output")
        if output and "task_status" in output:
            status = output["task_status"]
            print(f"当前任务状态: {status}")

            if status.upper() in ("SUCCEEDED", "FAILED", "UNKNOWN"):
                finished = True
                print("任务完成，最终结果如下：")
                print(json.dumps(query_data, indent=2, ensure_ascii=False))
        else:
            print("查询返回内容:", query_data)

if __name__ == "__main__":
    main()
```

<a id="java-sdk-2"></a>

<a id="java-sdk-2-h4"></a>

#### Java SDK

<a id="code-block-8"></a>

```java
import com.alibaba.dashscope.audio.qwen_asr.*;
import com.alibaba.dashscope.utils.Constants;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonObject;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.HashMap;

public class Main {
    public static void main(String[] args) {
        // 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
        QwenTranscriptionParam param =
                QwenTranscriptionParam.builder()
                        // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                        // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：.apiKey("sk-xxx")
                        .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                        .model("qwen3-asr-flash-filetrans")
                        .fileUrl("{YOUR_AUDIO_URL}")
                        //.parameter("language", "zh")
                        //.parameter("channel_id", new ArrayList<String>(){{add("0");add("1");}})
                        .parameter("enable_itn", false)
                        .parameter("enable_words", true)
                        .build();
        try {
            QwenTranscription transcription = new QwenTranscription();
            // 提交任务
            QwenTranscriptionResult result = transcription.asyncCall(param);
            System.out.println("create task result: " + result);
            // 检查任务是否提交成功
            if (result.getTaskId() == null) {
                System.out.println("Error: " + result.getOutput());
                return;
            }
            // 查询任务状态
            result = transcription.fetch(QwenTranscriptionQueryParam.FromTranscriptionParam(param, result.getTaskId()));
            System.out.println("task status: " + result);
            // 等待任务完成
            result =
                    transcription.wait(
                            QwenTranscriptionQueryParam.FromTranscriptionParam(param, result.getTaskId()));
            System.out.println("task result: " + result);
            // 获取语音识别结果
            QwenTranscriptionTaskResult taskResult = result.getResult();
            if (taskResult != null) {
                // 获取识别结果的url
                String transcriptionUrl = taskResult.getTranscriptionUrl();
                // 获取url内对应的结果
                HttpURLConnection connection =
                        (HttpURLConnection) new URL(transcriptionUrl).openConnection();
                connection.setRequestMethod("GET");
                connection.connect();
                BufferedReader reader =
                        new BufferedReader(new InputStreamReader(connection.getInputStream()));
                // 格式化输出json结果
                Gson gson = new GsonBuilder().setPrettyPrinting().create();
                System.out.println(gson.toJson(gson.fromJson(reader, JsonObject.class)));
            }
        } catch (Exception e) {
            System.out.println("error: " + e);
        }
    }
}
```

<a id="python-sdk-3"></a>

<a id="python-sdk-3-h4"></a>

#### Python SDK

<a id="code-block-9"></a>

```python
import os

import dashscope

# run the transcription script
if __name__ == '__main__':
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    # 若没有配置环境变量，请将下行替换为自己的API Key：api_key="sk-xxx"
    client = dashscope.Client(
    # 新加坡/美国地域和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    # 若没有配置环境变量，请将下行替换为自己的API Key：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
    workspace="{WorkspaceId}",
    region="cn-beijing",
)
    # 提交任务
    job = client.audio.asr.jobs.create(
        model='qwen3-asr-flash-filetrans',
        file_urls=['{YOUR_AUDIO_URL}'],
        parameters={
            # 'language': 'zh',
            'enable_itn': False,
            'enable_words': True
        }
    )
    print(f'task_response: {job}')
    print(job.task_id)
    # 查询任务执行结果
    job = client.audio.asr.jobs.fetch(job.task_id)
    print(f'query_response: {job}')
    # 等待任务结束
    job = client.audio.asr.jobs.wait(job.task_id)
    print(f'task_result: {job}')
```

<a id="下载识别结果"></a>

<a id="下载识别结果-h4"></a>

#### 下载识别结果

任务成功后，查询接口返回的 `output.result.transcription_url` 指向公网可下载的 JSON 文件，包含完整识别结果。该 URL 默认在 **24 小时**内有效，请及时下载并落盘保存。

<a id="code-block-10"></a>

```bash
# 将 {transcription_url} 替换为查询接口返回的 transcription_url 值
curl -sS '{transcription_url}' -o transcription.json
cat transcription.json | jq .
```

<a id="提交任务"></a>

<a id="88657039c4x0g"></a>

### 提交任务

<a id="url-3"></a>

<a id="8ebdb3a43eq9j"></a>

#### URL

<a id="sec-tabs-8"></a>

<a id="华北2-北京-3"></a>

<a id="华北2-北京-3-h4"></a>

#### 华北2（北京）

HTTP请求地址：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/asr/transcription`

SDK调用配置的base\_url：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="新加坡-3"></a>

<a id="新加坡-3-h4"></a>

#### 新加坡

HTTP请求地址：`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/audio/asr/transcription`

SDK调用配置的base\_url：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

> **重要**
>
> 阿里云百炼为华北2（北京）、新加坡地域推出了业务空间专属域名，能够为推理请求提供卓越的性能和更高的稳定性，建议迁移至新域名：
>
> -   华北2（北京）地域：从 `dashscope.aliyuncs.com` 迁移至 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
> -   新加坡地域：从 `dashscope-intl.aliyuncs.com` 迁移至 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`

<table><tbody><tr><td><a id="1a2369eebaueh"></a><h4>请求参数</h4><p><strong>model</strong><code>string</code><strong>（必选）</strong></p><p><a href="../model-user-guide/model-experience/speech-and-audio/speech-recognition/non-realtime-speech-recognition-user-guide.md">模型</a>名称。仅适用于千问3-ASR-Flash-Filetrans模型。</p><p><strong>input</strong><code>object</code><strong>（必选）</strong></p><a id="accordion-属性-24"></a><section><p>属性</p><div><p><strong>file_url</strong> <code>string</code><strong>（必选）</strong></p><p>待识别音频文件URL，URL必须公网可访问。</p><p>使用SDK时，若录音文件存储在<a href="https://help.aliyun.com/zh/oss/user-guide/simple-upload#a632b50f190j8">阿里云OSS</a>，不支持使用以 <code>oss://</code>为前缀的临时 URL。</p><p>使用RESTful API时，若录音文件存储在<a href="https://help.aliyun.com/zh/oss/user-guide/simple-upload#a632b50f190j8">阿里云OSS</a>，支持使用以 <code>oss://</code>为前缀的临时 URL。但需注意：</p><div><div><p><strong>重要</strong></p><ul><li>临时 URL 有效期48小时，过期后无法使用，<strong>请勿用于生产环境。</strong></li><li>文件上传凭证接口限流为 100 QPS 且不支持扩容，<strong>请勿用于生产环境、高并发及压测场景。</strong></li><li>生产环境建议使用<a href="https://help.aliyun.com/zh/oss/user-guide/what-is-oss">阿里云OSS</a> 等稳定存储，确保文件长期可用并规避限流问题。</li></ul></div></div></div></section><p><strong>parameters</strong><code>object</code>（可选）</p><a id="accordion-属性-25"></a><section><p>属性</p><div><p><strong>language</strong> <em>string</em>（可选）无默认值</p><p>若已知音频的语种，可通过该参数指定待识别语种，以提升识别准确率。</p><p>只能指定一个语种。</p><p>若音频语种不确定，或包含多种语种（例如中英日韩混合），请勿指定该参数。</p><a id="accordion-取值范围-5"></a><section><p>取值范围</p><div><ul><li>zh：中文（普通话、四川话、闽南语、吴语）</li><li>yue：粤语</li><li>en：英文</li><li>ja：日语</li><li>de：德语</li><li>ko：韩语</li><li>ru：俄语</li><li>fr：法语</li><li>pt：葡萄牙语</li><li>ar：阿拉伯语</li><li>it：意大利语</li><li>es：西班牙语</li><li>hi：印地语</li><li>id：印尼语</li><li>th：泰语</li><li>tr：土耳其语</li><li>uk：乌克兰语</li><li>vi：越南语</li><li>cs：捷克语</li><li>da：丹麦语</li><li>fil：菲律宾语</li><li>fi：芬兰语</li><li>is：冰岛语</li><li>ms：马来语</li><li>no：挪威语</li><li>pl：波兰语</li><li>sv：瑞典语</li></ul></div></section><p><strong>enable_itn</strong><code>boolean</code>（可选）默认值为<code>false</code></p><p>是否启用ITN（Inverse Text Normalization，逆文本标准化）。该功能仅适用于中文和英文音频。</p><p>开启后，语音识别结果中的中文数字（如&quot;一百二十三&quot;）或英文数字（如&quot;one hundred&quot;）将自动转换为阿拉伯数字（如&quot;123&quot;）。</p><p>参数值：</p><ul><li>true：开启；</li><li>false：关闭。</li></ul><p><strong>enable_words</strong><code>boolean</code>（可选）默认值为<code>false</code></p><p>控制是否返回字级别时间戳：</p><ul><li><p><code>false</code>：返回句级时间戳</p></li><li><p><code>true</code>：返回字级时间戳</p><p>字级别时间戳仅支持以下语种：中文、英语、日语、韩语、德语、法语、西班牙语、意大利语、葡萄牙语、俄语，其他语种可能无法保证准确性</p></li></ul><p>同时，该参数还影响断句规则：</p><ul><li><code>false</code>：基于 VAD（语音活动检测）断句</li><li><code>true</code>：基于 VAD + 标点符号断句</li></ul><p><strong>channel_id</strong><code>array</code>（可选）默认值为<code>[0]</code></p><p>指定在多音轨音频文件中需要识别的音轨索引，索引从 0 开始。例如，[0] 表示识别第一个音轨，[0, 1] 表示同时识别第一和第二个音轨。如果省略此参数，则默认处理第一个音轨。</p><div><div><p><strong>重要</strong>指定的每一个音轨都将独立计费。例如，为单个文件请求 [0, 1] 会产生两笔独立的费用。</p></div></div></div></section></td><td><a id="sec-tabs-9"></a><section><a id="curl-3"></a><section><a id="curl-3-h4"></a><h4>cURL</h4><a id="code-block-11"></a><pre class="language-bash"><code># ======= 重要提示 =======
# 以下为华北2（北京）地域的配置，调用时请将&quot;{WorkspaceId}&quot;替换为真实的业务空间ID，各地域的配置不同。
# 新加坡地域和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# === 执行时请删除该注释 ===

curl --location --request POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/asr/transcription' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header &quot;Content-Type: application/json&quot; \
--header &quot;X-DashScope-Async: enable&quot; \
--data '{
    &quot;model&quot;: &quot;qwen3-asr-flash-filetrans&quot;,
    &quot;input&quot;: {
        &quot;file_url&quot;: &quot;{YOUR_AUDIO_URL}&quot;
    },
    &quot;parameters&quot;: {
        &quot;channel_id&quot;:[
            0
        ],
        &quot;enable_itn&quot;: false
    }
}'
</code></pre></section><a id="java"></a><section><a id="java-h4"></a><h4>Java</h4><p>SDK示例请参见<a href="qwen-asr-api-reference-6234af32190b8ba9.md#qwen-asr-async-examples">调用示例</a>。</p><a id="code-block-12"></a><pre class="language-java"><code>import com.google.gson.Gson;
import com.google.gson.annotations.SerializedName;
import okhttp3.*;

import java.io.IOException;

public class Main {
    // 以下为华北2（北京）地域的配置，调用时请将&quot;{WorkspaceId}&quot;替换为真实的业务空间ID，各地域的配置不同。
    private static final String API_URL = &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/asr/transcription&quot;;

    public static void main(String[] args) {
        // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        // 若没有配置环境变量，请用百炼API Key将下行替换为：String apiKey = &quot;sk-xxx&quot;
        String apiKey = System.getenv(&quot;DASHSCOPE_API_KEY&quot;);

        OkHttpClient client = new OkHttpClient();
        Gson gson = new Gson();

        /*String payloadJson = &quot;&quot;&quot;
                {
                    &quot;model&quot;: &quot;qwen3-asr-flash-filetrans&quot;,
                    &quot;input&quot;: {
                        &quot;file_url&quot;: &quot;{YOUR_AUDIO_URL}&quot;
                    },
                    &quot;parameters&quot;: {
                        &quot;channel_id&quot;: [0],
                        &quot;enable_itn&quot;: false,
                        &quot;language&quot;: &quot;zh&quot;,
                        &quot;corpus&quot;: {
                            &quot;text&quot;: &quot;&quot;
                        }
                    }
                }
                &quot;&quot;&quot;;*/
        String payloadJson = &quot;&quot;&quot;
                {
                    &quot;model&quot;: &quot;qwen3-asr-flash-filetrans&quot;,
                    &quot;input&quot;: {
                        &quot;file_url&quot;: &quot;{YOUR_AUDIO_URL}&quot;
                    },
                    &quot;parameters&quot;: {
                        &quot;channel_id&quot;: [0],
                        &quot;enable_itn&quot;: false
                    }
                }
                &quot;&quot;&quot;;

        RequestBody body = RequestBody.create(payloadJson, MediaType.get(&quot;application/json; charset=utf-8&quot;));
        Request request = new Request.Builder()
                .url(API_URL)
                .addHeader(&quot;Authorization&quot;, &quot;Bearer &quot; + apiKey)
                .addHeader(&quot;Content-Type&quot;, &quot;application/json&quot;)
                .addHeader(&quot;X-DashScope-Async&quot;, &quot;enable&quot;)
                .post(body)
                .build();

        try (Response response = client.newCall(request).execute()) {
            if (response.isSuccessful() &amp;&amp; response.body() != null) {
                String respBody = response.body().string();
                // 用 Gson 解析 JSON
                ApiResponse apiResp = gson.fromJson(respBody, ApiResponse.class);
                if (apiResp.output != null) {
                    System.out.println(&quot;task_id: &quot; + apiResp.output.taskId);
                } else {
                    System.out.println(respBody);
                }
            } else {
                System.out.println(&quot;task failed! HTTP code: &quot; + response.code());
                if (response.body() != null) {
                    System.out.println(response.body().string());
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    static class ApiResponse {
        @SerializedName(&quot;request_id&quot;)
        String requestId;

        Output output;
    }

    static class Output {
        @SerializedName(&quot;task_id&quot;)
        String taskId;

        @SerializedName(&quot;task_status&quot;)
        String taskStatus;
    }
}
</code></pre></section><a id="python"></a><section><a id="python-h4"></a><h4>Python</h4><p>SDK示例请参见<a href="qwen-asr-api-reference-6234af32190b8ba9.md#qwen-asr-async-examples">调用示例</a>。</p><a id="code-block-13"></a><pre class="language-python"><code>import requests
import json
import os

# 以下为华北2（北京）地域的配置，调用时请将&quot;{WorkspaceId}&quot;替换为真实的业务空间ID，各地域的配置不同。
url = &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/asr/transcription&quot;

# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 若没有配置环境变量，请用百炼API Key将下行替换为：DASHSCOPE_API_KEY = &quot;sk-xxx&quot;
DASHSCOPE_API_KEY = os.getenv(&quot;DASHSCOPE_API_KEY&quot;)

headers = {
    &quot;Authorization&quot;: f&quot;Bearer {DASHSCOPE_API_KEY}&quot;,
    &quot;Content-Type&quot;: &quot;application/json&quot;,
    &quot;X-DashScope-Async&quot;: &quot;enable&quot;
}

payload = {
    &quot;model&quot;: &quot;qwen3-asr-flash-filetrans&quot;,
    &quot;input&quot;: {
        &quot;file_url&quot;: &quot;{YOUR_AUDIO_URL}&quot;
    },
    &quot;parameters&quot;: {
        &quot;channel_id&quot;: [0],
        # &quot;language&quot;: &quot;zh&quot;,
        &quot;enable_itn&quot;: False
        # &quot;corpus&quot;: {
        #     &quot;text&quot;: &quot;&quot;
        # }
    }
}

response = requests.post(url, headers=headers, data=json.dumps(payload))
if response.status_code == 200:
    print(f&quot;task_id: {response.json()[&quot;output&quot;][&quot;task_id&quot;]}&quot;)
else:
    print(&quot;task failed!&quot;)
    print(response.json())
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="eca6c7d3f35hn"></a><h4>响应参数</h4><p><strong>request_id</strong><code>string</code></p><p>本次调用的唯一标识符。</p><p><strong>output</strong><code>object</code></p><p>调用结果信息。</p><a id="accordion-属性-26"></a><section><p>属性</p><div><p><strong>task_id</strong><code>string</code></p><p>任务ID。该ID在查询语音识别任务接口中作为请求参数传入。</p><p><strong>task_status</strong><code>string</code></p><p>任务状态：</p><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section></td><td><a id="code-block-14"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;92e3decd-0c69-47a8-************&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;8fab76d0-0eed-4d20-************&quot;,
        &quot;task_status&quot;: &quot;PENDING&quot;
    }
}
</code></pre></td></tr></tbody></table>

<a id="获取任务执行结果"></a>

<a id="f9109f6ea3di2"></a>

### 获取任务执行结果

<a id="url-4"></a>

<a id="03eb4a771btn0"></a>

#### URL

<a id="sec-tabs-10"></a>

<a id="华北2-北京-4"></a>

<a id="华北2-北京-4-h4"></a>

#### 华北2（北京）

HTTP请求地址：`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`

SDK调用配置的base\_url：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="新加坡-4"></a>

<a id="新加坡-4-h4"></a>

#### 新加坡

HTTP请求地址：`GET https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/tasks/{task_id}`

SDK调用配置的base\_url：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

> **重要**
>
> 阿里云百炼为华北2（北京）、新加坡地域推出了业务空间专属域名，能够为推理请求提供卓越的性能和更高的稳定性，建议迁移至新域名：
>
> -   华北2（北京）地域：从 `dashscope.aliyuncs.com` 迁移至 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
> -   新加坡地域：从 `dashscope-intl.aliyuncs.com` 迁移至 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`

<table><tbody><tr><td><a id="6cd669c353c2i"></a><h4>请求参数</h4><p><strong>task_id</strong><code>string</code><strong>（必选）</strong></p><p>任务ID。将<a href="qwen-asr-api-reference-6234af32190b8ba9.md#88657039c4x0g">提交任务</a>返回结果中的task_id作为参数传入，查询语音识别结果。</p></td><td><a id="sec-tabs-11"></a><section><a id="curl-4"></a><section><a id="curl-4-h4"></a><h4>cURL</h4><a id="code-block-15"></a><pre class="language-bash"><code># ======= 重要提示 =======
# 以下为华北2（北京）地域的配置，调用时请将&quot;{WorkspaceId}&quot;替换为真实的业务空间ID，各地域的配置不同。
# 新加坡地域和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# === 执行时请删除该注释 ===

curl --location --request GET 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header &quot;Content-Type: application/json&quot;
</code></pre></section><a id="java-2"></a><section><a id="java-2-h4"></a><h4>Java</h4><p>SDK示例请参见<a href="qwen-asr-api-reference-6234af32190b8ba9.md#qwen-asr-async-examples">调用示例</a>。</p><a id="code-block-16"></a><pre class="language-java"><code>import okhttp3.*;

import java.io.IOException;

public class Main {
    public static void main(String[] args) {
        // 替换为实际的task_id
        String taskId = &quot;xxx&quot;;
        // 新加坡地域和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        // 若没有配置环境变量，请用百炼API Key将下行替换为：String apiKey = &quot;sk-xxx&quot;
        String apiKey = System.getenv(&quot;DASHSCOPE_API_KEY&quot;);

        // 以下为华北2（北京）地域的配置，调用时请将&quot;{WorkspaceId}&quot;替换为真实的业务空间ID，各地域的配置不同。
        String apiUrl = &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/&quot; + taskId;

        OkHttpClient client = new OkHttpClient();

        Request request = new Request.Builder()
                .url(apiUrl)
                .addHeader(&quot;Authorization&quot;, &quot;Bearer &quot; + apiKey)
                .addHeader(&quot;Content-Type&quot;, &quot;application/json&quot;)
                .get()
                .build();

        try (Response response = client.newCall(request).execute()) {
            if (response.body() != null) {
                System.out.println(response.body().string());
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
</code></pre></section><a id="python-2"></a><section><a id="python-2-h4"></a><h4>Python</h4><p>SDK示例请参见<a href="qwen-asr-api-reference-6234af32190b8ba9.md#qwen-asr-async-examples">调用示例</a>。</p><a id="code-block-17"></a><pre class="language-python"><code>import os
import requests

# 新加坡地域和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 若没有配置环境变量，请用百炼API Key将下行替换为：DASHSCOPE_API_KEY = &quot;sk-xxx&quot;
DASHSCOPE_API_KEY = os.getenv(&quot;DASHSCOPE_API_KEY&quot;)

# 替换为实际的task_id
task_id = &quot;xxx&quot;
# 以下为华北2（北京）地域的配置，调用时请将&quot;{WorkspaceId}&quot;替换为真实的业务空间ID，各地域的配置不同。
url = f&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}&quot;

headers = {
    &quot;Authorization&quot;: f&quot;Bearer {DASHSCOPE_API_KEY}&quot;,
    &quot;Content-Type&quot;: &quot;application/json&quot;
}

response = requests.get(url, headers=headers)
print(response.json())
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="b207932046i9z"></a><h4>响应参数</h4><p><strong>request_id</strong><code>string</code></p><p>本次调用的唯一标识符。</p><p><strong>output</strong><code>object</code></p><p>调用结果信息。</p><a id="accordion-属性-27"></a><section><p>属性</p><div><p><strong>task_id</strong><code>string</code></p><p>任务ID。该ID在查询语音识别任务接口中作为请求参数传入。</p><p><strong>task_status</strong><code>string</code></p><p>任务状态：</p><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>UNKNOWN：任务不存在或状态未知</li></ul><p><strong>result</strong><code>object</code></p><p>语音识别结果。</p><a id="accordion-属性-28"></a><section><p>属性</p><div><p><strong>transcription_url</strong><code>string</code></p><p>识别结果文件的下载 URL，链接有效期为 24 小时。过期后无法查询任务，也无法通过先前的 URL 下载结果。<br>识别结果以 JSON 文件保存，可通过该链接下载文件，或直接使用 HTTP 请求读取文件内容。<br></p><p>详情参见<a href="qwen-asr-api-reference-6234af32190b8ba9.md#2c27ad3e80p4y">异步调用识别结果说明</a>。</p></div></section><p><strong>submit_time</strong><code>string</code></p><p>任务提交时间。</p><p><strong>schedule_time</strong><code>string</code></p><p>任务调度时间，即开始执行时间。</p><p><strong>end_time</strong><code>string</code></p><p>任务结束时间。</p><p><strong>task_metrics</strong><code>object</code></p><p>任务指标，包含子任务状态的统计信息。</p><a id="accordion-属性-29"></a><section><p>属性</p><div><p><strong>TOTAL</strong><code>integer</code></p><p>子任务总数。</p><p><strong>SUCCEEDED</strong><code>integer</code></p><p>子任务成功数。</p><p><strong>FAILED</strong><code>integer</code></p><p>子任务失败数。</p></div></section><p><strong>code</strong><code>string</code></p><p>错误码，仅在任务失败时返回。</p><p><strong>message</strong><code>string</code></p><p>错误信息，仅任务失败时返回。</p><p><strong>usage</strong><code>object</code></p><p>本次请求的Token消耗信息。</p><a id="accordion-属性-30"></a><section><p>属性</p><div><p><strong>seconds</strong> <code>integer</code></p><p>千问3-ASR-Flash音频时长（秒）。</p></div></section></div></section></td><td><a id="fig-code-group-9"></a><div><a id="fig-code-group-9-running-tab"></a>RUNNING<div><a id="code-code-group-9-running"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;6769df07-2768-4fb0-ad59-************&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;9be1700a-0f8e-4778-be74-************&quot;,
        &quot;task_status&quot;: &quot;RUNNING&quot;,
        &quot;submit_time&quot;: &quot;2025-10-27 14:19:31.150&quot;,
        &quot;scheduled_time&quot;: &quot;2025-10-27 14:19:31.233&quot;,
        &quot;task_metrics&quot;: {
            &quot;TOTAL&quot;: 1,
            &quot;SUCCEEDED&quot;: 0,
            &quot;FAILED&quot;: 0
        }
    }
}
</code></pre></div><a id="fig-code-group-9-succeeded-tab"></a>SUCCEEDED<div><a id="code-code-group-9-succeeded"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;1dca6c0a-0ed1-4662-aa39-************&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;8fab76d0-0eed-4d20-929f-************&quot;,
        &quot;task_status&quot;: &quot;SUCCEEDED&quot;,
        &quot;submit_time&quot;: &quot;2025-10-27 13:57:45.948&quot;,
        &quot;scheduled_time&quot;: &quot;2025-10-27 13:57:46.018&quot;,
        &quot;end_time&quot;: &quot;2025-10-27 13:57:47.079&quot;,
        &quot;result&quot;: {
            &quot;transcription_url&quot;: &quot;http://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/pre/pre-funasr-mlt-v1/20251027/13%3A57/7a3a8236-ffd1-4099-a280-0299686ac7da.json?Expires=1761631066&amp;OSSAccessKeyId=YOUR_ACCESS_KEY_ID&amp;Signature=YOUR_SIGNATURE&amp;response-content-disposition=attachment%3Bfilename%3D7a3a8236-ffd1-4099-a280-0299686ac7da.json&quot;
        }
    },
    &quot;usage&quot;: {
        &quot;seconds&quot;: 3
    }
}
</code></pre></div><a id="fig-code-group-9-failed-tab"></a>FAILED<div><a id="code-code-group-9-failed"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;3d141841-858a-466a-9ff9-************&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;c58c7951-7789-4557-9ea3-************&quot;,
        &quot;task_status&quot;: &quot;FAILED&quot;,
        &quot;submit_time&quot;: &quot;2025-10-27 15:06:06.915&quot;,
        &quot;scheduled_time&quot;: &quot;2025-10-27 15:06:06.967&quot;,
        &quot;end_time&quot;: &quot;2025-10-27 15:06:07.584&quot;,
        &quot;code&quot;: &quot;FILE_403_FORBIDDEN&quot;,
        &quot;message&quot;: &quot;FILE_403_FORBIDDEN&quot;
    }
}
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="2c27ad3e80p4y"></a><h3>异步调用识别结果说明</h3><p><strong>file_url</strong> <code>string</code></p><p>被识别的音频文件URL。</p><p><strong>audio_info</strong><code>object</code></p><p>被识别音频文件相关信息。</p><a id="accordion-属性-31"></a><section><p>属性</p><div><p><strong>format</strong> <code>string</code></p><p>音频格式。</p><p><strong>sample_rate</strong> <code>integer</code></p><p>音频采样率。</p></div></section><p><strong>transcripts</strong><code>array</code></p><p>完整的识别结果列表，每个元素对应一条音轨的识别内容。</p><a id="accordion-属性-32"></a><section><p>属性</p><div><p><strong>channel_id</strong><code>integer</code></p><p>音轨索引，以0为起始。</p><p><strong>text</strong><code>string</code></p><p>识别结果文本。</p><p><strong>sentences</strong><code>object</code></p><p>句子级别的识别结果列表。</p><a id="accordion-属性-33"></a><section><p>属性</p><div><p><strong>begin_time</strong><code>integer</code></p><p>句子开始时间戳（毫秒）。</p><p><strong>end_time</strong><code>integer</code></p><p>句子结束时间戳（毫秒）。</p><p><strong>text</strong><code>string</code></p><p>识别结果文本。</p><p><strong>sentence_id</strong><code>integer</code></p><p>句子索引，以0为起始。</p><p><strong>language</strong><code>string</code></p><p>被识别音频的语种。当请求参数<code>language</code>已指定语种时，该值与所指定的参数一致。</p><a id="accordion-取值范围-6"></a><section><p>取值范围</p><div><ul><li>zh：中文（普通话、四川话、闽南语、吴语）</li><li>yue：粤语</li><li>en：英文</li><li>ja：日语</li><li>de：德语</li><li>ko：韩语</li><li>ru：俄语</li><li>fr：法语</li><li>pt：葡萄牙语</li><li>ar：阿拉伯语</li><li>it：意大利语</li><li>es：西班牙语</li><li>hi：印地语</li><li>id：印尼语</li><li>th：泰语</li><li>tr：土耳其语</li><li>uk：乌克兰语</li><li>vi：越南语</li><li>cs：捷克语</li><li>da：丹麦语</li><li>fil：菲律宾语</li><li>fi：芬兰语</li><li>is：冰岛语</li><li>ms：马来语</li><li>no：挪威语</li><li>pl：波兰语</li><li>sv：瑞典语</li></ul></div></section><p><strong>emotion</strong><code>string</code></p><p>被识别音频的情感。情感识别固定开启，无需额外配置。支持的情感如下：</p><ul><li><code>surprised</code>：惊讶</li><li><code>neutral</code>：平静</li><li><code>happy</code>：愉快</li><li><code>sad</code>：悲伤</li><li><code>disgusted</code>：厌恶</li><li><code>angry</code>：愤怒</li><li><code>fearful</code>：恐惧</li></ul><p><strong>words</strong><code>object</code></p><p>词级别的识别结果列表。当请求参数<code>enable_words</code>设为<code>true</code>时展示该结果。</p><a id="accordion-属性-34"></a><section><p>属性</p><div><p><strong>begin_time</strong><code>integer</code></p><p>开始时间戳（毫秒）。</p><p><strong>end_time</strong><code>integer</code></p><p>结束时间戳（毫秒）。</p><p><strong>text</strong><code>string</code></p><p>识别结果文本。</p><p><strong>punctuation</strong><code>string</code></p><p>标点符号。</p></div></section></div></section></div></section></td><td><a id="code-block-18"></a><pre class="language-json"><code>{
    &quot;file_url&quot;: &quot;https://***.mp3&quot;,
    &quot;audio_info&quot;: {
        &quot;format&quot;: &quot;mp3&quot;,
        &quot;sample_rate&quot;: 22050
    },
    &quot;transcripts&quot;: [
        {
            &quot;channel_id&quot;: 0,
            &quot;text&quot;: &quot;欢迎使用阿里云。&quot;,
            &quot;sentences&quot;: [
                {
                    &quot;sentence_id&quot;: 0,
                    &quot;begin_time&quot;: 0,
                    &quot;end_time&quot;: 1440,
                    &quot;language&quot;: &quot;zh&quot;,
                    &quot;emotion&quot;: &quot;neutral&quot;,
                    &quot;text&quot;: &quot;欢迎使用阿里云。&quot;,
                    &quot;words&quot;: [
                        {
                            &quot;begin_time&quot;: 0,
                            &quot;end_time&quot;: 160,
                            &quot;text&quot;: &quot;欢&quot;,
                            &quot;punctuation&quot;: &quot;&quot;
                        },
                        {
                            &quot;begin_time&quot;: 160,
                            &quot;end_time&quot;: 320,
                            &quot;text&quot;: &quot;迎&quot;,
                            &quot;punctuation&quot;: &quot;&quot;
                        },
                        {
                            &quot;begin_time&quot;: 320,
                            &quot;end_time&quot;: 640,
                            &quot;text&quot;: &quot;使&quot;,
                            &quot;punctuation&quot;: &quot;&quot;
                        },
                        {
                            &quot;begin_time&quot;: 640,
                            &quot;end_time&quot;: 720,
                            &quot;text&quot;: &quot;用&quot;,
                            &quot;punctuation&quot;: &quot;&quot;
                        },
                        {
                            &quot;begin_time&quot;: 880,
                            &quot;end_time&quot;: 960,
                            &quot;text&quot;: &quot;阿&quot;,
                            &quot;punctuation&quot;: &quot;&quot;
                        },
                        {
                            &quot;begin_time&quot;: 1040,
                            &quot;end_time&quot;: 1120,
                            &quot;text&quot;: &quot;里&quot;,
                            &quot;punctuation&quot;: &quot;&quot;
                        },
                        {
                            &quot;begin_time&quot;: 1120,
                            &quot;end_time&quot;: 1440,
                            &quot;text&quot;: &quot;云&quot;,
                            &quot;punctuation&quot;: &quot;。&quot;
                        }
                    ]
                }
            ]
        }
    ]
}
</code></pre></td></tr></tbody></table>
