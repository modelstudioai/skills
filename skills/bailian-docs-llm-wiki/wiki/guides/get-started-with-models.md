# get started with models

阿里云百炼提供开箱即用的大模型服务，兼容 OpenAI 接口规范，覆盖文本生成、视觉理解、图像/视频生成、语音、嵌入等多种模态。开发者只需获取 [API Key](../concepts/api-key.md)、选择地域和模型，即可通过几行代码完成首次调用。本文汇总了从账号开通到生产接入所需的核心信息。

## 平台概览

百炼是一站式大模型开发与应用平台，集成自研千问（Qwen）全系列及 DeepSeek、Kimi、GLM 等第三方模型。面向开发者提供兼容 OpenAI 的 API 和全链路模型服务（调优、部署、评测）；面向业务人员提供可视化智能体和工作流构建能力。详见[什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。

## 可用模型

百炼按能力和成本分为三档核心文本模型，并提供丰富的[多模态](../concepts/multimodal.md)和领域模型。完整列表见[选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。

### 文本生成（千问系列）

| 模型 | 定位 | 适用场景 |
|------|------|----------|
| qwen3.7-max | 效果最强 | 复杂、多步骤推理任务 |
| qwen3.7-plus | 效果/速度/成本均衡 | 多数生产场景（推荐） |
| qwen3.6-flash | 高性价比、低延迟 | 简单任务、快速响应 |

### 第三方模型

deepseek-v4-pro、deepseek-v4-flash、kimi-k2.7-code、glm-5.2、MiniMax-M2.7 等，API 格式与千问一致。

### [多模态](../concepts/multimodal.md)与领域模型

- **视觉理解**：qwen3.7-plus、qwen3.5-omni-plus
- **图像生成**：wan2.7-image-pro、qwen-image-2.0-pro
- **视频生成**：happyhorse-1.1-t2v / i2v / r2v
- **3D 生成**：Tripo-H3.1、Tripo-P1.0
- **语音识别/合成**：qwen3.5-omni-plus、cosyvoice-v2 等
- **Embedding/Rerank**：text-embedding-v4、qwen3-rerank

## 首次调用

完整步骤见[首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)，核心流程如下：

### 1. 账号准备

1. 注册阿里云账号并完成实名认证。
2. 用主账号访问百炼控制台，阅读并同意协议即可开通。
3. 在 [API Key](../concepts/api-key.md) 页面创建 Key。
4. 使用北京、新加坡、东京、法兰克福地域时，还需在[业务空间](../concepts/workspace.md)管理页面获取 WorkspaceId。

### 2. 配置 [API Key](../concepts/api-key.md)

建议将 API Key 配置到环境变量 `DASHSCOPE_API_KEY`，避免硬编码泄露：

```bash
# Linux / macOS (Zsh)
echo 'export DASHSCOPE_API_KEY="sk-xxx"' >> ~/.zshrc && source ~/.zshrc
```

```powershell
# Windows PowerShell
[Environment]::SetEnvironmentVariable("DASHSCOPE_API_KEY", "sk-xxx", "User")
```

### 3. 发起请求

百炼兼容 OpenAI SDK，迁移成本极低：

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen3.7-plus",
    messages=[{"role": "user", "content": "你是谁？"}]
)
print(completion.choices[0].message.content)
```

也支持 DashScope SDK 和 curl 调用，详见原文。

## 地域与接入域名

百炼在 5 个地域提供服务，地域决定数据存储位置和接入点，服务部署范围决定推理执行位置。详见[选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)。

| 地域 | 服务部署范围 | 特点 |
|------|-------------|------|
| 华北2（北京） | 中国内地 | 功能最全：支持应用开发、模型调优、批量推理 |
| 新加坡 | 国际 | 支持批量推理，不支持调优和应用开发 |
| 美国（弗吉尼亚） | 全球/美国 | 用 `-us` 后缀模型名限定美国境内推理 |
| 德国（法兰克福） | 全球/欧盟 | 通过[业务空间](../concepts/workspace.md)选择部署范围 |
| 日本（东京） | 全球/日本 | 通过[业务空间](../concepts/workspace.md)选择部署范围 |

> **注意**：各地域的 API Key 相互独立、不能跨地域使用。Base URL 必须与同一地域的 API Key 配套，否则会报 401 错误。

## Base URL 选择

百炼提供三类按量付费域名和两类套餐域名，详见[Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)。

| 域名类型 | 格式示例（北京，OpenAI 兼容） | 说明 |
|----------|-------------------------------|------|
| 业务空间专属域名（推荐） | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | 更高吞吐、更低时延、业务空间级隔离 |
| Dashscope 域名 | `https://dashscope.aliyuncs.com/compatible-mode/v1` | 中心化共享域名，建议迁移到专属域名 |
| 试用域名 | `https://trial.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | 限流值较小，适合临时测试 |
| [Token](../concepts/token.md) Plan 专属 | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | 仅限 Claude Code 等 AI 工具交互式使用 |
| Coding Plan 专属 | `https://coding-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | 固定月费套餐，仅限 AI 工具交互式使用 |

百炼同时支持 Anthropic 兼容接口，将路径中 `/compatible-mode/v1` 替换为 `/apps/anthropic` 即可。

## 限流

百炼按主账号维度对模型调用设置 RPM（每分钟请求数）和 TPM（每分钟 [Token](../concepts/token.md) 数）限流，账号下所有 RAM 子账号、业务空间和 API Key 的调用量合并计算。详见[限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)。

### 主要模型限流参考（北京/中国内地）

| 模型 | RPM | TPM |
|------|-----|-----|
| qwen3.7-max | 30,000 | 5,000,000 |
| qwen3.7-plus | 30,000 | 5,000,000 |
| qwen3.6-flash | 30,000 | 10,000,000 |
| qwen-plus | 30,000 | 5,000,000 |
| qwq-plus | 600 | 1,000,000 |

> **注意**：限流策略可能按秒级 RPS（RPM/60）和 TPS（TPM/60）执行，即使每分钟总量未超限，瞬时高峰也可能触发限流。稳定版/最新版比带日期的快照版本限流更宽松。

### 应对限流的建议

1. **选用高限流模型**：优先使用 qwen-plus 等限流额度更高的稳定版模型。
2. **平滑请求速率**：采用匀速调度或指数退避，避免瞬时请求爆发。
3. **添加备选模型**：触发限流后自动切换到备用模型继续生成。
4. **使用 Batch API**：批量推理场景不受限流限制。

## 费用控制

百炼按量付费，本身没有自动扣费开关。控制费用的关键措施：

- **删除 API Key** 从源头阻断调用。
- **停止所有调用** 并排查定时任务和后台进程。
- **清理[计费](../concepts/billing.md)资源**：删除不用的知识库，下线按时长[计费](../concepts/billing.md)的部署实例。
- **新用户可开启"免费额度用完即停"**：额度耗尽后服务自动停止，不转为付费（仅限北京地域、免费额度有效期内）。
- **设置费用预警**：在账单详情和模型监控中配置高额消费预警。

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)


