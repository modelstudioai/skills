# MiMo-小米

本文档介绍如何在阿里云百炼平台调用小米直供的 MiMo 系列模型推理服务。

> **重要**
>
> 小米直供模型 xiaomi/mimo-v2.5-pro 将于2026年10月21日下线，推荐使用 [xiaomi/mimo-v2.6-pro-ultraspeed](../../../_short/mimo-v2-6-pro-ultraspeed-9c24e7f1d6d136d1.md) 替代。

> **重要**
>
> 本文档描述的功能仅在华北2（北京）地域可用，如需使用模型，需从华北2（北京）地域[获取与配置 API Key](../../../model-api-reference/preparations/get-api-key.md)。

<a id="快速开始"></a>

<a id="61623d75547kl"></a>

## 快速开始

mimo-v2.5-pro 是小米直供的混合推理模型，默认开启思考模式（`enable_thinking`默认为`true`），如需直接输出结果可显式传入`enable_thinking: false`。运行以下代码快速调用思考模式的 mimo-v2.5-pro 模型。

需要已[获取与配置 API Key](../../../model-api-reference/preparations/get-api-key.md)并完成[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。如果通过SDK调用，需要[安装SDK](../../../model-api-reference/preparations/install-sdk.md)。

<a id="sec-tabs"></a>

<a id="openai兼容"></a>

<a id="openai兼容-h4"></a>

#### OpenAI兼容

> **说明**
>
> `enable_thinking`非 OpenAI 标准参数，OpenAI Python SDK 通过 `extra_body`传入，Node.js SDK 作为顶层参数传入。

<a id="sec-tabs-2"></a>

<a id="python"></a>

<a id="python-h4"></a>

#### Python

<a id="ddb5892c91y4c"></a>

### 示例代码

<a id="code-block"></a>

```python
from openai import OpenAI
import os

# 初始化OpenAI客户端
client = OpenAI(
    # 如果没有配置环境变量，请用阿里云百炼API Key替换：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

messages = [{"role": "user", "content": "1+1 等于多少？"}]
completion = client.chat.completions.create(
    model="xiaomi/mimo-v2.6-pro-ultraspeed",
    messages=messages,
    # mimo-v2.5-pro 默认开启思考模式，如需关闭可改为 {"enable_thinking": False}
    stream=True,
    stream_options={
        "include_usage": True
    },
)

reasoning_content = ""  # 完整思考过程
answer_content = ""  # 完整回复
is_answering = False  # 是否进入回复阶段
print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")

for chunk in completion:
    if not chunk.choices:
        print("\n" + "=" * 20 + "Token 消耗" + "=" * 20 + "\n")
        print(chunk.usage)
        continue

    delta = chunk.choices[0].delta

    # 只收集思考内容
    if hasattr(delta, "reasoning_content") and delta.reasoning_content is not None:
        if not is_answering:
            print(delta.reasoning_content, end="", flush=True)
        reasoning_content += delta.reasoning_content

    # 收到content，开始进行回复
    if hasattr(delta, "content") and delta.content:
        if not is_answering:
            print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
            is_answering = True
        print(delta.content, end="", flush=True)
        answer_content += delta.content
```

<a id="f2828e7338ck1"></a>

### 返回结果

<a id="code-block-2"></a>

```text
====================思考过程====================

用户问了一个简单的算术问题：1+1等于多少。
这是最基础的加法运算，答案是 2。我直接给出答案并简要说明即可。
====================完整回复====================

1+1 等于 2。这是最基本的加法运算。
====================Token 消耗====================

CompletionUsage(completion_tokens=42, prompt_tokens=9, total_tokens=51, prompt_tokens_details={'cached_tokens': 0})
```

<a id="node-js"></a>

<a id="node-js-h4"></a>

#### Node.js

<a id="25ed2818c5km2"></a>

### 示例代码

<a id="code-block-3"></a>

```javascript
import OpenAI from "openai";
import process from 'process';

// 初始化OpenAI客户端
const openai = new OpenAI({
    // 如果没有配置环境变量，请用阿里云百炼API Key替换：apiKey: "sk-xxx"
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    baseURL: 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1'
});

let reasoningContent = ''; // 完整思考过程
let answerContent = ''; // 完整回复
let isAnswering = false; // 是否进入回复阶段

async function main() {
    try {
        const messages = [{ role: 'user', content: '1+1 等于多少？' }];

        const stream = await openai.chat.completions.create({
            model: 'xiaomi/mimo-v2.6-pro-ultraspeed',
            messages,
            // mimo-v2.5-pro 默认开启思考模式，如需关闭可改为 enable_thinking: false
            stream: true,
            stream_options: {
                include_usage: true
            },
        });

        console.log('\n' + '='.repeat(20) + '思考过程' + '='.repeat(20) + '\n');

        for await (const chunk of stream) {
            if (!chunk.choices?.length) {
                console.log('\n' + '='.repeat(20) + 'Token 消耗' + '='.repeat(20) + '\n');
                console.log(chunk.usage);
                continue;
            }

            const delta = chunk.choices[0].delta;

            // 只收集思考内容
            if (delta.reasoning_content !== undefined && delta.reasoning_content !== null) {
                if (!isAnswering) {
                    process.stdout.write(delta.reasoning_content);
                }
                reasoningContent += delta.reasoning_content;
            }

            // 收到content，开始进行回复
            if (delta.content !== undefined && delta.content) {
                if (!isAnswering) {
                    console.log('\n' + '='.repeat(20) + '完整回复' + '='.repeat(20) + '\n');
                    isAnswering = true;
                }
                process.stdout.write(delta.content);
                answerContent += delta.content;
            }
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

main();
```

<a id="1f1fdf8de1624"></a>

### 返回结果

<a id="code-block-4"></a>

```text
====================思考过程====================

用户问了一个简单的算术问题：1+1等于多少。
这是最基础的加法运算，答案是 2。我直接给出答案并简要说明即可。
====================完整回复====================

1+1 等于 2。这是最基本的加法运算。
====================Token 消耗====================

{ prompt_tokens: 9, completion_tokens: 42, total_tokens: 51, prompt_tokens_details: { cached_tokens: 0 } }
```

<a id="http"></a>

<a id="http-h4"></a>

#### HTTP

<a id="bcaf8f53f8n2x"></a>

### 示例代码

<a id="sec-tabs-3"></a>

<a id="curl"></a>

<a id="curl-h4"></a>

#### curl

<a id="code-block-5"></a>

```bash
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "xiaomi/mimo-v2.6-pro-ultraspeed",
    "messages": [
        {
            "role": "user",
            "content": "1+1 等于多少？"
        }
    ],
    "stream": true,
    "stream_options": {
        "include_usage": true
    }
}'
```

<a id="多模态输入"></a>

<a id="h-mimo-multimodal"></a>

## 多模态输入

xiaomi/mimo-v2.6-pro-ultraspeed 支持图片、音频和视频输入。在 user 消息的 `content` 数组中同时传入文本和多模态内容：图片使用 `image_url`，音频使用 `input_audio` 并通过 `format` 指定音频格式，视频使用 `video_url`。

<a id="sec-tabs-4"></a>

<a id="图片"></a>

<a id="图片-h4"></a>

#### 图片

<a id="code-block-6"></a>

```bash
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "xiaomi/mimo-v2.6-pro-ultraspeed",
    "messages": [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "图中描绘的是什么景象？"},
                {"type": "image_url", "image_url": {"url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"}}
            ]
        }
    ]
}'
```

<a id="音频"></a>

<a id="音频-h4"></a>

#### 音频

<a id="code-block-7"></a>

```bash
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "xiaomi/mimo-v2.6-pro-ultraspeed",
    "messages": [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "音频中说的内容是什么？"},
                {"type": "input_audio", "input_audio": {"data": "http://paas-aliyun-beijing.oss-cn-beijing.aliyuncs.com/qwen-translation/Cindy.wav", "format": "wav"}}
            ]
        }
    ]
}'
```

<a id="视频"></a>

<a id="视频-h4"></a>

#### 视频

<a id="code-block-8"></a>

```bash
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "xiaomi/mimo-v2.6-pro-ultraspeed",
    "messages": [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "视频里面有什么？"},
                {"type": "video_url", "video_url": {"url": "http://paas-aliyun-beijing.oss-cn-beijing.aliyuncs.com/qwen-translation/normal_video.mp4"}}
            ]
        }
    ]
}'
```

<a id="其它功能"></a>

<a id="d062ed0e4d5fe"></a>

## 其它功能

| 功能 | 支持情况 | 备注 |
| --- | --- | --- |
| [多轮对话](../../model-experience/text-generation-model/multi-round-conversation.md) | 支持 | 思考模式下需在每轮 assistant 消息中保留 `reasoning_content` 字段，否则会报错 |
| [Function Calling](../../model-experience/text-generation-model/tool-calls/qwen-function-calling.md#dd5a3dca390k9) | 支持 | `tool_choice` 仅支持 `auto`；工具函数名只能包含 a-z、A-Z、0-9、下划线、连字符，最大长度 64 |
| [上下文缓存](../../model-experience/text-generation-model/context-cache.md) | 支持 | 隐式缓存，自动开启 |
| [结构化输出](../../model-experience/text-generation-model/qwen-structured-output.md) | 支持 | `response_format`不支持 json\_schema |
| [联网搜索](../../model-experience/text-generation-model/tool-calls/web-search.md) | 不支持 | — |
| [前缀续写](../../model-experience/text-generation-model/partial-mode.md) | 不支持 | — |
| [多模态输入](#h-mimo-multimodal) | 因模型而异 | xiaomi/mimo-v2.6-pro-ultraspeed 支持图片、音频和视频输入；xiaomi/mimo-v2.5-pro 不支持 |

mimo-v2.5-pro 不支持以下参数：`top_k`、`reasoning_effort`、`thinking_budget`、`modalities`、`repetition_penalty`、`vl_high_resolution_images`、`preserve_thinking`、`tool_stream`、`enable_code_interpreter`、`parallel_tool_calls`、`seed`、`logprobs`、`top_logprobs`、`n`、`audio`、`enable_search`、`search_options`、`X-DashScope-DataInspection`、`skill`。

支持的参数中，部分参数取值范围与功能与百炼不一致：

| 参数 | 百炼 | MiMo |
| --- | --- | --- |
| `temperature` | 范围为 \[0, 2) | mimo-v2.5-pro：范围 \[0, 1.5\]，默认 1.0<br><br>mimo-v2.6-pro-ultraspeed：不支持自定义，传入其他值时仍按 1.0 生效 |
| `top_p` | 范围为 (0, 1.0\] | mimo-v2.5-pro：范围 \[0.01, 1.0\]，默认 0.95<br><br>mimo-v2.6-pro-ultraspeed：不支持自定义，传入其他值时仍按 0.95 生效 |
| `presence_penalty` | — | 范围为 \[-2, 2\]，默认值为 0 |
| `stop` | — | 最多 4 个序列 |
| `max_tokens` | 不限制模型思维链长度，仅限制输出长度 | 限制模型的输出和思维链长度 |

<a id="模型列表与计费"></a>

<a id="a1208aad3d0k8"></a>

## 模型列表与计费

MiMo 系列模型是小米直供的混合推理模型，提供思考与非思考两种模式。

模型上下文长度与价格信息请参见[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)。

按照模型的输入与输出 Token 计费。

> 思考模式下，思维链按照输出 Token 计费。

<a id="错误码"></a>

<a id="2048aa1f92x46"></a>

## 错误码

MiMo 系列模型由小米直供，其错误码与百炼平台标准错误码存在差异。调用 MiMo 模型时，请以下表为准。

<table><thead><tr><th><p><strong>错误码</strong></p></th><th><p><strong>错误原因</strong></p></th><th><p><strong>解决方法</strong></p></th></tr></thead><tbody><tr><td><p>400 - 格式错误</p></td><td><p>请求体格式错误</p></td><td><ul><li><p>检查 JSON 格式是否正确</p></li><li><p>检查是否包含所有必需参数</p></li><li><p>检查参数值是否在有效范围内</p></li><li><p>检查消息格式是否符合接口要求</p></li><li><p>检查字段是否输入正确</p></li><li><p>多轮对话思考模式下，需完整回传 <code>reasoning_content</code> 字段给接口</p></li></ul></td></tr><tr><td><p>401 - 认证失败</p></td><td><p>缺少或无效的 API Key，或 Authorization 请求头格式错误</p></td><td><p>检查 API Key 及请求头格式是否正确</p></td></tr><tr><td><p>402 - 余额不足</p></td><td><p>账户余额不足</p></td><td><p>检查账户余额，及时进行充值</p></td></tr><tr><td><p>403 - 拒绝访问</p></td><td><p>服务暂不支持当前地区，或 API Key 被风控</p></td><td><p>新建 API Key，并注意输入内容安全</p></td></tr><tr><td><p>404 - 资源未找到</p></td><td><p>接口或模型不支持图像输入能力</p></td><td><p>确认使用的模型或接口是否支持多模态图像输入</p></td></tr><tr><td><p>421 - 内容拦截</p></td><td><p>内容审核拦截</p></td><td><p>避免输入不安全或敏感内容</p></td></tr><tr><td><p>429 - 请求超限</p></td><td><p>请求过于频繁</p></td><td><p>实现指数退避和重试逻辑，或降低请求频率</p></td></tr><tr><td><p>500 - 服务器失败</p></td><td><p>服务器内部故障</p></td><td><p>请稍后重试，或联系我们解决</p></td></tr><tr><td><p>503 - 服务器故障</p></td><td><p>服务器负载过高</p></td><td><p>请稍后重试</p></td></tr></tbody></table>
