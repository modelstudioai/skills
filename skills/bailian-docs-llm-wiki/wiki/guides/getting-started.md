# getting started

百炼平台提供统一的 API 接口与 CLI 工具，支持快速接入大模型能力。本文档面向开发者，说明基础使用路径、关键配置项及约束条件，帮助你在 5 分钟内完成首次调用。所有操作均需通过 API Key 鉴权，且默认启用流式响应。

## 支持的模型/功能

当前平台支持以下核心模型（截至 v2.3.0）：
- 文本生成：`qwen-max`、`qwen-plus`、`qwen-turbo`
- 多模态理解：`qwen-vl-plus`（需显式指定 `input.image_urls`）
- [函数调用](../concepts/function-calling.md)（Function Calling）：仅 `qwen-max` 和 `qwen-plus` 支持，需传入 `tools` 参数并启用 `tool_choice`

> **注意**：`qwen-turbo` 不支持[函数调用](../concepts/function-calling.md)或图像输入，该限制在 [开始使用](../../raw/cli/getting-started.md) 中未明确说明，但已在 [模型能力矩阵](../../raw/models/capabilities.md) 中确认。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型 ID，必须与平台当前可用列表一致，详见 [模型能力矩阵](../../raw/models/capabilities.md) |
| `input.messages` | array | 是 | 至少包含一个 `role: "user"` 的 message 对象，`content` 支持字符串或结构化数组（含 `text`/`image_url`） |
| `parameters.temperature` | number | 否 | 默认 `0.8`，取值范围 `[0.0, 1.0]`；设为 `0` 时启用确定性采样 |

## 使用方式

1. **安装 CLI**：运行 `pip install aliyun-bailian`（Python ≥ 3.8），详细步骤见 [安装与鉴权](../../raw/cli/getting-started.md)  
2. **配置凭证**：设置环境变量 `BAI_LIAN_API_KEY` 或通过 `bailian configure` 交互式录入  
3. **发起请求**：  
   ```bash
   bailian chat --model qwen-turbo --message "你好"
   ```
   或调用 REST API（POST `/v1/chat/completions`），参考 [快速开始](../../raw/cli/getting-started.md)

## 限制和注意事项

- 单次请求 `input.messages` 最多 10 条，总 token 数上限为模型 context length 的 90%（例如 `qwen-max` 为 32k → 实际上限约 28.8k）  
- 图像输入仅支持公网可访问的 HTTPS URL，不支持本地文件或 Base64；该要求在 [开始使用](../../raw/cli/getting-started.md) 的示例中未体现，但为实际运行必需  
- 流式响应（`stream: true`）下，`usage` 字段仅在最终 `data: [DONE]` 帧中返回，中间 chunk 不含 token 统计  

> **注意**：文档中提及的 `bailian init` 命令已废弃（v2.2.0 起），应统一使用 `bailian configure`，该变更未同步更新至 [开始使用](../../raw/cli/getting-started.md)，请以 CLI `--help` 输出为准。

## 来源文档

- [开始使用](../../raw/cli/getting-started.md)


