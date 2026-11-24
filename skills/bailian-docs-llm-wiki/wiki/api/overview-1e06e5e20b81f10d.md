# [overview](overview.md) 1e06e5e20b81f10d

MCP API 是百炼平台提供的服务管理接口，用于全生命周期管控 MCP（Model Calling Protocol）服务，包括官方 MCP 与自定义 MCP 的查询、创建、启停、开通/关闭、工具调用及推荐。该 API 面向开发者设计，需配合工作空间 ID 和 API Key 使用，所有响应遵循统一结构并携带 `x-request-id` 便于问题追踪。详细行为规范请参阅 [MCP API 概览](../../raw/application-api-reference/overview-1e06e5e20b81f10d.md)。

## 支持的模型/功能

- **服务类型支持**：`STDIO`（npx/uvx 启动，部署于函数计算 FC）、`HTTP`（远程 Streamable HTTP）、`SSE`（远程 SSE）、`OPENAPI`（将现有 HTTP API 封装为 MCP）。
- **服务归属类型**：`OFFICIAL`（阿里云官方提供）与 `CUSTOMER`（用户自定义）两类，元信息字段存在差异（如 `icon`、`provider` 仅限官方 MCP）。
- **核心能力**：
  - 官方 MCP：开通（`activate`）、关闭（`deactivate`）
  - 自定义 MCP：创建（`create`）、更新（`update`）、启用（`enable`）、停用（`disable`）、删除（`delete`）
  - 工具层：查询工具列表（`/tools`）、调用工具（`/tools/call`）、按自然语言推荐工具（`/tools/recommend`）

> **注意**：[MCP API 概览](../../raw/application-api-reference/overview-1e06e5e20b81f10d.md) 中明确说明 `meta_info` 字段对自定义 MCP 不返回 `icon`、`provider`、`is_onekey`，但部分旧版文档示例未强调此差异，实际开发中应以该文档为准。

## 关键参数

- **路径参数**：`mcpCode`（MCP 唯一编码），用于详情、启停、工具调用等接口。
- **分页参数**：`pageNo`、`pageSize`（snake_case），适用于 `/list` 等列表接口。
- **推荐参数**：`topN`（指定推荐工具数量），用于 `/tools/recommend`。
- **认证参数**：必须在请求头中携带 `Authorization: Bearer <api_key>`，认证方式详见 [认证](../../raw/application-api-reference/overview/authentication-58370587ddc046ee.md)。
- **敏感字段**：`mcp_config.headers` 等配置项会原样返回，可能含密钥或 [Token](../concepts/token.md)，需严格限制调用环境与响应日志留存。

## 使用方式

- **Endpoint 格式**：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/mcp/servers`  
  其中 `workspace_id` 需从[百炼控制台](https://bailian.console.aliyun.com/)右上角工作空间菜单复制获取。
- **请求体/响应格式**：全部使用 `snake_case`（工具调用结果中的 `isError` 除外，遵循 MCP 协议）。
- **响应结构统一**：无论成功或业务错误，均返回标准 JSON 结构，含 `success`、`error_code`、`error_msg`、`data`、`request_id` 字段；工具执行是否成功需进一步检查 `data.isError`。
- 接口调用前须确保已满足前提条件：[开通百炼服务并创建 API Key](../../raw/model-api-reference/preparations/get-api-key.md)，且已获取有效 `workspace_id`。

## 限制和注意事项

- **状态字段语义差异**：`server_status` 的文案在官方与自定义 MCP 中不一致（如 `INACTIVE` 对应“未启用” vs “未开通”），解析时应结合 `type` 字段判断上下文，避免硬编码文案匹配。
- **敏感信息风险**：`mcp_config` 中的 `headers`、`env` 等字段可能包含凭证，[MCP API 概览](../../raw/application-api-reference/overview-1e06e5e20b81f10d.md) 明确警告“请仅在可信环境调用，并妥善保护响应内容”，生产环境禁止打印或落库完整响应。
- **错误处理**：所有错误码与含义详见 [MCP API 错误码](../../raw/application-api-reference/overview/errors-972b4127b84f4429.md)，不建议依赖 `error_msg` 做逻辑分支，应以 `error_code` 为主。
- **One Key MCP 限制**：官方 MCP 若标记 `is_onekey: true`，则不支持手动启停，其生命周期由平台统一管控，调用 `enable`/`disable` 将返回明确错误。

## 来源文档

- [MCP API 概览](../../raw/application-api-reference/overview-1e06e5e20b81f10d.md)


