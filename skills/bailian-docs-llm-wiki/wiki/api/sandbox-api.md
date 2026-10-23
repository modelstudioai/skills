# sandbox api

Sandbox API 是阿里云百炼提供的沙箱环境生命周期管理接口，基于 E2B 协议兼容设计，支持沙箱实例与模版的创建、查询、启停和销毁。所有请求需通过百炼 API Key 鉴权，并经由工作空间专属 Endpoint 发起。该 API 适用于需要动态执行代码、隔离运行环境或构建可复现 Agent 工作流的开发者场景。

## 支持的模型/功能

Sandbox API 不直接提供“模型”调用能力，而是提供**沙箱运行时环境**（即计算容器），其底层镜像由模版定义。当前支持的官方基础镜像包括 `code-interpreter-v1`、`browser` 和 `all-in-one`，均托管于 `fc-e2b-registry.cn-beijing.cr.aliyuncs.com/runtime/`。这些镜像已预装 Python、Node.js、浏览器及常用数据科学库，具体能力详见 [概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md) 中的镜像说明。用户也可通过自定义 `fromImage` 或 `mntConfig` 挂载文件构建私有模版。

> **注意**：文档中多次提及 `code-interpreter-v1` 等镜像名称，但未明确列出各镜像的具体版本号、Python 版本或预装包清单；实际使用前请以控制台最新文档或 `GET /v2/templates` 返回的 `envdVersion` 字段为准。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `Authorization` | Header | string | 是 | `Bearer <your-api-key>`，来自[认证](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md) |
| `workspace_id` | Endpoint 路径 | string | 是 | 控制台右上角获取，形如 `ws-xxx` |
| `region` | Endpoint 路径 | string | 是 | 当前仅支持 `cn-beijing` |
| `templateID` | 请求体（创建实例）或路径（模版操作） | string | 是（创建实例等） | 模版唯一标识，需先通过 `/v3/templates` 创建并等待 `buildStatus=ready` |
| `sandboxID` | 路径 | string | 是 | 实例唯一 ID，由 `POST /sandboxes` 返回，用于后续所有实例操作 |
| `originFileId` | `mntConfig` 数组元素 | string | 是（若使用挂载） | 文件 ID，必须是 `source=sandbox_template` 且 `status=available` 的文件，详见[文件上传](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md) |

其他关键参数包括：
- `timeout`（实例/连接超时，单位秒，范围 `[300, 604800]`）
- `cpuCount` / `memoryMB`（必须成对出现，且仅支持平台预设规格组合）
- `allow_internet_access`（布尔值，控制公网访问）
- `mntConfig.mountPath`（必须以 `/home/user/workspace/uploads/` 开头，否则挂载无效）

## 使用方式

### 1. 基础准备
- 创建 API Key：在[百炼控制台 → API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key)生成；
- 完成 SLR 授权：首次使用需按[快速开始](../../raw/application-user-guide/agent-development/sandbox/sandbox-start-using/sandbox-quick-start.md)完成服务授权；
- 获取 `workspace_id`：控制台右上角下拉菜单查看。

### 2. 标准流程（推荐）
1. **上传模版依赖文件**（如 `config.json`, `requirements.txt`）  
   ```bash
   curl -X POST "$BASE_URL/api/v1/agentstudio/files" \
     -H "Authorization: Bearer $API_KEY" \
     -F "file=@./config.json" \
     -F "source=sandbox_template"
   ```
   → 轮询 `GET /api/v1/agentstudio/files/{file_id}` 直至 `status=available`。

2. **创建模版**（`POST /v3/templates`）  
   在 `mntConfig` 中引用上一步的 `originFileId`，指定 `cpuCount`/`memoryMB` 等。

3. **等待构建就绪**（`GET /templates/{templateID}/builds/{buildID}/status`）  
   确保 `status=ready` 后再进行下一步。

4. **创建实例**（`POST /sandboxes`）  
   传入 `templateID` 及可选配置（如 `timeout`, `envVars`）。

5. **连接与交互**（`POST /sandboxes/{sandboxID}/connect`）  
   获取 `domain` 和 `envdAccessToken`，用于后续数据面通信。

### 3. SDK 支持
可直接使用 E2B 官方 SDK（如 `e2b-python`），只需将 `api_key` 设为占位符（如 `e2b_${ALIYUN_UID}`），Endpoint 和鉴权由百炼侧接管。详细用法见 [实例管理与使用](../../raw/application-user-guide/agent-development/sandbox/sandbox-sdk.md)。

## 限制和注意事项

- **地域限制**：当前仅支持 `cn-beijing` 地域，Endpoint 中 `region` 字段不可更改。
- **文件限制**：单文件 ≤ 50 MB，工作空间总容量 ≤ 100 GB，保存时效 30 天；仅 `.yaml` 明确支持，`.csv`、`.yml`、`.sh`、`.whl`、`.tar.gz`、`.ts` 等被明确拒绝（见[错误码](../../raw/application-api-reference/sandbox-api/sandbox-api-errors.md)）。
- **模版删除约束**：`DELETE /templates/{templateCode}` 会校验关联实例状态，若存在 `running` 或 `paused` 实例则返回 `409`，必须先调用 `DELETE /sandboxes/{sandboxID}` 释放所有实例。
- **网络配置差异**：`networkConfig.denyOut` 不支持域名（仅 IPv4/IPv6/CIDR），而 `allowOut` 支持域名；此限制在创建/更新模版文档中明确，但列举/获取模版响应中未体现字段约束，需以请求体校验逻辑为准。
- **E2B 兼容性边界**：除模版更新（`PUT /templates/{templateCode}`）为百炼扩展协议外，其余接口方法、路径、响应结构贴近 E2B 官方定义；但错误响应不封装为百炼统一 `Result<T>` 结构，而是直接返回 E2B 风格 JSON（含 `code`/`message`），详见[错误码](../../raw/application-api-reference/sandbox-api/sandbox-api-errors.md)。

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
- [恢复实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-resume.md)
- [释放实例](../../raw/application-api-reference/sandbox-api/sandbox-api-instances/sandbox-api-delete.md)
- [列举模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-list.md)
- [创建模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-create.md)
- [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md)
- [更新模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-update.md)
- [获取模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-get.md)
- [获取构建状态](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-build-status.md)
- [删除模版](../../raw/application-api-reference/sandbox-api/sandbox-api-templates/sandbox-api-template-delete.md)


