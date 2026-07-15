# DashScope SDK

DashScope SDK 是阿里云百炼平台官方提供的软件开发工具包，封装了模型与应用调用的原生（DashScope）接口，让开发者用少量代码即可接入通义千问、万相、Qwen-MT、Qwen-OCR 等模型能力以及智能体/工作流应用。相比 HTTP 直连和 [OpenAI 兼容接口](openai-compatible-interface.md)，DashScope 原生接口暴露的参数最完整、功能集最丰富。

## 适用语言与安装

DashScope SDK 主要提供 Python 与 Java 两种官方实现，部分场景也可用 HTTP（如 Node.js 借助 `axios`）替代：

- **Python**：`python3 -m pip install -U dashscope`
- **Java**：通过 Maven / Gradle 引入 `com.alibaba:dashscope-sdk-java`，建议版本 `>= 2.12.0`
- **Node.js / 其他语言**：目前无官方 SDK，直接走 HTTP API（发起 POST 请求）

> 注意：不同能力对 SDK 语言与地域的支持存在差异。例如 `qwen-deep-research` **仅支持 Python DashScope SDK，且仅限华北2（北京）地域**，暂不支持 Java SDK 与 [OpenAI 兼容接口](openai-compatible-interface.md)。

## 在不同场景中的使用

### 1. 调用文本生成模型（Qwen 系列）

Qwen 系列可通过 OpenAI 兼容、Anthropic 兼容或 DashScope 原生三类接口调用。其中 DashScope 是百炼原生接口，**功能集最完整、参数支持最丰富**；当需要使用最全的采样参数、插件或业务字段而兼容接口未暴露时，应改用 DashScope 原生接口。

### 2. 调用专用模型（[more](../api/more.md) models）

法律、意图理解、翻译、OCR 等专用模型大多支持 OpenAI 兼容或 DashScope 两种方式调用：

- `farui-plus`（法律大模型）：通过 DashScope SDK（Python / Java）调用
- `tongyi-intent-detect-v3` / `qwen-mt-plus` / `qwen3.5-ocr`：OpenAI 兼容或 DashScope 均可
- `qwen-deep-research`（深度研究）：仅 Python DashScope SDK

### 3. 调用图像生成与编辑模型

千问-图像（Qwen-Image）、万相（Wan/Wanx）、Z-Image 等图像模型均可通过 HTTP 或 DashScope SDK 调用，覆盖文生图、图像编辑、图像翻译、风格迁移等能力。

### 4. 调用智能体应用与工作流应用

已创建并发布的智能体应用、工作流应用可通过 DashScope SDK 集成到业务系统，二者调用方式一致：

- Python：`from dashscope import Application`，调用 `Application.call(...)`
- Java：构造 `ApplicationParam` 后调用 `application.call(param)`
- HTTP 等价接口：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`

响应统一为 `{"output": {...}, "usage": {...}, "request_id": "..."}` 结构，业务侧主要消费 `output.text`。

## 关键参数与配置

### 鉴权（API Key）

- SDK 通过 [API Key 鉴权](api-key.md)，**推荐将密钥写入环境变量 `DASHSCOPE_API_KEY`**，SDK 会自动读取，避免在代码中硬编码。
- 调用特定地域（如华北2/北京）或子业务空间下的模型/应用时，需使用对应地域的 API Key，并按需提供 Workspace ID。

### 通用请求参数

- `model`（string，必选）：目标模型名称。
- `messages`（array）：对话消息列表，按顺序排列，需由调用方维护上下文。
- `app_id`（应用调用）：目标应用 ID，从控制台应用卡片复制。
- `prompt` / `input`：用户输入内容。
- `stream`（bool，可选）：是否[流式输出](streaming.md)；如 `qwen-deep-research` 的反问阶段需设为 `true`。
- `session_id`（应用多轮对话）：由云端维护上下文，免去手动拼接历史。

### 模型专属参数示例

- **Qwen-MT（翻译）**：通过 `translation_options`（OpenAI SDK 中放入 `extra_body`）控制 `source_lang`、`target_lang`、`terms`（术语干预）、`tm_list`（翻译记忆）、`domain_prompt`（领域提示）。
- **Qwen-OCR**：`messages.content` 为[多模态](multimodal.md)数组，可设 `min_pixels` / `max_pixels` 控制图像像素阈值。

## Python 快速示例（应用调用）

```python
import os
from http import HTTPStatus
from dashscope import Application

response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id='YOUR_APP_ID',
    prompt='你是谁？'
)

if response.status_code != HTTPStatus.OK:
    print(f'code={response.status_code}, message={response.message}')
else:
    print(response.output.text)
```

## 使用建议

- 优先使用环境变量管理 API Key，区分不同地域的密钥。
- 需要最完整功能与参数时选 DashScope 原生接口；追求生态兼容、迁移成本最低时可选 [OpenAI 兼容接口](openai-compatible-interface.md)。
- 接入前先对照具体模型的 API 参考，确认其支持的 SDK 语言、协议与地域。

## 关联主题页

- [image generation](../api/image-generation.md)
- [more models](../api/more-models.md)
- [bailian application calling](../guides/bailian-application-calling.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [application call](../api/application-call.md)




