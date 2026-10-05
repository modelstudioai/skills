# get started with models

阿里云百炼提供开箱即用的大模型服务，支持通过兼容 OpenAI 的 API 快速调用千问（Qwen）全系列及主流第三方模型。开发者无需自行部署或运维，仅需配置 API Key、Base URL 和模型名称，即可在几分钟内完成首次调用。平台同时覆盖文本、图像、音频、视频、3D、向量、决策等多模态能力，满足从原型验证到生产部署的全场景需求。

## 支持的模型与功能

百炼提供自研千问（Qwen）全系模型（如 `qwen3.8-max`、`qwen3.8-plus`、`qwen3.8-flash`）、第三方模型（如 `deepseek-v4-pro-0813`、`kimi/kimi-k3`、`glm-5.3`）及领域专用模型（法律、长文本、意图理解等）。模型能力覆盖：

- **文本生成**：通用对话、摘要、创作、代码生成；
- **多模态理解与生成**：图文理解（`qwen3.8-omni-flash`）、图像生成（`qwen-image-3.0-pro`）、视频生成（`wan3.0-video`）、语音识别（`qwen-audio-3.1-asr-flash-streaming`）与合成（`qwen-audio-3.0-tts-plus`）；
- **向量与重排序**：`qwen3.7-text-embedding-flash`、`qwen3.7-text-rerank`；
- **世界模型与3D生成**：`happyoyster-1.0-adventure`、`Tripo/Tripo-H3.1`；
- **决策模型**：结构化分类与置信度输出（`decision-model-preview`）。

完整模型列表请参见[选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。

> **注意**：文档 3 中列出的 `qwen3.7-plus` 与文档 1 中推荐的 `qwen3.8-plus` 存在版本不一致；实际应以控制台最新模型广场为准，当前主力推荐为 `qwen3.8-plus`（文档 1 明确标注“效果、速度和成本均衡，是多数场景的**推荐选择**”），`qwen3.7-plus` 已属历史版本，限流策略与性能均弱于新版（参见[限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)中 RPM/TPM 对比）。

## 关键参数

调用模型必需的核心参数包括：

- `model`：模型标识符，如 `"qwen3.8-max"`、`"deepseek-v4-pro-0813"`，必须与所选地域支持的模型一致；
- `base_url`：接入域名，**必须与地域和计费方案严格匹配**（例如北京地域业务空间专属域名为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）；
- `api_key`：通过 [API Key 管理页面](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key) 创建，**不同地域的 API Key 不通用**；
- `messages`：标准 OpenAI 格式消息数组，支持 `system`、`user`、`assistant` 角色；
- `workspace_id`：业务空间 ID，用于构造 `base_url`，仅在华北2（北京）、新加坡、日本（东京）、德国（法兰克福）、中国香港、美国（弗吉尼亚）地域必需，可在[业务空间管理](https://bailian.console.aliyun.com/cn-beijing/settings/workspace)页面获取。

更多参数说明（如 `max_tokens`、`temperature`、`top_p`）详见 [通义千问 API 参考](../../raw/model-api-reference/qwen-api-reference.md)。

## 使用方式

### 1. 环境准备
- 注册阿里云账号并完成实名认证；
- 开通百炼服务，创建 API Key 并配置为环境变量 `DASHSCOPE_API_KEY`；
- 获取业务空间 ID（非北京/新加坡等指定地域可跳过）；
- 安装 SDK：`pip install -U openai`（推荐）或 `pip install -U dashscope`。

### 2. 发起调用（OpenAI SDK 示例）
```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",  # 替换 {WorkspaceId}
)

completion = client.chat.completions.create(
    model="qwen3.8-plus",  # 推荐首选
    messages=[{"role": "user", "content": "你是谁？"}]
)
print(completion.choices[0].message.content)
```

> **注意**：文档 5 明确指出 DashScope 域名（如 `dashscope.aliyuncs.com`）将于 2026 年 9 月 30 日起停止支持新特性，**生产环境必须使用业务空间专属域名**（参见[Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)）。

### 3. 多语言支持
除 Python 外，官方提供 Node.js、curl 示例（见[什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)），其他语言可基于 OpenAI 兼容规范自行对接。

## 限制和注意事项

- **地域隔离**：各地域（北京、新加坡、美国等）的 Base URL、API Key、模型列表、计费规则完全独立，**严禁跨地域混用**；
- **限流机制**：
  - 主账号维度统一计算 RPM（每分钟请求数）与 TPM（每分钟 Token 消耗），所有子账号、业务空间、API Key 合并计入；
  - `qwen3.8-max`、`qwen3.8-flash` 等主力模型采用[动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)，TPM 阈值随月消费金额自动提升（如北京地域消费 ¥50 万对应 `qwen3.8-max` TPM 1000 万）；
  - 试用域名 RPM 仅为 1000，**禁止用于生产**；
- **费用控制**：
  - 新用户享有北京地域免费额度，用完后可开通“免费额度用完即停”开关避免扣费；
  - Coding Plan 与 Token Plan 专属域名（如 `coding.dashscope.aliyuncs.com/v1`）**仅限交互式工具使用，不可用于后端服务调用**；
- **安全与合规**：
  - 按量付费与 Token Plan 团队版承诺不使用客户数据训练模型（参见[合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)）；
  - Token Plan 个人版与 Coding Plan 数据使用条款不同，调用前务必确认协议。

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)
- [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)


