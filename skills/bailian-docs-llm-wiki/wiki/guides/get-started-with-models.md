# get started with models

阿里云百炼是一站式大模型开发与应用平台，提供兼容 OpenAI 的 API，集成千问（Qwen）全系列模型及 DeepSeek、Kimi、GLM 等第三方大模型。开发者只需几行代码即可完成模型调用，平台覆盖文本生成、视觉理解、图像/视频生成、语音识别与合成、向量嵌入等多种能力。本文汇总从账号开通到首次 API 调用的完整流程，以及地域选择、接入域名和限流等关键配置。

## 支持的模型

百炼提供开箱即用的模型服务，无需自行部署或运维，详见[选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。主要模型分类如下：

### 文本生成

- **千问旗舰模型**：qwen3.7-max（效果最强，适合复杂多步骤任务）、qwen3.7-plus（效果与成本均衡，多数场景推荐）、qwen3.6-flash（高性价比低延迟）。
- **第三方模型**：deepseek-v4-pro、deepseek-v4-flash、kimi-k2.7-code、glm-5.2、MiniMax-M2.7 等，API 格式与千问模型一致。

### [多模态](../concepts/multimodal.md)与其他能力

| 能力类别 | 代表模型 |
|---------|---------|
| 图像/视频理解 | qwen3.7-plus、qwen3.5-omni-plus |
| 图像/视频生成 | wan2.7-image-pro、qwen-image-2.0-pro、happyhorse-1.1-t2v |
| 3D 模型生成 | Tripo/Tripo-H3.1、Tripo/Tripo-P1.0 |
| 语音合成（TTS） | cosyvoice-v3.5-plus、MiniMax/speech-2.8-hd |
| 语音识别（ASR） | fun-asr-realtime、fun-asr |
| 语音转语音（S2S） | qwen3.5-omni-plus-realtime |
| 全模态 | qwen3.5-omni-plus-realtime |
| 向量与重排序 | text-embedding-v4、qwen3-rerank |
| 音乐生成 | fun-music-v1 |

## 首次 API 调用

完成以下准备步骤后即可发起第一个请求，详细指引见[首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)。

### 1. 账号设置

1. 注册阿里云账号并完成实名认证。
2. 使用主账号前往百炼控制台，阅读并同意协议即可开通服务。
3. 在 [API Key](../concepts/api-key.md) 页面创建 [API Key](../concepts/api-key.md)。
4. 如使用华北2（北京）、新加坡、日本（东京）或德国（法兰克福）地域，需在 Base URL 中填入[业务空间](../concepts/workspace.md) ID（WorkspaceId）。

### 2. 配置 [API Key](../concepts/api-key.md) 环境变量

建议将 API Key 配置到环境变量 `DASHSCOPE_API_KEY`，避免代码中硬编码：

```bash
# Linux / macOS (Zsh)
echo "export DASHSCOPE_API_KEY='YOUR_DASHSCOPE_API_KEY'" >> ~/.zshrc
source ~/.zshrc

# Windows (PowerShell)
[Environment]::SetEnvironmentVariable("DASHSCOPE_API_KEY", "YOUR_DASHSCOPE_API_KEY", [EnvironmentVariableTarget]::User)
```

### 3. 发起请求（Python 示例）

安装 SDK 后即可调用：

```bash
pip install -U openai
```

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 华北2（北京）业务空间专属域名，将 {WorkspaceId} 替换为真实 ID
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': '你是谁？'}
    ]
)
print(completion.choices[0].message.content)
```

百炼同时支持 DashScope Python SDK、Node.js SDK 和 curl 调用。

## 地域与接入域名

调用前需选择地域和接入域名，各地域的 API Key 相互独立、不能跨地域混用。详见[选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)。

### 可用地域

| 地域 | 地域 ID | 服务部署范围 | 典型场景 |
|------|---------|------------|---------|
| 华北2（北京） | cn-beijing | 中国内地 | 数据不出中国内地 |
| 新加坡 | ap-southeast-1 | 国际（除中国内地） | 数据不经过中国内地 |
| 美国（弗吉尼亚） | us-east-1 | 全球 / 美国 | 无合规限制或限美国 |
| 德国（法兰克福） | eu-central-1 | 全球 / 欧盟 | 无合规限制或限欧盟 |
| 日本（东京） | ap-northeast-1 | 全球 / 日本 | 无合规限制或限日本 |

### 接入域名类型

百炼提供三种接入域名，详见[Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)：

| 域名类型 | 格式 | 适用场景 | 请求超时 | SLA |
|---------|------|---------|---------|-----|
| **[业务空间](../concepts/workspace.md)专属（推荐）** | `{WorkspaceId}.{region}.maas.aliyuncs.com` | 生产环境 | 3600s | 99.9% |
| Dashscope | `dashscope.aliyuncs.com` | 存量兼容 | 600s | 99.9% |
| 试用 | `trial.{region}.maas.aliyuncs.com` | 快速验证 | 600s | 不提供 |

此外，Coding Plan 和 [Token](../concepts/token.md) Plan 有各自的专属域名和 API Key，仅限 AI 编码工具交互式使用，不能用于后端服务。

> **注意**：美国（弗吉尼亚）地域目前不支持[业务空间](../concepts/workspace.md)专属域名，仅能使用 Dashscope 域名 `dashscope-us.aliyuncs.com`。德国（法兰克福）和日本（东京）地域不支持 Dashscope 域名和试用域名，仅支持业务空间专属域名。

## 限流

百炼按主账号维度对模型调用设置限流，账号下所有 RAM 子账号、业务空间和 API Key 的调用量合并计算。详见[限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)。

### 限流指标

- **RPM**（每分钟请求数）和 **TPM**（每分钟 [Token](../concepts/token.md) 数，含输入与输出），超出任一即触发限流。
- 限流还可能按秒级 RPS（RPM/60）与 TPS（TPM/60）执行，短时间爆发请求即使未达分钟级上限也可能被限流。

### 主要模型限流额度（华北2-北京，稳定版）

| 模型 | RPM | TPM |
|------|-----|-----|
| qwen3.7-max | 30,000 | 5,000,000 |
| qwen3.7-plus | 30,000 | 5,000,000 |
| qwen3.6-flash | 30,000 | 10,000,000 |
| qwen-plus | 30,000 | 5,000,000 |
| qwen-turbo | 1,200 | 5,000,000 |

> **注意**：带日期后缀的快照版本（如 qwen3.7-max-2026-06-08）限流额度通常远低于稳定版，使用前请确认。

### 避免限流的建议

1. 优先使用稳定版模型（限流额度更高）。
2. 平滑请求速率，采用匀速调度或指数退避，避免瞬时高峰。
3. 配置备选模型：主模型限流时自动切换到备用模型。
4. 将大批量任务拆分为小批次分时段提交。
5. 无需实时响应时，使用批量推理（Batch API），不受实时限流约束。
6. 默认额度不足时，在控制台「限流提额」页面提升临时 TPM 额度，提交后立即生效，有效期 30 天。

## 费用与成本控制

- 开通百炼免费，调用模型按量付费。新用户享有北京地域的免费额度。
- 可开启「免费额度用完即停」功能，避免超出免费额度后产生费用。
- 通过删除 API Key、停止调用、下线部署实例等方式阻断计费。
- 在费用中心设置高额消费预警，及时发现异常消费。
- Coding Plan（AI 编码套餐）采用固定月费，提供月度请求额度，无按量扣费风险。

## 各地域功能差异

| 功能 | 北京 | 新加坡 | 美国 | 德国 | 日本 |
|------|------|-------|------|------|------|
| 实时推理 | 支持 | 支持 | 支持 | 支持 | 支持 |
| 批量推理 | 支持 | 支持 | 不支持 | 不支持 | 不支持 |
| 模型调优 | 支持 | 不支持 | 不支持 | 不支持 | 不支持 |
| 应用开发 | 支持 | 不支持 | 不支持 | 不支持 | 不支持 |

> **注意**：模型调优和应用开发（智能体、工作流等）目前仅在华北2（北京）地域可用。如需这些功能，请选择北京地域。

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)


