# agent store

`agent store` 是阿里云百炼平台中统一管理外部能力扩展的核心模块，主要包含两类可复用能力：**MCP（Model Context Protocol）服务**和**Skill（技能包）**。MCP 服务面向工具集成，提供标准化的大模型与外部 API/服务的交互通道；Skill 面向文件与数据处理任务，以声明式描述驱动智能体自动识别并调用。二者均支持官方预置与用户自定义，可在智能体或工作流应用中直接配置使用。

## 支持的模型/功能

- **MCP 服务**：支持两类接入方式  
  - **官方 MCP 服务**：阿里云百炼已部署并托管的云服务（如 `Amap Maps`、`WebSearch`、`Sequential Thinking`），开箱即用，部分支持 [One Key MCP](../../raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md) 一键配置；  
  - **自定义 MCP 服务**：支持三种部署路径：① 使用脚本（npx/uvx）托管开源或自研 MCP Server；② 通过 [AI 网关导入现有 RESTful API](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md)；③ 从 [阿里云 OpenAPI 导入云产品能力](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md)。  

- **Skill**：分为两类  
  - **官方 Skill**：平台预置、免配置的通用能力（如 `xlsx`、`pdf`、`csv` 处理），自动随平台更新；  
  - **自定义 Skill**：用户上传 ZIP 包（含 `SKILL.md` 元信息文件），用于覆盖特定业务场景（如行业报表解析、私有格式转换）。  

> **注意**：MCP 服务与 Skill 功能定位不同，不可互换。MCP 用于实时调用外部 API（如查天气、搜网页），Skill 用于处理用户上传的文件或结构化数据输入。文档 7 和 8 中 Skill 的介绍未提及与 MCP 的协同机制，实际应用中二者需按任务类型分别选用。

## 关键参数

| 类别 | 参数 | 说明 |
|--------|------|------|
| **MCP 通用** | `DASHSCOPE_API_KEY` | 所有官方及自定义 MCP 服务的统一鉴权凭证，无需为单个服务单独申请密钥（见 [官方 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md)）。 |
| **MCP 自定义部署** | `type`（`stdio`/`sse`/`streamableHttp`）、`url`、`command`/`args` | 决定连接方式与启动行为；必须与服务端端点严格匹配（如 `type: "sse"` 对应 `/sse` 路径），否则触发 `11200058` 错误（见 [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)）。 |
| **Skill** | `name`（唯一标识）、`description`（YAML 中必填字段） | `description` 直接影响智能体调用准确率，需明确触发条件、支持操作、输入类型及排除场景（见 [Skill 介绍](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md)）。 |

## 使用方式

- **MCP 服务**  
  - **平台内集成**：在智能体应用中最多添加 5 个 MCP 服务，由大模型根据对话自动调度；在工作流中需手动指定 MCP 节点的工具名（如 `maps_weather`）及输入参数（需前置大模型节点提取城市名）；  
  - **外部调用**：支持 CLI（`bl mcp call --target <名称>.<工具>`）、SDK（`mcp.client.streamable_http`）及主流客户端（Qoder/Cursor 等），需配置 `Authorization: Bearer ${DASHSCOPE_API_KEY}` 请求头。  

- **Skill**  
  - **添加方式**：在智能体配置页的「技能」区域点击加号，或从 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 详情页直接添加；  
  - **触发逻辑**：智能体基于 `SKILL.md` 中的 `description` 进行语义匹配，无需显式指令（如用户说“帮我整理这个 Excel 表”即可触发 `xlsx` Skill）。  

## 限制和注意事项

- **MCP 服务限制**  
  - 官方 MCP 服务中，`WebSearch` 有免费额度（2000 次/月），超限后按 29 元/千次计费；  
  - 自定义 MCP 服务不支持访问本地资源（如本地数据库、文件系统），且远程服务需配置函数计算 FC 的 IP 白名单或 VPC 打通（见 [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)）；  
  - `npx`/`uvx` 部署的服务版本更新后**不会自动同步**，需手动重新部署（见 [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)）。  

- **Skill 限制**  
  - ZIP 包大小 ≤ 10 MB，`SKILL.md` 必须位于根目录且符合 YAML frontmatter 规范；  
  - `name` 字段全局唯一，重名上传将创建新版本而非覆盖；  
  - Skill 仅适用于智能体应用，**不支持在工作流中直接调用**。  

- **通用注意事项**  
  - MCP 调用会增加模型输入 [Token](../concepts/token.md)（返回结果作为上下文注入）和潜在输出 [Token](../concepts/token.md)（更详尽响应）；  
  - MCP 服务**不能直接接入千问 API 调用链**，仅限智能体/工作流应用内使用（见 [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)）；  
  > **注意**：文档 3 提到“云部署 MCP 服务限时免部署费用”，但文档 4 中自定义部署的“基础模式”明确标注“无部署费用”，而“极速模式”收取部署费率。两者表述一致，无矛盾；但文档 3 的“限时”措辞未在其他文档中佐证，建议以控制台实时计费策略为准。

## 来源文档

- [MCP](../../raw/application-user-guide/agent-store/model-context-protocol.md)
- [官方 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md)
- [模型上下文协议（MCP）](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-introduction.md)
- [自定义 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md)
- [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)
- [外部调用](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-external-calls.md)
- [Skill](../../raw/application-user-guide/agent-store/skill.md)
- [Skill](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md)


