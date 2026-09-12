# llm application

`llm application` 是百炼平台中用于封装和部署大语言模型能力的核心应用类型，支持从低代码智能体到高代码定制化服务的多种形态。开发者可通过配置或编码方式快速构建面向终端用户的 LLM 服务，适用于对话、问答、工作流编排等场景。所有应用均运行在百炼统一的推理与调度基础设施之上。

## 支持的模型/功能

- **智能体应用（Agent）**：分为 Agent 1.0（基础单步调用）和 Agent 2.0（支持多工具协同、状态管理与异步执行），详见 [应用开发](../../raw/application-user-guide/llm-application.md)  
- **工作流应用**：通过可视化节点编排实现多模型/多步骤逻辑，支持条件分支、循环与外部 API 集成  
- **高代码应用**：允许开发者上传自定义 Python 代码（含 FastAPI 入口），完全控制输入/输出协议与业务逻辑  
- **文件问答应用**：专用于文档解析与[检索增强生成](../concepts/rag.md)（RAG），支持 PDF/Word/Excel 等格式，底层调用百炼内置文档解析引擎  

> **注意**：[应用开发](../../raw/application-user-guide/llm-application.md) 中提及的“新版智能体应用（Agent 2.0）”已全面替代 Agent 1.0，后者仅保留兼容性支持，新项目应优先使用 Agent 2.0。

## 关键参数

- `model_id`：必需，指定后端使用的模型 ID（如 `qwen-max`, `qwen-plus`），需与应用类型兼容（例如 Agent 2.0 要求模型支持 function calling）  
- `input_schema`：可选，JSON Schema 格式，用于声明输入字段结构与校验规则，影响前端表单生成与 API 参数校验  
- `output_schema`：可选，同上，用于约束输出结构并支持自动 JSON 解析  
- `timeout`：默认 30s，最大支持 300s；工作流应用中各节点可单独设置超时  

## 使用方式

1. **控制台创建**：进入 Model Studio → 应用管理 → 新建应用 → 选择类型（如“智能体应用”）→ 配置模型、提示词、工具等 → 发布  
2. **API 调用**：发布后获取 `app_id`，通过 `/v1/applications/{app_id}/chat` 接口发起请求（需携带 `Authorization: Bearer <api_key>`）  
3. **SDK 集成**：推荐使用 `dashscope` Python SDK（v1.18.0+），调用 `Application.call()` 方法，自动处理鉴权、重试与流式响应解析，参考 [应用开发](../../raw/application-user-guide/llm-application.md) 中的示例代码片段  

## 限制和注意事项

- 单次请求最大上下文长度受所选模型限制（如 `qwen-max` 为 32768 tokens），应用层不额外截断，需自行控制输入长度  
- 文件问答应用单次上传文件总数 ≤ 10，总大小 ≤ 50MB；解析后的文本块将按 chunk size（默认 512）切分并索引  
- Agent 2.0 应用不支持直接调用非百炼托管的外部模型（如自部署 vLLM 实例），如需混合调度，须通过高代码应用封装  
- 所有应用默认启用敏感词过滤与内容安全审核，不可关闭；若需绕过（如内部测试），需提交工单申请白名单，详见 [应用开发](../../raw/application-user-guide/llm-application.md) 的“安全策略”章节

## 来源文档

- [应用开发](../../raw/application-user-guide/llm-application.md)



