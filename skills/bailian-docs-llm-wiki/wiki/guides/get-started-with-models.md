# get started with models

阿里云百炼是一站式大模型开发与应用平台，提供开箱即用的模型服务，兼容 OpenAI 接口规范。开发者只需获取 API Key 并配置 Base URL，即可快速调用千问（Qwen）全系列及 DeepSeek、Kimi、GLM 等第三方模型，覆盖文本、图像、音频、视频等多种模态。

## 平台概述

百炼面向开发者提供兼容 OpenAI 的 API 和全链路模型服务，面向业务人员提供可视化应用构建能力。主要能力包括 API 调用、智能体应用构建、工作流编排和模型微调。平台还支持模型调优（SFT/CPT/DPO）、[模型部署](../concepts/model-deployment.md)和模型评测等服务。详见[什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。

## 可用模型

百炼覆盖文本、图像、音频、视频、3D 等多种模态，完整列表参见[选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。

### 千问（Qwen）系列

| 模型层级 | 代表模型 | 适用场景 |
|---------|---------|---------|
| Max | qwen3.7-max | 效果最好，适合复杂、多步骤任务 |
| Plus | qwen3.7-plus | 效果、速度和成本均衡，多数场景推荐 |
| Flash | qwen3.6-flash | 高性价比、低延迟，适合快速响应的简单任务 |

### 第三方模型

API 格式与千问模型一致，包括 deepseek-v4-pro、deepseek-v4-flash、kimi-k2.6、glm-5.1、MiniMax-M2.7 等。

### 多模态覆盖

- **视觉理解**：qwen3.7-plus、qwen3.5-omni-plus、kimi-k2.6
- **图像/视频生成**：wan2.7-image-pro、qwen-image-2.0-pro、happyhorse 系列
- **语音合成（TTS）**：cosyvoice-v3.5-plus、MiniMax/speech-2.8-hd
- **语音识别（ASR）**：fun-asr-realtime、fun-asr、qwen3.5-omni-plus
- **语音转语音**：qwen3.5-omni-plus-realtime（端到端语音对话）
- **全模态**：qwen3.5-omni-plus 融合文本、图像、音频、视频的理解与生成
- **向量与重排序**：text-embedding-v4、tongyi-embedding-vision-plus、qwen3-rerank
- **3D 模型生成**：Tripo-H3.1、Tripo-P1.0
- **音乐生成**：fun-music-v1

## 快速开始：首次 API 调用

完成以下步骤即可发起第一个 API 请求，详细流程参见[首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)。

### 1. 账号准备

1. 注册阿里云账号并完成实名认证
2. 使用主账号前往百炼控制台，开通服务
3. 在 API Key 页面创建 API Key
4. 若使用新加坡或德国（法兰克福）地域，还需获取[业务空间](../concepts/workspace.md) ID（WorkspaceId）

### 2. 配置环境变量

将 API Key 配置到环境变量 `DASHSCOPE_API_KEY`，避免在代码中硬编码：

```bash
# Linux / macOS
export DASHSCOPE_API_KEY="YOUR_DASHSCOPE_API_KEY"

# Windows CMD
set DASHSCOPE_API_KEY=YOUR_DASHSCOPE_API_KEY

# Windows PowerShell
$env:DASHSCOPE_API_KEY = "YOUR_DASHSCOPE_API_KEY"
```

### 3. 发送请求

百炼兼容 OpenAI 接口规范，只需调整 `api_key`、`base_url` 和模型名称即可迁移现有代码。

**Python**（需先 `pip install -U openai`）：

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen-plus",
    messages=[{'role': 'user', 'content': '你是谁？'}]
)
print(completion.choices[0].message.content)
```

**Node.js**（需先 `npm install openai`）：

```javascript
import OpenAI from "openai";

const openai = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
});

const completion = await openai.chat.completions.create({
    model: "qwen-plus",
    messages: [{ role: "user", content: "你是谁？" }],
});
console.log(completion.choices[0].message.content);
```

除 OpenAI SDK 外，百炼也支持 DashScope SDK 和 curl 调用。

## 选择地域和服务部署范围

调用百炼前需选择**地域**（决定接入点和数据存储位置）和**服务部署范围**（决定推理执行位置）。每个地域有独立的 Base URL、API Key 和模型列表，**不能跨地域混用**。详细说明参见[选择地域和服务部署范围](../../raw/model-user-guide/get-started-with-models/regions.md)。

### 可用地域

| 地域 | Base URL（OpenAI 兼容） | 典型场景 |
|------|------------------------|---------|
| 华北2（北京） | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | 数据不出中国内地 |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` | 数据不经过中国内地 |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` | 追求更大推理资源池或数据不出美国 |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1` | 追求更大推理资源池或数据不出欧盟 |

> **注意**：华北2（北京）和新加坡地域推出了新版域名格式 `{WorkspaceId}.{region}.maas.aliyuncs.com`，旧版域名（`dashscope.aliyuncs.com`、`dashscope-intl.aliyuncs.com`）即将下线，请尽快替换。

### 各地域功能差异

- **模型调优**：仅华北2（北京）支持
- **批量推理**：华北2（北京）和新加坡支持，弗吉尼亚和法兰克福不支持
- **模型告警**：华北2（北京）和新加坡支持
- **美国境内限定推理**：弗吉尼亚地域使用 `-us` 后缀模型名（如 `qwen-plus-us`），不带后缀默认全球推理

## 限流机制

百炼按**主账号维度**对模型调用设置限流，账号下所有 RAM 子账号、[业务空间](../concepts/workspace.md)和 API Key 的调用量合并计算。不同模型限流额度相互独立。详细限流额度参见[限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)。

### 限流指标

- **RPM**（每分钟请求数）：稳定版模型通常为 1,200 - 30,000
- **TPM**（每分钟 Token 消耗）：含输入与输出 Token，稳定版通常为 1,000,000 - 10,000,000

> **注意**：除 RPM/TPM 外，系统可能按秒级 RPS（RPM/60）和 TPS（TPM/60）执行限流。短时间内的请求爆发即使未超分钟级限额也可能触发限流。

### 主要模型限流额度（华北2-北京）

| 模型 | RPM | TPM |
|------|-----|-----|
| qwen3.7-max | 30,000 | 5,000,000 |
| qwen3.7-plus | 30,000 | 5,000,000 |
| qwen3.6-flash | 30,000 | 10,000,000 |
| qwen-plus | 30,000 | 5,000,000 |

快照版本（带日期后缀）的限流额度通常远低于稳定版，优先使用不带日期的稳定版模型。

### 应对限流策略

1. **选用高限流模型**：优先使用稳定版（如 `qwen-plus`），限流额度更高
2. **平滑请求速率**：采用匀速调度、指数退避或请求队列，避免瞬时高峰
3. **配置备选模型**：主模型限流时自动切换到备用模型
4. **使用批量推理**（Batch API）：不受实时限流约束，适合无实时响应需求的场景
5. **提升临时限流额度**：在控制台限流提额页面申请，提交后立即生效，有效期 30 天

## 计费说明

- 开通百炼无需费用，调用模型按量计费
- 新用户可获得北京地域专属的免费额度
- 可开启"免费额度用完即停"功能避免意外扣费
- 已认证用户免费额度用完后自动转为按量付费
- 未认证用户需完成认证并充值后才能继续使用
- 如需固定月费方案，可订阅 Coding Plan（AI 编码套餐），提供月度请求额度
- 模型调用按分钟出账，确保阿里云账户余额充足

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [选择地域和服务部署范围](../../raw/model-user-guide/get-started-with-models/regions.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)



