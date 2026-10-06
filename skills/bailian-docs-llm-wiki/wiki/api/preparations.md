# preparations

在调用百炼平台模型服务前，开发者需完成 API Key 获取与配置、SDK 安装、环境准备及参数校验等基础工作。这些步骤直接影响调用的稳定性、安全性与兼容性。本文汇总核心准备事项，覆盖从凭证管理到错误排查的完整链路，所有操作均需结合地域、业务空间和模型能力进行精细化配置。

## 支持的模型/功能

百炼支持两类主流调用路径：  
- **DashScope 原生协议**：适用于所有标准模型（文本生成、图像/视频生成、语音合成/识别、向量嵌入、排序等），需使用 `dashscope` SDK 或直接调用 HTTP 接口；  
- **OpenAI 兼容协议**：支持 Python/Node.js/Java/Go 等多语言 OpenAI SDK，适用于文本生成、嵌入、文件上传等场景，但**不支持 Realtime API 的实时语音或多模态流式交互**（该能力需通过 [AOQ SDK](raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md) 实现）[安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)。  
> **注意**：部分模型（如 `qwen3-235b-a22b-thinking-2507`）强制要求 `enable_thinking=true`，而结构化输出（`response_format="json_object"`）与思考模式互斥，二者不可同时启用——详见 [错误码文档](../../raw/model-api-reference/preparations/error-code.md) 中对应条目。

## 关键参数

调用时需严格校验以下参数范围与格式，否则将触发 `400-InvalidParameter` 错误：  
- `temperature`: `[0.0, 2.0)`；`top_p`: `(0.0, 1.0]`；`top_k`: `≥ 0`；`repetition_penalty`/`presence_penalty`: `> 0.0` / `[-2.0, 2.0]`；  
- `max_tokens`: 必须在模型文档标注的「最大输出 [Token](../concepts/token.md) 数」范围内；  
- `stream`: 部分模型（如思考模式模型、音频输出模型）**仅支持流式调用**，非流式请求将被拒绝；  
- `messages` 格式：纯文本模型要求 `content` 为字符串，多模态模型要求 `content` 数组中每个元素为合法对象（`type` 仅限 `text`/`image_url`/`video_url` 等）；  
- `response_format`: 使用 `json_object` 时，提示词中**必须包含 `json` 关键词**（不区分大小写），且 `enable_thinking` 必须为 `false`。  
详细参数约束见 [错误码文档](../../raw/model-api-reference/preparations/error-code.md)。

## 使用方式

1. **获取并配置 API Key**：  
   - 在控制台按地域创建 API Key，**各地域 Key 独立，不可跨地域混用**；  
   - 推荐配置为环境变量 `DASHSCOPE_API_KEY`（Linux/macOS/Windows 均有标准化配置方法）；  
   - 生产环境严禁在客户端代码中硬编码长期 Key，应使用 [临时 API Key](raw/model-api-reference/more-about-models/generate-temporary-api-key.md)（最长 1800 秒）[获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)。  

2. **安装 SDK**：  
   - Python：`pip install -U dashscope`（推荐 ≥1.27.3 以启用 SDK Expert）或 `pip install -U openai`；  
   - Java/Node.js/Go：参考 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md) 文档中的 Gradle/Maven/npm/go get 示例；  
   - 多模态或通义以外模型需额外安装：`pip install -U 'dashscope[acli-all]'`。  

3. **启用智能辅助（可选）**：  
   - DashScope SDK ≥1.27.3 内置 [SDK Expert CLI](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md)，支持自然语言生成可运行代码、诊断报错、解释逻辑等，启动命令为 `dashscope` 或 `python -m dashscope.acli`。

## 限制和注意事项

- **地域隔离**：API Key、Base URL、模型列表均按地域独立，华北2（北京）的 Key 无法调用新加坡地域模型；  
- **业务空间权限**：API Key 权限由其归属业务空间决定，**同一空间内所有 Key 权限一致**；子业务空间下的 Key 仅能调用该空间已授权的模型；  
- **数量限制**：单账号+单地域最多 50 个 API Key；自定义权限下最多勾选 30 个模型、20 个 IP 白名单地址；  
- **安全红线**：  
  - 禁止在浏览器/移动 App 等不可信环境使用长期 API Key；  
  - 使用 `sudo` 运行脚本时需加 `-E` 参数传递环境变量（`sudo -E python xx.py`）；  
  - systemd 等服务管理器需显式加载环境文件（如 `/etc/your-app/env`）；  
- **调试必备**：调用失败时务必记录 `request_id`（UUID 格式），用于日志查询或提工单；未开启推理日志则无法追溯历史调用。

## 来源文档

- [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [DashScope SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)


