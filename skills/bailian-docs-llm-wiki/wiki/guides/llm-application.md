# llm application

`llm application` 是百炼平台提供的 LLM 应用构建能力，支持通过低代码/高代码方式快速封装大模型能力为可调用服务。开发者可基于预置模板或自定义逻辑创建智能体、工作流、文件问答等应用类型，并通过 API 或 SDK 集成到业务系统中。该能力依托平台统一的模型路由与上下文管理机制，屏蔽底层模型差异。

## 支持的模型/功能

- 支持的应用类型包括：**智能体应用（Agent 1.0 和 Agent 2.0）**、**工作流应用**、**高代码应用**、**文件问答**  
- 所有应用类型均支持接入平台托管的主流开源及闭源模型（如 Qwen 系列、GLM 系列），具体可用模型列表以控制台「应用配置 → 模型选择」实时下拉项为准  
- 文件问答类应用默认启用向量检索增强（RAG），支持上传 PDF/DOCX/TXT/CSV 等格式，相关实现细节见 [应用开发](../../raw/application-user-guide/llm-application.md)

## 关键参数

- `app_id`: 应用唯一标识，创建后生成，用于 API 调用鉴权与日志追踪  
- `stream`: 布尔值，控制是否启用流式响应（仅对支持流式的模型和应用类型生效）  
- `temperature`: 控制输出随机性，范围 `[0.0, 2.0]`，默认 `0.8`；注意该参数在 Agent 2.0 中可能被内部策略覆盖，详见 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application.md)  
- `max_tokens`: 输出最大 token 数，上限受所选模型 context length 限制  

## 使用方式

1. 在 Model Studio 控制台创建应用，选择对应类型（如「工作流应用」）并完成节点编排  
2. 发布应用获取 `app_id`  
3. 调用 `/v1/applications/{app_id}/chat` 接口（POST），请求体需包含 `input` 字段（字符串或结构化对象，依应用类型而定）  
4. 示例请求（Python）：
   ```python
   import requests
   resp = requests.post(
       "https://dashscope.aliyuncs.com/api/v1/applications/{app_id}/chat",
       headers={"Authorization": "Bearer YOUR_API_KEY"},
       json={"input": {"text": "你好"}}
   )
   ```

> **注意**：文档中提及的「[智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application.md)」已进入维护模式，新项目应优先选用 Agent 2.0；两者在工具调用协议与错误码定义上不兼容，迁移前请务必验证。

## 限制和注意事项

- 单次请求 `input.text` 长度上限为 32768 字符（文件问答类应用的原始文件内容不计入此限）  
- 工作流应用最大节点数为 50，超限时提交失败且无明确提示，建议提前规划流程复杂度  
- 所有应用默认启用输入内容安全审核，若触发拦截将返回 `400 Bad Request` 及 `error.code=InputBlocked`，可通过控制台关闭（不推荐生产环境关闭）  
- 流式响应中 `event: done` 的触发时机与模型实际结束时间可能存在毫秒级偏差，客户端应以完整 `data:` 块拼接为准

## 来源文档

- [应用开发](../../raw/application-user-guide/llm-application.md)


