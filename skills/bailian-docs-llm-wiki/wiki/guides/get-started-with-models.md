# get started with models

阿里云百炼提供开箱即用的大模型服务，支持通过兼容 OpenAI 的 API 快速调用千问（Qwen）全系列及主流第三方模型。开发者无需自行部署或运维，只需配置 API Key、Base URL 和模型名称，即可在几分钟内完成首次调用。平台同时覆盖文本、图像、音频、视频、3D、向量等多模态能力，并提供微调、部署、评测等全链路模型工程能力。

## 支持的模型与功能

百炼提供自研千问（Qwen）全系列模型（如 `qwen3.8-max`、`qwen3.8-plus`、`qwen3.8-flash`）、DeepSeek、Kimi、GLM、MiniMax、Tripo 等第三方模型，覆盖文本生成、多模态理解与生成、语音合成/识别、音乐生成、世界模型、3D 生成、嵌入向量与重排序等场景。所有模型均按模态和用途分类，可在[模型广场](https://bailian.console.aliyun.com/cn-beijing/model/market)统一查看与体验。  
> **注意**：文档 3 中列出的 `qwen3.8-omni-flash-realtime` 和 `qwen3.8-omni-flash` 均指向同一类全模态模型，但其调用协议与适用场景存在差异（离线 vs 实时），实际使用需严格参照 [qwen3.8-omni-flash-realtime](raw/model-user-guide/support/model-studio-model-list/model-list-omni/qwen3-8-omni-flash-realtime.md) 和 [qwen3.8-omni-flash](raw/model-user-guide/support/model-studio-model-list/model-list-omni/qwen3-8-omni-flash.md) 的具体说明，避免混淆。

- **文本生成主力模型**：`qwen3.8-max`（复杂任务首选）、`qwen3.8-plus`（效果/速度/成本均衡，推荐通用场景）、`qwen3.8-flash`（高性价比、低延迟）。
- **多模态能力**：`qwen3.8-omni-flash`（音视频分析+文本生成）、`qwen3.8-omni-flash-realtime`（端到端实时语音对话）。
- **向量与检索增强**：`qwen3.7-text-embedding-flash`、`qwen3.7-text-rerank` 等，专用于 RAG 场景。
- **领域与细分模型**：法律、长文本、意图理解、角色扮演等专用模型，详见[选择模型](raw/model-user-guide/get-started-with-models/models.md)。

## 关键参数

调用模型必需的核心参数包括：

- `model`：模型标识符（如 `"qwen3.8-max"`），必须与所选地域支持的模型列表一致；
- `base_url`：接入域名，**必须与 API Key 所属地域和计费方案严格匹配**，否则返回 401 错误；
- `api_key`：通过[API Key](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key)页面创建，不同地域的 Key 不通用；
- `messages`：标准 Chat Completions 格式，支持 `system`/`user`/`assistant` 角色；
- `workspace_id`：华北2（北京）、新加坡、日本（东京）、德国（法兰克福）、中国香港、美国（弗吉尼亚）地域均需在 `base_url` 中填入业务空间 ID（WorkspaceId），该 ID 在[业务空间管理](https://bailian.console.aliyun.com/cn-beijing/settings/workspace)中获取。

> **注意**：文档 1 和文档 2 均强调 `base_url` 中 `{WorkspaceId}` 需手动替换为真实值，但文档 6 明确指出“DashScope 域名（如 `dashscope.aliyuncs.com`）自2026年9月30日起不再支持新特性”，而文档 7 的 [Token](../concepts/token.md) Plan 和 Coding Plan 域名（如 `token-plan.cn-beijing.maas.aliyuncs.com`）明确标注“仅限 AI 工具交互式使用，不能用于后端服务”。三者存在明显定位冲突——生产环境必须使用业务空间专属域名，且不可混用 Key 与 URL；若沿用 DashScope 域名，将面临功能缺失与未来停用风险。

## 使用方式

### 1. 环境准备
- 注册阿里云账号并完成实名认证；
- 开通百炼服务，在[API Key 页面](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key)创建 Key；
- 在[业务空间管理](https://bailian.console.aliyun.com/cn-beijing/settings/workspace)获取 `WorkspaceId`；
- 将 `DASHSCOPE_API_KEY` 配置为环境变量（推荐），避免硬编码。

### 2. SDK 调用（OpenAI 兼容）
```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",  # 替换 {WorkspaceId}
)

completion = client.chat.completions.create(
    model="qwen3.8-plus",
    messages=[{"role": "user", "content": "你是谁？"}]
)
print(completion.choices[0].message.content)
```

完整示例与 Node.js/curl 版本见 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。  
首次调用全流程指引详见 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)。

### 3. 域名选择策略
- **生产环境**：强制使用**业务空间专属域名**（如 `llm-xxx.cn-beijing.maas.aliyuncs.com`），具备更高并发、更低延迟与流量隔离；
- **快速验证**：可临时使用试用域名（如 `trial.cn-beijing.maas.aliyuncs.com`），但 RPM 限流仅为 1000，不适用于压测；
- **存量迁移**：DashScope 域名（如 `dashscope.aliyuncs.com`）仍可用，但需尽快按[迁移至业务空间专属域名](../../raw/model-user-guide/get-started-with-models/regions.md)指南升级。

## 限制和注意事项

### 限流机制
- **账号级聚合限流**：RPM（每分钟请求数）与 TPM（每分钟 [Token](../concepts/token.md) 消耗）按主账号维度合并计算，子账号、业务空间、API Key 共享同一额度；
- **动态限流模型**：`qwen3.8-max`、`qwen3.8-flash` 等主力模型采用动态限流，TPM 阈值随百炼月消费金额自动提升（如北京地域消费 ¥10万~¥100万档位对应 1000万 TPM），详情见 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)；
- **静态限流模型**：历史版本（如 `qwen3.7-max-2026-06-08`）采用固定 RPM/TPM（如 600/1,000,000），详见 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md) 表格；
- **触发恢复**：限流后通常 60 秒内自动恢复，错误码 `429` 表示速率超限，`403` 表示免费额度耗尽。

### 其他关键限制
- **请求体大小**：不含 Base64 的请求 ≤ 16 MiB；含 Base64 的请求整体 ≤ 64 MiB，且解码后仍需 ≤ 16 MiB，否则返回 HTTP 413；
- **地域隔离**：各地域 Endpoint、API Key、模型列表完全独立，不可跨地域混用；
- **[Token](../concepts/token.md) Plan/Coding Plan 限制**：专属域名（如 `token-plan.cn-beijing.maas.aliyuncs.com`）仅支持交互式工具调用，**禁止用于后端服务或自动化脚本**，否则调用将失败或产生意外计费；
- **数据隐私承诺差异**：按量付费与 Token Plan 团队版承诺“不使用客户数据训练模型”，但 **Token Plan 个人版与 Coding Plan 明确不包含该承诺**，详见 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md) 中的常见问题说明。

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)
- [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)


