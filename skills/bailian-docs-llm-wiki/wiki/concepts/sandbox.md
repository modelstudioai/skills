# 沙箱执行环境

沙箱执行环境是百炼平台提供的轻量级、隔离式运行时容器，专为高风险、需资源约束与强安全边界的代码执行任务设计。它不承载大模型推理逻辑，而是作为受控的“计算副脑”，在独立 Linux 用户空间中执行 Python 代码、浏览器自动化脚本或数据处理任务，并与主 Agent 通过结构化输入/输出进行协同。

## 在百炼平台的不同场景中，这个概念如何使用

- **Managed Agent 中的工具执行**：启用 `enable_sandbox: true` 后，Agent 自动将 `code_interpreter`、`web_browser` 等工具调用路由至沙箱环境执行，保障模型输出的任意代码不会影响主服务进程或泄露敏感上下文。
- **Flow Agent 的自定义节点**：在工作流中插入「Sandbox 节点」，可编写 `main.py` 实现复杂逻辑（如调用私有 API、解析二进制文件、生成图表），支持 `pip install` 第三方包，但所有依赖需在模版构建阶段预装或挂载。
- **独立沙箱 API 调用**：通过 Sandbox API 直接管理沙箱生命周期（创建/暂停/恢复/释放），适用于需要精细控制执行时长、网络策略或文件挂载的场景，例如批量数据清洗、可信浏览器爬取、RAG 文档预处理等。
- **Agent Store 中的 Skill 执行底座**：部分官方 Skill（如 `pdf-parser`、`xlsx-analyzer`）底层默认运行于沙箱环境，确保文件解析逻辑与用户代码完全隔离，避免恶意文档触发系统级漏洞。
- **调试与开发验证**：在 Sandbox Agent 开发模式下，开启 `debug_mode: true` 可获得实时 stdout/stderr 日志与断点支持，便于快速验证代码逻辑与依赖兼容性。

> ⚠️ 注意：沙箱**不共享 Agent 会话内存**，也不持久化 `/home/user/workspace/` 以外的任何数据；单次执行超时默认为 30 秒（API 创建时可设为 5 分钟–7 天），超时后自动终止并释放资源。

## 关键参数和配置

| 参数 | 作用 | 推荐值/范围 | 说明 |
|------|------|-------------|------|
| `enable_sandbox` | Managed Agent 全局开关 | `true` / `false` | 设为 `true` 后，所有支持沙箱的工具自动启用隔离执行 |
| `timeout` | 沙箱实例生命周期上限 | `300`–`604800`（秒） | 影响计费时长，建议按任务实际需求设置，避免资源闲置 |
| `templateID` | 基础运行环境标识 | 如 `code-interpreter-v1`、`browser` | 必须为已构建完成（`status=ready`）的模版；镜像地址勿硬编码，优先使用平台预置模版名 |
| `mntConfig[].originFileId` | 挂载文件 ID | 文件上传时返回的 `file_id` | 文件需以 `source=sandbox_template` 上传，且状态为 `available` |
| `cpu` / `memory` | 资源规格（仅模版创建时） | `cpu: "1"` / `memory: "2Gi"` | 默认规格为 1 CPU + 2GB 内存；旗舰款支持更高配，详见控制台模版配置页 |
| `network` | 网络策略（仅模版创建时） | `"public"` / `"private"` | `public` 允许访问白名单域名；`private` 完全禁止外网出向，适合处理敏感数据 |

> ✅ 提示：所有沙箱实例均默认启用**内容安全检测**（含代码静态扫描与动态行为分析），禁止访问 `/etc/`、`/proc/`、`/sys/` 等系统路径，且 DNS 查询仅允许阿里云白名单域名（如 `alibaba.com`, `aliyuncs.com`）。

## 面向开发者，简洁实用

- **快速上手**：控制台 → 「应用开发」→ 新建 Sandbox Agent → 编写 `main.py`（必须含 `def main(input: dict) -> dict:`），点击「调试」即可运行。
- **API 集成**：直接复用 E2B SDK（如 `e2b.Sandbox()`），只需替换 `api_key` 为占位符 `e2b_${ALIYUN_UID}`，Endpoint 改为百炼专属地址 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox`。
- **文件处理**：上传文件时指定 `source=sandbox_template`，创建沙箱时通过 `mntConfig` 挂载至 `/home/user/workspace/uploads/`，代码中直接 `open("/home/user/workspace/uploads/my_data.csv")` 即可读取。
- **成本控制**：沙箱按**运行时长 + 数据保留量**计费；暂停实例仍产生快照存储费，如无需恢复，务必调用 `DELETE /sandboxes/{id}` 彻底释放。
- **排障要点**：若沙箱启动失败，优先检查 `templateID` 是否就绪、`originFileId` 是否可用、`timeout` 是否超出平台限制；执行报错请查看 `GET /sandboxes/{id}` 返回的 `logs` 字段。

## 关联主题页

- [sandbox api](../api/sandbox-api.md)
- [get started with agents](../guides/get-started-with-agents.md)
- [agent billing](../guides/agent-billing.md)
- [agent development](../guides/agent-development.md)
- [agent store](../guides/agent-store.md)


