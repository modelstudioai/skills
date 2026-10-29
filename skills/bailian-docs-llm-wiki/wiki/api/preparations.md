# preparations

在调用阿里云百炼平台模型服务前，开发者需完成 SDK 安装、API Key 获取与配置、环境准备等基础步骤。这些准备工作直接影响后续模型调用的稳定性、安全性和兼容性。本文汇总了官方推荐的标准化流程，覆盖主流语言 SDK、关键参数约束、典型使用方式及常见限制，适用于所有模型类型（文本、图像、视频、语音、向量、排序等）。

## 支持的模型/功能

百炼平台支持通过 DashScope SDK 和 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)调用全栈模型能力，包括文本生成（如 `qwen-plus`、`qwen-max`）、多模态对话（如 `qwen3-vl-plus`）、图像生成（如 `wanx2.1-t2i-turbo`）、视频生成（如 `wan3.0-video`）、语音识别（如 `paraformer-v2`）、语音合成（如 `cosyvoice-v3-flash`）、文本向量（如 `qwen3.7-text-embedding`）和重排序（如 `qwen3.7-rerank`）等。实时语音或多模态模型需通过 AOQ SDK 调用，具体支持范围请参见[模型与协议支持范围](https://help.aliyun.com/zh/model-studio/realtime-api-overview#rtov-s02h2) [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)。[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)支持 Python、Node.js、Java、Go 等多语言 SDK，但需注意部分高级功能（如 AOQ 实时流）仅 DashScope SDK 原生支持。

> **注意**：DashScope Python SDK 1.x 已进入冻结维护状态，仅修复缺陷、不增新功能；新项目必须使用 SDK 2.0（≥2.0.1），存量项目可并存但应逐步迁移。1.x 的 `Assistants / Threads / Runs` 系列 API 已下线，服务端不再支持 [DashScope Python SDK 1.x 历史用法参考](../../raw/model-api-reference/preparations/dashscope-1x-legacy-reference.md)。

## 关键参数

- **API Key**：必须通过百炼控制台按地域单独创建，各地域 Key 独立且不可混用；建议归属业务空间并选择“全部”权限，精细化控制需切换为“自定义”并配置 IP 白名单与模型范围 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)。
- **Base URL**：华北2（北京）固定为 `https://dashscope.aliyuncs.com/compatible-mode/v1`；其他地域需查[Base URL 总览](raw/model-user-guide/get-started-with-models/base-url.md)，AOQ 实时 API 则使用 `https://{workspace-id}.{region}.maas.aliyuncs.com/api/v1` 格式。
- **模型名称**：必须严格匹配模型市场中的 ID（如 `qwen3.7-plus`），区分大小写，不可混用开源社区命名（如 `Qwen/Qwen3.7-Plus`）；调用前需确认该模型已在对应业务空间开通 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)。
- **关键请求参数**：
  - `stream`：思考模式模型（如 `qwen3.7-plus`）强制要求 `true`；纯音频输出（TTS）也必须启用流式。
  - `enable_thinking`：开启后需同时设置 `incremental_output=true` 且 `result_format="message"`；结构化输出（`response_format={"type": "json_object"}`）时必须设为 `false`。
  - `messages`：内容必须为字符串或符合规范的对象数组（`type` 仅限 `text`/`image_url`/`video_url` 等）；纯文本模型禁止传入图片等多模态元素。
  - `max_tokens`、`temperature`、`top_p` 等采样参数须在模型文档标明的合法范围内，超限将返回 `400-InvalidParameter` 错误 [错误码](../../raw/model-api-reference/preparations/error-code.md)。

## 使用方式

1. **SDK 安装**：Python 推荐 `pip install -U "dashscope>=2.0.1"`（2.0.1+ 必选）或 `openai`；Java 用 Maven/Gradle 引入 `com.alibaba:dashscope-sdk-java` 或 `com.openai:openai-java:3.5.0`；Node.js 用 `npm install openai`；Go 用 `go get 'github.com/openai/openai-go/v3@v3.8.1'` [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)。
2. **API Key 配置**：优先设为环境变量 `DASHSCOPE_API_KEY`（Linux/macOS 用 `export`，Windows 用系统属性或 `setx`），避免硬编码；生产环境禁用客户端暴露长期 Key，应使用临时 API Key（最长 1800 秒） [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)。
3. **代码调用**：SDK 2.0 统一使用 `Client` 实例构造（传入 `api_key`、`region`、`workspace`），不再依赖全局变量；文本生成示例：`client.chat.completions.create(model="qwen-plus", messages=[{"role":"user","content":"..."}])`；流式需遍历 `stream` 迭代器并处理 `chunk.choices[0].delta.content` [DashScope Python SDK 1.x 历史用法参考](../../raw/model-api-reference/preparations/dashscope-1x-legacy-reference.md)。
4. **智能辅助开发**：安装 `dashscope>=1.27.3` 后，运行 `dashscope` CLI 启动 SDK Expert，可自然语言描述需求（如“用 qwen-plus [流式输出](../concepts/streaming-output.md)并统计 token”）直接生成校验过版本的可运行代码，或贴报错/文件路径自动诊断修复 [DashScope SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md)。

## 限制和注意事项

- **地域隔离**：API Key、Base URL、模型列表均按地域独立，跨地域调用必然失败；各地域接入信息详见[时效性与限制](https://help.aliyun.com/zh/model-studio/regions#h2_cc92e61c) [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)。
- **配额与数量**：单账号+单地域最多 50 个 API Key；自定义权限下最多勾选 30 个模型；IP 白名单最多 20 个地址；临时 API Key 最长 1800 秒 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)。
- **环境变量生效问题**：临时变量仅对当前终端会话有效；IDE/服务需重启才能加载新变量；`sudo` 默认不继承环境变量，需加 `-E` 参数 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)。
- **错误排查**：务必记录 `request_id`（响应 Header 或 Body 中），用于日志查询与工单提交；JSON 请求体格式错误（如引号未闭合、逗号多余）是高频原因，建议用 jsonlint.com 校验 [错误码](../../raw/model-api-reference/preparations/error-code.md)。
- **安全红线**：严禁在浏览器、移动 App 等客户端代码中嵌入长期 API Key；敏感数据（如诊断时上传的源码）会经模型推理，需自行脱敏 [DashScope SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md)。

## 来源文档

- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [DashScope SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md)
- [DashScope Python SDK 1.x 历史用法参考](../../raw/model-api-reference/preparations/dashscope-1x-legacy-reference.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)


