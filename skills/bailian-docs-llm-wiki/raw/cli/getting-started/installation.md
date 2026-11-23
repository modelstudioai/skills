# 安装与鉴权

安装阿里云百炼 CLI 与 Skills，完成鉴权配置并校验。

本页介绍如何安装阿里云百炼 CLI、安装配套 Skills，以及完成鉴权配置。

## 前置条件

-   能访问网络（npm registry 或 `bailian.aliyun.com`，取决于下方选择的安装方式）。
-   若选择 npm 安装：**Node.js ≥ 18.17.0**（执行 `node -v` 确认）与 **npm**（执行 `npm -v` 确认）。若本机没有 Node.js 或版本过低，可直接用下方的二进制安装脚本，无需装 Node。

## 安装 CLI

#### npm（已有 Node.js 环境）

```
npm install -g bailian-cli
```

即使本机已安装 pnpm / yarn，安装 `bailian-cli` 时仍需使用 npm；不要改用 pnpm / yarn 安装 CLI。

#### 二进制脚本（无需 Node.js）

macOS / Linux：

```
curl -fsSL https://bailian.aliyun.com/cli/install.sh | bash
```

Windows（PowerShell）：

```
irm https://bailian.aliyun.com/cli/install.ps1 | iex
```

安装成功后，PATH 中会新增两个命令：`bl`（短别名）与 `bailian`（全名）。校验：

```
bl --version
which bl   # Windows 可用 where bl
```

后续可随时执行 `bl update` 检查并更新 CLI 到最新版本。

**说明**若提示 `command not found`，检查全局 bin 目录是否在 PATH 中：npm 安装执行 `npm config get prefix`，其下的 `bin` 目录需加入 PATH；二进制安装按脚本输出提示的路径加入 PATH。

## 通过阿里云 CLI 调用

已安装阿里云 CLI 时，可以通过 `aliyun bl` 调用同一套命令：

```
aliyun bl --version
aliyun bl auth status
```

帮助、示例、操作指引和结构化命令会按 `aliyun bl` 入口显示。阿里云 CLI 宿主提供的 AccessKey 按阿里云环境变量处理，不需要在 `bl` 配置中重复保存。

## 安装 Skills

CLI 校验通过后，安装配套 Skills，让 Agent 具备完整的阿里云百炼能力调度。首选内置的一键安装命令：

```
bl skill init
```

该命令一次装齐 registry 中全部 `bailian-*` Skills（含共享协议 `bailian-protocol`），是官方推荐的安装方式。若 `bl skill init` 不可用，可改用 skills 工具（需要本机有 Git；最新 skills 要求 Node.js ≥ 22.20，Node.js 18 环境请固定 `skills@1.5.18`）：

```
npx skills@1.5.18 add modelstudioai/cli --skill '*' -g
```

只安装某个 Skill 时，把 `--skill '*'` 换成具体名称；`--list` 可查看仓库内的全部 Skill。

## 鉴权配置

安装后必须完成鉴权才能调用 API。根据环境选择下列任一方式。

#### 控制台登录（推荐）

适用于本机交互式安装，无需手动复制 API Key。命令会拉起浏览器完成阿里云控制台登录授权：

```
bl auth login --console
```

此方式同时打通 `app list`、`usage free` 等控制台能力，并自动配置 API Key 调用所需的鉴权信息。无法拉起浏览器时，可使用 `bl auth login --console --no-browser` 打印登录链接，或通过 `--token-stdin` 从标准输入导入访问令牌。

#### 普通 API Key

适用于无法拉起浏览器的环境（远程 SSH、CI 调试等）。先在 [阿里云百炼控制台 API Key 页](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/api-key) 获取 Key，再执行：

```
bl auth login --api-key <你的_API_Key>
```

登录命令会先测试 Key 可用性，通过后才保存。

#### Token Plan

使用 [Token Plan](https://bailian.console.aliyun.com/cn-beijing?tab=plan#/efm/subscription/overview) 订阅的 API Key：

```
bl auth login --config token-plan --api-key <你的_API_Key>
```

`token-plan` Profile 已内置默认 Base URL，无需额外配置接入地址。

#### AK/SK 临时令牌

适用于用阿里云 AccessKey 生成 CLI 访问令牌的场景（如与 Postman 等工具配合）。`--access-key-id` 与 `--access-key-secret` 为必填：

```
bl auth generate-access-token --access-key-id <AccessKey ID> --access-key-secret <AccessKey Secret>
```

生成的临时访问令牌可用于后续调用，避免长期暴露 AK/SK；使用 STS 临时凭证时可追加 `--security-token`。

#### 环境变量

不落盘到配置文件，在 shell 中设置 `DASHSCOPE_API_KEY` 即可（接入地址可通过 `BAILIAN_BASE_URL` 覆盖）。适合 CI / 非交互环境，通过密钥管理注入，避免在脚本中硬编码。

需要 OpenAPI 或控制台能力时，可以设置 `BAILIAN_ACCESS_KEY_ID`、`BAILIAN_ACCESS_KEY_SECRET` 和可选的 `BAILIAN_SECURITY_TOKEN`。AK/SK 按“命令参数 → 百炼环境变量 → 百炼配置 → 阿里云环境变量”整组解析，不跨来源拼接字段。控制台令牌缺失或过期时，CLI 会用可用的 AK/SK 自动获取。

普通 API Key 与 Token Plan 订阅的 API Key 差异如下：

对比项

普通 API Key

Token Plan API Key

计费归属

按量计费（含新用户免费额度）

扣减 Token Plan 订阅额度

权限范围

调用模型服务

调用 Token Plan 支持的模型

典型场景

未订阅套餐或按量调用

已订阅 Token Plan，优先消耗套餐额度

配置方式

`bl auth login --api-key <Key>`

`bl auth login --config token-plan --api-key <sk-sp-Key>`

## 校验配置

登录命令本身已完成可用性测试，通过后只需确认配置状态：

```
bl auth status --output json
```

无需再执行重复的模型调用测试。若登录失败，可根据输出中的 `hint` 或 `message` 排查（网络、Key 无效、`base_url` 等）。

**警告**汇报鉴权状态时只使用 masked 字段，切勿回显完整 API Key，也不要把真实 Key 写入仓库、日志或聊天记录的可公开部分。

## 退出登录

需要清除本地凭证、退出登录状态时，执行：

```
bl auth logout
```

## 常见问题

bl: command not found

全局 bin 目录不在 PATH 中。执行 `npm config get prefix`，将其下的 `bin` 目录加入 PATH 后重试。

安装报错 engines

Node.js 版本过低。升级到 ≥ 18.17.0 后重新安装。

401 / 鉴权失败

未登录或 API Key 无效。按 Key 类型重新执行对应的登录命令（普通 API Key 或 Token Plan）。

为什么 CLI 调用模型没有扣减 Token Plan？

当前生效的凭据是普通 API Key（`default` Profile）。Token Plan 需使用订阅的 API Key 并登录到 `token-plan` Profile；可用 `bl auth status --output json` 查看当前生效的凭据来源。

如何让 CLI 调用模型时使用 Token Plan？

使用订阅 API Key 登录 Token Plan Profile：`bl auth login --config token-plan --api-key <sk-sp-Key>`。已有该 Profile 时，用 `bl config use --name token-plan` 将其切换为当前生效配置。

只配置 Token Plan API Key 能否使用全部 CLI 功能？

不能。模型调用类命令可用；控制台类命令（如 `app list`、`usage free`、`workspace`）需要先完成控制台登录（`bl auth login --console`），Token Plan 席位管理等命令还需要阿里云 OpenAPI AK/SK 凭据。对比见[鉴权配置](#%E9%89%B4%E6%9D%83%E9%85%8D%E7%BD%AE)。

如何查看和切换当前生效的 API Key？

执行 `bl auth status --output json` 查看当前凭据（脱敏输出）；执行 `bl config list` 查看全部 Profile，`bl config use --name <profile>` 切换当前 Profile。

企业网络无法访问 npm

需配置镜像或代理。配置 registry 或代理后再安装。

本机只有 pnpm、没有 npm

改用二进制安装脚本（无需 Node.js/npm）：`curl -fsSL https://bailian.aliyun.com/cli/install.sh | bash`；也可以先安装或修复 npm 再用 `npm install -g bailian-cli`，但不要改用 pnpm / yarn 安装 CLI。
