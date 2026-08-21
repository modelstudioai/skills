# 快速模式

快速模式（Fast mode）为对输出速度敏感的场景提供更高的 TPS。当前为 preview 阶段。

## **使用方式**

快速模式具备以下关键特性：

-   **高速输出**：TPS 提升至标准 API 的 1.5~2 倍，达 80~100 TPS；适用于 AI 编程助手、Agent 多步推理、实时对话等对输出速度敏感的场景。
    
-   **按 token 计费**：计费逻辑与标准 API 一致，按输入与输出 token 计费，具体价格见[模型调用计费](https://help.aliyun.com/zh/model-studio/model-pricing)。
    
-   **特殊限流**：超出 TPM 额度不会立即实行限流，请求会进入排队队列。
    
-   **preview 阶段**：当前为预览阶段，能力与规格可能随版本调整。
    

调用时将 model 参数指定为[支持的模型](#fast-models-h2)的model ID 即可开启，无需额外参数。接入域名格式为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`，其中 `{workspace_id}`可在 [业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management) 页面切换到对应地域后查看。

基础调用示例：

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

## **支持的模型**

## 华北2（北京）

**模型名称**

**模型计费（每百万Token）**

**输入单价**

**输出单价**

**缓存命中**

glm-5.2-fast-preview

16元

56元

4元

## 新加坡

**模型名称**

**模型计费（每百万Token）**

**输入单价**

**输出单价**

**缓存命中**

glm-5.2-fast-preview

20.98元

65.95元

4.20元

## **使用示例**

glm-5.2 默认返回 `reasoning_content` 思考字段；流式输出时思考内容与回答内容分别通过 `delta.reasoning_content` 与 `delta.content` 推送。流式调用示例：

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

## **计费说明**

关于快速模式的计费规则与价格表，请参见 [模型调用计费](https://help.aliyun.com/zh/model-studio/model-pricing)。

## **错误码**

关于快速模式调用过程中可能出现的错误码及对应的解决方法，请参见 [错误码](https://help.aliyun.com/zh/model-studio/error-code)。
