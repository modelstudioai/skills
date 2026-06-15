# OpenAI 兼容接口

OpenAI 兼容接口是阿里云百炼平台提供的一组遵循 OpenAI API 规范的服务端点，开发者只需将 `api_key`、`base_url` 和模型名称替换为百炼平台的对应值，即可将现有基于 OpenAI SDK 的应用无缝迁移至百炼服务。

## 接口类型

百炼提供多种 OpenAI 兼容接口，覆盖不同使用场景：

| 接口 | 用途 | 说明 |
|------|------|------|
| Chat Completions | 文本对话、function call | 与 OpenAI 客户端库直接兼容，迁移成本最低 |
| Responses API | 智能体原生功能 | 内置联网搜索、代码解释器等工具，自动管理对话历史 |
| Completions | 代码补全、文本续写 | 支持前缀补全和中间填充（FIM） |
| Vision | 图像/视频理解 | 配合 Qwen-VL 等视觉模型使用 |
| Embedding | 文本向量化 | 配合 text-embedding 系列模型 |
| Files | 文件上传与管理 | 配合 Qwen-Long、Batch、Fine-tune 使用 |
| Batch | 批量推理 | 支持同步批量和异步文件批量两种模式 |

## 基础配置

所有 OpenAI 兼容接口共享三个核心配置参数：

- **base_url**：百炼服务端点，根据地域选择对应的 URL
- **api_key**：百炼平台的 API Key（环境变量 `DASHSCOPE_API_KEY`）
- **model**：百炼支持的模型名称（如 `qwen-plus`、`qwen-max`）

### 各地域服务端点

| 地域 | base_url |
|------|----------|
| 华北2（北京） | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1` |

> 不同地域的 API Key 不通用，不能跨地域混用。新加坡和德国地域需要在 URL 中嵌入 WorkspaceId。

## 调用示例

以 Python 为例，使用标准 OpenAI SDK 调用百炼模型：

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen-plus",
    messages=[{"role": "user", "content": "你好"}]
)
print(completion.choices[0].message.content)
```

Node.js 调用方式类似，使用 `openai` npm 包即可。

## 适用模型

OpenAI 兼容接口不仅支持千问（Qwen）全系列模型，还支持百炼平台上的第三方模型和专用模型：

- **通用文本模型**：qwen-max、qwen-plus、qwen-flash 等，以及 DeepSeek、Kimi、GLM、MiniMax 等第三方模型
- **翻译模型**：qwen-mt-turbo / qwen-mt-plus，通过 `extra_body.translation_options` 传递翻译参数
- **OCR 模型**：qwen-vl-ocr-latest，用于图像文字提取
- **GUI 交互模型**：gui-plus，用于界面交互自动化
- **音视频翻译**：qwen3-livetranslate-flash，离线音视频翻译
- **意图识别**：tongyi-intent-detect-v3，百毫秒级意图识别

## 与 [DashScope 接口](dashscope-api.md)的区别

百炼同时提供 DashScope 原生接口。两者的核心差异：

- **兼容性**：OpenAI 兼容接口可直接使用 OpenAI SDK，迁移成本最低；[DashScope 接口](dashscope-api.md)需要使用专用 SDK 或特定 HTTP 格式
- **功能覆盖**：[DashScope 接口](dashscope-api.md)提供最完整的功能集和参数支持；OpenAI 兼容接口在部分高级参数上可能有差异
- **选择建议**：已有 OpenAI 代码的项目优先选 OpenAI 兼容接口；需要平台全部能力时选 DashScope 接口

## 注意事项

- 部分模型的高级参数（如翻译选项、高分辨率图像处理）需通过 `extra_body` 传入，这是 OpenAI SDK 的扩展机制
- [流式输出](streaming-output.md)需设置 `stream: true`，可通过 `stream_options: {"include_usage": true}` 获取用量信息
- Responses API 会自动管理对话历史，通过 `previous_response_id` 关联上下文，与 Chat Completions 的手动消息管理方式不同

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [get started with models](../guides/get-started-with-models.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [more models](../api/more-models.md)
- [specialized model](../api/specialized-model.md)
- [speech translation api reference](../api/speech-translation-api-reference.md)
- [more about models](../api/more-about-models.md)


