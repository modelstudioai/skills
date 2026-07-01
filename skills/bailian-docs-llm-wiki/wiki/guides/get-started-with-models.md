# get started with models

阿里云百炼是一站式大模型开发平台，兼容 OpenAI 接口规范，提供千问（Qwen）全系列及 DeepSeek、Kimi 等第三方模型的即开即用服务。开发者只需获取 [API Key](../concepts/api-key.md)、配置 Base URL，即可通过几行代码完成模型调用。

## 平台概览

百炼面向开发者提供模型 API 调用、模型调优与部署、应用构建三大核心能力。详细介绍参见[什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。

主要功能包括：

- **模型调用**：兼容 OpenAI / Anthropic / DashScope 三种接口协议，覆盖文本生成、视觉理解、图像生成、语音识别与合成、嵌入向量等多种模态
- **应用构建**：可视化创建智能体、工作流应用，或通过高代码模式部署 Python 后端服务
- **模型调优与部署**：支持 SFT、CPT、DPO 微调，以及资源专享的推理服务部署

## 模型选择

百炼提供多层级的千问模型，按需选择（详见[选择模型](../../raw/model-user-guide/get-started-with-models/models.md)）：

| 模型层级 | 推荐模型 | 适用场景 |
|---------|---------|---------|
| Max（最强） | qwen3.7-max | 复杂、多步骤推理任务 |
| Plus（均衡） | qwen3.7-plus | 多数场景的推荐选择，效果/速度/成本均衡 |
| Flash（高性价比） | qwen3.6-flash | 快速响应的简单任务，低延迟 |

此外还提供长文本处理、翻译、数据挖掘等细分领域模型，以及 DeepSeek（仅北京地域）等第三方模型。

## 快速开始

### 1. 账号准备

1. 注册阿里云账号并完成实名认证
2. 前往百炼控制台开通服务（自动开通，无需额外费用）
3. 创建 [API Key](../concepts/api-key.md)
4. 获取[业务空间](../concepts/workspace.md) ID（使用北京、新加坡、东京、法兰克福地域时需要）

### 2. 配置环境变量

将 [API Key](../concepts/api-key.md) 配置到 `DASHSCOPE_API_KEY` 环境变量，避免硬编码泄露风险：

```bash
# macOS/Linux
export DASHSCOPE_API_KEY="YOUR_DASHSCOPE_API_KEY"

# 永久生效（zsh）
echo 'export DASHSCOPE_API_KEY="YOUR_DASHSCOPE_API_KEY"' >> ~/.zshrc
source ~/.zshrc
```

### 3. 发起第一次调用

使用 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)（Python）：

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen3.7-plus",
    messages=[{'role': 'user', 'content': '你是谁？'}]
)
print(completion.choices[0].message.content)
```

完整的环境配置与多语言示例参见[首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)。

## 地域与接入域名

百炼在多个地域提供服务，每个地域有独立的接入域名、API Key 和模型列表，不能跨地域混用。详细信息参见[选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)。

| 地域 | 地域 ID | 服务部署范围 | 推荐场景 |
|------|--------|------------|---------|
| 华北2（北京） | cn-beijing | 中国内地 | 数据不出中国内地 |
| 新加坡 | ap-southeast-1 | 国际（除中国内地外） | 数据不经过中国内地 |
| 美国（弗吉尼亚） | us-east-1 | 全球 / 美国 | 无驻留限制或限美国境内 |
| 德国（法兰克福） | eu-central-1 | 全球 / 欧盟 | 无驻留限制或限欧盟境内 |
| 日本（东京） | ap-northeast-1 | 全球 / 日本 | 无驻留限制或限日本境内 |

### 接入域名类型

百炼提供三种接入域名（详见[Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)）：

- **[业务空间](../concepts/workspace.md)专属域名**（推荐）：`{WorkspaceId}.{region}.maas.aliyuncs.com`，生产环境使用，高并发、低延迟、SLA 99.9%、请求超时 3600 秒
- **Dashscope 域名**：`dashscope.aliyuncs.com`，存量兼容，建议迁移至专属域名
- **试用域名**：`trial.{region}.maas.aliyuncs.com`，快速验证用，RPM 限制为 1000

> **注意**：Base URL 必须与同一[计费](../concepts/billing.md)方案的 API Key 配套使用，否则会报错 401。Coding Plan 和 [Token](../concepts/token.md) Plan 有各自专属的 Base URL 和 API Key，不能混用。

## 限流

百炼按主账号维度对模型调用设置限流（RPM 和 TPM），超出限制时请求被拒绝，通常一分钟内恢复。详见[限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)。

主要模型的限流额度（北京地域）：

| 模型 | RPM | TPM |
|------|-----|-----|
| qwen3.7-max | 30,000 | 5,000,000 |
| qwen3.7-plus | 30,000 | 5,000,000 |
| qwen3.6-flash | 30,000 | 10,000,000 |

避免限流的策略：
1. 优先使用稳定版模型（限流更宽松）
2. 平滑请求速率，避免瞬时高峰
3. 添加备选模型做 fallback
4. 无实时需求时使用 Batch API（不受限流限制）
5. 在控制台申请临时提额（立即生效，有效期 30 天）

## [计费](../concepts/billing.md)

开通百炼无费用，调用模型按量付费。新用户可获得北京地域免费额度。

控制费用的关键措施：
- 删除不用的 API Key 从源头阻断调用
- 开启「免费额度用完即停」避免意外扣费
- 设置高额消费预警
- 订阅 Coding Plan（固定月费，月度请求额度）

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)


