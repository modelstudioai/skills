# [overview](overview.md) 1e06e5e20b81f10d

MCP API 是百炼平台提供的服务管理接口，用于统一管控官方 MCP 和自定义 MCP 的全生命周期（查询、创建、启停、开通、删除）及工具能力（列表、调用、推荐）。该 API 面向开发者设计，需配合工作空间 ID 和 API Key 使用，所有请求均通过 RESTful 方式交互。详细错误处理机制和认证要求请参考 [原文标题](../../raw/application-api-reference/overview-1e06e5e20b81f10d.md)。

## 支持的模型/功能

- **MCP 类型支持**：区分 `OFFICIAL`（官方 MCP）与 `CUSTOMER`（自定义 MCP），二者在状态文案、元信息字段（如 `icon`、`provider`）和操作权限上存在差异。
- **服务类型支持**：`STDIO`（FC 函数部署）、`HTTP`（远程流式 HTTP）、`SSE`（远程 SSE）、`OPENAPI`（HTTP API 封装为 MCP）。
- **核心功能**：
  - 全生命周期管理：创建、更新、启用/停用（自定义）、开通/关闭（官方）、删除；
  - 工具能力：获取工具列表、执行工具调用、按自然语言推荐工具；
  - 元数据聚合：提供调用量、成功率、平均耗时等运营指标（仅官方 MCP 的 `meta_info` 中返回）。

> **注意**：自定义 MCP 不支持 `activate`/`deactivate` 接口，仅官方 MCP 可开通/关闭；而 `enable`/`disable` 仅适用于自定义 MCP。该行为与 [原文标题](../../raw/application-api-reference/overview-1e06e5e20b81f10d.md) 中“接口列表”章节一致，但需注意 `update` 接口文档未明确说明是否允许修改 `server_type` —— 实际调用中修改 `server_type` 将被拒绝，此限制未在 [原文标题](../../raw/application-api-reference/overview-1e06e5e20b81f10d.md) 中显式声明。

## 关键参数

- **Endpoint 路径变量**：`{workspace_id}` 必须为实际工作空间 ID，构成完整 endpoint：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/mcp/servers`。
- **分页与筛选**：统一使用 `pageNo`（从 1 开始）、`pageSize`；工具推荐使用 `topN`。
- **路径参数**：关键资源操作均以 `mcpCode` 为路径参数（如 `GET /{mcpCode}`）。
- **请求体/响应字段命名**：全部采用 `snake_case`（如 `server_name`, `mcp_config`），**仅工具调用结果例外**：保留 MCP 协议字段名 `inputSchema`、`additionalProperties`，并使用 `isError` 判断执行结果（见 [原文标题](../../raw/application-api-reference/overview-1e06e5e20b81f10d.md) “请求命名”节）。

## 使用方式

1. **前置准备**：
   - 开通百炼服务，[创建 API Key](../model-api-reference/preparations/get-api-key.md)；
   - 登录控制台获取工作空间 ID（路径：右上角工作空间菜单 → 复制 ID）。
2. **认证**：所有请求需携带 `Authorization: Bearer <api_key>` 请求头（认证细节见 [原文标题](../../raw/application-api-reference/overview-1e06e5e20b81f10d.md) 中“说明”部分引用的认证文档）。
3. **调用示例（查询列表）**：
   ```bash
   curl -X GET "https://<workspace_id>.cn-beijing.maas.aliyuncs.com/api/v1/mcp/servers/list?pageNo=1&pageSize=10" \
     -H "Authorization: Bearer <your_api_key>"
   ```
4. **响应解析**：始终检查 `success` 字段；若为 `true`，业务数据在 `data` 中；若为 `false`，错误码与信息在 `error_code`/`error_msg` 中；`request_id` 用于问题排查。

## 限制和注意事项

- **敏感信息风险**：`mcp_config`（尤其含 `headers`）可能包含密钥等敏感配置，响应中会原样返回。**必须仅在可信后端环境调用，并禁止透传至前端或日志明文输出**（见 [原文标题](../../raw/application-api-reference/overview-1e06e5e20b81f10d.md) “警告”节）。
- **状态一致性**：`server_status` 与 `server_status_text` 并非一一映射（如 `INACTIVE` 对应“未启用”或“未开通”），客户端应优先依据 `server_status` 做逻辑判断，而非文案。
- **字段空值语义**：`DetailResponse` 中多数字段为 `null` 容忍（如 `mcp_code`、`description`），表示未设置；`CreateResponse` 则仅返回已赋值字段，需做好字段存在性检查。
- **地域硬编码**：当前 endpoint 固定为 `cn-beijing`，不支持跨地域调用，暂无 region 参数化机制。

## 来源文档

- [MCP API 概览](../../raw/application-api-reference/overview-1e06e5e20b81f10d.md)


