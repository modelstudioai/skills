# 优速模式

高速模式为对输出速度敏感的场景提供更高的 TPS。

## 使用方式

优速模式具备以下关键特性：

-   **高速输出**：TPS 提升至标准 API 的 1.5~2 倍；适用于 AI 编程助手、Agent 多步推理、实时对话等对输出速度敏感的场景。
-   **按 token 计费**：计费逻辑与标准 API 一致，按输入与输出 token 计费。
-   **特殊限流**：调用量达到限流值时，若平台仍有剩余资源，则不会触发限流，因此**实际可用 TPS** 不低于限流值。

调用时将 model 参数指定为[支持的模型](https://help.aliyun.com/zh/model-studio/fast-mode#fast-models-h2)的 model ID 即可开启，无需额外参数。接入域名格式为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`，其中 `{workspace_id}`可在[业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management)页面切换到对应地域后查看。

基础调用示例：

> glm 5.2 的 prime 模式的模型名称仍然为 glm-5.2-fast-preview。

```
curl -X POST https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "glm-5.2-fast-preview",
    "messages": [{"role": "user", "content": "你是谁"}],
    "stream": false
}'
```

## 支持的模型

> 模型支持的能力、使用限制与原版模型相同

#### 华北2（北京）

**文本生成模型**

**模型计费（每百万Token）**

**输入单价**

**输出单价**

**缓存命中**

qwen3.8-max-prime

24元

72元

3元

glm-5.2-fast-preview

16元

56元

4元

**视频生成模型**

**模型计费（元/秒）**

**480P**

**720P**

**1080P**

wan3.0-video-prime

0.45元/秒

0.9元/秒

1.8元/秒

#### 新加坡

**文本生成模型**

**模型计费（每百万Token）**

**输入单价**

**输出单价**

**缓存命中**

glm-5.2-fast-preview

20.98元

65.95元

4.20元

**视频生成模型**

**模型计费（元/秒）**

**480P**

**720P**

**1080P**

wan3.0-video-prime

0.496元/秒

1.02元/秒

2.04元/秒

## 使用示例

> 模型支持的能力、使用限制与原版模型相同

流式调用示例：

```
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

```
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

## 计费说明

关于快速模式的计费规则与价格表，请参见 [模型调用计费](raw/model-user-guide/test-1/model-pricing.md)。

## 错误码

关于快速模式调用过程中可能出现的错误码及对应的解决方法，请参见 [错误码](raw/model-api-reference/preparations/error-code.md)。
