# getting started

百炼平台提供命令行工具（bailian-cli）作为开发者快速接入模型服务的轻量级方式，适用于本地调试、脚本集成与自动化任务。本文档指导你完成环境准备、身份认证及首次调用，所有操作均基于 CLI v2.3+ 版本。如需更底层控制，可直接调用 [REST API](../../raw/api/overview.md)。

## 支持的模型与功能

当前 CLI 支持调用百炼平台托管的主流大语言模型（如 Qwen 系列、Baichuan、GLM），以及内置的文本生成、结构化输出（JSON Schema）、流式响应和多轮对话管理功能。图像理解（多模态）与[函数调用](../concepts/function-calling.md)（Function Calling）暂未通过 CLI 暴露，需使用 SDK 或直接调用 [REST API](../../raw/api/overview.md)。模型列表以 [概览](../../raw/cli/getting-started/overview.md) 中实时更新为准。

## 关键参数

- `--model`: 必填，指定模型 ID（如 `qwen-max`, `qwen-plus`），不支持别名或模糊匹配  
- `--input`: 必填，原始输入文本；若需多轮对话，须用 `--history` 传入 JSON 格式历史记录  
- `--stream`: 布尔值，启用[流式输出](../concepts/streaming-output.md)（仅限终端交互，不适用于管道重定向）  
- `--temperature`, `--top_p`, `--max_tokens`: 数值型采样参数，语义与 [REST API](../../raw/api/overview.md) 一致  
> **注意**：`--max_tokens` 在 CLI 中默认为 `1024`，而 [REST API](../../raw/api/overview.md) 默认为 `2048`，实际生成长度以服务端限制为准。

## 使用方式

1. **安装与鉴权**：执行 `pip install bailian-cli`，然后运行 `bailian configure` 并按提示输入 API Key 和 Region（如 `cn-beijing`）——详细步骤见 [安装与鉴权](../../raw/cli/getting-started/installation.md)  
2. **首次调用**：  
   ```bash
   bailian chat --model qwen-plus --input "你好，请用中文简要介绍你自己"
   ```  
3. **进阶用法**：结合 `--history` 实现上下文保持，或使用 `bailian list-models` 查询可用模型——参考 [快速开始](../../raw/cli/getting-started/quickstart.md)

## 限制和注意事项

- 单次请求 `--input` 长度上限为 32768 字符；超出部分将被截断且无警告  
- CLI 不支持异步任务提交（如长文本摘要、批量推理），此类场景请改用 [REST API](../../raw/api/overview.md) 的 `/v1/jobs` 接口  
- 所有请求默认超时时间为 60 秒，不可配置；如遇 `TimeoutError`，建议检查网络或降级至更轻量模型  
> **注意**：[安装与鉴权](../../raw/cli/getting-started/installation.md) 中提到的 `bailian configure --profile` 多配置文件功能，在 v2.3.1 中存在 profile 切换失效问题，该缺陷已在 v2.4.0 修复，建议升级 CLI 至最新版。

## 来源文档

- [开始使用](../../raw/cli/getting-started.md)


