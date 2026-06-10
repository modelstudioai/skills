# get started with models

阿里云百炼提供兼容 OpenAI 的 API 接口，开发者只需几行代码即可调用千问（Qwen）全系列及 DeepSeek、Kimi 等第三方大模型。本文汇总从账号注册、API Key 获取、地域选择到限流应对的完整上手流程，帮助开发者快速接入模型服务。

## 平台概览

百炼是一站式大模型开发与应用平台，核心能力包括：

- **模型调用**：通过 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)调用文本生成、视觉理解、图像/视频生成、语音识别与合成、向量嵌入等多种模态模型。
- **应用构建**：可视化创建智能体、工作流应用，或通过高代码模式部署 Python 后端服务。
- **模型调优与部署**：支持 SFT、CPT、DPO 微调，以及资源专享的推理服务部署。

详细的平台能力介绍参见 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。

## 快速开始

### 1. 账号准备

1. 注册阿里云账号并完成实名认证。
2. 使用主账号访问百炼控制台，阅读并同意服务协议即可开通。
3. 前往 API Key 管理页面创建 API Key。

### 2. 配置环境变量

将 API Key 配置到环境变量 `DASHSCOPE_API_KEY`，避免在代码中硬编码：

```bash
# macOS / Linux
export DASHSCOPE_API_KEY="your-api-key"

# Windows PowerShell
$env:DASHSCOPE_API_KEY = "your-api-key"
```

建议写入 `~/.zshrc`（macOS）或 `~/.bashrc`（Linux）以永久生效。完整的多平台配置步骤参见 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)。

### 3. 发起第一个请求

百炼兼容 OpenAI 接口，只需替换 `api_key`、`base_url` 和模型名称：

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen3.7-plus",
    messages=[{"role": "user", "content": "你是谁？"}]
)
print(completion.choices[0].message.content)
```

也支持 Node.js（OpenAI SDK）、curl 以及 DashScope SDK 调用。

## 模型选择

百炼提供丰富的模型矩阵，按场景选择：

| 定位 | 推荐模型 | 适用场景 |
|------|----------|----------|
| 旗舰 | qwen3.7-max | 复杂多步骤任务，推理能力最强 |
| 均衡 | qwen3.7-plus | 效果、速度、成本均衡，多数场景推荐 |
| 高性价比 | qwen3.6-flash | 快速响应的简单任务，低延迟 |
| 第三方 | deepseek-v4-pro、kimi-k2.6、glm-5.1 等 | API 格式与千问一致，按需选用 |

除文本生成外，还覆盖：

- **视觉理解与生成**：qwen3.7-plus（视觉）、wan2.7-image-pro（图像生成）、happyhorse 系列（视频生成/编辑）
- **语音**：cosyvoice-v3.5-plus（TTS）、fun-asr（ASR）
- **全模态**：qwen3.5-omni-plus（文本+图像+音频+视频的理解与生成）
- **向量与重排序**：text-embedding-v4、qwen3-rerank

完整模型列表参见 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。

## 地域与接入点

百炼在四个地域提供服务，每个地域有独立的 Base URL 和 API Key，**不能跨地域混用**。

| 地域 | Base URL（OpenAI 兼容） | 适用场景 |
|------|------------------------|----------|
| 华北2（北京） | `https://dashscope.aliyuncs.com/compatible-mode/v1` | 数据不出中国内地 |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` | 全球推理或限定美国推理 |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` | 数据不经过中国内地 |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1` | 全球推理或限定欧盟推理 |

关键概念：

- **地域**决定接入点和数据存储位置，就近选择可降低延迟。
- **服务部署范围**决定推理执行位置。例如美国地域可选"全球"（更大资源池）或"美国"（数据不出境），使用 `-us` 后缀的模型名称可限定美国境内推理。
- 新加坡和法兰克福地域的 Base URL 需要填入[业务空间](../concepts/workspace.md) ID（WorkspaceId）。

详细的地域对比和功能支持矩阵参见 [选择地域和服务部署范围](../../raw/model-user-guide/get-started-with-models/regions.md)。

> **注意**：新加坡地域的旧版域名 `https://dashscope-intl.aliyuncs.com` 即将下线，请迁移到新版域名。

## 限流与应对策略

百炼按主账号维度限流，账号下所有 RAM 子账号、[业务空间](../concepts/workspace.md)和 API Key 的调用量合并计算。不同模型的限流额度相互独立。

### 限流指标

- **RPM**（每分钟请求数）：超出时返回 `Requests rate limit exceeded`。
- **TPM**（每分钟 Token 数，含输入与输出）：超出时返回 `Allocated quota exceeded`。
- 系统还可能按秒级 RPS/TPS 执行，短时间请求爆发即使总量未超限也可能触发。

### 主流模型限流参考（北京地域）

| 模型 | RPM | TPM |
|------|-----|-----|
| qwen3.7-max | 30,000 | 5,000,000 |
| qwen3.7-plus | 30,000 | 5,000,000 |
| qwen3.6-flash | 30,000 | 10,000,000 |
| qwen-plus | 30,000 | 5,000,000 |

稳定版（不带日期后缀）比快照版本限流额度更宽松。

### 应对措施

1. **优先选用高限流模型**：如 qwen-plus、qwen3.7-plus 等稳定版。
2. **平滑请求速率**：采用匀速调度或指数退避，避免瞬时高峰。
3. **添加备选模型**：主用模型触发限流时自动切换到备用模型。
4. **批量推理**：无实时要求时使用 Batch API，不受实时限流约束。
5. **临时提额**：在百炼控制台的"限流提额"页面提升 TPM 额度，提交后立即生效，有效期 30 天。

详细的限流规则与各地域模型限流表参见 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)。

## 计费要点

- 开通百炼免费，调用模型按量付费（按分钟出账）。
- 新用户可获得北京地域的免费额度用于体验。
- 可开启"免费额度用完即停"功能防止意外扣费。
- Coding Plan（AI 编码套餐）提供固定月费的请求额度，需使用专属 Base URL 和 API Key。

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [选择地域和服务部署范围](../../raw/model-user-guide/get-started-with-models/regions.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)


