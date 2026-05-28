# 快速开始

三步完成 Token Plan 团队版订阅和接入：选择套餐、获取 API Key、配置 AI 工具。

## **步骤一：订阅 Token Plan 团队版**

访问 [Token Plan 团队版购买页面](https://common-buy.aliyun.com/token-plan/)，选择坐席类型和数量并完成订阅，主账号和 RAM 账号均可订阅。

## **步骤二：获取 API Key 和 Base URL**

-   **API Key**：在[管理后台](https://tokenplan-enterprise.bailian.console.aliyun.com)创建成员账号（账号格式：英文字母、数字、下划线，不能以数字开头），分配席位后，为成员生成 API Key。详见[团队管理](https://help.aliyun.com/zh/model-studio/token-plan-team)。
    
-   **Base URL**：根据 AI 工具支持的协议，选择对应的 Base URL。
    

**协议**

**Base URL**

OpenAI 兼容

`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`

Anthropic 兼容

`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`

## **步骤三：接入 AI 工具**

 [**OpenClaw**开源、自托管个人 AI 助手](https://help.aliyun.com/zh/model-studio/openclaw)

 [**Hermes Agent**开源 AI 代理框架，内置自学习循环](https://help.aliyun.com/zh/model-studio/hermes-agent)

 [**Claude Code**AI 终端编码助手，支持自然语言编程](https://help.aliyun.com/zh/model-studio/claude-code)

 [**OpenCode**开源 AI 编程代理工具](https://help.aliyun.com/zh/model-studio/opencode)

 [**Cursor**AI 原生代码编辑器](https://help.aliyun.com/zh/model-studio/cursor)

 [**Codex**OpenAI 推出的命令行编程工具](https://help.aliyun.com/zh/model-studio/codex)

 [**Qwen Code**开源命令行 AI 编码工具](https://help.aliyun.com/zh/model-studio/qwen-code)

 [**Cherry Studio**多模型桌面客户端](https://help.aliyun.com/zh/model-studio/cherry-studio)

 [**Chatbox**跨平台 AI 桌面客户端](https://help.aliyun.com/zh/model-studio/chatbox)

 [**Cline**VS Code 扩展，智能代码补全和调试](https://help.aliyun.com/zh/model-studio/cline)

 [**Qoder**面向真实软件开发的 Agentic 编码平台](https://help.aliyun.com/zh/model-studio/qoder-agent)

 [**Lingma**阿里云智能编码助手，提供独立 IDE](https://help.aliyun.com/zh/model-studio/lingma-agent)

 [**Kilo CLI**轻量高性能命令行编程工具](https://help.aliyun.com/zh/model-studio/kilo-cli)

[··· **更多工具**其他编程工具](https://help.aliyun.com/zh/model-studio/more-tools)

## **可选：接入图像生成模型**

Token Plan 团队版支持图像生成模型（qwen-image-2.0、wan2.7-image 等）。图像生成模型使用独立的接口，需要通过 AI 工具的 Skill 或扩展机制接入。

具体配置方法请参见[接入多模态生成模型](https://help.aliyun.com/zh/model-studio/token-plan-multimodal-gen)。

## **可选：工具调用**

通过接入工具调用，模型可以在对话中调用联网搜索、代码解释器等扩展能力。

-   qwen3.7-max、qwen3.6-plus、qwen3.6-flash：内置联网搜索、代码解释器、网页抓取、以图搜图、文搜图 5 个工具，通过 Responses API 直接调用。内置工具不额外收费，产生的 token 消耗统一从套餐 Credits 中抵扣。
    
-   其他模型：通过 MCP 服务接入工具。
    

详细说明请参见[工具调用](https://help.aliyun.com/zh/model-studio/token-plan-tool)。
