# Prime 模式

Prime 模式为对输出速度敏感的场景提供更高的 TPS。

<a id="使用方式"></a>

<a id="prime-usage-h2"></a>

## 使用方式

Prime 模式具备以下关键特性：

-   **高速输出**：TPS 提升至标准 API 的 1.5~2 倍；适用于 AI 编程助手、Agent 多步推理、实时对话等对输出速度敏感的场景。
-   **按 token 计费**：计费逻辑与标准 API 一致，按输入与输出 token 计费。
-   **特殊限流**：调用量达到限流值时，若平台仍有剩余资源，则不会触发限流，因此**实际可用 TPS** 不低于限流值。

调用时将 model 参数指定为[支持的模型](prime-mode.md#prime-models-h2)的 model ID 即可开启，无需额外参数。接入域名格式为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`，其中 `{workspace_id}`可在[业务空间管理](https://bailian.console.aliyun.com/cn-beijing/settings/workspace)页面切换到对应地域后查看。

基础调用示例：

> glm 5.2 的 prime 模式的模型名称仍然为 glm-5.2-fast-preview。

<a id="code-block"></a>

```bash
curl -X POST https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "glm-5.2-fast-preview",
    "messages": [{"role": "user", "content": "你是谁"}],
    "stream": false
}'
```

<a id="支持的模型"></a>

<a id="prime-models-h2"></a>

## 支持的模型

> 模型支持的能力、使用限制与原版模型相同
> 
> wan3.0-video-prime 的输入视频和输出视频均按**秒数**计费，价格由输出视频的分辨率决定。计费时长 = 输入视频时长 + 输出视频时长。

<a id="sec-tabs"></a>

<a id="华北2-北京"></a>

<a id="华北2-北京-h4"></a>

#### 华北2（北京）

<table><thead><tr><th rowspan="2"><p><strong>文本生成模型</strong></p></th><th colspan="3"><p><strong>模型计费（每百万Token）</strong></p></th></tr><tr><th><p><strong>输入单价</strong></p></th><th><p><strong>输出单价</strong></p></th><th><p><strong>缓存命中</strong></p></th></tr></thead><tbody><tr><td><p>glm-5.3-prime</p></td><td><p>¥16</p></td><td><p>¥56</p></td><td><p>¥4</p></td></tr><tr><td><p>glm-5.2-fast-preview</p></td><td><p>¥16</p></td><td><p>¥56</p></td><td><p>¥4</p></td></tr><tr><td colspan="4"></td></tr><tr><td rowspan="2"><p><strong>视频生成模型</strong></p></td><td colspan="3"><p><strong>模型计费（元/秒）</strong></p></td></tr><tr><td><p><strong>480P</strong></p></td><td><p><strong>720P</strong></p></td><td><p><strong>1080P</strong></p></td></tr><tr><td><p>wan3.0-video-prime</p></td><td><p>0.45元/秒</p></td><td><p>0.9元/秒</p></td><td><p>1.8元/秒</p></td></tr></tbody></table>

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

<table><thead><tr><th rowspan="2"><p><strong>文本生成模型</strong></p></th><th colspan="3"><p><strong>模型计费（每百万Token）</strong></p></th></tr><tr><th><p><strong>输入单价</strong></p></th><th><p><strong>输出单价</strong></p></th><th><p><strong>缓存命中</strong></p></th></tr></thead><tbody><tr><td><p>glm-5.3-prime</p></td><td><p>¥20.42</p></td><td><p>¥64.17</p></td><td><p>¥4.08</p></td></tr><tr><td><p>glm-5.2-fast-preview</p></td><td><p>¥20.984</p></td><td><p>¥65.948</p></td><td><p>¥4.196</p></td></tr><tr><td colspan="4"></td></tr><tr><td rowspan="2"><p><strong>视频生成模型</strong></p></td><td colspan="3"><p><strong>模型计费（元/秒）</strong></p></td></tr><tr><td><p><strong>480P</strong></p></td><td><p><strong>720P</strong></p></td><td><p><strong>1080P</strong></p></td></tr><tr><td><p>wan3.0-video-prime</p></td><td><p>0.496元/秒</p></td><td><p>1.02元/秒</p></td><td><p>2.04元/秒</p></td></tr></tbody></table>

<a id="使用示例"></a>

<a id="prime-example-h2"></a>

## 使用示例

> 模型支持的能力、使用限制与原版模型相同

流式调用示例：

<a id="code-block-2"></a>

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ.get("API_KEY"),
    base_url=os.environ.get("BASE_URL"),
)

completion = client.chat.completions.create(
    model="glm-5.2-fast-preview",
    messages=[{"role": "user", "content": "你是谁"}],
    stream=True,
)

# glm-5.2 默认返回 reasoning_content 思考字段；
# 流式输出时思考内容与回答内容分别通过 delta.reasoning_content 与 delta.content 推送。
for chunk in completion:
    if not chunk.choices:
        continue
    delta = chunk.choices[0].delta
    if hasattr(delta, "reasoning_content") and delta.reasoning_content:
        print(delta.reasoning_content, end="", flush=True)
    if hasattr(delta, "content") and delta.content:
        print(delta.content, end="", flush=True)
```

返回示例：

<a id="code-block-3"></a>

```json
{
  "id": "chatcmpl-xxx",
  "object": "chat.completion",
  "model": "glm-5.2-fast-preview",
  "choices": [{
    "index": 0,
    "message": {
      "role": "assistant",
      "reasoning_content": "...",
      "content": "..."
    },
    "finish_reason": "stop"
  }],
  "usage": {
    "prompt_tokens": 14,
    "completion_tokens": 137,
    "total_tokens": 151,
    "prompt_tokens_details": { "cached_tokens": 0 },
    "completion_tokens_details": { "reasoning_tokens": 127 }
  }
}
```

<a id="计费说明"></a>

<a id="prime-billing-h2"></a>

## 计费说明

关于快速模式的计费规则与价格表，请参见 [模型调用计费](../test-1/model-pricing.md)。

<a id="错误码"></a>

<a id="prime-errorcode-h2"></a>

## 错误码

关于快速模式调用过程中可能出现的错误码及对应的解决方法，请参见 [错误码](../../model-api-reference/preparations/error-code.md)。
