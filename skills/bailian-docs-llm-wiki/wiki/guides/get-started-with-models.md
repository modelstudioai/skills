# get started with models

阿里云百炼是一站式大模型开发与应用平台，集成千问（Qwen）及主流第三方模型，提供兼容 OpenAI 的 API 与全链路模型服务。本页汇总从选择模型、获取 API Key、首次调用、选择地域到限流控制的完整上手路径，面向开发者快速跑通第一个模型调用并理解生产环境注意事项。详见 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。

## 平台与模型概览

百炼提供开箱即用的模型服务，无需自行部署或运维，直接调用千问全系列及 DeepSeek、Kimi、GLM、MiniMax 等第三方大模型，覆盖文本、图像、视频、音频、3D、全模态、向量与重排序等多种能力，详见 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。

千问系列旗舰文本模型按"能力最强到成本最低"排列：

- **千问 Max（qwen3.7-max）**：Qwen 系列效果最好，适合复杂、多步骤任务。
- **千问 Plus（qwen3.7-plus / qwen-plus）**：效果、速度和成本均衡，是多数场景的推荐选择。
- **千问 Flash（qwen3.6-flash / qwen-flash）**：高性价比、低延迟，适合快速响应的简单任务。

除文本外，平台还提供：视觉理解（qwen3.7-plus、qwen3.5-omni-plus）、图像/视频生成（wan2.7-image-pro、qwen-image-2.0-pro、happyhorse 系列）、3D 生成（Tripo-H3.1）、语音合成（cosyvoice-v3.5-plus）、语音识别（fun-asr、qwen3.5-omni-plus）、全模态（qwen3.5-omni-plus）、向量化与重排序（text-embedding-v4、qwen3-rerank）等。完整列表前往模型广场查看。

百炼还支持模型调优（SFT/CPT/DPO）、[模型部署](../concepts/model-deployment.md)（资源专享推理）和模型[评测](../concepts/evaluation.md)（人工/自动/基线），以及智能体、工作流、高代码应用三种应用构建模式。

## 首次调用 API

完整步骤见 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)，核心流程如下：

1. **注册并开通**：使用阿里云主账号前往百炼控制台阅读并同意协议开通服务；如提示未实名认证需先完成认证。
2. **获取 API Key**：在 API Key 页面创建，建议配置到环境变量 `DASHSCOPE_API_KEY`，避免在代码中硬编码。
3. **获取业务空间 ID（WorkspaceId）**：使用华北2（北京）、新加坡、日本（东京）或德国（法兰克福）地域时，需在 Base URL 中填入 WorkspaceId，可在业务空间管理页面查看。
4. **安装 SDK**：可选 OpenAI Python SDK（`pip install -U openai`）或 DashScope Python SDK（`pip install -U dashscope`）；Node.js 使用 `openai` 包；也可直接用 curl。

百炼兼容 OpenAI 接口规范，现有 OpenAI 代码只需修改 `api_key`、`base_url` 和 `model` 即可迁移。最小调用示例（北京地域，专属域名）：

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen-plus",
    messages=[{"role": "user", "content": "你是谁？"}],
)
print(completion.choices[0].message.content)
```

> **注意**：不同文档中的示例模型名不一致——"什么是百炼"用 `qwen3.7-plus`，"首次调用千问 API"用 `qwen-plus`。前者为最新版本别名，后者为稳定版别名，均可调用，生产环境建议按 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 中的稳定版或带日期快照版本以获得更稳定的限流额度。

## 选择地域与接入域名

调用前需选择**地域**（决定接入点与数据存储位置）、**服务部署范围**（决定推理执行位置）和**接入域名**（影响并发上限、超时等服务保障），详见 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)。

可用地域：华北2（北京，`cn-beijing`）、新加坡（`ap-southeast-1`）、美国（弗吉尼亚）、德国（法兰克福，`eu-central-1`）、日本（东京，`ap-northeast-1`）。各地域接入域名、API Key、模型列表**不能跨地域混用**。

| 服务部署范围需求 | 推荐地域 |
| --- | --- |
| 数据不出中国内地 | 华北2（北京） |
| 数据不经过中国内地 | 新加坡 |
| 数据不出美国 | 美国（弗吉尼亚） |
| 数据不出欧盟 | 德国（法兰克福） |
| 数据不出日本 | 日本（东京） |
| 无驻留限制，追求更大推理资源池 | 美国/德国/日本（全球部署） |

接入域名分三种，生产环境推荐**专属域名** `{WorkspaceId}.{region}.maas.aliyuncs.com`（SLA 99.9%、超时 3600 秒、支持 HTTP/SSE/WebSocket/WebRTC）；共享域名 `dashscope.aliyuncs.com` 用于存量兼容；试用域名 `trial.{region}.maas.aliyuncs.com` 仅用于快速体验，不建议生产。

从共享域名迁移到专属域名只需替换 Base URL 中的域名部分，业务逻辑代码无需修改。德国（法兰克福）、日本（东京）通过业务空间区分全球/欧盟或全球/日本部署范围，调用前需先在业务空间管理页面创建并选择；美国（弗吉尼亚）使用带 `-us` 后缀的模型名（如 `qwen-plus-us`）可限定美国境内推理，不带后缀默认全球推理。

> **注意**：功能支持因地域差异较大——批量推理、模型告警、模型调优、应用开发仅在华北2（北京）和新加坡支持；美国、德国、日本均不支持模型调优与应用开发。跨地域迁移前请核对功能矩阵。

## 限流与用量控制

百炼按**主账号维度**限流，账号下所有 RAM 子账号、业务空间和 API Key 的调用量合并计算；不同模型限流额度相互独立，详见 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)。

限流类型按错误信息区分：

- `Requests rate limit exceeded` / `You exceeded your current requests list`：触发每分钟请求数（RPM）限流。
- `Allocated quota exceeded` / `You exceeded your current quota`：触发每分钟 Token 消耗（TPM）限流。
- `Request rate increased too quickly`：短时间请求激增触发的稳定性保护，即使总量未达上限也会触发。

除 RPM/TPM 外，系统可能按秒级 RPS（RPM/60）与 TPS（TPM/60）执行，瞬时爆发也会触发限流。触发后通常一分钟内自动恢复。

北京地域参考限流（稳定版/最新版远高于带日期快照版）：

| 模型 | 服务部署范围 | RPM | TPM |
| --- | --- | --- | --- |
| qwen3.7-max | 中国内地 | 30,000 | 5,000,000 |
| qwen3.7-plus | 中国内地 | 30,000 | 5,000,000 |
| qwen3.6-flash | 中国内地 | 30,000 | 10,000,000 |
| qwen-plus | 中国内地 | 30,000 | 5,000,000 |
| qwen-plus-2025-07-28（快照） | 中国内地 | 60 | 1,000,000 |
| qwen-max | 中国内地 | 1,200 | 1,000,000 |
| qwen-turbo | 中国内地 | 1,200 | 5,000,000 |
| qwen-long | 中国内地 | 1,200 | 3,000,000 |

避免限流的实践：

1. **选用高限流模型**：优先 `qwen-plus`、`qwen3.6-flash` 等额度更高的稳定版；带日期快照版本额度通常低一个数量级。
2. **优化调用策略**：收到 RPM 限流降频率；收到 TPM 限流缩短输入或限制输出长度；收到激增告警采用匀速调度、指数退避或请求队列。
3. **添加备选模型**：主模型 429 后自动切换备用模型重试。
4. **拆分任务**：长对话或大文档拆为小批次分时段提交。
5. **批量推理**：非实时场景用 Batch API，不受实时限流约束（需考虑排队时间）。
6. **提升临时限流额度**：在百炼控制台"限流提额"页面提升模型临时 TPM，提交后立即生效，有效期 30 天，仅支持华北2（北京）和新加坡。

限流仅约束速率，不限制累计用量。控制费用支出可：设置月度消费限额与费用告警；对支持免费额度的模型开启"免费额度用完即停"；定期在模型监控页面查看 Token 用量（数据按小时更新，调用完约一小时后可查）。

## 计费要点

开通百炼本身免费，调用、微调、部署模型时产生费用，按分钟出账。新用户在华北2（北京）地域有专属免费额度：未认证用户用完即止，需完成认证并充值后才能继续按量付费；已认证用户免费额度用完后自动转按量付费，可开启"免费额度用完即停"避免意外扣费。Coding Plan 为固定月费套餐，提供月度请求额度，需使用专属 Base URL 和 API Key 调用，否则按量付费。

避免产生费用的最彻底方式是删除所有 API Key 从源头阻断调用，并停止应用、智能体、工作流中的模型调用，清理按算力时长计费的部署实例。

## 上手清单

1. 注册阿里云账号并完成实名认证 → 主账号开通百炼。
2. 在 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 中确定所需模型与模态。
3. 在 [选择地域](../../raw/model-user-guide/get-started-with-models/regions.md) 中按数据合规需求选定地域与服务部署范围，获取专属域名与 WorkspaceId。
4. 创建 API Key 并配置到环境变量 `DASHSCOPE_API_KEY`。
5. 安装 OpenAI 或 DashScope SDK，按 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md) 跑通最小示例。
6. 上量前核对 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md) 表，必要时在控制台提升临时 TPM。

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)


