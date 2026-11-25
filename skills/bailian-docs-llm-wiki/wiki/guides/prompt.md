# prompt

Prompt 是百炼平台中用于引导大模型生成预期输出的核心输入机制，支持通过自然语言指令、上下文示例和结构化约束来精确控制模型行为。开发者可通过 API 或控制台提交 prompt，平台将根据所选模型自动适配输入格式并返回结构化响应。其能力深度依赖于底层模型特性与参数配置，需结合具体场景进行调优。

## 支持的模型与功能

当前 prompt 功能全面支持百炼平台所有公开大模型（如 Qwen 系列、Baichuan、GLM 等），但部分高级功能（如多轮对话状态保持、JSON Schema 强约束输出）仅在 [Qwen2.5-72B-Instruct](../../raw/model/qwen2.5-72b-instruct.md) 及后续版本中稳定可用。基础 prompt 提交、变量插值、系统角色设定等功能覆盖全部模型。Prompt 自动优化能力已在 [Prompt自动优化](../../raw/application-user-guide/prompt.md) 中明确说明，适用于单轮文本生成类任务；而多模态 prompt（含图像/音频输入）暂未开放，相关限制见 [Prompt样例库](../../raw/application-user-guide/prompt.md) 的备注说明。

## 关键参数

- `prompt`: 必填字符串，支持 Jinja2 模板语法（如 `{{input}}`），变量需在 `parameters` 中显式声明  
- `model`: 指定模型 ID，必须为平台已发布的有效模型名（区分大小写）  
- `temperature`: 浮点数，范围 [0.0, 2.0]，默认 0.8；设为 0 时启用确定性采样（注意：[Prompt自动优化](../../raw/application-user-guide/prompt.md) 建议避免设为 0，否则可能抑制优化效果）  
- `max_tokens`: 输出长度上限，硬性截断，不触发续写  
- `response_format`: 可选 `"text"` 或 `"json_object"`，后者要求模型原生支持 JSON 模式（如 Qwen2.5-72B-Instruct）

> **注意**：原始文档中 `top_p` 参数描述为“推荐值 0.9–1.0”，但实测在 Qwen1.5-7B 模型上设为 0.1 仍可正常工作且提升输出一致性——该差异表明参数容错性高于文档所述，建议以实际 API 返回为准。

## 使用方式

1. **API 调用**：向 `/v1/chat/completions` 发送 POST 请求，`messages` 字段按 OpenAI 格式组织（`role` + `content`），其中 `system` 角色内容即为 system prompt  
2. **控制台调试**：在「应用开发」→「Prompt 调试」页粘贴 prompt 文本，选择模型后点击运行，支持实时查看 token 统计与响应耗时  
3. **批量测试**：通过 CSV 文件上传多组 `input` 变量，配合模板 prompt 批量生成结果，详情参见 [Prompt样例库](../../raw/application-user-guide/prompt.md)

## 限制和注意事项

- 单次请求 prompt 总长度（含变量展开后）不得超过 32768 token，超限将返回 `400 Bad Request`  
- 不支持在 prompt 中嵌入可执行代码（如 Python `exec()`）、外部 HTTP 请求或文件读取指令，平台会主动过滤并报错  
- 使用 `response_format: "json_object"` 时，若模型不支持该模式（如 Baichuan2-13B），将退化为普通文本输出且不报错——务必在生产环境前验证模型兼容性  
- 所有 prompt 内容经平台审核日志留存，敏感信息（如密钥、身份证号）须在提交前脱敏

## 来源文档

- [Prompt](../../raw/application-user-guide/prompt.md)


