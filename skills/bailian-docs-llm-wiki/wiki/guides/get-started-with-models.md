# get started with models

阿里云百炼提供兼容 OpenAI 接口规范的大模型 API 服务，支持直接调用自研千问（Qwen）全系列模型及 DeepSeek、Kimi、GLM 等主流第三方模型。开发者只需配置 [[api-key]] 与对应地域的接入地址，即可通过主流 SDK 或标准 HTTP 请求快速完成集成。本指南涵盖模型选型、核心参数配置、调用示例及生产环境限制说明。

## 支持的模型与功能

百炼按模态与场景提供多类别模型服务，无需自行部署即可按需调用：
- **文本生成**：提供千问 Max（复杂推理/多步任务）、Plus（均衡推荐）、Flash（低延迟/高性价比）及 Long（长上下文）等梯队，并覆盖 DeepSeek、Kimi、MiniMax 等三方文本模型。详细列表参见 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。
- **多模态与专项能力**：涵盖视觉理解（VL）、图像/视频生成、3D 生成、语音合成/识别/语音转语音（S2S）、全模态融合（Omni）以及向量化与重排序（Embedding & Rerank）模型。
- **高级服务**：除实时推理外，平台还提供 [[batch-inference]]（适用于离线大批量处理，不受实时限流约束）、[[model-tuning]]（SFT/CPT/DPO 定制）及 [[model-deployment]]（资源专享实例，支持按时长/包月计费）。

## 关键参数配置

调用模型时需严格匹配地域、接入点与部署范围，核心参数如下：

| 参数 | 说明 | 示例/备注 |
|:---|:---|:---|
| `api_key` | 身份鉴权凭证 | 强烈建议通过环境变量 `DASHSCOPE_API_KEY` 注入，禁止硬编码。各地域 Key 物理隔离，**不可跨地域混用**。 |
| `base_url` | API 接入端点 | 华北2（北京）：`...dashscope.aliyuncs.com/...`<br>美国（弗吉尼亚）：`...dashscope-us.aliyuncs.com/...`<br>新加坡：`...dashscope-intl.aliyuncs.com/...`<br>德国（法兰克福）：需替换 `{WorkspaceId}`，详见 [选择地域和服务部署范围](../../raw/model-user-guide/get-started-with-models/regions.md) |
| `model` | 模型标识 | 需与控制台当前地域可用列表一致。美国地域若限定境内推理，需使用带 `-us` 后缀的名称（如 `qwen-plus-us`）。 |
| `messages` | 对话上下文 | 遵循 `[{role: "user", content: "..."}]` 格式，支持 `system` 设定与多轮历史。 |

> **注意**：服务部署范围（中国内地/全球/国际/美国/欧盟）决定推理节点位置。无合规要求的场景建议选择**全球**范围以获取更大资源池；有数据驻留要求的需按表选择对应地域与范围。静态数据始终持久化在所选接入地域，推理过程全链路加密且不留存。

## 调用方式

推荐使用 OpenAI 兼容 SDK，可无缝迁移现有代码。以下为 Python 核心调用示例：

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1", # 按实际地域替换
)

completion = client.chat.completions.create(
    model="qwen-plus", # 替换为目标模型ID
    messages=[
        {"role": "system", "content": "你是一个专业的技术助手。"},
        {"role": "user", "content": "简述异步调用的优势。"}
    ],
    max_tokens=512,
    temperature=0.7
)
print(completion.choices[0].message.content)
```

完整的环境变量配置、虚拟环境隔离、多语言（Node.js/cURL）及 DashScope 原生 SDK 调用步骤，请参考 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)。生产环境建议结合 [[rate-limit-policy]] 实现指数退避重试与熔断降级。

## 限制与注意事项

- **限流策略**：限流按主账号维度合并计算，不同模型额度独立。触发条件通常为 RPM（每分钟请求数）或 TPM（每分钟 Token 消耗）超限。瞬时请求激增（即使未达分钟上限）也可能触发稳定性保护。可通过控制台 [[rate-limit-policy]] 查看明细或申请临时提额（有效期 30 天）。
- **模型版本命名**：带日期的快照版本（如 `qwen-plus-2025-07-28`）限流通常较宽松且能力固定；生产环境建议优先使用稳定版（如 `qwen-plus` 或 `qwen-plus-latest`）以获得持续优化与更高配额。
- **计费与额度**：采用按量付费，调用后约 1 小时出账。新用户享北京地域专属体验额度，耗尽即停功能开启后服务会自动暂停以防超额扣费。详细计量规则见 [[billing]]。
- **监控延迟**：[[model-monitoring]] 数据按小时级聚合，调用统计通常在请求完成后约一小时可查，高峰期可能存在延迟。

> **注意**：各文档中列出的模型支持列表、限流阈值（RPM/TPM）及功能支持表（如法兰克福暂不支持批量推理与模型调优）会随版本迭代动态调整。开发前请务必通过控制台[[model-list]]与限流管理页面核对最新数据，避免依赖静态快照信息。

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [选择地域和服务部署范围](../../raw/model-user-guide/get-started-with-models/regions.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)

