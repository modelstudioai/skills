# get started with models

阿里云百炼是一站式大模型开发与应用平台，提供兼容 OpenAI 的 API 接口，集成千问（Qwen）全系列及 DeepSeek、Kimi、GLM 等第三方模型。开发者只需获取 API Key 并配置 Base URL，即可通过几行代码完成大模型调用。本页面汇总从账号准备到发出第一个请求所需的关键信息。

## 平台能力概览

百炼面向开发者提供以下核心能力（详见[什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)）：

- **模型调用**：通过 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)、[DashScope SDK](../concepts/dashscope-sdk.md) 或 curl 直接调用大模型，支持文本生成、视觉理解、图像/视频生成、语音识别与合成、向量嵌入等多种模态。
- **应用构建**：可视化方式创建智能体应用、工作流应用；高代码模式支持部署 Python 后端服务。
- **模型调优与部署**：支持有监督微调（SFT）、继续预训练（CPT）、直接偏好优化（DPO），以及将模型部署为资源专享的推理服务。
- **知识库与插件**：通过 RAG 知识库接入私有数据，通过插件和 MCP 协议调用外部服务。

## 可用模型

百炼模型广场覆盖多种模态和场景（详见[选择模型](../../raw/model-user-guide/get-started-with-models/models.md)）：

| 类别 | 代表模型 |
|------|----------|
| 文本生成（千问） | qwen3.7-max、qwen3.7-plus、qwen3.6-flash |
| 文本生成（第三方） | deepseek-v4-pro、deepseek-v4-flash、kimi-k2.7-code、glm-5.2、MiniMax-M2.7 |
| 图像与视频理解 | qwen3.7-plus、qwen3.5-omni-plus |
| 图像与视频生成 | wan2.7-image-pro、qwen-image-2.0-pro、happyhorse-1.0-t2v |
| 语音合成/识别 | cosyvoice-v3.5-plus、fun-asr、fun-asr-realtime |
| 全模态 | qwen3.5-omni-plus-realtime |
| 向量与重排序 | text-embedding-v4、qwen3-rerank |
| 3D 模型生成 | Tripo-H3.1、Tripo-P1.0 |

千问旗舰模型的选型建议：

- **qwen3.7-max**：效果最强，适合复杂、多步骤任务。
- **qwen3.7-plus**：效果、速度和成本均衡，多数场景的推荐选择。
- **qwen3.6-flash**：高性价比、低延迟，适合简单任务的快速响应。

## 快速开始

### 1. 账号准备

1. 注册阿里云账号并完成实名认证。
2. 使用主账号访问百炼控制台，阅读并同意服务协议即可开通。
3. 在 API Key 管理页面创建 API Key。
4. 如使用华北2（北京）、新加坡、日本（东京）或德国（法兰克福）地域，还需获取业务空间 ID（WorkspaceId）填入 Base URL。

### 2. 配置环境变量

建议将 API Key 配置到环境变量 `DASHSCOPE_API_KEY`，避免在代码中硬编码（详见[首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)）：

```bash
# Linux / macOS
export DASHSCOPE_API_KEY="YOUR_DASHSCOPE_API_KEY"

# Windows CMD
set DASHSCOPE_API_KEY=YOUR_DASHSCOPE_API_KEY

# Windows PowerShell
$env:DASHSCOPE_API_KEY = "YOUR_DASHSCOPE_API_KEY"
```

### 3. 发送第一个请求

百炼兼容 OpenAI 接口规范，只需调整 `api_key`、`base_url` 和模型名称即可迁移现有 OpenAI 代码。

**Python（OpenAI SDK）：**

```python
import os
from openai import OpenAI

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

**Node.js：**

```javascript
import OpenAI from "openai";

const openai = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
});

const completion = await openai.chat.completions.create({
    model: "qwen3.7-plus",
    messages: [{ role: "user", content: "你是谁？" }],
});
console.log(completion.choices[0].message.content);
```

> **注意**：代码中的 `{WorkspaceId}` 需替换为真实的业务空间 ID。美国（弗吉尼亚）地域的 Base URL 格式不同，为 `https://dashscope-us.aliyuncs.com/compatible-mode/v1`，不需要 WorkspaceId。

## 地域与服务部署范围

百炼在多个地域提供服务，每个地域有独立的 Base URL、API Key 和模型列表，不能跨地域混用（详见[选择地域和服务部署范围](../../raw/model-user-guide/get-started-with-models/regions.md)）：

| 地域 | Base URL（OpenAI 兼容） | 适用场景 |
|------|-------------------------|----------|
| 华北2（北京） | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | 数据不出中国内地 |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` | 数据不经过中国内地 |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` | 全球推理或限定美国境内 |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1` | 全球推理或限定欧盟境内 |
| 日本（东京） | `https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/compatible-mode/v1` | 全球推理或限定日本境内 |

关键差异：

- 北京地域模型最全，支持模型调优、批量推理、模型告警等完整功能。
- 弗吉尼亚地域使用 `-us` 后缀的模型名称（如 `qwen-plus-us`）可限定美国境内推理，不带后缀则使用全球推理。
- 法兰克福和东京通过业务空间区分部署范围（全球 / 区域内），不同空间的 API Key 相互隔离。

## 限流与配额

百炼按主账号维度设置限流，所有 RAM 子账号、业务空间和 API Key 的调用量合并计算（详见[限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)）。

主要限流指标：

- **RPM**（每分钟请求数）：如 qwen3.7-plus 为 30,000 RPM。
- **TPM**（每分钟 Token 消耗）：如 qwen3.7-plus 为 5,000,000 TPM。

> **注意**：即使每分钟总调用量未超限，短时间内的请求爆发也可能触发秒级限流（RPS = RPM/60）。

应对限流的策略：

1. 优先选用稳定版模型（限流额度更宽松）。
2. 添加备选模型，触发限流后自动切换。
3. 采用匀速调度或指数退避平滑请求速率。
4. 将大批量任务拆分为小批次，或使用批量推理（Batch API）。
5. 在百炼控制台的"限流提额"页面提升临时 TPM 额度（提交后立即生效，有效期 30 天）。

## 计费说明

开通百炼无需费用，调用模型时按量付费。新用户可获得北京地域的免费额度用于体验。

- 未认证用户免费额度用完后需完成认证并充值。
- 已认证用户可开启"免费额度用完即停"，避免意外扣费。
- 可通过删除 API Key、停止调用、下线部署实例等方式控制费用。
- Coding Plan（AI 编码套餐）提供固定月费模式，适合 AI 编码工具的使用场景。

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [选择地域和服务部署范围](../../raw/model-user-guide/get-started-with-models/regions.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)


