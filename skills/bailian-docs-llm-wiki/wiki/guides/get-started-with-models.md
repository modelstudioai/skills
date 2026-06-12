# get started with models

阿里云百炼是一站式大模型开发与应用平台，提供兼容 OpenAI 的 API 接口，集成千问（Qwen）全系列及 DeepSeek、Kimi、GLM 等第三方模型。开发者只需几行代码即可完成模型调用，平台还提供可视化应用构建、模型微调和部署等全链路服务。

## 平台概览

百炼的核心能力包括 API 调用、智能体构建、工作流编排和模型微调。平台兼容 OpenAI 接口规范，只需调整 API Key、`base_url` 和模型名称即可将现有 OpenAI 代码迁移至百炼。详细的平台能力介绍请参见 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。

## 快速开始

### 1. 账号准备

1. 注册阿里云账号并完成实名认证
2. 前往百炼控制台开通服务（阅读并同意协议后自动开通）
3. 在 API Key 页面创建 API Key
4. 如使用新加坡或德国（法兰克福）地域，还需获取[业务空间](../concepts/workspace.md) ID（WorkspaceId）

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

建议将其写入 `~/.bashrc`、`~/.zshrc` 或系统环境变量以永久生效。

### 3. 发起第一个 API 请求

安装 OpenAI SDK 后即可调用千问模型。完整的环境配置和调用步骤请参见 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)。

**Python 示例：**

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen3.7-plus",
    messages=[{'role': 'user', 'content': '你是谁？'}]
)
print(completion.choices[0].message.content)
```

百炼同时支持 DashScope SDK 和 curl 调用方式。

## 模型选择

百炼提供覆盖文本、图像、音频、视频、3D 等多种模态的模型服务，详见 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。

### 千问文本模型（按能力分级）

| 模型 | 定位 | 适用场景 |
|------|------|----------|
| qwen3.7-max | 旗舰级，效果最强 | 复杂、多步骤推理任务 |
| qwen3.7-plus | 均衡型 | 多数场景的推荐选择 |
| qwen3.6-flash | 高性价比、低延迟 | 需要快速响应的简单任务 |

### 第三方模型

API 格式与千问一致，包括 deepseek-v4-pro、deepseek-v4-flash、kimi-k2.6、glm-5.1 等。

### 其他模态

- **视觉理解与生成**：图像分析、文生图、视频生成（wan2.7-image-pro、happyhorse 系列）
- **语音**：语音合成（cosyvoice-v3.5-plus）、语音识别（fun-asr）、语音转语音
- **全模态**：qwen3.5-omni-plus 支持文本、图像、音频、视频的统一理解与生成
- **向量与重排序**：text-embedding-v4、qwen3-rerank

## 地域与接入点

百炼在多个地域提供服务，每个地域有独立的 Base URL 和 API Key，**不能跨地域混用**。详见 [选择地域和服务部署范围](../../raw/model-user-guide/get-started-with-models/regions.md)。

| 地域 | OpenAI 兼容 Base URL | 说明 |
|------|---------------------|------|
| 华北2（北京） | `https://dashscope.aliyuncs.com/compatible-mode/v1` | 支持功能最全（含模型调优、批量推理） |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` | 使用 `-us` 后缀模型名可限定美国境内推理 |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` | 需替换 WorkspaceId |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1` | 通过[业务空间](../concepts/workspace.md)区分全球/欧盟部署范围 |

地域选择要点：
- **无数据驻留限制**：选择美国或德国 + 全球部署范围，推理资源池更大
- **数据不出中国内地**：选择华北2（北京）+ 中国内地部署范围
- **数据不经过中国内地**：选择新加坡 + 国际部署范围

## 限流机制

百炼按主账号维度对模型调用设置限流，所有 RAM 子账号、[业务空间](../concepts/workspace.md)和 API Key 的调用量合并计算。详见 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)。

### 主要限流指标

- **RPM**（每分钟请求数）：如 qwen3.7-plus 北京地域为 30,000 RPM
- **TPM**（每分钟 Token 数）：如 qwen3.7-plus 北京地域为 5,000,000 TPM

稳定版/最新版模型的限流额度通常远高于带日期的快照版本。

### 应对限流策略

1. 优先选用高限流额度的稳定版模型（如 qwen-plus）
2. 平滑请求速率，避免瞬时高峰
3. 添加备选模型，主模型限流时自动切换
4. 无实时需求时使用批量推理（Batch API），不受限流约束
5. 在控制台「限流提额」页面提升临时 TPM 额度（提交后立即生效，有效期 30 天）

> **注意**：即使每分钟总调用量未超限，短时间内的请求爆发也可能触发秒级 RPS/TPS 限流。

## 计费概要

- 开通百炼免费，调用模型按量计费
- 新用户可获得北京地域专属免费额度
- 可开启「免费额度用完即停」避免意外扣费
- 订阅 Coding Plan 可获得固定月费的请求额度（需使用专属 Base URL 和 API Key）

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [选择地域和服务部署范围](../../raw/model-user-guide/get-started-with-models/regions.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)


