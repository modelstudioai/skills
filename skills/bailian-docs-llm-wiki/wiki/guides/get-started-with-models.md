# get started with models

阿里云百炼是一站式大模型开发与应用平台，集成千问（Qwen）全系列及 DeepSeek、Kimi、GLM 等主流第三方模型，提供兼容 OpenAI 的 API 与全链路模型服务。本页面面向开发者，梳理从选择模型、获取 API Key、配置调用地址到发起首次请求的完整入门路径，并汇总地域、Base URL 与限流等关键约束。

## 支持的模型与能力

百炼提供开箱即用的模型服务，无需自行部署或运维即可直接调用，覆盖多种模态（详见 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)）：

- **文本生成**：千问旗舰系列按能力与成本梯度排列——`qwen-max`（复杂多步骤任务）、`qwen-plus`（效果、速度、成本均衡，**多数场景推荐**）、`qwen-flash`（高性价比、低延迟）；三方模型（DeepSeek、Kimi、GLM、MiniMax 等）API 格式与千问一致。
- **图像与视频**：视觉理解、图像生成、视频生成。
- **音频与语音**：语音合成（TTS）、语音识别（ASR）、语音转语音（S2S）、音乐生成。
- **全模态**：融合文本、图像、音频、视频的理解与生成（如 omni 系列）。
- **向量与重排序**：文本/图文向量化（embedding）配合 rerank 提升检索精度。
- **3D 模型生成**：文生 3D、图生 3D。

除调用外，平台还支持模型调优（SFT/CPT/DPO）、模型部署、模型评测，以及可视化/高代码的应用构建。

## 快速上手：首次调用千问 API

完整流程见 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)，核心步骤如下：

1. **注册并开通**：使用阿里云主账号开通百炼（需完成实名认证）。
2. **获取 API Key**：在控制台 API Key 页面创建。
3. **获取业务空间 ID（WorkspaceId）**：使用北京、新加坡、东京、法兰克福地域时，Base URL 中需填入 WorkspaceId。
4. **配置环境变量**：推荐将 API Key 写入 `DASHSCOPE_API_KEY` 环境变量，避免在代码中硬编码。
5. **安装 SDK 并调用**：可用 OpenAI 兼容 SDK 或 [DashScope SDK](../concepts/dashscope-sdk.md)（Python 需 ≥ 3.8）。

OpenAI 兼容方式的最简调用示例：

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 北京地域，请将 {WorkspaceId} 替换为真实业务空间 ID
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen-plus",
    messages=[{"role": "user", "content": "你是谁？"}],
)
print(completion.choices[0].message.content)
```

> **注意**：百炼兼容 OpenAI 接口规范，迁移现有 OpenAI 代码通常只需调整 `api_key`、`base_url` 和模型名称。[DashScope SDK](../concepts/dashscope-sdk.md) 则通过 `dashscope.base_http_api_url` 指定地址（结尾为 `/api/v1` 而非 `/compatible-mode/v1`）。

## 地域、服务部署范围与接入域名

调用前需先确定**地域**（决定接入点与数据存储位置）、**服务部署范围**（决定推理执行位置，用于满足数据合规）、**接入域名**（影响并发、超时等服务保障）。各地域的接入域名、API Key 和模型列表相互独立，**不能跨地域混用**，详见 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)。

目前提供的地域：华北2（北京，`cn-beijing`）、新加坡（`ap-southeast-1`）、美国弗吉尼亚（`us-east-1`）、德国法兰克福（`eu-central-1`）、日本东京（`ap-northeast-1`）。建议就近选择以降低延迟。

关键差异：

- 数据要求不出中国内地 → 选北京（中国内地推理）。
- 追求更大推理资源池且无数据驻留限制 → 选弗吉尼亚/法兰克福/东京（全球部署范围）。
- 美国弗吉尼亚使用带 `-us` 后缀的模型名（如 `qwen-plus-us`）可限定美国境内推理。
- **模型调优、应用开发、批量推理、模型告警仅在华北2（北京）等部分地域支持**，海外地域功能受限。

## Base URL 与接入域名选择

Base URL 是模型 API 的调用地址，**必须与同计费方案的 API Key 配套使用**，否则报 401。域名类型见 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)：

| 域名类型 | 格式（以北京为例） | 适用场景 |
| --- | --- | --- |
| 业务空间专属域名（**推荐**） | `{WorkspaceId}.cn-beijing.maas.aliyuncs.com` | 生产环境，高并发、请求超时 3600 秒、SLA 99.9% |
| Dashscope 域名（存量） | `dashscope.aliyuncs.com` | 兼容存量业务，建议迁移，超时 600 秒 |
| 试用域名 | `trial.cn-beijing.maas.aliyuncs.com` | 快速验证，RPM 限 1000，不建议生产 |

- [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)路径为 `/compatible-mode/v1`，Anthropic 兼容接口为 `/apps/anthropic`，DashScope 接口为 `/api/v1`。
- **Token Plan / Coding Plan** 有独立域名，仅限 Claude Code、Codex 等 AI 工具交互式使用，不能用于后端服务，且需使用对应套餐的专属 API Key。

> **注意**：从 Dashscope/试用域名迁移到业务空间专属域名无需改动业务逻辑，只需替换 Base URL 中的域名部分。

## 限流与配额

百炼按**主账号维度**限流，账号下所有 RAM 子账号、业务空间和 API Key 的调用量合并计算；不同模型的限流额度相互独立。超限请求会被拒绝，通常一分钟内自动恢复，详见 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)。

- **RPM**（每分钟请求数）超限：报 `Requests rate limit exceeded`。
- **TPM**（每分钟 Token 数，含输入与输出）超限：报 `Allocated quota exceeded`。
- **请求速率激增**：报 `Request rate increased too quickly`，即使未达 RPM/TPM 上限也会触发；服务可能按秒级 RPS（RPM/60）、TPS（TPM/60）执行。

规避与提额策略：

- 优先选用限流更高的模型（如 `qwen-plus`）；稳定版/最新版比带日期快照版限流更宽松。
- 平滑请求速率（匀速调度、指数退避、请求队列），并配置备选模型自动重试。
- 对无需实时响应的任务改用 **Batch API**，不受实时限流约束。
- 华北2（北京）与新加坡地域支持在控制台**限流提额**页面临时提升 TPM 额度，提交即生效，有效期 30 天。

> **注意**：限流仅约束单位时间内的调用速率，**不限制累计用量**。如需控制费用，应另行设置消费限额、费用告警，或对新用户开启"免费额度用完即停"。

## 计费与费用控制

开通百炼免费，调用、微调、部署模型时按量计费（模型调用按分钟出账），调用统计约一小时后可在模型监控查看。控制费用的主要手段：删除 API Key 从源头阻断调用、下线按算力时长计费的部署实例、设置消费预警，或订阅固定月费的 Coding Plan（需使用其专属 Base URL 和 API Key，否则仍按量付费）。

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)


