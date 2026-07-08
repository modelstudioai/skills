# API Key

API Key 是调用阿里云百炼平台模型服务和应用的唯一鉴权凭证，用于标识调用者身份并控制其可访问的模型与资源范围。

## 基本概念

百炼平台的 API Key 由控制台统一管理，归属于特定的[业务空间](workspace.md)和用户。每个 API Key 只能属于一个地域内的一个[业务空间](workspace.md)和一个用户，且不能转移。API Key 没有失效日期，手动删除后即失效。

根据用途和计费方式的不同，百炼平台存在三类 API Key：

| 类型 | 前缀 | Base URL | 计费方式 |
|------|------|----------|----------|
| 按量计费 | `sk-xxx` / `sk-ws-xxx` | `dashscope.aliyuncs.com` | 按 [Token](token.md) 用量后付费 |
| [Token](token.md) Plan 团队版 | `sk-sp-xxx` | `token-plan.cn-beijing.maas.aliyuncs.com` | 预付费 Credits 抵扣 |
| Coding Plan | `sk-sp-xxx` | `coding.dashscope.aliyuncs.com` | 预付费按调用次数 |

三类 API Key 与 Base URL 互不相通，误用会导致非预期扣费或 401/403 报错。

## 创建与获取

### 操作权限

创建 API Key 需使用主账号，或具备「管理员」或「API-Key」页面权限的子账号（RAM 用户）。

### 创建步骤

1. 登录百炼控制台（不同地域入口不同：华北2、新加坡、日本、德国使用 `bailian.console.aliyun.com`；美国使用 `modelstudio.console.aliyun.com`）。
2. 进入密钥管理页面，点击创建 API Key。
3. 选择归属[业务空间](workspace.md)（建议选默认空间）。
4. 配置权限范围（全部模型或自定义 IP 白名单 + 模型范围）。
5. 创建成功后立即复制保存——升级后新创建的 API Key 以 `sk-ws` 开头，仅在创建时展示一次明文，关闭弹窗后无法再次查看。

## 权限模型

API Key 的调用权限由其归属业务空间决定，同一空间内的 API Key 权限相同，无需为不同模型类型（文生文、文生图、语音合成）分别创建。

- **默认业务空间**：API Key 可调用所有标准模型，无法设置模型级限制。
- **子业务空间**：API Key 仅可调用该空间内已授权的模型，支持按模型维度配置调用权限、请求数限流和 [Token](token.md) 限流。

自 2026 年 3 月 25 日起，华北2（北京）地域所有新创建的 API Key 均归属主账号，并支持设置 IP 访问白名单。

### 失效场景

- 将 RAM 账号移出业务空间会使其 API Key 失效（重新加入后恢复）。
- 在 RAM 控制台删除账号或角色则会使 API Key 永久失效，不可恢复。
- 各地域的 API Key 不互通，跨地域调用将失败。

## 环境变量配置

建议将 API Key 配置到环境变量 `DASHSCOPE_API_KEY`，避免在代码中硬编码：

- **Linux**：在 `~/.bashrc` 中追加 `export DASHSCOPE_API_KEY="your-key"`，然后执行 `source ~/.bashrc`。
- **macOS**：在 `~/.zshrc` 中追加 `export DASHSCOPE_API_KEY="your-key"`，然后执行 `source ~/.zshrc`。
- **Windows**：通过系统属性设置系统变量，或在 CMD 中使用 `setx`、PowerShell 中使用 `[Environment]::SetEnvironmentVariable` 设置。

> **注意**：设置环境变量后，已打开的 IDE 或终端不会自动加载新变量，需要重启。使用 `sudo` 运行脚本时默认不继承用户环境变量，需加 `-E` 参数。

## 临时 API Key

在浏览器、移动 App 等不可信环境中，应通过后端服务生成临时 API Key，避免永久 API Key 泄露。

**生成方式**：

```
POST https://dashscope.aliyuncs.com/api/v1/tokens?expire_in_seconds=<TTL>
```

| 参数 | 说明 |
|------|------|
| `expire_in_seconds` | 有效期，范围 [1, 1800] 秒，默认 60 秒 |

返回的 `token` 字段即为临时 API Key（以 `st-` 开头），`expires_at` 为 UNIX 过期时间戳。临时 API Key 继承生成它的永久 API Key 的全部权限，到期后自动失效，无法手动删除或提前撤销。

## 在不同场景中的使用

### 模型 API 调用

通过 [DashScope SDK](dashscope-sdk.md) 或 OpenAI 兼容 SDK 调用模型时，API Key 作为 Bearer Token 传入请求头，或通过 SDK 客户端的 `api_key` 参数指定。

### 应用调用

调用百炼智能体或工作流应用时，需同时提供 API Key 和 APP ID。若应用位于子业务空间，还需提供 Workspace ID。

### 框架集成

- **LlamaIndex**：按百炼通用约定配置环境变量 `DASHSCOPE_API_KEY`。
- **Spring AI Alibaba**：应用集成推荐 `DASHSCOPE_API_KEY`，知识库检索推荐 `AI_DASHSCOPE_API_KEY`。

### Token Plan / Coding Plan

订阅制套餐使用专属 API Key（`sk-sp-xxx`），由管理员在成员管理页面创建成员并分配席位后自动生成，需搭配专属 Base URL 使用。

## 安全最佳实践

1. **永远不要在前端代码中硬编码 API Key**，使用环境变量或密钥管理服务。
2. 对外暴露的场景（浏览器、移动端）使用临时 API Key，有效期设置为满足业务需求的最短时长。
3. 利用子业务空间和 IP 白名单实现最小权限原则。
4. 定期检查并清理不再使用的 API Key。
5. 按环境（dev/test/prod）划分业务空间，实现权限与成本隔离。

## 关联主题页

- [preparations](../api/preparations.md)
- [more](../api/more.md)
- [application call](../api/application-call.md)
- [security and compliance](../guides/security-and-compliance.md)
- [frameworks](../api/frameworks.md)
- [token plan guide](../guides/token-plan-guide.md)
- [more about models](../api/more-about-models.md)


