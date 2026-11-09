# prompt

Prompt 是百炼平台中用于引导大模型生成预期输出的核心输入文本，其设计质量直接影响模型响应的准确性、相关性和可控性。开发者可通过结构化提示词（如角色设定、任务指令、示例演示）显式约束模型行为，适用于问答、摘要、代码生成等多种场景。平台提供 Prompt 自动优化与样例库等辅助能力，降低人工调优成本。

## 支持的模型与功能

所有百炼平台支持的大语言模型（包括 Qwen 系列、Baichuan、GLM 等）均兼容标准文本 prompt 输入。除基础 prompt 外，平台还支持：
- **Prompt 自动优化**：基于历史调用数据和反馈自动重写 prompt，提升任务完成率 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)；
- **Prompt 样例库**：提供覆盖 20+ 垂直场景（如客服话术生成、法律条款解析）的可复用 prompt 模板 [Prompt样例库](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)；
- **多轮对话上下文管理**：通过 `messages` 数组格式支持 system/user/assistant 角色交替的 prompt 构建，适用于对话类应用。

## 关键参数

调用 API 时，prompt 相关核心参数如下：

| 参数 | 类型 | 说明 |
|------|------|------|
| `prompt` | string | （已弃用）仅兼容旧版单字符串输入；新接口必须使用 `messages` |
| `messages` | array | 推荐方式，每个元素含 `role`（"system"/"user"/"assistant"）和 `content` 字段；system message 用于设定全局角色或约束，优先级最高 |
| `stop` | array<string> | 指定停止生成的 token 序列（如 `["\n\n", "<|eot_id|>"]`），影响 prompt 截断行为 |

> **注意**：原始文档 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md) 中提及“支持对 `prompt` 字符串直接优化”，但该字段已在 v3.2+ API 中标记为 deprecated；实际优化仅作用于 `messages` 结构，开发者应迁移至结构化输入。

## 使用方式

1. **基础用法**：构造 `messages` 数组，至少包含一个 `"role": "user"` 条目：
   ```json
   {
     "messages": [
       {"role": "system", "content": "你是一名资深Python工程师，只输出可运行代码，不加解释。"},
       {"role": "user", "content": "写一个快速排序函数"}
     ]
   }
   ```

2. **启用自动优化**：在请求中添加 `"enable_prompt_optimization": true`，平台将基于任务类型和历史效果动态调整 prompt 结构 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)。

3. **复用样例**：从 [Prompt样例库](../../raw/application-user-guide/prompt/prompt-sample-optimization.md) 获取模板后，替换占位符（如 `{{input}}`）并注入 `messages.content`。

## 限制和注意事项

- 单次请求 `messages` 总长度（字符数）上限为 32768；超长 prompt 将被截断，建议优先压缩 system message；
- `system` 角色消息不可为空，且不应包含用户敏感信息（如 PII），因其可能参与模型内部 attention 计算；
- 启用 `enable_prompt_optimization` 后，实际下发至模型的 prompt 可能与原始输入不同，调试时需通过响应头 `X-Prompt-Optimized` 查看优化后版本；
- 避免在 prompt 中嵌入未经转义的 JSON 特殊字符（如双引号、换行符），否则可能导致解析失败——此限制在 [Prompt样例库](../../raw/application-user-guide/prompt/prompt-sample-optimization.md) 的“安全编码规范”章节有明确示例。

## 来源文档

- [Prompt](../../raw/application-user-guide/prompt.md)


