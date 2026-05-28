# token plan guide

Token Plan 团队版是面向开发团队与企业用户的 AI 大模型订阅服务，采用 Credits 统一计量体系，覆盖主流文本推理、视觉理解与图像生成模型。该服务提供独立的 API 通道与团队化管理后台，旨在为日常 AI 辅助编程、智能体交互提供平稳运行且预算可控的调用环境。

## 支持的模型与功能
Token Plan 严格限定在以下已适配的模型列表内调用，不支持列表外模型：
* **深度推理与文本生成**：`qwen3.7-max`、`qwen3.6-plus`、`qwen3.6-flash`、`deepseek-v4-pro`/`flash`、`deepseek-v3.2`、`kimi-k2.6`/`k2.5`、`MiniMax-M2.5`、`glm-5.1`/`glm-5`。
* **多模态/图像生成**：`qwen-image-2.0`/`2.0-pro`、`wan2.7-image`/`image-pro`。

功能架构上，服务通过标准 API 协议提供能力，详细说明参考 [Token Plan（团队版）概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)。针对 `qwen3.7-max`/`plus`/`flash`，模型内置联网搜索、代码解释器与网页抓取等工具，启用后自动触发且不计额外费用；其他模型需通过外挂 [[mcp-service]] 扩展能力。

## 关键参数与计费机制
* **专属 Base URL**：
  * OpenAI 兼容协议：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
  * Anthropic 兼容协议：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`
* **专属 API Key**：格式为 `sk-sp-xxx`，由管理员在 [[team-management]] 分配席位后生成。
* **Credits 消耗模型**：单次请求消耗由输入 Token、缓存 Token 与输出 Token 动态计算。实际抵扣优先级为：坐席月度套餐额度 → 共享用量包（多包时优先抵扣最早到期包） → 额度耗尽后服务暂停。配置细节见 [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-quickstart.md)。
> **注意**：各模型单价及缓存策略可能随平台调整，实际消耗请以账单为准。套餐与共享包额度均按自然月或订阅周期重置，**当月未用额度不累积**，过期自动清零。

## 使用方式
1. **订阅与成员接入**：在购买页选择坐席档位后，进入管理后台添加成员。支持手动创建或通过 SAML 2.0/钉钉 SSO 同步身份。分配席位后系统生成专属 `sk-sp-xxx` Key。
2. **工具端配置**：在兼容的 AI 编程客户端（如 [[claude-code]]、[[opencode]]、[[cursor]] 等）中将 Provider 的 Base URL 替换为上述端点，并填入专属 API Key。
3. **图像生成接入**：文生图模型使用独立接口 `api/v1/services/aigc/multimodal-generation/generation`。需通过客户端扩展机制（Slash Command、Skill 或 Agent）编写脚本调用，不可直接走文本流协议。
4. **工具扩展（MCP）**：为 `deepseek`、`glm` 等模型接入联网搜索等外部能力时，需在百炼控制台开通对应服务。**此处鉴权必须使用百炼通用 API Key（`sk-xxx` 格式）**，具体配置逻辑与示例参考 [工具调用](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-tool.md)。

## 限制与注意事项
* **调用场景限制**：仅限在兼容的 AI 编程与智能体工具中进行**交互式对话**。严禁用于自动化脚本、后端服务批量调用或任何非交互场景，违规将触发封禁。
* **地域与网络**：服务当前仅部署于**华北2（北京）**。跨地域或海外调用需开发者自行处理网络延迟与合规要求。
* **数据安全**：采用多租户隔离架构，平台承诺不将对话数据用于模型训练。传输全链路 HTTPS 加密。
* **退款策略**：预付费订阅模式，**不支持退款或中途退订**。购买前请充分评估团队用量。
> **注意**：Token Plan 与 [[coding-plan]] 为完全独立的产品线，切勿混淆。Coding Plan 按请求次数计费且设有时窗/周/月硬性限额，高峰期需排队且用户数据授权用于模型优化；Token Plan 无频次限制、调用平稳且严格数据隔离。两者的 Base URL 与 API Key 体系完全隔离，混用会导致鉴权报错（如 `InvalidApiKey` 或 `invalid access token`）或异常扣费，配置时请务必核对端点域名与 Key 前缀。

## 来源文档

- [Token Plan（团队版）概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-quickstart.md)
- [团队管理](../../raw/model-user-guide/token-plan-guide/token-plan-team.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-faq.md)
- [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)
- [工具调用](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-tool.md)
- [Coding Plan概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)
- [联网搜索](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/web-search-for-coding-plan.md)
- [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/add-vision-skill.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)

