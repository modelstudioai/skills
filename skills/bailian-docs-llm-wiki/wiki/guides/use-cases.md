# use cases

百炼平台的 use cases 文档汇总了面向开发者的核心实践场景与工程化指南，覆盖从基础 [Prompt 工程](../concepts/prompt.md)、多模态生成（文生图/文生视频/数字人）、RAG 构建到模型集成与生产运维等关键路径。所有用例均基于真实 API 调用与 SDK 实践验证，适用于快速原型开发与企业级应用落地。部分指南需配合特定模型版本或服务权限使用，详见各子文档说明。

## 支持的模型/功能

- **文本生成类**：Qwen 系列（Qwen1.5、Qwen2、Qwen2.5）、Qwen-VL（多模态理解）、Qwen-Audio（语音理解）  
- **图像生成类**：万相 2.1 / 3.0（支持 text-to-image、inpainting、style transfer）  
- **视频生成类**：万相 3.0 视频生成（text-to-video）、[视频生成Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md) 中明确限定仅支持 `wanx-v3` 模型 ID  
- **智能体与 RAG**：Hermes Agent 框架、LlamaIndex 集成（见 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)）  
- **第三方集成**：支持通过百炼统一网关调用 OpenAI、Claude、Gemini 等三方模型（参见 [三方模型调用教程](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md)）

> **注意**：[万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md) 中描述的 `--aspect-ratio 16:9` 参数在 v3.0.2+ SDK 中已弃用，应改用 `aspect_ratio: "16:9"` 字段（JSON 格式），旧参数将被静默忽略。

## 关键参数

- `model`: 必填，如 `"qwen-max"`、`"wanx-v3"`、`"gpt-4o"`（三方模型需提前配置白名单）  
- `input`: 结构依模型而异：文本模型为 `{"prompt": "..."}`；万相图像/视频需传 `{"prompt": "...", "size": "1024*1024", ...}`  
- `parameters`: 可选，常见字段包括 `temperature`（0.1–1.0）、`top_p`、`max_tokens`（文本）、`seed`（生成确定性控制）  
- `enable_cache`: 布尔值，启用显式缓存需设为 `true`，并配合 [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md) 使用  

## 使用方式

1. **API 调用**：通过 `/v1/services/aigc/text-generation/generate`（文本）、`/v1/services/aigc/image-generation/generate`（图像）等路径发起 POST 请求  
2. **SDK 调用**（Python 示例）：
   ```python
   from aliyunsdkcore.client import AcsClient
   from aliyunsdkalimt.request.v20181012 import GenerateRequest
   # 注意：图像/视频生成需使用 WanxClient（非 AlimtClient）
   ```
3. **[Prompt 工程](../concepts/prompt.md)**：严格遵循各领域指南格式，例如文生图需按 [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md) 组织 prompt 结构（含 negative prompt、style keywords 分隔符）  

## 限制和注意事项

- 单次请求最大 `input` 长度：文本模型 ≤ 32768 tokens；万相图像 prompt ≤ 1000 字符；视频 prompt ≤ 500 字符  
- 视频生成任务最长超时 180 秒，失败后不自动重试，需业务层实现幂等重试逻辑  
- 显式缓存（`enable_cache=true`）仅对完全相同的 `model + input + parameters` 组合生效，`seed` 不同即视为不同请求  
- 实时音视频流接入需单独申请 `realtime-audio-video` 权限，并参考 [实时音视频接入](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md) 完成信令与媒体流对接  
- 所有生成类接口默认启用限流（QPS/账户级），高并发场景必须实施 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md) 中的退避与队列策略

## 来源文档

- [实践教程](../../raw/model-user-guide/use-cases.md)


