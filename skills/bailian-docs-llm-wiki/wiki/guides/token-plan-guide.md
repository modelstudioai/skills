# token plan guide

阿里云百炼推出两种订阅制 AI 大模型套餐：**Token Plan 团队版**面向团队/企业场景，以 Credits 统一计量，支持文本生成与图像生成模型，提供团队管理与数据安全保障；**Coding Plan** 面向个人开发者，按模型调用次数计费，价格更低但有频次限制。两者均兼容主流 AI 编程和智能体工具，通过专属 API Key + Base URL 接入。

## Token Plan 团队版

### 产品特点

- **多模型灵活切换**：支持千问、DeepSeek、月之暗面、智谱、MiniMax 等品牌的文本生成与图像生成模型，通过 Credits 统一抵扣
- **多工具兼容**：适配 Claude Code、Cursor、OpenClaw、Hermes Agent、Qwen Code 等主流 AI 编程和智能体工具
- **团队管理**：提供管理后台，支持席位分配与回收、成员用量分析、SSO/钉钉接入
- **数据安全**：承诺不使用对话数据训练模型，多租户隔离架构

> **注意**：Token Plan 团队版目前仅支持**华北2（北京）**地域。

### 支持的模型

Token Plan 团队版采用精确字符串白名单，模型 ID 必须完全匹配，不做版本兼容推理。主要支持的模型包括：

| 品牌 | 模型 ID | 能力 |
|------|---------|------|
| 千问 | qwen3.7-max、qwen3.7-plus、qwen3.6-plus、qwen3.6-flash | 推理/视觉理解/文本生成 |
| 千问 | qwen-image-2.0、qwen-image-2.0-pro | 图像生成 |
| 万相 | wan2.7-image、wan2.7-image-pro | 图像生成 |
| DeepSeek | deepseek-v4-pro、deepseek-v4-flash、deepseek-v3.2 | 推理/文本生成 |
| 月之暗面 | kimi-k2.6、kimi-k2.5 | 推理/视觉理解/文本生成 |
| 智谱 AI | glm-5.2、glm-5.1、glm-5 | 文本生成 |
| MiniMax | MiniMax-M2.5 | 推理/文本生成 |

### 套餐与定价

| 坐席类型 | 价格 | 额度 | 适用场景 |
|----------|------|------|----------|
| 标准坐席 | 198 元/坐席/月 | 25,000 Credits/月 | 轻度使用 |
| 高级坐席 | 698 元/坐席/月 | 100,000 Credits/月 | 日常高频使用 |
| 尊享坐席 | 1,398 元/坐席/月 | 250,000 Credits/月 | 重度依赖 AI |

另有**共享用量包**（5,000 元/个，625,000 Credits），当坐席额度用尽后跨坐席弹性抵扣。Credits 抵扣顺序：坐席月度额度 > 共享用量包 > 全部用尽后服务暂停。详见 [Token Plan（团队版）概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)。

### 快速接入

1. **订阅套餐**：访问 Token Plan 团队版购买页面，选择坐席类型和数量
2. **获取凭证**：在管理后台创建成员并分配席位，系统自动生成 API Key
3. **配置 Base URL**：
   - OpenAI 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
   - Anthropic 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`
4. **接入工具**：在 AI 工具中填入专属 API Key 和 Base URL 即可使用

详见 [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-quickstart.md)。

### 团队管理

团队管理支持通过阿里云控制台或独立管理平台操作，核心功能包括：

- **角色体系**：拥有者、管理员（权限等同拥有者）、成员（仅可使用 API Key 调用模型）
- **成员管理**：手动添加（仅 API 调用）或通过 SSO/钉钉登录（可访问管理平台）
- **席位操作**：分配、回收、加购、升级席位；支持批量操作
- **用量分析**：在管理平台查看 Credits 消耗趋势、模型用量、成员用量明细

SSO 接入支持标准 SAML 2.0 协议对接企业 IdP（如阿里云 IDaaS），钉钉接入需创建企业内部应用并配置回调域名。详见 [团队管理](../../raw/model-user-guide/token-plan-guide/token-plan-team.md)。

## Coding Plan

### 产品特点

Coding Plan 面向个人开发场景，整合千问、GLM、Kimi、MiniMax 模型，按调用次数计费，固定月费模式。

| 项目 | 内容 |
|------|------|
| 价格 | 200 元/月 |
| 支持模型 | qwen3.7-plus、qwen3.6-plus、kimi-k2.5、glm-5、MiniMax-M2.5 等 |
| 用量限制 | 每 5 小时 6,000 次、每周 45,000 次、每月 90,000 次 |
| Base URL（OpenAI） | `https://coding.dashscope.aliyuncs.com/v1` |
| Base URL（Anthropic） | `https://coding.dashscope.aliyuncs.com/apps/anthropic` |

> **注意**：Coding Plan Lite 基础版已于 2026 年 3 月 20 日停止新购，4 月 13 日停止续费与升级。

### Token Plan 团队版与 Coding Plan 的主要区别

| 维度 | Token Plan 团队版 | Coding Plan |
|------|-------------------|-------------|
| 适用场景 | 团队/企业 | 个人开发 |
| 计费方式 | 按 Token 消耗抵扣 Credits | 按模型调用次数 |
| 频次限制 | 无 | 每 5 小时/每周/每月有上限 |
| 图像生成 | 支持 | 不支持 |
| 数据安全 | 不用于模型训练 | 数据用于服务改进 |
| 高峰期 | 多租户隔离，不排队 | 可能排队 |

详见 [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-faq.md)。

## 工具调用与扩展能力

### 模型内置工具

qwen3.7-max、qwen3.7-plus、qwen3.6-plus、qwen3.6-flash 通过 Responses API 内置以下工具，启用后模型自动按需调用，不额外收费：

- 联网搜索、代码解释器、网页抓取、以图搜图、文搜图

### MCP 服务

其他模型可通过百炼 MCP 广场接入工具能力（如联网搜索 MCP）。MCP 服务使用百炼通用 API Key（sk-xxx 格式），与套餐专属 API Key 不同。联网搜索 MCP 前 2,000 次调用免费，之后按 29 元/千次计费。

各工具的 MCP 配置方式大同小异：在工具的配置文件中添加 Streamable HTTP Endpoint 和百炼 API Key 即可。详见 [工具调用](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-tool.md)。

### 图像生成模型接入

图像生成模型（qwen-image-2.0、wan2.7-image 等）使用独立接口，无法通过文本模型 Base URL 直接调用，需通过工具的 Skill 或扩展机制接入。例如在 Claude Code 中创建 `.claude/commands/text-to-image.md` Slash Command，通过 curl 调用多模态生成 API。详见 [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)。

### 视觉理解能力

- qwen3.7-plus、qwen3.6-plus、qwen3.6-flash、kimi-k2.6、kimi-k2.5 原生支持视觉理解，可直接处理图片输入
- glm-5、MiniMax-M2.5 等纯文本模型可通过添加 Skill/Agent 调用视觉模型获得图片理解能力

> **注意**：OpenCode 和 OpenClaw 使用视觉模型时需在配置文件中显式声明 `modalities` 参数（`"input": ["text", "image"]"`），否则无法识别图片。详见 [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/add-vision-skill.md)。

## 常见错误排查

| 错误信息 | 原因 | 解决方案 |
|----------|------|----------|
| 401 InvalidApiKey | API Key 错误或混用 | 确认使用套餐专属 API Key（Token Plan: sk-sp-xxx） |
| 404 model not found | 模型名称拼写错误或不在支持列表 | 按白名单精确匹配模型 ID |
| 401 invalid access token | Base URL 与套餐不匹配 | 使用对应套餐的专属 Base URL |
| 429 rate limit exceeded | 请求过于密集 | 等待后重试，确认 API Key 未被共享 |
| 429 quota exceeded | 额度用尽 | 加购共享用量包或等待下一计费周期 |
| 400 Range of input length | 输入超出上下文限制 | 新建会话或使用 `/compact` 压缩上下文 |

## 使用限制

- **仅限交互式使用**：不可用于自动化脚本或应用后端，违规可能导致订阅暂停或 API Key 封禁
- **账号不可共享**：API Key 仅限分配的成员本人使用
- **API Key 不互通**：Token Plan 团队版、Coding Plan、百炼按量计费三者的 API Key 和 Base URL 互不兼容，切勿混用

## 来源文档

- [Token Plan（团队版）概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-quickstart.md)
- [团队管理](../../raw/model-user-guide/token-plan-guide/token-plan-team.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-faq.md)
- [工具调用](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-tool.md)
- [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)
- [Coding Plan概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)
- [联网搜索](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/web-search-for-coding-plan.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)
- [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/add-vision-skill.md)


