# 沙箱环境

沙箱环境是百炼平台提供的**云端隔离计算环境**，为 AI 智能体、代码执行、浏览器自动化及文件处理等任务提供安全、可控、可复用的运行时上下文。每个沙箱实例拥有独立的 CPU/内存资源、私有文件系统、进程空间与网络策略，与宿主系统及其他实例完全隔离，确保任务可信执行。

## 在百炼平台的不同场景中如何使用

- **智能体（Managed Agents）**：作为智能体的默认执行底座，托管 `bash`、`read`/`write`、`download_file` 等内置工具调用；开发者通过配置 `environment_id` 将会话绑定到预设沙箱环境，实现命令执行、依赖安装（`pip install`/`apt-get`）、临时文件读写与状态持久化。
- **LLM 应用（Agent 2.0 / Workflow）**：在智能体应用中，沙箱作为“代码解释器”或“浏览器工具”的底层载体，支撑模型生成的 Python/Node.js 代码执行或网页截图、表单填写等 UI 自动化任务；工作流中的“代码执行节点”或“浏览器节点”也隐式调度沙箱实例。
- **SDK 与 API 直接调用（Sandbox SDK / Sandbox API）**：开发者可通过 E2B 兼容 SDK 或 RESTful API 主动创建、控制沙箱实例，适用于模型调试、动态脚本执行、安全文件解析等需精细生命周期管理的场景。
- **插件与自定义工具集成**：当插件需执行不可信代码或访问外部资源（如爬取网页），可将其封装为沙箱内调用，规避服务端直接暴露风险；RAG 文件解析后的代码执行、图片 OCR 后的数据清洗等均推荐在此环境中完成。

> ✅ 提示：所有场景下，沙箱不运行大语言模型本身，仅作为模型决策后**工具执行的受控容器**。

## 关键参数和配置

| 参数 | 说明 | 注意事项 |
|------|------|----------|
| `template`（SDK） / `template_id`（API） | 模板唯一标识符（英文 code），如 `"code-interpreter-v1"`、`"browser"`、`"all-in-one"` | UI 显示中文名（如“代码解释器”）仅为别名，API/SDK 必须传英文 code；模板需在控制台预先创建并获取 code |
| `api_url` | 接入地址：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox` | `workspace_id` 必须准确，不可省略或替换为占位符 |
| `Authorization: Bearer <API Key>` | 鉴权头，使用百炼控制台生成的 `sk-...` 格式密钥 | 唯一有效鉴权方式；`api_key` 字段（E2B SDK 中）仅为格式兼容占位，**阿里云侧完全忽略**，建议设为 `e2b_{ALIYUN_UID}` |
| `idle_timeout_seconds` / `max_duration_seconds` | 实例空闲超时（秒）或最大存活时间（秒） | 二者**二选一**，不可共存；`max_duration_seconds` 最长支持 604800（7 天）；超时后实例释放，状态不可恢复 |
| `networking.type`（环境配置） | 网络策略：`unrestricted`（允许出站）、`none`（禁用外网）、`public`（API 中显式启用） | 默认禁止外连；需公网访问时，必须在模板或环境配置中明确开启，否则 `curl`/`requests` 等将失败 |
| `timeout`（API `/run`） | 同步执行超时时间（秒），默认 30，最大 600 | 仅对 `/v1/sandbox/run` 接口生效；异步实例通过 `max_duration_seconds` 控制 |

## 面向开发者的实用建议

- ✅ **优先使用模版**：避免每次创建实例都指定镜像与资源，统一在控制台 [Sandbox > 我的模版](https://bailian.console.aliyun.com/cn-beijing/sandbox/my-template) 中预置常用配置（如 `all-in-one` + 4C8G + `unrestricted` 网络）。
- ✅ **正确处理生命周期**：调用 `sbx.pause()` 可暂停并保留状态；但 `sbx.kill()` 或超时释放后无法恢复——长时任务请用异步实例 + `max_duration_seconds` 延长存活期。
- ✅ **文件操作路径规范**：所有写入默认落盘至 `/tmp`（可写），根文件系统为只读；读取上传文件时，路径以 `/mnt/data/` 开头（如 `/mnt/data/report.pdf`）。
- ✅ **依赖安装**：在 `all-in-one` 或 `code-interpreter-v1` 模板中，可直接运行 `pip install -U pandas` 或 `npm install axios`，安装结果在实例生命周期内持续有效。
- ⚠️ **注意并发限制**：同一 API Key 下，沙箱实例并发上限为 20，同步 `/run` 请求限频 60 次/分钟；高并发场景请复用实例或使用 `pause`/`resume` 降低创建开销。
- ⚠️ **输出截断风险**：同步执行（`/run`）响应体最大 1 MB，超长日志或大文件内容会被截断；需完整输出时，请改用异步实例 + `sbx.commands.run(..., timeout=300)` 并轮询结果。

## 关联主题页

- [sandbox](../guides/sandbox.md)
- [sandbox api](../api/sandbox-api.md)
- [managed agents](../guides/managed-agents.md)
- [llm application](../guides/llm-application.md)
- [application support](../guides/application-support.md)


