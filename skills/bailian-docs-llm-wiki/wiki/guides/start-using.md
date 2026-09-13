# start using

本文档介绍如何快速开始使用百炼平台构建和部署 AI 应用，涵盖模型调用、应用配置及基础开发流程。开发者可通过控制台或 API 快速接入，无需从零训练模型。所有操作均基于百炼提供的托管服务，需确保已开通对应模型的调用权限。

## 支持的模型/功能

百炼平台当前支持通义千问系列（Qwen1.5、Qwen2、Qwen2.5、Qwen3）、Qwen-VL、Qwen-Audio 等开源模型，以及部分专属微调版本（如 qwen-max、qwen-plus）。应用层功能包括知识库问答、工作流编排、RAG 增强、多轮对话管理等。具体模型列表与能力说明详见 [开始使用](../../raw/application-user-guide/start-using.md)。注意：`qwen-max` 为闭源模型，其输入长度上限与公开 Qwen 系列不同，不可直接套用 Qwen2 的 token 计算逻辑 —— 详见 [开始使用](../../raw/application-user-guide/start-using.md) 中的“模型选型建议”章节（该章节在 2024-09 版本中已更新，旧版文档中未体现差异）。

## 关键参数

调用模型时需关注以下核心参数：
- `model`: 必填，如 `"qwen-max"` 或 `"qwen2-72b"`；
- `input.messages`: 消息数组，格式为 `[{ "role": "user", "content": "..." }]`；
- `parameters.temperature`: 控制输出随机性（0.0–1.0），默认 0.85；
- `parameters.top_p`: 核采样阈值，默认 0.8；
- `parameters.max_tokens`: 输出最大 token 数，各模型有硬性上限（例如 qwen2-72b 为 8192，qwen-max 为 32768）。

参数兼容性请以 [开始使用](../../raw/application-user-guide/start-using.md) 中的“API 参数参考表”为准；该表已同步最新模型规格，旧版 SDK 文档中部分默认值存在滞后。

## 使用方式

1. **控制台快速启动**：登录百炼控制台 → 创建应用 → 选择模板（如“知识库问答”）→ 绑定知识库或配置 Prompt → 发布并获取 API Key；
2. **API 直接调用**：使用 `POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`，携带 `Authorization: Bearer <api_key>`；
3. **SDK 调用（推荐）**：安装 `dashscope` Python SDK（≥1.20.0），调用 `Generation.call()` 方法，示例见 [开始使用](../../raw/application-user-guide/start-using.md) 中的“代码示例”小节。

> **注意**：自 2024-10-15 起，`/v1/chat/completions` 兼容 OpenAI 格式的 endpoint 已下线，仅保留百炼原生 `/v1/services/aigc/...` 路径。旧文档中提及的 OpenAI 兼容模式属于过时信息。

## 限制和注意事项

- 免费额度按账户粒度分配，不跨子账号共享；
- 单次请求 `input.messages` 总长度（含 system [prompt](prompt.md)）不得超过模型 context 长度的 95%（预留空间用于生成）；
- 知识库问答类应用需提前完成文档切片与向量化，延迟生效约 1–3 分钟；
- 流式响应（`stream=true`）仅支持部分模型（如 qwen2-7b、qwen2-72b），`qwen-max` 暂不支持流式，详见 [开始使用](../../raw/application-user-guide/start-using.md) 的“功能支持矩阵”。

## 来源文档

- [开始使用](../../raw/application-user-guide/start-using.md)


