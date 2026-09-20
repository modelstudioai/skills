# [sandbox](../guides/sandbox.md) api

Sandbox API 是阿里云百炼提供的沙箱实例与模版全生命周期管理接口，兼容 E2B 协议，用于在隔离环境中安全执行代码、运行模型或调试应用。所有请求通过阿里云百炼 AI 网关转发，需使用百炼 API Key 鉴权。开发者可通过 REST 直调或 E2B 官方 SDK 接入，适用于自动化工作流、AI Agent 执行环境、CI/CD 沙箱测试等场景。

## 支持的模型/功能

Sandbox API 不直接提供“模型推理”能力，而是提供**可编程沙箱环境**（即轻量级容器化运行时），支持以下核心功能：

- **实例管理**：创建、列举、获取、连接、暂停、恢复、释放沙箱实例；
- **模版管理**：创建、列举、获取、更新、查询构建状态、删除沙箱模版；
- **环境配置**：支持 CPU/内存规格选择、网络策略（白名单/黑名单）、环境变量、文件挂载、公网访问控制；
- **生命周期控制**：支持 `timeout` 自动暂停、`maxRunningTimeout` 强制释放、`autoResume` 连接自动恢复等。

> **注意**：文档中多次提及“兼容 E2B 协议”，但阿里云百炼侧对部分字段和行为做了扩展或约束（如 `autoPauseTime` 与 `maxRunningTimeout` 的优先级逻辑、`mntConfig` 中 `originFileId` 必须为当前工作空间真实文件 ID）。实际行为以 [API 总览与认证](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md) 和各接口文档为准，而非 E2B 官方文档。

## 关键参数

### 实例创建（`POST /sandboxes`）
- `templateID`（必填）：已构建完成的模版 ID，未就绪时返回 409；
- `timeout`（可选）：实例生命周期秒数，范围 `[300, 604800]`；
- `allow_internet_access`（可选）：是否允许公网访问（注意：文档 3 与文档 5 字段名不一致，前者用下划线，后者用驼峰 `allowInternetAccess`；实际请求体应使用 `allow_internet_access`，响应体返回 `allowInternetAccess`）；
- `lifecycle.on_timeout`（可选）：到期行为，值为 `"pause"` 或 `"terminate"`（文档 3 示例中为 `"pause"`，但未明确枚举 `terminate`；文档 9 中 `maxRunningTimeout` 到期为强制释放，二者语义不同）；
- `network.allowOut` / `denyOut`（可选）：出口域名/IP 白名单与黑名单，`denyOut` 不支持域名（见 [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)）。

### 模版创建（`POST /v3/templates`）
- `cpuCount` 与 `memoryMB`（必填且必须同时指定）：需匹配平台预设规格组合（如 `1/2048`, `4/8192`），非法组合返回 400；
- `maxRunningTimeout`（可选）：最大运行时间（秒），优先级高于 `autoPauseTime`；两者均未传时默认 604800 秒；
- `mntConfig`（可选）：挂载配置，`originFileId` 必须为当前工作空间内真实存在的文件 ID，否则构建失败。

## 使用方式

### 1. 基础配置
- **Endpoint**：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox`（仅支持 `cn-beijing` 地域）；
- **鉴权**：HTTP Header `Authorization: Bearer <your-api-key>`；
- **前提**：开通百炼服务、创建 API Key、完成 SLR 授权、获取工作空间 ID（见 [API 总览与认证](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)）。

### 2. 典型流程
```bash
# 1. 创建模版（获取 templateID + buildID）
curl -X POST "$BASE_URL/v3/templates" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{"name":"py311","cpuCount":2,"memoryMB":4096}'

# 2. 轮询构建状态（直到 status == "ready"）
curl "$BASE_URL/templates/{templateID}/builds/{buildID}/status" \
  -H "Authorization: Bearer $API_KEY"

# 3. 创建实例（基于就绪模版）
curl -X POST "$BASE_URL/sandboxes" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{"templateID":"...","timeout":3600}'

# 4. 连接实例（获取 domain/token）
curl -X POST "$BASE_URL/sandboxes/{sandboxID}/connect" \
  -H "Authorization: Bearer $API_KEY"
```

### 3. SDK 支持
推荐使用 E2B 官方 SDK（如 Python `e2b` 包），但需注意：
- SDK 的 `api_key` 参数仅用于协议占位（如填 `e2b_${ALIYUN_UID}`），**业务鉴权仍依赖 HTTP Header `Authorization`**；
- 部分方法（如 `update_template`）为百炼自定义扩展，SDK 原生可能不支持，需手动封装（见 [实例管理与使用](raw/application-user-guide/sandbox/sandbox-sdk.md)）。

## 限制和注意事项

- **地域限制**：当前仅支持 `cn-beijing`，Endpoint 中 region 固定不可更改；
- **资源规格**：CPU 与内存必须成对选用平台预设组合，单独修改任一参数将导致 400 错误；
- **模版构建依赖**：创建实例前必须确保模版 `buildStatus == "ready"`，否则返回 409（见 [创建实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md)）；
- **实例释放约束**：删除模版前，必须确保无 `running` 或 `paused` 实例，否则返回 409（见 [删除模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)）；
- **网络规则差异**：`denyOut` 仅支持 IPv4/IPv6/CIDR，**不支持域名**（文档 9 明确说明），而 `allowOut` 支持域名；
- **错误处理**：所有接口遵循统一错误结构 `{ "code": number, "message": string, "requestID": string }`，HTTP 状态码含义详见 [API 总览与认证](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md) 中的错误响应章节。

## 来源文档

- [API 总览与认证](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)
- [实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md)
- [创建实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md)
- [列举实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-list.md)
- [获取实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-get.md)
- [连接实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-connect.md)
- [恢复实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-resume.md)
- [暂停实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-pause.md)
- [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)
- [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md)
- [获取模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-get.md)
- [列举模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-list.md)
- [获取构建状态](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-build-status.md)
- [删除模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)
- [释放实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-delete.md)
- [更新模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-update.md)


