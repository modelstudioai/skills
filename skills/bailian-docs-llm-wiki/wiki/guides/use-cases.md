# use cases

百炼平台的 use cases 文档汇总了面向开发者的核心实践场景与工程化落地方法，覆盖从基础 Prompt 工程、多模态生成（文生图/文生视频/数字人）、RAG 构建，到模型集成、缓存与限流等生产级最佳实践。所有用例均基于真实调用链路验证，强调可复现性与参数可控性。开发者应结合具体模型能力边界选择适配方案。

## 支持的模型/功能

当前 use cases 覆盖以下能力域：
- **文本生成类**：Qwen 系列（含 Qwen1.5、Qwen2、Qwen2.5）、Qwen-VL、Qwen-Audio，支持结构化输出、[函数调用](../concepts/function-calling.md)、多轮对话状态管理；
- **多模态生成类**：万相（WanX）系列（含 WanX 2.0、WanX 3.0）、通义听悟（Tongyi Tingwu），支持文生图、文生视频、语音克隆、文档转视频；
- **检索增强类**：LlamaIndex 集成、自定义向量库构建与混合检索；
- **系统集成类**：三方模型（如 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)）、实时音视频 SDK 接入、显式缓存控制。

> **注意**：`[历史模型指南](../../raw/use-cases/legacy-resources.md)` 中列出的部分模型（如 Qwen-VL-Chat v1.0）已停止维护，其 Prompt 格式与当前 Qwen-VL v2.1 不兼容，实际开发中请优先参考 `[文生图Prompt指南](../../raw/use-cases/text-to-image-prompt.md)` 中的最新约束。

## 关键参数

各用例依赖的关键参数具有强上下文敏感性，需严格匹配模型版本：
- `model`：必须为平台控制台启用的模型 ID（如 `qwen-max`, `wanx-v3`），不可使用别名或旧版 ID；
- `stream`：仅对文本生成类模型生效；视频/图像类模型不支持流式响应；
- `seed`：在 WanX 系列中用于控制生成一致性，但 `seed=0` 表示随机，非固定值；
- `max_tokens` / `n` / `size`：不同用例对参数语义要求不同，例如 `[万相3.0视频生成Prompt指南](../../raw/use-cases/wan3-video-generation-prompt-guide.md)` 明确要求 `duration` 必须为 2/4/6 秒整数，且 `size` 仅支持 `"1080p"` 或 `"720p"`。

## 使用方式

所有用例均通过标准 REST API 或 SDK 调用，无特殊协议要求：
- Prompt 工程类（如 `[文生文Prompt指南](../../raw/use-cases/prompt-engineering-guide.md)`）推荐使用 `system` + `user` + `assistant` 三段式 message 结构，并启用 `enable_search` 控制 RAG 触发；
- 多模态生成类需上传二进制资源（如图片 base64、音频 WAV）至临时 URL 后传入 `input.image_url` 或 `input.audio_url`；
- RAG 类用例依赖预置知识库 ID（`retrieval.knowledge_id`），该 ID 需通过控制台创建并发布，不可直接使用本地文件路径。

## 限制和注意事项

- 单次请求最大输入长度：Qwen 系列为 32768 tokens，WanX 系列为 2048 chars（含空格），超长文本需分块处理；
- 视频生成类任务（如 `[视频生成Prompt指南](../../raw/use-cases/text-to-video-prompt.md)`）默认异步返回，需轮询 `job_id` 获取结果，超时时间为 15 分钟；
- 显式缓存（`cache_level=2`）仅对完全相同的 `model` + `input` + `parameters` 组合生效，微小 Prompt 差异（如标点、换行）即视为不同 key；
- 三方模型调用（见 `[三方模型调用教程](../../raw/use-cases/third-party-model-integration-tutorial.md)`）不支持百炼原生的 `function_call` 和 `tool_choice` 参数，需自行解析 schema。

## 来源文档

- [实践教程](../../raw/model-user-guide/use-cases.md)


