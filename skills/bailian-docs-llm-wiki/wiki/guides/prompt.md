# prompt

Prompt 是百炼平台中用于引导大模型生成预期输出的核心输入机制，支持模板化、自动化优化与人工反馈迭代。开发者可通过结构化 Prompt 设计提升模型响应的准确性、一致性与可控性。所有 Prompt 功能均依托于百炼统一的推理服务接口，与模型选型深度解耦。

## 支持的模型与功能

当前所有百炼托管模型（包括 Qwen 系列、Baichuan、GLM 等）均原生支持 Prompt 输入，无需额外适配。核心功能包括：  
- **Prompt 模板管理**：提供预置模板库与自定义模板能力，支持变量占位符（如 `{{input}}`）和多轮上下文注入；  
- **自动优化**：基于历史调用日志与反馈数据，对低效 Prompt 进行语义重写与结构精简；  
- **反馈驱动优化**：允许用户对单次响应标注“有用/无用”，系统据此微调模板权重 [Prompt自动优化](../../raw/application-user-guide/prompt.md)；  
- **样例库集成**：内置覆盖客服、摘要、代码生成等场景的 Prompt 样例，可一键复用或二次编辑 [Prompt样例库](../../raw/application-user-guide/prompt.md)。

## 关键参数

在 API 调用或控制台配置中，以下参数直接影响 Prompt 行为：  
- `prompt_template_id`（string）：指定模板 ID，为空时使用默认模板；  
- `variables`（object）：传入模板中占位符对应的键值对，如 `{"input": "总结下文", "context": "..."}`；  
- `enable_optimization`（boolean）：启用后触发实时自动优化逻辑，仅对已标记为“生产环境”的模板生效；  
- `temperature` / `top_p` 等采样参数仍独立作用于模型层，不改变 Prompt 解析逻辑。  
> **注意**：`enable_optimization` 在 v3.2+ 版本中默认关闭，旧版文档中“默认开启”描述已过时，请以 [自定义Prompt模板](../../raw/application-user-guide/prompt.md) 中最新参数说明为准。

## 使用方式

1. **控制台操作**：进入「应用开发」→「Prompt 管理」，创建/导入模板，设置变量映射后绑定至 API 端点；  
2. **API 调用**：在 `/v1/chat/completions` 请求体中，将完整 Prompt 字符串（或模板 ID + variables）置于 `messages[0].content` 字段；  
3. **SDK 集成**：Python SDK 提供 `PromptTemplate.render()` 方法渲染变量，返回标准消息格式，兼容所有百炼模型客户端。

## 限制和注意事项

- 单次请求中 `messages[0].content` 的 Prompt 总长度（含变量展开后）不得超过 8192 token，超长将被截断并返回警告；  
- 自动优化功能依赖至少 50 条有效反馈样本，新模板首次启用需预留冷启动周期；  
- 模板中禁止嵌入可执行代码或外部 HTTP 调用指令，该类内容将被安全网关拦截；  
- 所有 Prompt 操作均受项目级权限控制，`prompt:read` 和 `prompt:manage` 权限需显式授予。

## 来源文档

- [Prompt](../../raw/application-user-guide/prompt.md)



