# sandbox

Sandbox 是阿里云百炼提供的云端安全沙箱服务，为 AI 智能体提供隔离的代码执行、浏览器操作与文件处理环境。它基于模版（Template）启动实例（Sandbox），每个实例拥有独立计算资源、文件系统与网络隔离，并完全兼容 E2B SDK/API 协议。开发者可通过控制台、E2B SDK 或 REST API 快速接入和管理。

## 支持的模型/功能

Sandbox 不运行大语言模型本身，而是提供三种预置基础镜像作为运行时环境：

- **`code-interpreter-v1`**：轻量级代码解释器，支持 Python / Node.js，适用于数据分析、脚本执行等任务；
- **`browser`**：基于 Chromium 的浏览器环境，支持 UI 自动化、截图、网页交互；
- **`all-in-one`**（全能型）：集成 Python、Node.js、Chromium、常见 CLI 工具及依赖的综合镜像，适用于多阶段、多能力协同的任务。

所有镜像均支持标准数据面操作：命令执行（`commands.run`）、文件读写（`files.write`/`files.read`）、目录管理（`files.make_dir`），以及通过 `e2b-code-interpreter` 扩展包调用 `run_code`。浏览器镜像额外支持 `sbx.browser` 接口进行页面导航与 DOM 操作（详见 [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md)）。

> **注意**：文档 1 和文档 3 均列出三类镜像名称，但文档 2 的快速开始示例中写作 `code-interpreter-v1`（带 `-v1` 后缀），而文档 5 更新日志中未带版本号。实际创建模版时必须使用带版本后缀的完整镜像标识（如 `code-interpreter-v1`），否则模版创建失败 —— 此为当前生产环境强制要求，[快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md) 中的配置字段说明已体现该约束。

## 关键参数

| 参数 | 说明 | 来源/约束 |
|------|------|-----------|
| `template` | 模版唯一标识符（`templateCode`），由控制台创建模版后生成，必填 | 见 [模版管理](../../raw/application-user-guide/sandbox/sandbox-templates.md) |
| `api_url` | 百炼沙箱接入地址，格式为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox` | 需替换 `{workspace_id}`，详见 [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md) |
| `headers.Authorization` | 真实鉴权凭证，值为 `Bearer <阿里云百炼 API Key>`（`sk-...` 格式） | **必须**，SDK 不校验 `api_key` 字段，仅用于满足 E2B SDK 格式要求 |
| `api_key` | E2B SDK 必填字段，仅需满足 `e2b_` + 十六进制字符格式（如 `e2b_123456789`），推荐使用 `e2b_${ALIYUN_UID}` | [快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md) 明确说明其为占位参数 |
| 生命周期参数 | `idle_timeout_seconds`（空闲超时）或 `max_duration_seconds`（最大存活时间），二选一，上限均为 604800 秒（7 天） | 模版级配置，见 [概述](../../raw/application-user-guide/sandbox/sandbox-introduction.md) |

## 使用方式

1. **前置准备**：开通百炼服务并完成 [服务关联角色（SLR）授权](../../raw/application-user-guide/sandbox/sandbox-quick-start.md)，获取阿里云 UID 与 `sk-...` 格式的 API Key；
2. **创建模版**：在控制台 [Sandbox > 我的模版](https://bailian.console.aliyun.com/cn-beijing/sandbox/my-template) 中选择镜像、资源配置（1C2G 或 4C8G）及可选高级配置（网络白名单、环境变量等）；
3. **初始化 SDK**：
   ```python
   from e2b import Sandbox
   sbx = Sandbox.create(
       api_url="https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox",
       api_key=f"e2b_{ALIYUN_UID}",
       headers={"Authorization": f"Bearer {BAILIAN_API_KEY}"},
       template="your-template-code"
   )
   ```
4. **数据面操作**：调用 `sbx.commands.run()`、`sbx.files.write()`、`sbx.run_code()` 等方法；
5. **生命周期管理**：`sbx.pause()` 暂停（保留状态），`Sandbox.connect()` 恢复连接，`sbx.kill()` 彻底释放。

## 限制和注意事项

- **实例生命周期**：空闲超时与最大存活时间上限均为 7 天（604800 秒），超时后实例自动释放，不可恢复；
- **资源规格**：仅支持两种预设配置（1 Core｜2 GB 或 4 Core｜8 GB），不支持自定义 CPU/内存配比；
- **文件挂载**：模版创建时最多可上传 5 个初始文件，实例运行时通过 `sbx.files.*` API 无数量限制；
- **网络访问**：默认禁止外网访问；如需访问公网，须在模版高级配置中显式设置网络白名单（支持域名或 CIDR）；
- **鉴权安全**：`api_key` 参数**不参与业务鉴权**，真实鉴权仅依赖 `Authorization: Bearer <sk-...>` 请求头 —— 此设计已在 [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md) 中明确强调；
- **模版删除约束**：若模版下存在运行中或已暂停的实例，则无法删除模版，需先调用 `sbx.kill()` 或控制台释放所有关联实例。

## 来源文档

- [概述](../../raw/application-user-guide/sandbox/sandbox-introduction.md)
- [快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md)
- [模版管理](../../raw/application-user-guide/sandbox/sandbox-templates.md)
- [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md)
- [更新日志](../../raw/application-user-guide/sandbox/sandbox-changelog.md)


