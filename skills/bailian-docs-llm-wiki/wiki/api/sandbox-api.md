# sandbox api

Sandbox API 是百炼平台提供的用于动态创建、管理与销毁隔离沙箱环境的 RESTful 接口，适用于需要临时计算资源、代码执行或模型推理验证的场景。它支持按需启动预置模板的沙箱实例，并提供完整的生命周期控制能力。该 API 与百炼主推理服务解耦，但可与 [Sandbox API 概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md) 中定义的运行时行为保持一致。

## 支持的模型/功能

- **沙箱类型**：仅支持基于 Docker 镜像构建的轻量级 Linux 容器沙箱（不支持 Windows 或 GPU 加速沙箱）；
- **内置能力**：支持标准 Python 3.9+ 运行时、HTTP 服务暴露（端口映射）、文件上传/下载、以及 5 分钟内自动超时回收；
- **模板来源**：所有沙箱必须基于已注册的模板启动，模板可通过 [Sandbox API 模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md) 创建和更新；
- **注意**：原始文档中提及“支持 Jupyter 内核直连”，但该功能已在 v2.3.0 后移除，实际调用将返回 `400 UnsupportedFeature` —— 请以 [Sandbox API 实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md) 的最新响应体字段为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `template_id` | string | 是 | 模板唯一标识，需通过 `/templates` 接口获取； |
| `timeout_seconds` | integer | 否 | 实例存活时间，范围 60–1800 秒，默认 300； |
| `env` | object | 否 | 环境变量键值对（最多 20 对，单个值 ≤ 4KB）； |
| `ports` | array | 否 | 端口映射列表，如 `[{"container_port": 8080, "protocol": "http"}]`； |

> **注意**：`ports` 中 `protocol` 字段当前仅接受 `"http"`，`"https"` 和 `"tcp"` 均被拒绝，此限制未在 [Sandbox API 概览](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md) 中明确说明，但已被 [Sandbox API 实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md) 的 OpenAPI Schema 严格约束。

## 使用方式

1. **认证**：使用 Bearer [Token](../concepts/token.md)，[Token](../concepts/token.md) 需通过百炼平台 OAuth2 流程获取，并具备 `sandbox:instances:write` scope；
2. **创建实例**：`POST /v1/sandbox/instances`，请求体为 JSON，含上述关键参数；
3. **轮询状态**：通过 `GET /v1/sandbox/instances/{instance_id}` 获取 `status`（`pending`/`running`/`failed`/`terminated`）；
4. **交互**：实例就绪后，通过返回的 `endpoint`（格式 `https://<id>.sandbox.qwen.ai`）发起 HTTP 请求；
5. 所有操作均需遵循 [Sandbox API 认证](../../raw/application-api-reference/sandbox-api/sandbox-api-authentication.md) 中定义的签名与重试策略。

## 限制和注意事项

- 单用户并发沙箱实例上限为 5 个，超出时返回 `429 Too Many Requests`；
- 每个沙箱内存上限 2GB，CPU 配额为 1 核（不可调整）；
- 实例创建后若 60 秒内未进入 `running` 状态，将自动标记为 `failed` 并释放资源；
- 日志仅保留最近 24 小时，且不支持流式拉取（需调用 `/logs` 接口一次性获取完整文本）；
- 错误响应结构统一遵循 [Sandbox API 错误码](../../raw/application-api-reference/sandbox-api/sandbox-api-errors.md)，建议解析 `error.code` 而非 HTTP 状态码做业务判断。

## 来源文档

- [Sandbox API](../../raw/application-api-reference/sandbox-api.md)


