# use cases

`use cases` 页面汇总了百炼平台支持的典型应用场景与对应技术路径，涵盖从基础生成到复杂[多模态](../concepts/multi-modal.md)实时交互的完整能力谱系。开发者可根据业务需求，结合模型能力、参数配置与接入方式快速选型落地。所有用例均基于平台当前 GA 版本验证，部分高级功能需配合特定模型或服务（如 AOQ、WebRTC）使用。

## 支持的模型/功能

百炼平台支持覆盖文本、图像、视频、音频、数字人及智能体编排的全栈用例，包括但不限于：
- 文生文、文生图、文生视频/图生视频等生成类任务，详见 [文生文Prompt指南](../../raw/model-user-guide/use-cases.md)、[文生图Prompt指南](../../raw/model-user-guide/use-cases.md) 和 [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases.md)；
- [多模态](../concepts/multi-modal.md)实时交互：依托 `qwen3.5-omni-plus-realtime`、`qwen-audio-3.0-realtime-plus` 等模型，支持 WebRTC 或 AOQ 接入实现语音对话、TTS、ASR 等低延迟场景；
- RAG 应用构建：推荐基于 LlamaIndex 框架集成，参考 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases.md)；
- 数字人与声音克隆：通过 `avatar` 和 `voice-cloning` 解决方案实现低成本内容生产；
- 智能体开发：支持 Hermes Agent 自进化框架及通用 AI 工作流编排。

> **注意**：`qwen3.5-omni-plus-realtime` 在 WebRTC 与 AOQ 两种接入路径下的能力边界存在差异（如音频流处理粒度、中断响应时延），具体以 [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases.md) 和 [使用 AOQ 接入 qwen3.5-omni-plus-realtime 实现按键语音对话](../../raw/model-user-guide/use-cases.md) 的实测说明为准，不可直接互换配置。

## 关键参数

不同用例对请求参数敏感度差异显著：
- 生成类任务（如文生图、文生视频）需严格遵循 Prompt 结构规范，超长 [prompt](prompt.md) 可能触发截断或语义偏移；
- 实时语音类任务（ASR/TTS/对话）必须设置 `stream=true`，并配合 `audio_format`、`sample_rate`、`chunk_size_ms` 等音轨级参数；
- RAG 场景建议启用显式缓存（`cache_level=2`），参见 [显式缓存最佳实践](../../raw/model-user-guide/use-cases.md)；
- 高并发调用需主动配置限流策略，避免触发平台默认熔断，详见 [限流应对最佳实践](../../raw/model-user-guide/use-cases.md)。

## 使用方式

- **API 直连**：所有用例均可通过 `/v1/chat/completions` 或专用 endpoint（如 `/v1/audio/speech`）调用，需在请求头携带 `Authorization: Bearer <token>`；
- **SDK 封装**：Python/Java/Node.js SDK 已内置[多模态](../concepts/multi-modal.md)参数模板，推荐优先使用 `dashscope` 官方 SDK；
- **低代码集成**：AI 智能体与工作流可通过 [高效搭建 AI 智能体与工作流应用](../../raw/model-user-guide/use-cases.md) 提供的可视化画布快速配置；
- **三方模型扩展**：支持通过 [三方模型调用教程](../../raw/model-user-guide/use-cases.md) 接入非百炼托管模型，但不享受平台级缓存、审计与限流协同保障。

## 限制和注意事项

- 所有生成类用例均受输入长度（max_tokens）、输出长度（max_output_tokens）及单次请求大小（如图片 base64 ≤ 10 MB）限制；
- 实时语音类用例要求客户端网络 RTT < 300 ms，否则可能出现音频卡顿或连接重置；
- `fun-asr-realtime` 与 `qwen-audio-3.0-realtime-plus` 不兼容同一音频流输入，混用将导致 ASR 结果异常；
- 文档转视频、深度研究等高资源消耗用例仅对开通专属配额的用户开放，普通试用账号默认禁用；
- 自定义[模型部署](../concepts/model-deployment.md)后需单独验证 Prompt 兼容性，部分原生用例（如数字人驱动）可能无法直接复用，参见 [自定义模型最佳实践](../../raw/model-user-guide/use-cases.md)。

## 来源文档

- [实践教程](../../raw/model-user-guide/use-cases.md)



