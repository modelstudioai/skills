# sandbox api

sandbox api 是百炼平台提供的用于安全隔离环境内运行代码、调试模型及执行沙箱化任务的 RESTful 接口集合。它支持按需创建临时计算实例、加载预置模板或自定义镜像，并提供标准 HTTP 接口进行生命周期管理与交互。该 API 适用于需要可控执行环境的场景，如模型推理验证、用户代码安全执行、自动化测试等。

## 支持的模型/功能

- 支持基于容器的轻量级沙箱实例，可运行 Python、Node.js、Shell 等主流运行时；
- 提供预置模板（如 `python3.11-cpu`、`llm-inference-base`），也支持通过 [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md) 接口上传自定义 Docker 镜像；
- 支持同步执行（`/run`）与异步任务（`/submit` + `/status`）两种调用模式，适用于短时脚本与长时推理任务；
- 实例支持挂载用户上传的文件（通过 `file_ids` 参数）、设置环境变量及指定 CPU/GPU 资源规格（需配额许可）。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `template_id` | string | 是 | 模板唯一标识，可从 [模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md) 获取列表；若使用自定义镜像，需先调用模板创建接口注册 |
| `code` | string | 否 | 待执行的源码（如 Python 脚本），与 `file_ids` 二选一；长度上限 64KB |
| `file_ids` | string[] | 否 | 已上传至百炼文件服务的文件 ID 列表，沙箱启动后自动解压并执行 `entrypoint`（默认 `main.py` 或 `index.js`） |
| `timeout` | integer | 否 | 执行超时时间（秒），范围 1–300，默认 60 |
| `env` | object | 否 | 环境变量键值对，如 `{"DEBUG": "1"}`，不支持敏感键名（如 `API_KEY`） |

> **注意**：原始文档中 [API 总览与认证](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md) 提到 `instance_type` 参数用于指定 GPU 类型，但该字段已在 v2.3+ 版本中废弃，实际资源规格由 `template_id` 决定，调用时传入将被忽略。

## 使用方式

1. **认证**：使用 Bearer Token 认证，Token 通过百炼控制台「API 密钥」生成，需具备 `sandbox:execute` 权限；
2. **创建并执行**：向 `POST /v1/sandbox/run` 发送请求，携带上述关键参数；
3. **异步流程**：调用 `POST /v1/sandbox/submit` 获取 `task_id`，再轮询 `GET /v1/sandbox/status/{task_id}` 查询结果；
4. **调试建议**：首次使用前，建议先通过 [实例管理](../../raw/application-api-reference/sandbox-api/sandbox-api-instances.md) 接口查看当前活跃实例状态，确认配额与模板可用性。

## 限制和注意事项

- 单次执行最大内存为 4GB，GPU 实例仅限企业版账户且需单独申请配额；
- 沙箱网络默认禁止外连（`outbound_network: false`），如需访问公网，须在模板中显式启用并经安全审批；
- 文件上传大小单个不超过 50MB，总 `file_ids` 数量不超过 10 个；
- 所有沙箱实例在任务结束后自动销毁，不保留磁盘状态；如需持久化输出，请在代码中显式打印或调用 `print()` 输出至 stdout/stderr —— 这是唯一保证返回的输出通道；
- 模板更新后，旧模板 ID 仍可使用，但新创建的实例将基于模板最新版本镜像，[模版管理](../../raw/application-api-reference/sandbox-api/sandbox-api-templates.md) 文档未明确说明此行为是否触发缓存失效，建议在关键场景中显式指定 `template_version`（如支持）。

## 来源文档

- [Sandbox](../../raw/application-api-reference/sandbox-api.md)


