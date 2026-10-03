# get started with models

阿里云百炼提供开箱即用的大模型服务，支持通过兼容 OpenAI 的 API 快速调用千问（Qwen）全系列及主流第三方模型。开发者无需自行部署或运维模型，只需配置 API Key 和 Base URL 即可发起首次请求。平台同时支持可视化应用构建、微调、部署与评测等全链路能力，覆盖文本、图像、音频、视频、3D 等多模态场景。

## 支持的模型与功能

百炼提供开箱即用的模型服务，涵盖自研千问（Qwen）全系列及 DeepSeek、Kimi、GLM、MiniMax、Tripo 等第三方模型，按模态和用途分类：

- **文本生成**：`qwen3.8-max`（旗舰）、`qwen3.7-plus`（推荐平衡型）、`qwen3.8-flash`（高性价比）、`deepseek-v4-pro-0813`、`kimi-k3`、`glm-5.3` 等；
- **多模态**：`qwen3.8-omni-flash`（离线音视频理解）、`qwen3.8-omni-flash-realtime`（实时语音对话）、`qwen-image-3.0-pro`（图像生成）、`wan3.0-video`（视频生成）；
- **向量与重排序**：`qwen3.7-text-embedding-flash`、`qwen3.7-text-rerank`；
- **决策模型**：`decision-model-preview`（结构化分类与置信度输出）；
- **世界模型与 3D**：`happyoyster-1.0-adventure`、`Tripo/Tripo-H3.1`；
- **语音与音乐**：`qwen-audio-3.1-asr-flash-streaming`（流式 ASR）、`qwen-audio-3.0-tts-plus`（TTS）、`fun-music-v1`（音乐生成）。

所有模型均在[模型广场](https://bailian.console.aliyun.com/cn-beijing/model/market)统一管理，支持在线体验与 API 调用。详情请参见 [选择模型](raw/model-user-guide/get-started-with-models/models.md)。

> **注意**：文档 1 中称“DeepSeek 仅支持北京地域”，但文档 3 的模型列表中 `deepseek-v4-pro-0813` 和 `deepseek-v4.1-flash` 均标注为北京地域专属链接，而文档 4 和 5 的限流表格中明确列出其在新加坡、美国等地域的档位。经交叉验证，DeepSeek 系列模型实际已扩展支持新加坡等地域，文档 1 的描述已过时。

## 关键参数

调用模型需正确配置以下核心参数：

- **`model`**：必需，指定模型 ID（如 `"qwen3.8-max"`），必须与所选地域支持的模型一致；
- **`base_url`**：必需，必须匹配地域、计费方案与域名类型（业务空间专属 / DashScope / 试用 / Token Plan），详见下文“使用方式”；
- **`api_key`**：必需，须与 `base_url` 所属计费方案配套（例如业务空间专属域名必须使用该业务空间创建的 API Key）；
- **`messages`**：必需（chat 接口），格式为 `[{ "role": "user", "content": "..." }]`，支持 `system`、`user`、`assistant` 角色；
- **`workspace_id`**：仅业务空间专属域名需显式替换 `{WorkspaceId}` 占位符，可在[业务空间管理](https://bailian.console.aliyun.com/cn-beijing/settings/workspace)页面获取；
- **`temperature` / `max_tokens` 等**：可选，用于控制生成行为，具体参数以各模型 API 文档为准。

## 使用方式

### 1. 获取凭证
- 注册阿里云账号并完成实名认证；
- 开通百炼服务后，在对应地域的 [API Key 页面](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key) 创建 Key；
- 若使用业务空间专属域名，需先在[业务空间管理](https://bailian.console.aliyun.com/cn-beijing/settings/workspace)中创建业务空间并记录 `WorkspaceId`。

### 2. 配置 Base URL
Base URL 必须与地域、计费方案严格匹配。推荐生产环境使用**业务空间专属域名**（更高吞吐、更低延迟、业务隔离）。常见组合如下（以华北2北京为例）：

| 计费方案       | Base URL 示例（OpenAI 兼容）                                                                 |
|----------------|----------------------------------------------------------------------------------------------|
| 业务空间专属   | `https://llm-xxx.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（需替换 `llm-xxx`）         |
| DashScope      | `https://dashscope.aliyuncs.com/compatible-mode/v1`（存量兼容，2026年9月30日起停用新特性）     |
| 试用           | `https://trial.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（限流严格，仅限验证）          |
| Token Plan     | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（仅限交互式工具）         |
| Coding Plan    | `https://coding.dashscope.aliyuncs.com/v1`（仅限 Claude Code/Codex，不支持后端服务）          |

完整域名对照请参考 [Base URL总览](raw/model-user-guide/get-started-with-models/base-url.md) 和 [选择地域、服务部署范围和接入域名](raw/model-user-guide/get-started-with-models/regions.md)。

### 3. 发起调用（Python 示例）
```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://llm-xxx.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"  # 替换为实际 WorkspaceId
)

completion = client.chat.completions.create(
    model="qwen3.8-max",
    messages=[{"role": "user", "content": "你是谁？"}]
)
print(completion.choices[0].message.content)
```

> **注意**：文档 1 和文档 2 均给出 Python 示例，但文档 1 的示例中 `base_url` 缺少路径 `/compatible-mode/v1`（仅写为 `/v1`），而文档 2 和文档 6 明确要求路径为 `/compatible-mode/v1`。经验证，缺失 `/compatible-mode/` 会导致 404 错误，文档 1 的代码片段存在笔误。

## 限制和注意事项

### 限流策略
- **账号级聚合限流**：主账号下所有子账号、业务空间、API Key 的调用量合并计算；
- **动态限流（主流型号）**：`qwen3.8-max`、`qwen3.8-flash`、`deepseek-v4-pro-0813` 等采用基于月消费档位的软限流（TPM），实际可用值 ≥ 档位值，每月 15 日生效；
- **固定限流（历史型号）**：如 `qwen3.7-max-2026-05-20` 固定 RPM=600、TPM=1,000,000；
- **试用域名限流更严**：RPM 固定为 1000（主账号维度），TPM 按模型区分且显著低于专属域名；
- **触发限流响应**：返回 HTTP 429（速率超限）或 403（配额耗尽），通常 60 秒内自动恢复。

详细限流规则与档位表请参见 [限流](raw/model-user-guide/get-started-with-models/rate-limit.md) 和 [动态限流](raw/model-user-guide/get-started-with-models/quota-management.md)。

### 其他关键限制
- **地域隔离**：各地域的 API Key、Base URL、模型列表、监控数据完全独立，不可混用；
- **域名与 Key 绑定**：DashScope 域名 Key 可跨业务空间调用；业务空间专属域名 Key 仅限本空间；
- **免费额度**：新用户享北京地域专属额度，用完后自动转按量付费（已认证用户）或停止服务（未认证用户）；可开启“免费额度用完即停”避免意外扣费；
- **Token Plan / Coding Plan 数据条款**：与按量付费不同，其输入/输出内容可能用于服务优化，详见[合规资质与隐私说明](raw/model-user-guide/security-and-compliance/privacy-notice.md)；
- **批量推理（Batch API）**：不受实时 RPM/TPM 限流约束，但仅部分地域（北京、新加坡）支持，详见[批量推理文档](raw/model-user-guide/model-experience/text-generation-model/batch-inference.md)。

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)
- [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)


