# agent store

agent store 是阿里云百炼平台中统一管理外部能力扩展的核心模块，包含 MCP（Model Context Protocol）服务和 Skill 两类能力组件。MCP 用于接入标准化的外部工具（如地图、搜索、天气等），通过协议化接口实现大模型与异构系统的安全、低代码集成；Skill 则面向文件处理与数据操作类任务，以声明式描述驱动智能体自动识别并调用。二者共同构成智能体应用的“能力货架”，支持在智能体或工作流中按需装配。

## 支持的模型/功能

- **MCP 服务**：支持官方托管服务（如 Amap Maps、WebSearch、Firecrawl）、One Key 免开通服务，以及三类自定义部署方式：  
  - 使用脚本部署（`npx`/`uvx` 托管本地 MCP Server）；  
  - 从 AI 网关导入现有 RESTful API；  
  - 从阿里云 OpenAPI 导入云产品能力（如 OSS、ECS）。  
  详细能力范围与接入示例见 [模型上下文协议（MCP）](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-introduction.md)。

- **Skill**：分为官方 Skill（预置 xlsx、pdf、csv 等文件处理能力，开箱即用）和自定义 Skill（通过 ZIP 包上传，含 `SKILL.md` 元信息定义触发逻辑）。Skill 不依赖外部 API，纯运行于百炼平台内，适用于结构化数据清洗、格式转换、报表生成等场景。[Skill 介绍文档](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md) 提供完整规范与示例。

> **注意**：文档 7 和文档 8 均指向 Skill 主题，但文档 8 仅为目录页，无实质内容；所有技术细节应以 [Skill](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md) 为准，避免引用空目录页。

## 关键参数

- **MCP 配置参数**：
  - `type`：必须与端点路径严格匹配（`"sse"` → `/sse`，`"streamableHttp"` → `/mcp`），不匹配将导致 `11200058` 错误；
  - `command`/`args`：脚本部署时指定启动命令（如 `npx @modelcontextprotocol/server-memory`）；
  - `env`：敏感环境变量（如 `AMAP_MAPS_API_KEY`）须通过 KMS 凭据加密，不可明文写入配置；
  - 部署模式：`基础模式`（按调用时长计费，有冷启动延迟） vs `极速模式`（额外收取部署时长费，常驻内存）。

- **Skill 关键字段**（在 `SKILL.md` 中定义）：
  - `name`：全局唯一标识，小写+连字符（如 `invoice-parser`）；
  - `description`：决定智能体调用准确性的核心字段，必须明确说明适用输入类型、支持操作、触发关键词及**不适用场景**（详见 [Skill 介绍文档](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md) 的完整示例）。

## 使用方式

- **MCP 接入流程**：
  1. 开通服务：前往 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，对 One Key 服务直接调用生效；对非 One Key 服务需点击“立即开通”；
  2. 在智能体中添加：最多支持同时配置 5 个 MCP 服务，大模型根据对话自动路由调用；
  3. 在工作流中使用：每个 MCP 节点仅绑定一个工具（如 `maps_weather`），需手动配置输入参数（常通过前置大模型节点提取）；
  4. 外部调用：支持一键配置至 Cherry Studio/Cursor，或通过 MCP SDK 编程集成（参考 [外部调用](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-external-calls.md) 中的 Python 示例）。

- **Skill 添加方式**：
  - 官方 Skill：在 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面点击“添加到智能体”；
  - 自定义 Skill：上传含合规 `SKILL.md` 的 ZIP 包（≤10 MB），审查通过后即可添加；
  - 添加位置：智能体应用配置页的“技能”区域，或 Skill 详情页右上角“添加到智能体”。

## 限制和注意事项

- **MCP 限制**：
  - 云部署 MCP 服务调用限流为 **15 QPS**（主账号与 RAM 子账号共享）；
  - 自定义部署的 MCP Server **无法访问本地资源**（如本地数据库、文件系统），且函数计算 FC 无固定出口 IP，访问云数据库需配置白名单或 VPC 打通；
  - 第三方 MCP Server（如 Notion/Github）需确保 API Key 权限充足，否则报错 `403 Forbidden`；
  - `npx`/`uvx` 部署的服务版本更新后**不会自动同步**，需手动重新部署（见 [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)）。

- **Skill 注意事项**：
  - 自定义 Skill 的 `description` 描述质量直接影响调用准确率，模糊或缺失“不适用场景”易导致误触发；
  - Skill 仅在**智能体应用**中生效，**不支持在工作流或直接调用千问 API 时使用**；
  - 官方 Skill 由平台自动更新，已添加的智能体会即时生效；自定义 Skill 更新需重新上传同名 ZIP 包。

- **通用注意事项**：
  - MCP 调用会增加模型 [Token](../concepts/token.md) 消耗：返回结果作为上下文注入输入，可能间接增加输出 [Token](../concepts/token.md)；
  - 所有自定义 MCP 服务（含脚本部署）仅限当前阿里云主账号及授权 RAM 用户访问，不对外公开；
  - 若遇连接失败（如错误码 `11200044`），优先执行 `curl <服务地址>` 测试连通性，并检查函数计算 FC 日志（需提前开启日志服务）。

## 来源文档

- [MCP](../../raw/application-user-guide/agent-store/model-context-protocol.md)
- [模型上下文协议（MCP）](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-introduction.md)
- [官方 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md)
- [自定义 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md)
- [外部调用](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-external-calls.md)
- [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)
- [Skill](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md)
- [Skill](../../raw/application-user-guide/agent-store/skill.md)


