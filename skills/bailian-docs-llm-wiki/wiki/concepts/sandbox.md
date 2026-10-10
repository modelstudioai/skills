# 安全沙箱

安全沙箱是百炼平台提供的**隔离、可控、按需启停的云端执行环境**，为 AI 智能体提供代码运行、浏览器自动化与文件处理的安全载体。它不运行大语言模型本身，而是作为智能体的“手脚”——在严格隔离的容器中执行工具调用、解析结果、访问网页或生成报告，所有操作均受限于资源配额、网络策略与生命周期管控。

## 在百炼平台的不同场景中，这个概念如何使用

- **Managed Agents（托管智能体）**：安全沙箱是其默认且唯一的执行底座。当智能体调用 `bash`、`read`、`write` 或 `web_fetch` 等内置工具时，实际指令均在后台沙箱实例中执行；上传的文件自动挂载至 `/mnt/session/uploads/`，记忆库内容也物化到沙箱文件系统，全程无需开发者手动管理沙箱生命周期——平台自动创建、复用、暂停与释放。
  
- **LLM Application（智能体应用）**：在 Agent 2.0 应用中，若启用「代码解释器」或「浏览器」工具，平台将基于预设模版（如 `code-interpreter-v1` 或 `all-in-one`）动态拉起沙箱实例，并将工具调用透传至该环境；工作流中的「脚本节点」或「MCP 工具节点」也可绑定自定义沙箱模版，实现复杂逻辑的隔离执行。

- **Sandbox SDK/API 直接调用**：面向需要精细控制的开发者，可通过 E2B SDK 或原生 API 手动创建、连接、操作沙箱实例。适用于需跨会话共享状态（如长期爬虫任务）、定制化环境（如预装私有库）、或与非百炼生态工具链集成（如 Playwright 自动化流水线）等场景。

- **安全体系中的关键隔离层**：在《安全指南》框架下，沙箱是「挡」环节的核心载体——工具调用被约束在沙箱内执行，网络出向受模版白名单控制，敏感凭证通过 Vault 注入而非明文传递，文件读写仅限挂载路径，天然阻断横向渗透与数据越界，构成默认防护的基础设施。

> ⚠️ 注意：沙箱**不替代模型安全检测**（如提示词攻击、内容过滤），也不提供持久化存储——所有实例释放后数据即销毁；如需长期保存，必须显式调用 `sbx.files.read()` 或通过 `mark_artifacts` 工具导出。

## 关键参数和配置

| 参数 | 说明 | 开发者须知 |
|------|------|------------|
| `template` / `templateID` | 模版唯一标识符，控制台创建后生成，大小写敏感，必填 | 必须与控制台中模版完全一致；API 中字段名为 `templateID`，SDK 中为 `template` |
| 镜像标识 | 实际运行环境，当前仅支持 `code-interpreter-v1`、`browser`、`all-in-one` | **不可简写**（如不能用 `code-interpreter`），否则创建失败；镜像由模版绑定，不可在实例创建时覆盖 |
| `timeoutMs`（SDK） / `timeout`（API） | 实例最大存活时间（毫秒 / 秒），范围 `[300, 604800]`（5 分钟 ~ 7 天） | 浏览器类任务建议 ≥300000ms（5 分钟），避免冷启动超时；到期行为默认 `kill`，可设为 `pause` 以保留状态 |
| `allow_internet_access`（API） / `network.allowPublicTraffic`（SDK） | 是否允许公网访问，默认 `false` | 如需访问外部网站，必须显式设为 `true`；若需更细粒度控制，请在模版中配置 `allowOut`（域名白名单）或 `denyOut`（IP 黑名单） |
| `cpuCount` & `memoryMB` | 模版级资源配置，必须成对指定，且仅支持平台预设组合（如 `1/2048`, `4/8192`） | 不支持任意值；资源越高，计费越高，但无性能弹性伸缩——请按任务峰值需求选型 |

## 面向开发者，简洁实用

- ✅ **起步最快方式**：用 E2B SDK（固定版本 `e2b==2.31.0`）+ 控制台已建模版，3 行代码即可运行：
  ```python
  from e2b import Sandbox
  sbx = Sandbox.create(template="your-template-code", api_url=API_URL, headers={"Authorization": "Bearer YOUR_API_KEY"})
  result = sbx.commands.run("python -c 'print(2+2)'")
  print(result.stdout)  # 输出: 4
  ```

- ✅ **必须遵守的硬约束**：
  - SDK 版本锁死：Python 用 `e2b==2.31.0`，Node.js 用 `e2b@2.31.0`；更高版本返回 HTTP 405；
  - 镜像名必须带版本号（`code-interpreter-v1`，非 `code-interpreter`）；
  - `api_key` 字段在百炼侧**完全忽略**，仅用于满足 E2B SDK 格式要求，填 `e2b_${ALIYUN_UID}` 即可；
  - 沙箱暴露的 `wss://<host>/ws/automation` 或 noVNC 地址等同于 root 权限，**严禁记录、打印、前端展示或日志输出**。

- ✅ **调试技巧**：
  - 创建失败？检查 `templateID` 是否存在、模版状态是否为 `ready`、`workspace_id` 和地域是否为 `cn-beijing`；
  - 命令卡住？增大 `timeoutMs`，并确认是否需 `allow_internet_access=true`；
  - 文件读不到？确认路径为绝对路径（如 `/mnt/session/uploads/file.pdf`），且文件已通过 `resources` 挂载或 `sbx.files.write()` 写入。

- ❌ **不要做**：
  - 不要在沙箱内安装未授权软件或修改系统级配置；
  - 不要尝试绕过网络限制（如 DNS 劫持、代理隧道）；
  - 不要将沙箱实例 ID 或 host 地址硬编码进前端代码或公开文档。

## 关联主题页

- [sandbox](../guides/sandbox.md)
- [sandbox api](../api/sandbox-api.md)
- [managed agents](../guides/managed-agents.md)
- [security guide](../guides/security-guide.md)
- [llm application](../guides/llm-application.md)


