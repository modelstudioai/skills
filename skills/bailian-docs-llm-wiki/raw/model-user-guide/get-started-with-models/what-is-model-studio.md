# 模型服务概览

提供文本、视觉、语音、全模态及向量模型 API，支持在线调用、推理调度与模型训练。

## 快速开始

通过 OpenAI 兼容 API 完成首次调用。

[首次调用](raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)[获取 API Key](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key)

curl

```
curl https://trial.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3.8-max",
    "messages": [{"role": "user", "content": "你是谁？"}]
  }'
```

Python

```
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://trial.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
response = client.chat.completions.create(
    model="qwen3.8-max",
    messages=[{"role": "user", "content": "你是谁？"}],
)
print(response.choices[0].message.content)
```

JavaScript

```
import OpenAI from "openai";

const client = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: "https://trial.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
});
const response = await client.chat.completions.create({
    model: "qwen3.8-max",
    messages: [{ role: "user", content: "你是谁？" }],
});
console.log(response.choices[0].message.content);
```

## 模型

[查看所有模型](https://bailian.console.aliyun.com/cn-beijing/model/market)

[

**Qwen3.8-Max**

旗舰与最强效果

](https://bailian.console.aliyun.com/cn-beijing/model/market/detail/qwen3.8-max?serviceSite=asia-pacific-china&ref=list)

[

**Qwen3.7-Plus**

均衡之选

](https://bailian.console.aliyun.com/cn-beijing/model/market/detail/qwen3.7-plus?serviceSite=asia-pacific-china&ref=list)

[

**Qwen3.8-Flash**

极致速度与高性价比

](https://bailian.console.aliyun.com/cn-beijing/model/market/detail/qwen3.8-flash?serviceSite=asia-pacific-china&ref=list)

## 开始构建

[

**文本生成与视觉理解**

生成文本，理解图像与视频内容。

](raw/model-user-guide/model-experience/text-generation-model.md)[

**图像生成**

从文字描述生成图像。

](raw/model-user-guide/model-experience/image-and-video-generation/image-model/text-to-image.md)[

**视频生成**

从文字或图像生成视频。

](raw/_short/wan3-video-generation-guide-0e56f533d7040652.md)[

**语音与音频**

识别、合成语音，接入实时对话。

](raw/model-user-guide/model-experience/speech-and-audio.md)[

**全模态**

结合文本、视觉与音频进行交互。

](raw/model-user-guide/model-experience/omni-modal.md)[

**向量与检索**

使用向量与重排序提升检索效果。

](raw/model-user-guide/model-experience/embedding-rerank-model.md)
