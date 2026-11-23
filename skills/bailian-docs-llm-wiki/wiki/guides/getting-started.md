# getting started

百炼平台提供统一的 CLI 工具，用于快速调用大模型服务、管理资源及调试提示词。本文档面向开发者，说明如何完成基础配置并发起首次请求。所有操作均基于 `bailian` CLI v2.0+，需配合有效的 API Key 使用。

## 支持的模型/功能

当前 CLI 支持调用百炼平台托管的全部公开模型（如 Qwen 系列、Baichuan、GLM 等）及部分私有微调模型（需对应权限）。支持的功能包括：文本生成（`chat`）、流式响应（`--stream`）、多轮会话管理（`--session-id`）、以及结构化输出（`--response-format json`）。模型列表与能力详情请参考 [开始使用](../../raw/cli/getting-started.md) 中的[概览](../../raw/cli/getting-started/overview.md)章节。

## 关键参数

必填参数为 `--model` 和 `--prompt`；常用可选参数包括：
- `--temperature`（默认 0.8，范围 0.0–2.0）
- `--max-tokens`（默认 1024）
- `--top-p`（默认 1.0）
- `--stop`（支持字符串或字符串数组，如 `--stop "\n" --stop "END"`）

> **注意**：`--top-k` 参数在 [安装与鉴权](../../raw/cli/getting-started/installation.md) 文档中被列为支持，但实际 v2.1.3 版本 CLI 尚未实现该参数，启用将报错 `unknown flag: --top-k`。请以 `bailian chat --help` 输出为准。

## 使用方式

1. 安装 CLI：`pip install bailian-cli`
2. 配置鉴权：`bailian configure --api-key <your_key>`（密钥可通过 [控制台 → API 密钥管理](https://bailian.console.aliyun.com) 获取）
3. 发起请求：  
   ```bash
   bailian chat --model qwen-max --prompt "你好，请用中文简要介绍你自己"
   ```

完整流程与错误排查见 [快速开始](../../raw/cli/getting-started/quickstart.md)。

## 限制和注意事项

- 单次请求 `--max-tokens` 不得超过模型上下文窗口的 90%（例如 qwen-plus 上限为 32k tokens，则最大设为 28800）
- 免费试用额度仅限新用户首月，超限后请求将返回 `429 Too Many Requests`
- 流式响应不支持 `--response-format json`，二者同时指定将导致解析失败  
- 所有请求默认启用服务端缓存，如需禁用，请显式添加 `--no-cache` 参数（详见 [开始使用](../../raw/cli/getting-started.md) 的[安装与鉴权](../../raw/cli/getting-started/installation.md)附录说明）

## 来源文档

- [开始使用](../../raw/cli/getting-started.md)


