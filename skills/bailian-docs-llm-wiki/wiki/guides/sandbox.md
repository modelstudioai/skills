# sandbox

Sandbox 是阿里云百炼提供的云端安全沙箱服务，为 AI 智能体提供隔离的代码执行、浏览器操作与文件处理环境。它基于模版（Template）启动实例（Sandbox），每个实例拥有独立计算资源、文件系统与网络，并完全兼容 E2B SDK/API 协议。该服务面向开发者设计，支持通过控制台、E2B SDK 或 REST API 三种方式接入和管理。

## 支持的模型/功能

Sandbox 不运行大语言模型本身，而是提供**运行时环境**，当前支持以下三类基础镜像（对应不同能力组合）：

- `code-interpreter-v1`：轻量级代码解释器镜像，预装 Python 3.11、Node.js 18、常用科学计算库（pandas、numpy、matplotlib 等），适用于数据分析、脚本执行等任务。  
- `browser`：基于 Chromium 的无头浏览器环境，支持 Puppeteer/Playwright 风格操作，适用于网页自动化、截图、UI 测试等场景。  
- `all-in-one`：全能型镜像，同时集成上述两类运行时及额外工具链（如 git、curl、ffmpeg），适用于需多语言协同或综合能力的任务。

> **注意**：文档 1 和文档 3 均列出三类镜像名称，但文档 2 的「步骤 2：创建模版」中将 `all-in-one` 写为 `all-in-one`（正确），而文档 5 的更新日志中误写为 `all-in-one`（实际应为 `all-in-one`）——以控制台 UI 和 API 实际接受值为准，推荐使用 `all-in-one`。该不一致已在 [更新日志](../../raw/application-user-guide/sandbox/sandbox-changelog.md) 中体现，但需开发者在调用时校验模版 code 是否生效。

所有镜像均支持标准数据面操作：命令执行（`commands.run`）、文件读写（`files.read`/`write`）、目录管理（`files.make_dir`），以及（仅 `code-interpreter-v1` 和 `all-in-one`）代码执行（`run_code`）。浏览器能力需在 `browser` 或 `all-in-one` 镜像中显式调用 Puppeteer/Playwright 客户端。

## 关键参数

| 参数 | 说明 | 来源与约束 |
|------|------|------------|
| `template` | 模版唯一标识符（`templateCode`），创建实例时必填。可在 [模版管理](../../raw/application-user-guide/sandbox/sandbox-templates.md) 控制台获取。 | 必须与已创建模版匹配；大小写敏感；长度 ≤ 64 字符 |
| `api_url` | 百炼沙箱接入地址，格式为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox`。`workspace_id` 需从控制台获取。 | 见 [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md) 示例代码 |
| `headers.Authorization` | 真实鉴权凭证，值为 `Bearer <阿里云百炼 API Key>`（`sk-...` 格式）。此字段用于百炼侧身份核验。 | **不可省略**；API Key 需具备 `bailian:SandboxFullAccess` 权限 |
| `api_key` | E2B SDK 强制要求的占位参数，仅用于满足 SDK 格式校验（需以 `e2b_` 开头且后缀为十六进制字符）。**百炼侧不使用该值鉴权**。推荐设为 `e2b_${ALIYUN_UID}`。 | 见 [快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md) 说明 |

生命周期相关参数（空闲超时、最大存活时间）仅在模版创建时配置，不可在实例创建时覆盖。最长存活时间为 7 天，详见 [概述](../../raw/application-user-guide/sandbox/sandbox-introduction.md)。

## 使用方式

### 1. 控制台快速上手  
完成服务授权 → 创建模版（选择镜像、资源配置、高级配置）→ 获取 API Key → 调用 SDK。全程约 3 分钟，详细流程见 [快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md)。

### 2. SDK 接入（推荐）  
安装指定版本 SDK：
```bash
pip install "e2b==2.31.0"
pip install "e2b-code-interpreter==2.8.1"  # 如需 run_code
```
创建并使用实例：
```python
from e2b import Sandbox

sbx = Sandbox.create(
    api_url="https://xxx.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox",
    api_key=f"e2b_{ALIYUN_UID}",
    headers={"Authorization": f"Bearer {BAILIAN_API_KEY}"},
    template="your-template-code",
)

# 执行命令、读写文件、运行代码（依镜像能力）
result = sbx.commands.run("ls -l")
sbx.files.write("/tmp/data.txt", "hello")
```

### 3. 直接调用 REST API  
所有管控面操作（模版增删改查、实例创建/暂停/释放）均兼容 E2B 协议，详见 [Sandbox API](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md)。注意：模版管理无稳定 SDK 封装，需自行构造 HTTP 请求。

## 限制和注意事项

- **资源限制**：单实例最大资源配置为 4 Core / 8 GB（见 [快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md)）；超出需提工单申请。
- **生命周期**：实例空闲超时后进入暂停状态，保留文件系统与内存；但若未在 7 天内恢复，将被自动释放。**暂停状态不计费，但释放后数据不可恢复**。
- **网络策略**：默认禁止外网访问；如需访问公网，必须在模版中配置网络白名单（支持 CIDR 或域名），且 `browser` 镜像需额外启用 `--no-sandbox` 标志（由平台自动注入）。
- **文件挂载**：模版创建时最多可挂载 5 个本地文件（≤ 100 MB 总大小），挂载路径固定为 `/home/user/workspace/` 下。
- **鉴权安全**：`api_key` 参数仅为 SDK 兼容性占位，**真实鉴权仅依赖 `Authorization` header**。切勿将百炼 API Key 填入 `api_key` 字段。
- **地域限制**：当前仅支持 `cn-beijing` 地域，`api_url` 中的 endpoint 必须匹配。

## 来源文档

- [概述](../../raw/application-user-guide/sandbox/sandbox-introduction.md)
- [快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md)
- [模版管理](../../raw/application-user-guide/sandbox/sandbox-templates.md)
- [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md)
- [更新日志](../../raw/application-user-guide/sandbox/sandbox-changelog.md)


