# use cases

`use cases` 页面汇总了百炼平台在实际业务场景中的典型应用模式与工程实践，涵盖从基础生成任务到复杂智能体构建的完整链路。开发者可依据具体需求，参考对应指南快速落地解决方案。所有用例均基于平台当前支持的模型能力与 API 接口设计，部分历史资源已归档至 [历史模型指南](../../raw/model-user-guide/use-cases/legacy-resources.md)。

## 支持的模型/功能

- 文生文：Qwen 系列（Qwen1.5、Qwen2、Qwen2.5）、Qwen-VL（多模态理解）、Qwen-Audio（语音理解）  
- 文生图：万相 2.1 / 3.0（支持 `text-to-image` 和 `image-to-image`）  
- 文生视频：万相 3.0 视频生成（`text-to-video`），需指定 `model=wanx-v3-video`  
- 声音克隆与数字人：依赖专属服务接口，非通用大模型 API，详见 [声音克隆：定制你的专属声线](../../raw/model-user-guide/use-cases.md) 和 [告别昂贵摄制，一图生成高清数字人](../../raw/model-user-guide/use-cases.md)  
- RAG 构建：支持通过 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md) 实现结构化知识增强  
> **注意**：文档中列出的“Hermes Agent”为独立技术方案链接，其底层实现未在百炼标准 API 中开放，当前平台不提供 Hermes Agent 的直接 SDK 或托管服务，相关能力请以 [技术解决方案](../../raw/model-user-guide/use-cases/technical-solutions.md) 中最新说明为准。

## 关键参数

- `model`：必需，值须为平台当前启用的模型标识（如 `qwen-max`, `wanx-v3-video`, `qwen-audio`），不可使用已下线模型名  
- `prompt` / `input`：文本类任务使用 `input` 字段；图像/视频生成需按 [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md) 和 [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md) 组织结构化输入  
- `cache_level`：控制显式缓存行为，取值 `0`（禁用）、`1`（启用）、`2`（强一致性），详见 [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)  
- `rate_limit` 相关头字段（如 `X-RateLimit-Strategy`）仅在企业版配额策略下生效，基础版默认遵循全局限流规则，参见 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)

## 使用方式

1. **调用前准备**：确认模型已开通权限（控制台 → 模型服务 → 启用对应模型）  
2. **构造请求**：  
   - 文生文：POST `/v1/services/aigc/text-generation/generation`，body 含 `model` + `input`  
   - 文生图：POST `/v1/services/aigc/text-to-image/generation`，body 含 `model` + `input.prompt` + `size`  
   - 文生视频：POST `/v1/services/aigc/text-to-video/generation`，body 含 `model=wanx-v3-video` + `input.prompt` + `duration`  
3. **结果处理**：[异步任务](../concepts/asynchronous-task.md)返回 `task_id`，需轮询 `/v1/tasks/{id}` 获取状态；同步接口直接返回 `output`  
4. **高级集成**：三方模型调用需配置 OAuth2 凭据并启用代理路由，流程见 [三方模型调用教程](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md)

## 限制和注意事项

- 视频生成任务最大时长为 8 秒，超时将被截断；万相 3.0 不支持自定义帧率或分辨率，固定输出 1080p@24fps  
- 所有 Prompt 类指南（如 [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)）要求输入长度 ≤ 32768 token，超出将被静默截断  
- 实时音视频接入（WebRTC 流）需单独申请白名单权限，且仅支持 `qwen-audio` 模型的流式 ASR，TTS 不支持实时流输出  
- 自定义模型训练产出的 `.pt` 文件不可直接部署为 API 服务，必须通过 [自定义模型最佳实践](../../raw/model-user-guide/use-cases/model-training-best-practices.md) 中描述的蒸馏+封装流程转换为百炼兼容格式

## 来源文档

- [实践教程](../../raw/model-user-guide/use-cases.md)


