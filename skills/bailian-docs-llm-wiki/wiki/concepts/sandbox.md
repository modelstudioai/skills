# 安全沙箱

安全沙箱是百炼平台提供的云端隔离执行环境，为 AI 智能体、代码片段、浏览器自动化脚本及文件处理任务提供资源独立、网络可控、文件系统私有、生命周期可管的运行时保障。它不提供模型推理能力，而是作为**可信的“执行引擎”**，确保不可信或动态生成的逻辑在受控边界内安全运行。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Managed Agents）**：作为 Agent 的默认执行底座，支撑 `bash`、`read`/`write`/`edit` 等内置工具调用。Agent 会话自动绑定一个按需创建、自动回收的沙箱实例，开发者无需手动管理生命周期，但可通过 `Environment` 配置预装依赖与网络策略。
  
- **Sandbox SDK/API 直接调用**：面向需要细粒度控制的开发者，通过 E2B 兼容 SDK 或 RESTful API 创建沙箱实例，适用于：
  - 动态执行用户提交的 Python 脚本（如数据分析、格式转换）；
  - 启动无头浏览器完成网页抓取、表单填写或截图；
  - 构建端到端流水线（如 `browser → download file → run_code → export result`），使用 `all-in-one` 模板实现跨能力协同。

- **LLM 应用（工作流 & 高代码应用）**：在工作流中，可通过「代码执行」节点或「自定义函数」节点触发沙箱；高代码应用则通过 `fastmcp.Client` 调用 MCP 工具时，底层由沙箱承载实际执行，实现模型逻辑与运行环境解耦。

- **Skill（技能）**：所有官方及自定义 Skill 的实际执行均运行于沙箱中。例如 `pdf-extractor` 或 `xlsx-cleaner` 技能会在隔离环境中加载文件、执行解析逻辑、返回结构化结果，避免依赖污染或资源冲突。

- **模型验证与调试**：开发者可利用沙箱快速验证模型输出的代码是否可安全执行（如生成的 Pandas 脚本）、测试模型调用外部服务的兼容性，或进行轻量级函数计算（如数据脱敏、特征工程），无需部署真实服务。

## 关键参数和配置

| 参数 | 说明 | 注意事项 |
|------|------|----------|
| `template` / `template_id` | 必填。模版唯一标识符，决定镜像类型（如 `code-interpreter-v1`、`browser`、`all-in-one`、`python39-cpu`）、资源配置（CPU/GPU/内存）及默认策略。模版在控制台创建后生成，不可修改。 | 模版更新不影响已创建实例；新实例继承最新模版定义。 |
| `timeout` / `timeoutMs` | 实例最大存活时间（秒或毫秒）。默认 60s（API）或 300s（SDK），浏览器类任务建议设为 `300000`–`900000`（5–15 分钟）。超时后自动销毁。 | 不是单次命令超时，而是整个实例生命周期上限。 |
| `enable_network`（API） | 布尔值，默认 `false`。启用后允许沙箱访问公网，但需提前在控制台申请网络白名单权限。 | 生产环境强烈建议关闭，或仅放行必要域名/IP。 |
| `api_url` + `Authorization` 头 | SDK/API 认证必需。`api_url` 格式为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox`；`Authorization: Bearer sk-...` 是**唯一生效的认证凭证**。 | `api_key` 字段（E2B SDK 要求）仅用于格式校验，百炼侧完全忽略，填 `e2b_${ALIYUN_UID}` 即可。 |
| `code`（API） | 可选。直接传入待执行的 Python 字符串，适合简单脚本。复杂逻辑建议先上传文件再执行。 | 不支持多文件或交互式会话，仅执行一次并返回 stdout/stderr。 |

> ⚠️ 版本兼容性：当前稳定 SDK 版本为 `e2b==2.31.0` 和 `e2b-code-interpreter==2.8.1`（或 `@e2b/code-interpreter==2.6.1`）。使用更高版本将返回 `405` 错误。

## 面向开发者，简洁实用

- ✅ **快速上手**：  
  ```bash
  pip install "e2b==2.31.0" "e2b-code-interpreter==2.8.1"
  ```
  ```python
  from e2b import Sandbox
  sbx = Sandbox.create(
      template="code-interpreter-v1",
      api_url="https://xxx.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox",
      headers={"Authorization": "Bearer sk-..."},
      timeoutMs=300000,
  )
  result = sbx.run_code("import pandas as pd; pd.__version__")
  print(result.text)
  sbx.close()  # 显式释放资源
  ```

- ✅ **最佳实践**：  
  - 优先复用模版，避免每次创建重复配置；  
  - 敏感操作（如文件写入、网络请求）务必在沙箱内完成，禁止在模型侧或应用层直接执行；  
  - 文件传输必须通过 `sbx.files.write()` / `sbx.files.read()` 或 `/upload` / `/download` 接口，沙箱内无持久存储；  
  - 浏览器任务连接 CDP 端口（`wss://<host>/ws/automation`）前，确认模版为 `browser` 或 `all-in-one` 类型且端口已暴露。

- ❌ **禁止行为**（沙箱内受限）：  
  - fork 进程、加载内核模块、访问 `/proc` `/sys` 等系统路径；  
  - 绑定本地端口、启动后台守护进程；  
  - 使用 `sudo` 或其他提权操作。  

安全沙箱不是“万能执行器”，而是你 AI 应用的**安全边界守门员**——明确它的能力边界，才能让智能体真正可靠地替你干活。

## 关联主题页

- [sandbox](../guides/sandbox.md)
- [sandbox api](../api/sandbox-api.md)
- [managed agents](../guides/managed-agents.md)
- [llm application](../guides/llm-application.md)
- [skill](../guides/skill.md)


