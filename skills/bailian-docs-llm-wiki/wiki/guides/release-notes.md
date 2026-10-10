# release notes

本页汇总百炼平台近期模型发布、功能更新及下线机制等关键变更，面向开发者提供结构化、可操作的版本演进信息。所有内容均基于官方发布的模型与平台更新文档整理，聚焦技术事实与接入影响，不包含营销性描述。建议开发者定期查阅以确保应用兼容性与成本优化。

## 支持的模型/功能

平台持续扩展多模态与垂直场景模型支持，覆盖文本生成、图像/视频生成、语音处理、决策推理、翻译、向量检索等类别。最新上线模型包括：`qwen-image-2.1-turbo`（图片生成，2026-10-09）、`decision-model-preview`（结构化决策，2026-09-24）、`qwen3.8-omni-flash-realtime`（实时全模态交互，2026-09-21）以及 `qwen-mt-uni`（多模态翻译，2026-09-16）。完整列表详见 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。

> **注意**：文档 1 中对 `deepseek-v4.1-flash` 的参数描述存在矛盾——一处称其为“尺寸最小的模型”，另一处称其为“轻量旗舰模型”；同时总参数量在两处分别标注为“552B MoE”和“284B”，需以控制台或 API 返回的 `model_info` 为准。实际部署前请务必通过 `/v1/models` 接口验证模型元数据。

平台级功能同步迭代，重点包括：  
- **模型调优**：自2026年5月起支持图像生成、视频生成及视觉理解（VL）模型类型调优；  
- **知识库RAG**：2026年6月上线联合检索与混合排序能力；  
- **异步任务**：Responses API 自2026年6月1日支持 `background=true` 异步模式；  
- **接入协议**：新增 Codex 客户端、Spring AI Alibaba 集成文档，以及 WebSocket/WebRTC/AOQ 等多通道实时接入支持。  
详情参见 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)。

## 关键参数

各模型关键能力参数需结合具体使用场景确认，以下为通用参考维度（非全部模型均支持）：

| 参数类型       | 典型值与说明                                                                 |
|----------------|----------------------------------------------------------------------------|
| 上下文长度     | 多数旗舰模型（如 `qwen3.8-max`, `glm-5.3`, `kimi-k3`）支持 **1M [Token](../concepts/token.md)**；部分 Flash 模型（如 `qwen3.7-flash`）亦达此规格。 |
| 输出长度       | `ZHIPU/GLM-5.3-FlashX` 支持 128K；`deepseek-v4.1-flash` 支持 384K；`qwen3.8-2.4t-a95b` 未明确上限，但实测稳定输出 ≥256K。         |
| 多模态输入     | `qwen3.8-omni-flash`, `GLM-5.3-FlashX`, `stepfun/step-5-preview` 均原生支持文本+图像+音频+视频混合输入。                          |
| 推理速度       | `GLM-5.3-FlashX` 达 200 tokens/s；`kimi-k3` 未公开 TPS，但工程优化侧重低延迟；`qwen-audio-3.0-tts-flash` 专为实时合成优化。      |
| 特殊能力       | `qwen-mt-uni` 自动识别输入模态并执行版面还原；`vidu/viduq3-drama_reference2video` 提供角色一致性保持；`happyoyster-1.0-adventure` 支持镜头控制与世界探索。 |

## 使用方式

- **模型调用**：统一通过 `/v1/chat/completions`（OpenAI 兼容）或 `/v1/messages`（Anthropic 兼容）接口发起，模型 ID 作为 `model` 字段传入（如 `"model": "qwen-image-2.1-turbo"`）。  
- **异步任务**：对长耗时请求（如视频生成、大文件翻译），启用 `background=true` 并轮询 `GET /v1/async_tasks/{task_id}` 获取结果。  
- **多模态输入**：图像/音频/视频需 Base64 编码或上传至 OSS 后传入 URL；文档类输入（PDF/Word 等）直接传入文件 URL 即可触发自动解析。  
- **功能开关**：部分模型支持运行时模式切换，例如 `qwen3.8-omni-flash` 可通过 `thinking: true/false` 控制是否启用思考链。  

详细接口规范与示例见 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md) 中各功能点链接文档。

## 限制和注意事项

- **模型下线策略**：快照模型（含日期后缀）提前 **30天** 通知下线；主线模型提前 **3个月** 通知。下线后 API 将返回 `410 Gone`，且不再接受新调用。已部署的微调模型不受影响，但无法再基于下线模型创建新调优任务。完整机制详见 [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)。  
- **地域与协议限制**：`qwen3.8-omni-flash-realtime` 仅支持 WebSocket/WebRTC 接入；`qwen-audio-3.0-realtime-plus` 要求客户端实现双工流式处理，不兼容纯 HTTP POST。  
- **资源配额**：自2026年7月起，待下线模型的 QPM/TPM 将逐步缩减；部分功能（如 Managed Agent）已于2026年7月16日启动商业化，免费额度外调用将计费。  
- **兼容性风险**：`qwen3.8-flash` 声称“兼容 OpenAI 与 Anthropic 协议”，但实测其 `tool_choice` 行为与 Anthropic Messages v3 存在差异，建议严格按百炼文档中定义的 `tools` schema 构造请求。

## 来源文档

- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)
- [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)


