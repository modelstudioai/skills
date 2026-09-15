# preparations

在调用百炼平台模型服务前，开发者需完成 API Key 获取与配置、SDK 安装、环境准备及参数校验等基础工作。这些步骤直接影响调用的可用性、安全性与稳定性。本文汇总核心准备事项，聚焦可执行操作与关键约束，避免常见配置陷阱。

## 支持的模型/功能

- 百炼支持文本生成（如 `qwen-plus`、`qwen3-8b`、`deepseek-r1`）、图像生成、视频生成、语音合成与识别、向量嵌入、排序、多模态及思考模式模型等全栈能力。具体模型清单请参见 [模型列表](raw/model-user-guide/get-started-with-models/models.md)。
- [OpenAI 兼容接口](../concepts/openai-compatible-api.md)支持主流模型（如 `gpt-4o` 别名映射至 `qwen3-235b-a22b-instruct-2507`），但**必须使用百炼控制台开通的模型 ID**，不可直接复用开源社区命名（例如应使用 `qwen3-235b-a22b-instruct-2507`，而非 `Qwen/Qwen3-235B-A22B-Instruct-2507`）[原文标题](../../raw/model-api-reference/preparations/error-code.md)。
- 部分模型有强制能力约束：例如 `qwen3-235b-a22b-thinking-2507` 要求 `enable_thinking=true`；Qwen-Omni 模型仅支持 `stream=true`；纯文本模型（如 `qwen3-max`）不接受 `image_url` 等多模态 `content` 元素，否则报错 [原文标题](../../raw/model-api-reference/preparations/error-code.md)。

> **注意**：文档 3 中提到的 `DASHSCOPE_HTTP_BASE_URL=https://{workspace-id}.{region}.maas.aliyuncs.com/api/v1` 为 MaaS 专属域名，而文档 1 推荐的通用 Base URL 是 `https://dashscope.aliyuncs.com/compatible-mode/v1`。二者适用场景不同：前者用于直连 MaaS 工作空间部署的私有模型，后者用于调用百炼标准模型服务。混用将导致 `Model not exist` 错误。请根据实际[模型部署](../concepts/model-deployment.md)方式选择 [原文标题](../../raw/model-api-reference/preparations/get-api-key.md)。

## 关键参数

- **API Key**：必须通过百炼控制台按地域单独创建，**不可跨地域复用**；建议归属业务空间并配置权限（默认“全部”，自定义时最多选 30 个模型）[原文标题](../../raw/model-api-reference/preparations/get-api-key.md)。
- **Base URL**：华北2（北京）为 `https://dashscope.aliyuncs.com/compatible-mode/v1`；其他地域请查 [Base URL 总览](raw/model-user-guide/get-started-with-models/base-url.md)。
- **模型名称（model）**：严格区分大小写与空格，须与 [模型列表](raw/model-user-guide/get-started-with-models/models.md) 一致。
- **流式参数**：思考模式模型（`enable_thinking=true`）要求 `stream=true` 且 `result_format="message"`；部分模型（如 Qwen-Omni）强制 `stream=true`；`incremental_output` 在思考模式下必须为 `true`。
- **结构化输出**：启用 `response_format={"type": "json_object"}` 时，提示词中必须包含 `json`（不区分大小写），且 `enable_thinking` 必须为 `false`。
- **Token 限制**：`max_tokens` 值须在 `[1, 模型最大输出 Token]` 区间；输入 `messages` 总长度不得超过模型最大输入 Token 数，超限需截断或开启新对话。

## 使用方式

- **API Key 配置**：推荐设为环境变量 `DASHSCOPE_API_KEY`（Linux/macOS/Windows 均支持永久/临时配置），**严禁硬编码于客户端代码中**；高安全场景应使用 [临时 API Key](raw/model-api-reference/more-about-models/generate-temporary-api-key.md)（最长 1800 秒）[原文标题](../../raw/model-api-reference/preparations/get-api-key.md)。
- **SDK 安装**：
  - Python：`pip install -U dashscope`（含 SDK Expert CLI）或 `pip install -U openai`；
  - Java/Node.js/Go：参考对应语言的 [OpenAI SDK 或 DashScope SDK 安装指南](../../raw/model-api-reference/preparations/install-sdk.md)。
- **SDK Expert（Python）**：`dashscope` CLI 提供自然语言生成代码、错误诊断（`/skill diagnose <file>`）、文档查询（`/skill api-doc Generation`）等能力，需 `dashscope>=1.27.3`；多模态模型需额外安装 `pip install -U 'dashscope[acli-all]'`。

## 限制和注意事项

- **地域隔离**：API Key、Base URL、模型列表均按地域独立，跨地域调用必失败。
- **配额与数量**：单业务空间最多 20 个 API Key；自定义权限下最多选 30 个模型；IP 白名单最多 20 个地址（IPv6 仅华北2支持）。
- **安全红线**：
  - API Key 不得出现在浏览器、移动 App 或公开代码库中；
  - `sudo python xx.py` 会丢失环境变量，应改用 `sudo -E python xx.py` 或避免 `sudo`；
  - systemd 等服务管理器需显式加载环境文件（如 `/etc/your-app/env`）。
- **调试必备**：所有 API 调用失败时，务必记录 `request_id`（响应 Header 或 Body 中），用于日志查询或工单提交；可借助 [阿里云 AI 助理](https://www.aliyun.com/ai-assistant/) 输入错误码快速定位 [原文标题](../../raw/model-api-reference/preparations/error-code.md)。
- **模型开通**：通过 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)调用前，必须在百炼控制台 [模型市场](https://bailian.console.aliyun.com/cn-beijing/model/market) 开通目标模型，否则返回 `The product is not activated`。

## 来源文档

- [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [DashScope SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)


