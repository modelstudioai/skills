# prompt

Prompt 是百炼平台中用于引导大模型生成预期输出的核心输入文本，其设计质量直接影响模型响应的准确性、相关性和可控性。开发者可通过结构化提示词（如角色设定、任务指令、示例演示）显式约束模型行为。所有支持的模型均通过统一 API 接收 prompt 输入，但具体解析逻辑与能力边界因模型而异。

## 支持的模型与功能

当前百炼平台所有公开模型（包括 Qwen 系列、Baichuan、GLM 等）均支持标准 prompt 输入。除基础文本生成外，还支持以下高级功能：  
- **Prompt 自动优化**：基于历史调用数据与反馈自动重写 prompt，提升任务完成率（详见 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)）；  
- **Prompt 样例库**：提供覆盖客服、摘要、代码生成等场景的可复用 prompt 模板（详见 [Prompt样例库](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)）；  
- **多轮对话上下文管理**：在 `/v1/chat/completions` 接口中，prompt 以 `messages` 数组形式传入，系统自动维护会话状态。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型 ID，如 `qwen-max`、`qwen-plus`，决定 prompt 解析策略 |
| `messages` | array | 是（chat 接口） | 每项含 `role`（`system`/`user`/`assistant`）和 `content` 字段；`system` 角色内容即为全局 prompt 指令 |
| `prompt` | string | 是（completion 接口） | 纯文本 prompt，不支持 role 分隔，适用于非对话场景 |
| `temperature` | number | 否 | 控制输出随机性（0.0–2.0），高值易导致 prompt 意图漂移 |

> **注意**：`system` 消息在部分旧版模型（如 `qwen-turbo` v2023.12）中可能被忽略，实际行为请以 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md) 中的兼容性说明为准。

## 使用方式

1. **构造 prompt**：优先使用 `messages` 格式，将角色设定（`system`）、用户请求（`user`）和参考回复（`assistant`）分层组织；  
2. **调用 API**：  
   - 对话类任务：POST `/v1/chat/completions`，传入 `messages`；  
   - 补全类任务：POST `/v1/completions`，传入 `prompt` 字符串；  
3. **验证效果**：建议先在控制台调试，再结合 [Prompt样例库](../../raw/application-user-guide/prompt/prompt-sample-optimization.md) 中的基准用例比对输出一致性。

## 限制与注意事项

- 单次请求 `messages` 总长度（token）上限为模型 context length 的 90%，超出将触发截断且无警告；  
- `system` 消息内容长度超过 512 字符时，部分模型可能降权处理，不保证完整遵循；  
- 避免在 prompt 中嵌入未声明的变量占位符（如 `{input}`），百炼不提供运行时模板渲染，该行为未在 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md) 中定义，属非标准用法。

## 来源文档

- [Prompt](../../raw/application-user-guide/prompt.md)


