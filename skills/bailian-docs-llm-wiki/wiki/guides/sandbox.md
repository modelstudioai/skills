# sandbox

Sandbox 是阿里云百炼提供的云端安全沙箱服务，为 AI 智能体提供隔离的代码执行、浏览器操作与文件处理环境，兼容 E2B SDK/API 协议。每个沙箱实例基于模版启动，拥有独立计算资源、文件系统与网络隔离，支持按需创建、暂停、恢复与释放。其设计目标是保障多租户场景下运行时的安全性与确定性，同时保持开发者体验的一致性。

## 支持的模型/功能

Sandbox 不提供“模型”本身，而是提供三种预置基础镜像（即运行时环境），用于支撑不同类型的智能体任务：

- **代码解释器**（`code-interpreter-v1`）：轻量级 Python/Node.js 执行环境，适用于数据分析、脚本运行等场景；需配合 `e2b-code-interpreter==2.8.1` 使用 `run_code()` 等能力 [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md)。
- **浏览器**（`browser`）：基于 Chromium 的 UI 自动化环境，支持截图、网页交互与 UI 测试。
- **全能型**（`all-in-one`）：集成 Python、Node.js、Chromium 及常用工具链的综合运行时，适用于需多语言或混合能力的任务。

> **注意**：所有镜像均不支持 GPU 加速，且未声明对 Rust、Go 或自定义二进制的原生支持；如需扩展能力，须通过模版挂载文件或注入环境变量实现。

## 关键参数

| 参数 | 说明 | 来源与约束 |
|------|------|------------|
| `template` | 模版唯一标识符（`templateCode`），控制台创建后生成，必填 | 见 [模版管理](../../raw/application-user-guide/sandbox/sandbox-templates.md) |
| `api_url` | 百炼沙箱接入地址，格式为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox` | 必须与工作区地域匹配，详见 [快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md) |
| `Authorization` | 实际鉴权凭证，值为 `Bearer <阿里云百炼 API Key>`（`sk-...`） | `api_key` 字段仅用于满足 E2B SDK 格式要求，**不参与业务鉴权** [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md) |
| `api_key` | E2B SDK 必填字段，格式须为 `e2b_` + 十六进制字符串（推荐 `e2b_${ALIYUN_UID}`） | 阿里云 UID 为纯数字，天然满足校验；该字段在百炼侧被忽略 |

## 使用方式

1. **前置准备**：确保账号已开通百炼服务并完成 [服务授权](../../raw/application-user-guide/sandbox/sandbox-quick-start.md)，获取 `ALIYUN_UID` 和 `sk-...` API Key；
2. **创建模版**：在控制台选择镜像、资源配置（1C2G 或 4C8G）、可选高级配置（文件挂载、网络白/黑名单、环境变量、生命周期）；
3. **调用 SDK**：
   ```python
   from e2b import Sandbox
   sbx = Sandbox.create(
       api_url="https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox",
       api_key=f"e2b_{ALIYUN_UID}",
       headers={"Authorization": f"Bearer {BAILIAN_API_KEY}"},
       template="your-template-code"
   )
   result = sbx.commands.run("ls -l /home/user/workspace")
   ```
4. **数据面操作**：支持 `sbx.commands.run()`、`sbx.files.write()`/`read()`、`sbx.run_code()`（需额外安装 `e2b-code-interpreter`）等标准 E2B 接口；
5. **生命周期管理**：`sbx.pause()` 暂停（保留状态）、`Sandbox.connect()` 恢复、`sbx.kill()` 彻底释放。

## 限制和注意事项

- **实例生命周期**：空闲超时与最大存活时间二选一，**最长不超过 7 天**；超过后实例自动释放，不可恢复 [概述](../../raw/application-user-guide/sandbox/sandbox-introduction.md)；
- **文件系统**：所有写入默认落盘至 `/home/user/workspace/`，挂载文件上限为 5 个，单文件大小建议 ≤ 100 MB；
- **网络访问**：默认禁止外网访问；如需访问公网，必须在模版中显式配置网络白名单（支持 CIDR 或域名）；
- **权限隔离**：沙箱内进程以非 root 用户（`user`）运行，无法执行 `sudo` 或修改系统级配置；
- **模版删除限制**：若模版关联有运行中或已暂停的实例，则无法删除，需先调用 `sbx.kill()` 或 `sbx.pause()` 清理 [模版管理](../../raw/application-user-guide/sandbox/sandbox-templates.md)；
- > **注意**：文档 2 与文档 5 均明确指出 `api_key` 仅为 E2B SDK 格式占位符，真实鉴权依赖 `Authorization` header —— 此为关键安全设计，切勿混淆用途。

## 来源文档

- [概述](../../raw/application-user-guide/sandbox/sandbox-introduction.md)
- [快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md)
- [模版管理](../../raw/application-user-guide/sandbox/sandbox-templates.md)
- [更新日志](../../raw/application-user-guide/sandbox/sandbox-changelog.md)
- [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md)


