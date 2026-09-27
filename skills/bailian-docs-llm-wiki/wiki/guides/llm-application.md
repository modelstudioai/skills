# llm application

`llm application` 是百炼平台提供的核心应用构建能力，用于将大语言模型能力封装为可部署、可调用的服务。它支持多种应用范式，覆盖从低代码智能体到高代码定制的全场景需求，适用于对话服务、自动化流程、文档分析等典型 LLM 应用场景。开发者可通过控制台或 API 快速创建、配置并发布应用。

## 支持的模型与功能

- **应用类型**：当前支持五类应用：智能体应用（含 Agent 1.0 和新版 Agent 2.0）、工作流应用、高代码应用、文件问答应用。各类型能力边界与适用场景详见 [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)。
- **模型兼容性**：所有应用类型均支持平台已接入的全部公开及私有 LLM（如 Qwen 系列、Qwen-VL、Qwen-Audio），但部分高级功能（如多模态工具调用）仅在 Agent 2.0 中完整支持，[新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md) 文档明确列出其增强能力。
- > **注意**：[智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md) 文档中描述的“自动工具发现”机制已被弃用，实际运行时依赖显式配置的工具列表，该差异已在 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md) 中统一修正。

## 关键参数

- `model_id`：必需，指定底层推理模型 ID（如 `qwen-max`），必须与所选应用类型兼容。
- `prompt_template`：可选，自定义系统提示词模板；工作流应用和高代码应用中该字段被忽略，由节点逻辑控制。
- `tools`：仅 Agent 类型应用有效，为工具列表数组，每个工具需包含 `name`、`description` 和 `parameters`（OpenAPI Schema 格式）。
- `streaming`：布尔值，控制响应是否流式返回；文件问答应用默认强制启用流式，不可关闭。

## 使用方式

- **控制台创建**：进入「应用开发」→「新建应用」→ 选择类型 → 配置模型、提示词、工具（如适用）→ 发布。
- **API 调用**：通过 `/v1/applications` 创建应用，再使用 `/v1/chat/completions`（带 `app_id`）发起推理请求。完整参数与示例见 [应用开发](../../raw/application-user-guide/llm-application.md) 主文档。
- **调试建议**：首次部署后，务必在控制台「测试」页验证工具调用链路与文件解析结果，尤其对文件问答应用，需确认上传文件格式（仅支持 PDF/TXT/DOCX/MD）与编码（UTF-8）符合要求。

## 限制和注意事项

- 单次请求最大上下文长度受所选 `model_id` 原生限制约束，应用层不额外截断；超长 [prompt](prompt.md) 将直接触发模型侧报错。
- 文件问答应用单次最多处理 10 个文件，总大小不超过 50 MB；超出限制将拒绝上传，不触发后台静默裁剪。
- 所有应用默认开启敏感词过滤（基于平台级策略），无法在应用维度关闭；如需绕过，须申请白名单权限并单独配置 `sensitive_check: false`（仅限高代码应用且需审批）。

## 来源文档

- [应用开发](../../raw/application-user-guide/llm-application.md)


