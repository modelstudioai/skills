# API Key

API Key 是调用阿里云百炼大模型与应用服务的鉴权凭证，由主账号或具备 `管理员`/`API-Key` 页面权限的子账号在百炼控制台创建。它贯穿模型调用、应用集成、框架接入、[知识库](knowledge-base.md)检索等所有百炼 API 场景，是接入百炼服务的前置条件。

## 在百炼平台中的使用场景

API Key 在百炼的不同场景中都承担鉴权职责，但调用方式略有差异：

- **模型调用**：通过 [OpenAI 兼容接口](openai-compatible-interface.md)或 DashScope SDK 调用千问及第三方模型时，API Key 作为 `Authorization: Bearer <API_KEY>` 请求头或 SDK 的 `api_key` 参数传入。各地域有独立的接入域名与模型列表，API Key 不能跨地域混用。
- **应用调用**：调用[智能体应用](agent-application.md)、工作流应用、新版智能体（Agent 2.0）时，API Key 与应用 ID（APP ID）共同作为凭证。应用位于子[业务空间](workspace.md)时还需提供 Workspace ID。
- **框架集成**：LlamaIndex 构建 RAG 应用、Spring AI Alibaba 集成百炼智能体或检索[知识库](knowledge-base.md)时，均以 API Key 鉴权，并复用百炼的数据管理与模型推理能力。
- **临时访问**：在浏览器、移动 App 等不可信环境中，通过后端调用令牌接口生成临时 API Key 下发到客户端，避免暴露永久密钥。

## 关键参数与配置

### 创建入口与地域

不同地域的创建入口略有差异：

- **华北2（北京）、新加坡、日本（东京）、德国（法兰克福）**：在百炼控制台右上角选择对应地域后创建。
- **美国（弗吉尼亚）**：前往 modelstudio 控制台创建，且需额外选择"归属账号"，不支持自定义权限配置。

### 权限配置

创建 API Key 时可选两种权限：

- **全部**：可调用所有模型与应用。
- **自定义**：可配置 IP 白名单（最多 20 个 IPv4/IPv6 地址或网段）和可访问模型范围。

### 格式与类型

- **按量付费 API Key**：安全升级后新建的 Key 统一以 `sk-ws` 开头，仅在创建时展示一次明文；升级前以 `sk-` 开头的旧 Key 可继续使用，建议逐步替换。
- **[Token](token.md) Plan 与 Coding Plan**：使用以 `sk-sp-` 开头的专属 API Key，不使用按量付费 API Key。
- **临时 API Key**：通过令牌接口生成，以 `st-` 开头，继承生成它的永久 API Key 的全部权限，无法进一步收窄。

### 环境变量配置

为避免硬编码泄露，建议将 API Key 配置到环境变量 `DASHSCOPE_API_KEY`，SDK 会自动读取。各系统配置方式：

- **Linux/macOS**：永久生效追加到 `~/.bashrc`（Bash）或 `~/.zshrc`（Zsh）后 `source`；临时生效用 `export DASHSCOPE_API_KEY="YOUR_KEY"`。
- **Windows**：永久用系统属性界面、CMD `setx` 或 PowerShell `[Environment]::SetEnvironmentVariable`；临时用 CMD `set` 或 PowerShell `$env:`。

若 `echo` 能读到环境变量但代码仍报找不到 API Key，常见原因：临时变量未重启 IDE/应用、systemd/supervisord 服务需在配置文件中显式添加、`sudo` 运行时不继承用户环境变量（改用 `sudo -E`）。

### 临时 API Key 生成

通过令牌接口生成临时 API Key：

| 参数 | 说明 |
| --- | --- |
| `expire_in_seconds` | 临时 Key 有效期，单位秒，范围 `[1, 1800]`，默认 60 秒 |

请求示例：

```
curl -X POST "https://dashscope.aliyuncs.com/api/v1/tokens?expire_in_seconds=1800" \
-H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

正常响应返回 `token`（临时 Key）与 `expires_at`（UNIX 时间戳，秒），到期自动失效，不能提前删除。

## 时效性与配额

- API Key 无失效日期，手动删除后即失效。
- 单个主账号在华北2/新加坡/日本/德国地域每个地域最多 50 个 API Key；美国（弗吉尼亚）地域每个归属账号最多 20 个。
- RAM 用户被禁用或删除后，其创建的 API Key 全部失效。
- 各地域（北京、新加坡、弗吉尼亚等）的 API Key 不互通，临时 Key 与生成它的永久 Key 必须属于同一地域。

## 子[业务空间](workspace.md)的 API Key

默认[业务空间](workspace.md)的 API Key 可调用所有模型，权限过大且费用难以分账。可将 RAM 用户归入子业务空间，仅授权必要模型，并要求使用该子空间的 API Key 调用。调用方式与默认空间基本一致，区别在于必须使用该子业务空间的 API Key。适用场景包括模型调用权限管控（限制某类用户只能调用被授权的模型）与费用分账（为不同业务创建独立子空间各自出账）。

## 关联主题页

- [preparations](../api/preparations.md)
- [application call](../api/application-call.md)
- [frameworks](../api/frameworks.md)
- [bailian application calling](../guides/bailian-application-calling.md)
- [more about models](../api/more-about-models.md)
- [more](../api/more.md)
- [get started with models](../guides/get-started-with-models.md)


