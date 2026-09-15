# get started with models

阿里云百炼提供一站式大模型调用服务，支持通过 OpenAI 兼容 API、DashScope SDK 等方式快速接入千问（Qwen）全系列及主流第三方模型。开发者无需自行部署或运维，仅需配置 API Key 和 Base URL，即可在数分钟内完成首次调用。平台覆盖文本、图像、音频、视频、3D、向量等多模态能力，并提供细粒度的限流控制与生产级域名支持。

## 支持的模型/功能

百炼提供开箱即用的模型服务，包括自研千问（Qwen）全系列旗舰模型（如 `qwen3.8-max`、`qwen3.7-plus`、`qwen3.8-flash`）以及 DeepSeek、Kimi、GLM、MiniMax、小米 Mimo 等第三方模型 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。模型按模态和场景分类：
- **文本生成**：支持通用对话、长文本处理、法律、翻译、意图理解等细分领域；
- **多模态**：涵盖视觉理解（`qwen3.5-omni-plus`）、图像生成（`qwen-image-3.0-pro`）、视频生成（`wan3.0-video`）、语音合成（`qwen-audio-3.0-tts-plus`）、语音识别（`qwen-audio-3.0-asr-flash-streaming`）等；
- **向量与重排序**：提供文本/图文嵌入（`qwen3.7-text-embedding`）和重排序（`qwen3.7-text-rerank`）模型；
- **全模态**：支持端到端多模态联合推理（如 `qwen3.5-omni-plus-realtime`）。

所有模型均在[模型广场](https://bailian.console.aliyun.com/cn-beijing/model/market)统一管理，各地域支持的模型列表存在差异，详情请参见 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。

> **注意**：文档 1 中称 “DeepSeek 仅支持北京地域”，但文档 3 的模型列表明确展示了 `deepseek-v4-pro-0813` 在新加坡等地域能力页存在。实际支持以控制台实时列表为准，建议优先查阅 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 获取最新地域覆盖信息。

## 关键参数

调用模型必需的核心参数包括：

- **`model`**：模型标识符（如 `"qwen3.8-max"`），必须与所选地域支持的模型一致；
- **`api_key`**：通过 [API Key 页面](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key) 创建，不同地域的 API Key 不通用；
- **`base_url`**：必须与 API Key 所属计费方案和地域严格匹配，否则返回 401 错误。推荐使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），其具备更高吞吐、更低时延与业务空间级隔离 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)；
- **`messages`**：遵循 OpenAI 格式，`role` 为 `"user"`/`"system"`/`"assistant"`，`content` 为字符串或结构化内容（如多模态输入）；
- **`WorkspaceId`**：使用业务空间专属域名时必需，可在 [业务空间管理](https://bailian.console.aliyun.com/cn-beijing/settings/workspace) 页面查看。

## 使用方式

1. **开通与准备**：注册阿里云账号 → 实名认证 → 开通百炼 → 创建 API Key → 获取 `WorkspaceId`（若使用业务空间专属域名）；
2. **配置环境**：将 `DASHSCOPE_API_KEY` 设为环境变量（避免硬编码）；
3. **发起调用**：使用 OpenAI Python SDK（推荐）、DashScope SDK 或 curl 发起请求。示例（OpenAI SDK）：
   ```python
   from openai import OpenAI
   client = OpenAI(
       api_key=os.getenv("DASHSCOPE_API_KEY"),
       base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
   )
   response = client.chat.completions.create(
       model="qwen3.8-max",
       messages=[{"role": "user", "content": "你是谁？"}]
   )
   ```
   > 完整代码与 Node.js/curl 示例详见 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)。

4. **生产部署建议**：
   - 优先选用业务空间专属域名，避免 DashScope 域名于 2026 年 9 月 30 日后停用 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)；
   - 对高并发场景，启用动态限流模型（如 `qwen3.8-max`）并确保月消费档位匹配业务需求；
   - 避免使用带日期后缀的快照模型（如 `qwen-plus-2025-07-28`），其限流额度显著低于稳定版（如 `qwen3.7-plus`）。

## 限制和注意事项

- **地域隔离**：各地域（北京、新加坡、美国弗吉尼亚等）的 Base URL、API Key、模型列表、计费策略完全独立，不可混用；
- **限流机制**：
  - 按主账号维度合并计算所有子账号、业务空间、API Key 的调用量；
  - `qwen3.8-max`、`qwen3.8-flash` 等主力模型采用[动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)，TPM 阈值随百炼月消费金额分档调整（如北京地域消费 ¥10–100 万对应 1000 万 TPM）；
  - 快照模型（含日期后缀）RPM/TPM 限流极低（常为 60 RPM / 100 万 TPM），仅适用于测试，生产环境应避免；
  - 请求体大小限制：不含 Base64 的请求 ≤ 16 MiB；含 Base64 的整体请求 ≤ 64 MiB，且解码后仍需 ≤ 16 MiB [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)；
- **费用与额度**：
  - 新用户享有北京地域免费额度，用尽后自动转为按量付费（已认证用户）或停止服务（未认证用户）；
  - Coding Plan 和 Token Plan 个人版的数据使用条款与按量付费不同，其输入/输出内容可能用于模型优化 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)；
- **安全与合规**：按量付费与 Token Plan 团队版承诺不使用客户数据训练模型；所有传输数据加密，静态数据存储于所选地域。

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)
- [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)


