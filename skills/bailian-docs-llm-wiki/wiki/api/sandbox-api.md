# sandbox api

Sandbox API 是阿里云百炼提供的沙箱环境生命周期管理接口，兼容 E2B 协议，支持沙箱实例与模版的创建、查询、更新和销毁。所有请求需通过阿里云百炼 API Key 鉴权，并经由工作空间专属 Endpoint 转发。该 API 适用于需要动态执行代码、隔离运行环境或构建 Agent 工具链的开发者场景。

## 支持的模型/功能

Sandbox API 不直接提供“模型”推理能力，而是提供**可编程沙箱环境**（即轻量级容器化运行时），其核心能力包括：

- **实例管理**：创建、列举、获取、连接、暂停、恢复和释放沙箱实例；
- **模版管理**：创建、列举、获取、更新、查询构建状态和删除沙箱模版；
- **文件挂载**：通过预上传的 `sandbox_template` 类型文件注入配置、脚本或依赖（如 `config.json`、`requirements.txt`）；
- **网络与生命周期控制**：支持出口白名单/黑名单、公网访问开关、超时自动暂停（`autoPause`）或自动释放（`maxRunningTimeout`）。

模版底层基于 envd 构建，官方预置镜像包括 `code-interpreter-v1`、`browser` 和 `all-in-one`，均托管于 `fc-e2b-registry.cn-beijing.cr.aliyuncs.com/runtime/`。详细模版能力说明见 [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md)。

> **注意**：文档中多次提及 `POST /templates` 为兼容路由，但实际推荐使用 `/v3/templates`（见 [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)），因 `/v3` 路径明确要求资源规格校验且响应字段更稳定；而 `/templates` 在部分旧文档中未声明此约束，存在歧义。

## 关键参数

| 参数 | 位置 | 必填 | 类型 | 说明 |
|------|------|------|------|------|
| `Authorization` | Header | 是 | string | `Bearer <your-api-key>`，来自 [认证](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md) 页面创建的百炼 API Key |
| `workspace_id` | Endpoint 路径 | 是 | string | 控制台右上角获取，形如 `ws-xxx`；拼入 Base URL：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox` |
| `templateID` | 请求体（创建实例）或路径（模版操作） | 是 | string | 模版唯一标识，必须已构建完成（`status=ready`），否则创建实例返回 409 |
| `sandboxID` | 路径 | 是 | string | 实例唯一 ID，格式如 `sbx-xxx`，由创建接口返回 |
| `originFileId` | `mntConfig` 数组内 | 是 | string | 文件 ID，**必须**是通过 `source=sandbox_template` 上传且 `status=available` 的文件（见 [概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)） |
| `mountPath` | `mntConfig` 数组内 | 是 | string | 必须以 `/home/user/workspace/uploads/` 开头；非此路径下挂载将被忽略 |
| `timeout` | 请求体（创建/连接/恢复） | 否 | integer | 取值范围 `[300, 604800]`（5 分钟 ~ 7 天），单位秒；超时后行为由 `lifecycle.on_timeout` 或 `autoPause` 决定 |

## 使用方式

### 1. 前置准备
- 开通百炼服务并[创建 API Key](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)；
- 在控制台完成 **SLR 授权**（首次使用必需），详见 [快速开始](../../raw/application-user-guide/agent-development/sandbox/sandbox-start-using/sandbox-quick-start.md)；
- 获取 `workspace_id` 并确认地域为 `cn-beijing`（当前唯一支持地域）。

### 2. 典型流程（模版 → 实例）
1. **上传文件**（如 `config.json`）：
   ```bash
   curl -X POST "$BASE_URL/api/v1/agentstudio/files" \
     -H "Authorization: Bearer $API_KEY" \
     -F "file=@./config.json" \
     -F "source=sandbox_template"
   ```
   轮询至 `status=available` 后记录 `id`。
2. **创建模版**（指定 `originFileId`）：
   ```bash
   curl -X POST "$BASE_URL/v3/templates" \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "my-py-env",
       "cpuCount": 1,
       "memoryMB": 2048,
       "mntConfig": [{
         "originFileId": "file_xxx",
         "mountPath": "/home/user/workspace/uploads/config.json"
       }]
     }'
   ```
   记录返回的 `templateID` 和 `buildID`。
3. **等待构建就绪**：
   ```bash
   curl "$BASE_URL/templates/{templateID}/builds/{buildID}/status" \
     -H "Authorization: Bearer $API_KEY"
   ```
   直至 `status=ready`。
4. **创建实例**：
   ```bash
   curl -X POST "$BASE_URL/sandboxes" \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"templateID": "tmpl-xxx", "timeout": 3600}'
   ```

### 3. SDK 支持
可直接使用 [E2B 官方 SDK](https://docs.e2b.dev/sdk)（如 Python `e2b` 包），仅需将 `api_key` 设为占位符（如 `e2b_${ALIYUN_UID}`），真实鉴权仍依赖 HTTP Header 中的百炼 API Key。详情见 [实例管理与使用](../../raw/application-user-guide/agent-development/sandbox/sandbox-sdk.md)。

## 限制和注意事项

- **地域限制**：当前仅支持 `cn-beijing`，Endpoint 中 `region` 字段不可替换为其他值；
- **文件限制**：
  - 单文件 ≤ 50 MB，工作空间总容量 ≤ 100 GB，保存时效 30 天；
  - 仅 `.yaml` 明确支持；`.csv`、`.yml`、`.sh`、`.whl`、`.tar.gz`、`.ts` 等**不支持**（见 [概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)）；
  - 文件必须带 `source=sandbox_template` 且状态为 `available`，否则模版创建/更新失败（错误码 `11900024`）；
- **模版与实例强绑定**：删除模版前，必须确保无 `running` 或 `paused` 实例（否则返回 409），见 [删除模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)；
- **错误处理**：兼容 E2B 协议的接口**不封装为百炼统一 `Result<T>` 结构**，错误响应直接返回 `{code, message, requestID}`，HTTP 状态码语义与 [错误码](../../raw/application-api-reference/sandbox-api/sandbox-api-errors.md) 文档一致；
- **网络配置差异**：`denyOut` 仅支持 IPv4/IPv6/CIDR，**不支持域名**（`allowOut` 支持），此限制在 `networkConfig` 和 `mntConfig` 的文档中均未显式强调，需特别注意。

## 来源文档

- [概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)
- [认证](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)
- [错误码](../../raw/application-api-reference/sandbox-api/sandbox-api-errors.md)
- [实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md)
- [创建实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md)
- [列举实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-list.md)
- [获取实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-get.md)
- [连接实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-connect.md)
- [恢复实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-resume.md)
- [暂停实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-pause.md)
- [释放实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-delete.md)
- [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md)
- [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)
- [列举模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-list.md)
- [获取模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-get.md)
- [更新模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-update.md)
- [获取构建状态](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-build-status.md)
- [删除模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)


