# start using

本文档指导开发者快速接入百炼平台，完成基础环境配置、模型调用与应用构建。适用于希望基于百炼 API 或控制台快速启动知识库问答、Agent 应用等场景的工程师。所有操作均需通过百炼控制台或 OpenAPI 完成，不依赖本地 SDK 封装。

## 支持的模型/功能

当前平台默认开放以下能力：  
- 通用大语言模型（如 Qwen-Max、Qwen-Plus）及轻量模型（Qwen-Turbo），支持文本生成、多轮对话；  
- 知识库增强问答（RAG）功能，可对接自有文档（PDF/Word/TXT/Markdown）并自动切片向量化；  
- 基础 Agent 框架，支持工具调用（HTTP 请求、数据库查询等）与流程编排。  
详细模型列表与能力矩阵请参见 [开始使用](../../raw/application-user-guide/start-using.md) 中的“应用功能动态”链接，该页面持续同步各模型的可用性与灰度范围。

## 关键参数

调用 API 时必需指定以下参数：  
- `model`: 模型 ID（如 `qwen-max`），必须与控制台开通权限一致；  
- `input.messages`: 至少包含一条 `user` 角色消息，`system` 角色为可选；  
- `parameters.temperature`: 推荐值 0.1–0.8，生产环境建议 ≤0.3 以保障确定性；  
- `parameters.top_p` 和 `parameters.max_tokens` 需显式设置，否则使用平台默认值（详见 [开始使用](../../raw/application-user-guide/start-using.md) 的参数说明章节）。  
> **注意**：原始文档中 `parameters.stop` 的示例值为字符串数组（如 `["\n"]`），但当前 API 实际仅接受字符串类型（如 `"\n"`），该差异已在 [0代码构建问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md) 的最新版本中修正。

## 使用方式

1. **控制台快速启动**：登录百炼控制台 → 创建应用 → 选择“知识库问答”模板 → 上传文档 → 发布；  
2. **API 直接调用**：使用 `POST /v1/chat/completions`，Header 中携带 `Authorization: Bearer <api_key>`；  
3. **集成开发**：参考 [0代码构建问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md) 提供的 Postman 集合与 cURL 示例，可跳过前端开发直接验证后端链路。

## 限制和注意事项

- 单次请求 `input.messages` 总长度上限为 32768 token（含 system [prompt](prompt.md)）；  
- 知识库文档单文件大小不得超过 50 MB，且不支持加密 PDF；  
- 免费额度仅限新注册账号首 30 天，超限后需绑定支付方式（具体计费规则见 [开始使用](../../raw/application-user-guide/start-using.md) 底部说明）；  
- 所有日志与 trace 数据默认保留 7 天，如需长期审计，须主动调用 `/v1/logs/export` 接口导出。

## 来源文档

- [开始使用](../../raw/application-user-guide/start-using.md)


