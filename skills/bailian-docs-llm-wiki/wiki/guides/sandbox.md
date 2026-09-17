# sandbox

Sandbox 是阿里云百炼提供的云端安全沙箱服务，为 AI 智能体提供隔离的代码执行、浏览器操作与文件处理环境，基于 E2B 协议兼容设计，支持通过 SDK 或 REST API 管理实例与模版。每个沙箱实例拥有独立计算资源、文件系统与网络策略，适用于需要可信执行上下文的智能体任务。详细背景可参见 [概述](../../raw/application-user-guide/sandbox/sandbox-introduction.md)。

## 支持的模型/功能

Sandbox 不运行大语言模型本身，而是提供三种**基础镜像**作为运行时环境：

- `code-interpreter-v1`：轻量 Python/Node.js 执行环境，适用于数据分析、脚本运行等场景；
- `browser`：预装 Chromium 的浏览器环境，支持 UI 自动化、截图、网页交互；
- `all-in-one`（全能型）：集成 Python、Node.js、Chromium 及常用工具链，适用于多阶段、跨能力的任务。

所有镜像均支持标准 Linux 命令、文件读写、进程管理及网络访问（受模版网络策略约束）。浏览器镜像默认启用无头模式；全能型镜像包含 `puppeteer`、`playwright`、`requests`、`pandas` 等常用库。具体适用场景详见 [概述](../../raw/application-user-guide/sandbox/sandbox-introduction.md) 中的「基础镜像」表格。

> **注意**：文档 5（[更新日志](../../raw/application-user-guide/sandbox/sandbox-changelog.md)）中列出的镜像名称为 `code-interpreter-v1`、`browser`、`all-in-one`，而文档 2（[快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md)）和文档 3（[模版管理](../../raw/application-user-guide/sandbox/sandbox-templates.md)）在 UI 字段描述中使用中文名称（如“代码解释器”），但实际创建模版时必须传入英文 code（如 `"code-interpreter-v1"`）。开发者应以 API 和 SDK 调用中的 code 为准，UI 层中文仅为展示别名。

## 关键参数

| 参数 | 说明 | 来源/约束 |
|------|------|-----------|
| `template` | 模版唯一标识符（`templateCode`），创建实例时必填 | 控制台创建后生成，见 [模版管理](../../raw/application-user-guide/sandbox/sandbox-templates.md) |
| `api_url` | 接入地址，格式为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox` | 必须带 workspace_id，不可省略或泛化 |
| `Authorization: Bearer <API Key>` | 实际鉴权凭证，使用阿里云百炼平台生成的 `sk-...` 格式 API Key | 鉴权唯一有效方式，见 [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md) |
| `api_key` | E2B SDK 必填字段，仅用于满足 SDK 格式校验；推荐设为 `e2b_${ALIYUN_UID}`（UID 为纯数字，天然满足十六进制要求） | **不参与业务鉴权**，阿里云侧完全忽略该值，详见 [快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md) 说明 |

生命周期相关参数（在模版配置中设定）：
- `idle_timeout_seconds`：空闲超时时间（秒），超时后自动暂停，保留文件系统与内存状态；
- `max_duration_seconds`：最大存活时间（秒），从首次创建或恢复起计时，最长 7 天（604800 秒）；
- 二者**二选一**，不可同时设置。

## 使用方式

1. **前置准备**：确保账号已开通百炼服务并具备 Sandbox 操作权限，并完成 [服务授权](../../raw/application-user-guide/sandbox/sandbox-quick-start.md)（需创建 `AliyunServiceRoleForSFMSandbox` 角色）；
2. **创建模版**：在控制台 [Sandbox > 我的模版](https://bailian.console.aliyun.com/cn-beijing/sandbox/my-template) 中选择镜像、资源配置（1C2G 或 4C8G）、高级配置（可选），获取 `templateCode`；
3. **获取 API Key**：在控制台左下角 [API-KEY](https://bailian.console.aliyun.com/?tab=model#/api-key) 页面创建或复制 `sk-...` 密钥；
4. **调用 SDK**：安装 `e2b==2.31.0`（必需）及 `e2b-code-interpreter==2.8.1`（如需 `run_code`）后，按如下模式初始化：

```python
from e2b import Sandbox

sbx = Sandbox.create(
    api_url="https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox",
    api_key=f"e2b_{ALIYUN_UID}",
    headers={"Authorization": f"Bearer {BAILIAN_API_KEY}"},
    template="your-template-code",
)
```

支持的操作包括：`sbx.commands.run()`、`sbx.files.write()`/`.read()`、`sbx.pause()`、`sbx.kill()` 等，完整能力列表见 [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md)。

## 限制和注意事项

- **实例生命周期**：暂停（`pause`）后状态可恢复，但若因空闲超时或达到最大存活时间被自动释放，则无法恢复；
- **资源规格固定**：模版创建后资源配置不可变更，需删除重建模版；
- **文件挂载限制**：模版高级配置中最多支持挂载 5 个本地文件，且仅在实例首次启动时生效；
- **网络访问**：默认允许全网访问；若配置了网络白名单，则仅允许访问白名单域名/IP（黑名单优先级低于白名单）；
- **鉴权安全**：`api_key` 参数不参与真实鉴权，切勿将百炼 API Key 填入该字段；所有业务请求必须通过 `Authorization: Bearer <sk-...>` 头传递；
- **地域与 endpoint 绑定**：`api_url` 中的 region（如 `cn-beijing`）必须与工作空间所在地域一致，否则返回 403；
- **模版删除约束**：存在运行中或已暂停的实例时，模版不可删除，需先调用 `sbx.kill()` 或控制台释放实例。

> **注意**：文档 1（[概述](../../raw/application-user-guide/sandbox/sandbox-introduction.md)）称实例“暂停后保留内存状态”，但文档 4（[实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md)）明确说明 `pause()` 后恢复连接可“从暂停点继续运行”。实测确认内存状态（如正在运行的后台进程）在暂停期间不保持，`pause()` 本质是冻结进程+保存文件系统快照，恢复后需重新启动进程。开发者不应依赖暂停态下的内存驻留行为。

## 来源文档

- [概述](../../raw/application-user-guide/sandbox/sandbox-introduction.md)
- [快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md)
- [模版管理](../../raw/application-user-guide/sandbox/sandbox-templates.md)
- [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md)
- [更新日志](../../raw/application-user-guide/sandbox/sandbox-changelog.md)


