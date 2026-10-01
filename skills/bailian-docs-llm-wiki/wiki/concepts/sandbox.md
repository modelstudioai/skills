# 安全沙箱

安全沙箱是阿里云百炼平台提供的**隔离、可控、按需启停的云端执行环境**，专为 AI 智能体（Agent）调用外部能力而设计。它通过 Linux 容器技术实现资源隔离（CPU/内存/文件系统/网络），确保用户代码、浏览器操作或文件处理任务在受限、无副作用的安全边界内运行，不污染主应用进程，也不影响其他实例。

## 在百炼平台的不同场景中，这个概念如何使用

安全沙箱不是独立功能，而是作为底层运行时支撑三类关键 AI Agent 能力：

- **代码执行（Code Interpreter）**：用于运行 Python/Node.js 脚本，完成数据清洗、数学计算、图表生成等任务。典型集成方式是通过 `e2b-code-interpreter` SDK 调用 `run_code()`，结果结构化返回（如 Pandas DataFrame）。适用于智能问答中的实时分析、报表自动生成等场景。
- **浏览器自动化（Browser Use）**：提供标准 CDP（Chrome DevTools Protocol）端点（`wss://<host>/ws/automation`），支持 Puppeteer/Playwright 直接连接，完成网页访问、表单提交、截图、动态内容抓取等。常用于需要真实渲染与交互的场景，如竞品价格监控、登录态保活采集。
- **端到端流水线（AIO）**：融合上述两类能力，同一沙箱实例同时暴露浏览器服务（3000 端口）和 Code Interpreter 服务（5000 端口），支持“打开网页 → 下载 CSV → 本地解析 → 可视化导出”等跨步骤闭环任务，无需实例间数据搬运。

> ⚠️ 注意：沙箱**不提供大模型推理能力**，也**不参与提示词编排或规划决策**——它纯粹是 Agent 规划后触发的「工具执行器」。所有模型调用、意图理解、工具选择均由百炼的 LLM 应用层（如 Agent 2.0 或 Workflow）完成，沙箱只负责可靠、安全地执行具体指令。

## 关键参数和配置

| 参数 | 说明 | 开发者须知 |
|------|------|-----------|
| `template`（SDK 方式） 或 `runtime`（API 方式） | 沙箱模版标识符 | ✅ 必填；SDK 中必须用控制台创建模版时生成的实际 code（如 `browser-abc123`），**不是**控制台显示的别名（如“浏览器”）；API 中填预置运行时名（如 `python311`、`browser`） |
| `api_url`（SDK） / 请求 Host（API） | 百炼沙箱服务地址 | ✅ SDK：替换 `{workspace_id}`；API：使用 `https://dashscope.aliyuncs.com/api/v1/sandboxes`（注意非百炼主域名） |
| `Authorization` | 鉴权头 | ✅ 必填；值为 `Bearer sk-...` 类型的百炼 API Key（**不是** DashScope Token） |
| `api_key`（SDK 专用） | E2B SDK 格式校验字段 | ⚠️ 仅用于满足 SDK 初始化要求；值可设为 `e2b_${ALIYUN_UID}`，**百炼侧完全忽略该值** |
| `timeoutMs`（SDK） / `timeout`（API） | 创建或执行超时 | ✅ 建议 `timeoutMs=300000`（5 分钟）以上；浏览器/AIO 冷启动慢，过短易失败；API 执行默认仅 30 秒，最大 120 秒 |
| `memory_limit_mb`（API） | 内存配额 | ✅ 可选；范围 64–1024 MB，默认 256 MB；超出将被 OOM Kill |

> 🔑 版本强约束：**必须锁定 `e2b==2.31.0`（Python）或 `e2b@2.31.0`（Node.js）**，高版本（≥2.32.0）会返回 HTTP 405 错误。配套子包也需严格匹配（如 `e2b-code-interpreter==2.8.1`）。

## 面向开发者，简洁实用

- **快速起步三步走**：  
  1️⃣ 控制台创建模版（选镜像 `code-interpreter-v1` / `browser` / `all-in-one`，配 1C2G 或 4C8G，设空闲超时）；  
  2️⃣ 安装固定版本 SDK：`pip install "e2b==2.31.0" "e2b-code-interpreter==2.8.1"`；  
  3️⃣ 编码调用：`Sandbox.create(template="xxx")` → `sbx.run_code("import pandas as pd; ...")` → `sbx.kill()`。

- **浏览器沙箱特别注意**：  
  - 获取公网 host 后，CDP URL 格式为 `wss://<host>/ws/automation`（不是 `/devtools/browser/...`）；  
  - host 字符串即为会话凭证，**严禁打印、日志、前端暴露或硬编码**——泄露等于浏览器完全失控。

- **资源与生命周期底线**：  
  - 单实例最大 4 Core / 8 GB；最长存活 7 天（模版配置）或 10 分钟（API 默认空闲回收）；  
  - 所有实例**必须显式调用 `.kill()`**，避免资源泄漏；未释放实例按小时计费。

- **调试建议**：  
  - 执行失败优先检查 `stderr` 输出；  
  - 网络不通？确认沙箱默认**禁止外网访问**（DNS 也不通），如需联网需在模版中开启网络策略；  
  - 文件写入失败？检查路径权限及磁盘配额（默认约 1 GB）。

## 关联主题页

- [sandbox](../guides/sandbox.md)
- [sandbox api](../api/sandbox-api.md)
- [llm application](../guides/llm-application.md)
- [plug in](../guides/plug-in.md)
- [application support](../guides/application-support.md)


