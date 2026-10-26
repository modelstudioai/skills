# sandbox api

Sandbox API 是阿里云百炼提供的沙箱环境生命周期管理服务，兼容 E2B 协议，支持沙箱实例与模版的创建、查询、更新和销毁，并提供文件挂载与网络策略配置能力。所有请求需通过阿里云百炼 AI 网关转发，使用 API Key 鉴权，Endpoint 按工作空间与地域拼装。该 API 适用于需要安全、隔离、可复现执行环境的 Agent 开发与代码解释场景。

## 支持的模型/功能

Sandbox API 不直接提供“模型”推理能力，而是提供**可定制化沙箱运行时环境**，其功能核心围绕两类资源展开：

- **沙箱实例（Sandbox Instance）**：基于模版启动的临时计算环境，支持运行代码、访问文件、联网（可配）、暂停/恢复/释放。实例状态包括 `running`、`paused`，不支持 `stopped`（仅暂停保留状态）。
- **沙箱模版（Template）**：定义实例基础镜像、资源配置（CPU/内存）、挂载文件、网络规则与环境变量的不可变配置单元。模版构建完成后（`status=ready`）方可创建实例。官方预置镜像位于 `fc-e2b-registry.cn-beijing.cr.aliyuncs.com/runtime/`，如 `code-interpreter-v1`、`browser`、`all-in-one`。

> **注意**：文档中多次提及“兼容 E2B 协议”，但模版更新（`PUT /templates/{templateCode}`）为阿里云百炼自定义扩展，[不声明完全兼容 E2B Update Template v2](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-update.md)，开发者应以本文档字段定义为准。

## 关键参数

| 参数 | 所属接口 | 必填 | 类型 | 说明 |
|------|----------|------|------|------|
| `templateID` | 创建实例 `/sandboxes` | 是 | string | 已构建完成（`status=ready`）的模版 ID；模版未就绪时返回 409 [详见创建实例文档](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md) |
| `timeout` | 创建/连接/恢复实例 | 否 | integer | 实例生命周期或连接会话超时时间（秒），取值范围 `[300, 604800]`（5 分钟至 7 天） |
| `allow_internet_access` | 创建实例 | 否 | boolean | 是否允许实例访问公网；等价于 `network.allowPublicTraffic=true` |
| `mntConfig` | 创建/更新模版 | 否 | array<object> | 文件挂载配置，要求 `originFileId` 对应 `source=sandbox_template` 且 `status=available` 的文件；`mountPath` **必须以 `/home/user/workspace/uploads/` 开头**，否则文件不会出现在实例中 [详见创建模版文档](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md) |
| `autoPauseTime` / `maxRunningTimeout` | 创建/更新模版 | 否 | integer | 控制实例自动行为：仅设 `autoPauseTime` 则到期暂停；两者均设则 `maxRunningTimeout` 优先生效（到期释放） |

## 使用方式

### 1. 前置准备
- 开通百炼服务，[创建 API Key](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)；
- 完成 SLR 服务授权（首次使用必需）；
- 获取工作空间 ID（控制台右上角下拉菜单）；
- Endpoint 格式：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox`（当前仅支持 `cn-beijing` 地域）。

### 2. 典型流程
1. **上传文件**（如配置、脚本）：  
   ```bash
   curl -X POST "$BASE_URL/api/v1/agentstudio/files" \
     -H "Authorization: Bearer $API_KEY" \
     -F "file=@./config.json" \
     -F "source=sandbox_template"
   ```
   轮询 `GET /api/v1/agentstudio/files/{file_id}` 直至 `status=available`。

2. **创建模版**：  
   在 `mntConfig` 中引用上步获得的 `originFileId`，提交 `POST /v3/templates`。获取 `buildID` 后调用 [获取构建状态](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-build-status.md) 等待 `status=ready`。

3. **创建实例**：  
   使用就绪模版 ID 调用 `POST /sandboxes`，获取 `sandboxID`。

4. **连接与操作**：  
   - 连接：`POST /sandboxes/{sandboxID}/connect` → 获取 `domain` 与 `envdAccessToken`；  
   - 暂停/恢复：`POST /sandboxes/{sandboxID}/pause` / `resume`；  
   - 释放：`DELETE /sandboxes/{sandboxID}`。

### 3. SDK 支持
可直接使用 E2B 官方 SDK（如 Python `e2b` 包），只需将 `api_key` 设为 `e2b_${ALIYUN_UID}` 即可，鉴权由阿里云百炼侧接管 [详见 SDK 文档](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)。

## 限制和注意事项

- **文件限制**：单文件 ≤ 50 MB，工作空间总容量 ≤ 100 GB，保存时效 30 天；仅 `.yaml` 明确支持，`.csv`、`.yml`、`.sh`、`.whl`、`.tar.gz`、`.ts` 等**明确不支持**（见 [文件上传文档](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)）。
- **模版删除约束**：若模版存在任何 `running` 或 `paused` 实例，`DELETE /templates/{templateCode}` 将返回 409 错误，必须先释放所有关联实例 [详见删除模版文档](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)。
- **错误处理**：API 返回原生 E2B 结构（非阿里云统一 `Result<T>`），HTTP 状态码语义遵循标准（如 401=API Key 无效，409=状态冲突），具体错误码见 [错误码文档](../../raw/application-api-reference/sandbox-api/sandbox-api-errors.md)。
- **网络配置差异**：`denyOut` 黑名单**不支持域名**（仅 IPv4/IPv6/CIDR），而 `allowOut` 白名单支持域名；此限制在创建/更新模版的 `networkConfig` 字段中生效。

## 来源文档

- [概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)
- [认证](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md)
- [错误码](../../raw/application-api-reference/sandbox-api/sandbox-api-errors.md)
- [实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md)
- [创建实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-create.md)
- [列举实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-list.md)
- [获取实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-get.md)
- [连接实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-connect.md)
- [暂停实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-pause.md)
- [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md)
- [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)
- [列举模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-list.md)
- [获取模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-get.md)
- [更新模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-update.md)
- [释放实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-delete.md)
- [删除模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)
- [获取构建状态](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-build-status.md)
- [恢复实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-resume.md)


