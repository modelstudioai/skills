# get started with models

阿里云百炼是一站式大模型开发与应用平台，集成千问（Qwen）系列自研模型及 DeepSeek、Kimi、GLM 等主流第三方模型，覆盖文本、图像、视频、音频、向量等多种模态。平台提供兼容 OpenAI 的 API 接口，开发者只需调整 API Key 与 Base URL 即可将现有 OpenAI 代码迁移至百炼；业务人员也可通过可视化工具零代码构建智能体、工作流、知识库问答等 AI 应用。本文引导开发者完成从选模型、配环境、发起第一次 API 调用，到选地域、处理限流的全流程。

## 支持的模型与能力

百炼的模型按模态分为以下几类：

- **文本生成**：千问旗舰系列（qwen3.7-max、qwen3.7-plus、qwen3.6-flash 等），以及 DeepSeek-V4 Pro/Flash、Kimi-K2.6、GLM-5.1、MiniMax-M2.7、Mimo-V2.5-Pro 等第三方模型。
- **视觉理解**：qwen3.7-plus、qwen3.5-omni-plus、kimi-k2.6 等，可分析图片和视频内容并返回文本描述。
- **图像与视频生成**：wan2.7-image-pro、qwen-image-2.0-pro、happyhorse 系列等。
- **3D 模型生成**：Tripo-H3.1 / Tripo-P1.0，支持文生 3D 与图生 3D。
- **语音与音频**：cosyvoice-v3.5-plus（TTS）、fun-music-v1（音乐生成）、fun-asr 系列（ASR）、qwen3.5-omni-plus-realtime（语音转语音）。
- **向量与重排序**：text-embedding-v4、tongyi-embedding-vision-plus、qwen3-rerank，用于 RAG 检索场景。
- **全模态**：qwen3.5-omni-plus 系列融合文本、图像、音频、视频多种模态。

完整模型列表与能力对照可在 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 中查看。除模型调用外，百炼还提供模型调优（SFT/CPT/DPO）、模型部署（资源专享推理）、模型评测等全链路服务。

## 首次调用 API

开始之前需完成账号设置与开发环境配置，详细步骤参见 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)。

### 1. 开通服务并获取 API Key

1. 使用阿里云主账号前往 [百炼控制台](https://bailian.console.aliyun.com/?tab=model#/model-market)，阅读并同意协议后自动开通。
2. 进入 [API Key 管理页](https://bailian.console.aliyun.com/?tab=model#/api-key)，单击**创建 API Key**。
3. 如使用**新加坡**或**德国（法兰克福）**地域，还需在[业务空间](../concepts/workspace.md)管理页获取 `WorkspaceId`，用于拼接 Base URL。

### 2. 配置环境变量

将 API Key 写入环境变量，避免在代码中硬编码：

- **Linux / macOS**：写入 `~/.bashrc`、`~/.zshrc` 或 `~/.bash_profile`，`export DASHSCOPE_API_KEY="sk-xxx"`，然后 `source` 使其生效。
- **Windows**：通过「系统属性 → 环境变量」或 `setx DASHSCOPE_API_KEY "sk-xxx"` 配置。

### 3. 安装 SDK 并发起调用

百炼兼容 OpenAI 接口规范，推荐使用 OpenAI SDK 或 DashScope SDK。以下以 OpenAI Python SDK 为例：

```bash
pip install -U openai
```

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 华北2（北京）
)
completion = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "你是谁？"},
    ],
)
print(completion.choices[0].message.content)
```

Node.js、curl 等调用方式参见 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。

## 选择地域与服务部署范围

调用前需选定**地域**（决定接入点与数据存储位置）和**服务部署范围**（决定推理执行位置）。各地域的 Base URL、API Key、模型列表相互独立，**不能跨地域混用**。

| 地域 | Base URL（OpenAI 兼容） | 典型使用场景 |
| --- | --- | --- |
| 华北2（北京） | `https://dashscope.aliyuncs.com/compatible-mode/v1` | 数据不出中国内地 |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` | 全球资源池或数据不出美国 |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` | 数据不经过中国内地 |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1` | 数据不出欧盟，或全球资源池 |

> **注意**：新加坡地域旧版域名 `dashscope-intl.aliyuncs.com` 即将下线，请迁移至新版 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`。

> **注意**：美国（弗吉尼亚）地域使用带 `-us` 后缀的模型名称（如 `qwen-plus-us`）时仅限美国境内推理；不带后缀默认走全球部署范围。法兰克福地域通过[业务空间](../concepts/workspace.md)区分部署范围，需先在控制台创建[业务空间](../concepts/workspace.md)并选定全球或欧盟模式。

地域选择与接入点详细说明请参见 [选择地域和服务部署范围](../../raw/model-user-guide/get-started-with-models/regions.md)。

## 限流与配额

百炼按**主账号维度**限流，账号下所有 RAM 子账号、业务空间、API Key 的调用量合并计算；不同模型的限流额度相互独立。限流包含每分钟请求数（RPM）与每分钟 Token 消耗（TPM）两个维度，超出任一数值即触发限流。

常见限流错误信息：

- `Requests rate limit exceeded` / `You exceeded your current requests list`：触发 RPM 限流。
- `Allocated quota exceeded` / `You exceeded your current quota`：触发 TPM 限流。
- `Request rate increased too quickly`：请求速率短时激增，即使未达 RPM/TPM 上限也会触发稳定性保护。

限流通常在一分钟内自动恢复。规避建议：

1. 优先选用限流额度更高的模型（如 `qwen-plus`、`qwen3.6-flash`），稳定版比带日期的快照版限流更宽松。
2. 匀速调度、指数退避，避免瞬时高峰。
3. 准备备选模型，触发限流时自动切换重试。
4. 无需实时响应时，使用**批量推理（Batch API）**，不受实时限流约束。
5. 在控制台的「限流提额」页面申请临时 TPM 额度，提交后立即生效，有效期 30 天（目前支持北京与新加坡地域）。

各模型的 RPM/TPM 具体数值请参见 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)。

## 计费与免费额度

开通百炼无需费用，仅在调用、微调、部署模型时按量计费：

- 模型调用按分钟出账，需确保阿里云账户余额充足。
- 新用户在北京地域享有**新人免费额度**；已认证用户额度用完后自动转为按量付费，可开启「免费额度用完即停」避免意外扣费。
- 如需固定月费、无按量扣费风险，可订阅 **Coding Plan**（AI 编码套餐），但需使用专属 Base URL 与 API Key。

## 常见问题

**Q：数据会被用于训练吗？**
不会。百炼严格保护数据隐私，所有传输数据均加密处理，不会用于模型训练。

**Q：如何避免产生费用？**
删除不再使用的 API Key、停止所有应用调用、下线按算力时长计费的部署实例，并开启「免费额度用完即停」。必要时可在费用中心设置高额消费预警。

**Q：如何快速体验模型？**
登录百炼控制台，进入「模型广场」或「模型体验」页面，选择目标地域后即可直接与模型对话。

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [选择地域和服务部署范围](../../raw/model-user-guide/get-started-with-models/regions.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)


