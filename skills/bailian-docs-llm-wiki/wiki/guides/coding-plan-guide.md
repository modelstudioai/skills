# coding plan guide

Coding Plan 是百炼平台面向代码生成任务提供的结构化推理能力，支持将自然语言需求拆解为可执行的编码步骤，并按计划逐步生成代码。该能力适用于复杂逻辑实现、多文件工程构建及需分步验证的开发场景。开发者需通过特定参数启用并控制其行为。

## 支持的模型与功能

当前仅 `qwen-coder-32b` 和 `qwen2.5-coder-32b` 模型原生支持 Coding Plan 功能；其他模型（如 `qwen-plus` 或 `qwen-max`）调用时将自动降级为普通代码生成，不触发计划模式。该功能默认关闭，需显式启用 `enable_coding_plan: true` 参数。详细支持列表见 [Coding Plan概述](../../raw/token-plan-user-guide/coding-plan-guide.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `enable_coding_plan` | boolean | 是 | 启用 Coding Plan 推理流程；设为 `true` 后模型将先输出 plan 步骤，再逐条生成代码 |
| `max_plan_steps` | integer | 否 | 最大计划步数，默认为 8，上限为 12；超出后终止 plan 阶段并进入 fallback 生成 |
| `plan_temperature` | float | 否 | Plan 阶段采样温度，默认 0.3，建议保持较低值以保障步骤逻辑严谨性 |

> **注意**：`plan_temperature` 与主生成阶段的 `temperature` 独立控制；旧版文档中曾建议统一设置，但 [Coding Plan概述](../../raw/token-plan-user-guide/coding-plan-guide.md) 已明确二者分离，以避免计划发散。

## 使用方式

在 API 请求中添加 `extra_parameters` 字段：

```json
{
  "model": "qwen2.5-coder-32b",
  "input": { "prompt": "实现一个支持增删查改的内存数据库 CLI 工具" },
  "parameters": {
    "enable_coding_plan": true,
    "max_plan_steps": 6
  }
}
```

响应体中将包含 `plan` 字段（数组形式的步骤描述）和 `steps` 字段（各步对应代码块），结构详见 [常见问题](../../raw/token-plan-user-guide/coding-plan-guide.md) 中的响应示例。

## 限制和注意事项

- 单次请求最大上下文长度为 32k tokens，其中 plan 步骤本身计入上下文，过长 plan 可能挤压代码生成空间；
- 不支持流式响应（`stream: true`），启用 Coding Plan 时必须禁用流式；
- 输入 [prompt](prompt.md) 中若含明确“只输出 plan 不要写代码”等指令，将导致 plan 阶段提前终止，且不进入代码生成——此行为与 [Coding Plan概述](../../raw/token-plan-user-guide/coding-plan-guide.md) 一致，但与部分早期 SDK 示例存在偏差，请以该文档为准。

## 来源文档

- [Coding Plan（旧版）](../../raw/token-plan-user-guide/coding-plan-guide.md)


