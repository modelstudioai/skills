# 用量与配额

阿里云百炼 CLI 用量统计、限流管理、模型权限与 Token Plan 的命令速查。

在终端查询用量统计、管理限流与模型权限、以及 Token Plan 席位管理。

> **重要**
>
> 任意命令追加 `--help` 可查看完整参数说明，例如 `bl usage stats --help`。本文命令明细以 bl 2.8.0 为基准核实。

<a id="用量统计"></a>

## 用量统计

<a id="bl-usage-free"></a>

### bl usage free

查询模型免费额度（省略 --model 时查询全部模型）。

**语法**

<a id="code-block"></a>

```bash
bl usage free [--model <model>[,model2,...]] [flags]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--model <model>` | string | 否 | 要查询的模型名称；多个名称以逗号分隔，省略时查询全部模型 |
| `--expiring <days>` | string | 否 | 仅显示将在 N 天内到期的额度 |
| `--sort <field>` | string | 否 | 排序方式：remaining（剩余额度升序）、expires（到期时间升序） |
| `--all` | switch | 否 | 显示全部模型，而不只显示前几行 |

**示例**：查询指定模型的免费额度

<a id="code-block-2"></a>

```bash
bl usage free --model qwen3-max
```

<a id="bl-usage-stats"></a>

### bl usage stats

查询模型用量统计。

**语法**

<a id="code-block-3"></a>

```bash
bl usage stats [--model <model>] [--days <days>] [flags]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--model <model>` | string | 否 | 模型名称，多个名称以逗号分隔；省略时查看概览 |
| `--days <days>` | string | 否 | 天数（默认：7） |
| `--type <type>` | string | 否 | 模型类型：Text、Vision、Multimodal、Audio、Embedding |

**示例**：查询指定天数的模型用量统计

<a id="code-block-4"></a>

```bash
bl usage stats --days 30
```

<a id="bl-usage-summary"></a>

### bl usage summary

显示统一用量摘要：免费额度和近期用量概览。

**语法**

<a id="code-block-5"></a>

```bash
bl usage summary [--days <days>] [flags]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--days <days>` | string | 否 | 用量概览的天数（默认：7） |

**示例**：预览最近指定天数的用量摘要

<a id="code-block-6"></a>

```bash
bl usage summary --days 30
```

<a id="bl-usage-freetier"></a>

### bl usage freetier

启用或停用免费额度模型自动停止。默认启用，使用 --off 停用。

**语法**

<a id="code-block-7"></a>

```bash
bl usage freetier <--model <model>[,model2,...] | --all> [--off] [flags]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--model <model>` | string | 否 | 模型名称，多个名称以逗号分隔 |
| `--all` | switch | 否 | 应用于全部免费额度模型 |
| `--on` | switch | 否 | 启用自动停止（默认行为） |
| `--off` | switch | 否 | 停用自动停止 |

**示例**：预览指定模型的免费额度自动停止设置

<a id="code-block-8"></a>

```bash
bl usage freetier --model qwen3-max
```

<a id="bl-usage-token-plan"></a>

### bl usage token-plan

查看 Token Plan 配额使用情况，显示月度配额的使用比例和重置时间。

**语法**

<a id="code-block-9"></a>

```bash
bl usage token-plan [flags]
```

该命令仅支持全局参数。

**示例**：查看 Token Plan 配额使用情况并输出 JSON

<a id="code-block-10"></a>

```bash
bl usage token-plan --output json
```

-   展示接口返回的全部配额窗口。
-   JSON 输出包含 `hasQuotaData`，用于区分没有配额数据与正常结果。

<a id="bl-usage-coding-plan"></a>

### bl usage coding-plan

查看 Coding Plan 配额使用情况。

**语法**

<a id="code-block-11"></a>

```bash
bl usage coding-plan [flags]
```

该命令仅支持全局参数。

**示例**：查看 Coding Plan 配额使用情况并输出 JSON

<a id="code-block-12"></a>

```bash
bl usage coding-plan --output json
```

<a id="bl-token-plan-harness-quota"></a>

### bl token-plan harness-quota

查看 Token Plan harness 权益额度用量。

**语法**

<a id="code-block-13"></a>

```bash
bl token-plan harness-quota [flags]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--type <type>` | string | 否 | 按类型筛选 harness 列表：official\_tool、infrastructure |

**示例**：按类型筛选并查看 harness 权益额度用量

<a id="code-block-14"></a>

```bash
bl token-plan harness-quota --type official_tool
```

<a id="限流管理"></a>

## 限流管理

<a id="bl-quota-list"></a>

### bl quota list

查看模型限流配置（QPM/TPM，账号级和 Workspace 级）。需要 API Key 鉴权。

**语法**

<a id="code-block-15"></a>

```bash
bl quota list [--model <model>] [--name <name>] [--page <n>] [--page-size <n>]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--model <model>` | string | 否 | 模型名称，多个以逗号分隔（精确匹配） |
| `--name <name>` | string | 否 | 按模型名称模糊搜索 |
| `--page <n>` | number | 否 | 页码（默认：1） |
| `--page-size <n>` | number | 否 | 每页结果数（默认：20） |

**示例**：查看指定模型的限流配置

<a id="code-block-16"></a>

```bash
bl quota list --model qwen3-max
```

-   用量与限流压力检查位于 `quota check`（Console 鉴权）。

<a id="bl-quota-check"></a>

### bl quota check

根据限流额度检查当前用量。

**语法**

<a id="code-block-17"></a>

```bash
bl quota check [--model <model>] [flags]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--model <model>` | string | 否 | 模型名称，多个名称以逗号分隔 |
| `--period <minutes>` | string | 否 | 查询最近 N 分钟的用量（默认：2） |

**示例**：检查指定模型的当前用量是否超出限流额度

<a id="code-block-18"></a>

```bash
bl quota check --model qwen3.6-plus
```

<a id="bl-quota-update"></a>

### bl quota update

更新模型限流配置（QPM/TPM）。需要 API Key 鉴权。

**语法**

<a id="code-block-19"></a>

```bash
bl quota update --model <model> [--rpm <n>] [--tpm <n>]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--model <model>` | string | 是 | 模型名称 |
| `--rpm <n>` | number | 否 | 每分钟最大请求数（QPM） |
| `--tpm <n>` | number | 否 | 每分钟最大 Token 数（TPM） |

**示例**：确认执行指定模型的限流配置更新

<a id="code-block-20"></a>

```bash
bl quota update --model qwen-plus --rpm 60 --tpm 100000
```

-   未指定的字段将保留当前值（服务端 OVERLAY 合并）。清除全部自定义限流配置请改用 “quota delete” 命令。
-   若当前没有 QPM 限制，单独设置 TPM 会被服务端拒绝——请先设置 --rpm，或同时传入。

<a id="bl-quota-delete"></a>

### bl quota delete

清除模型的所有自定义限流配置（QPM/TPM）。需要 API Key 鉴权。

**语法**

<a id="code-block-21"></a>

```bash
bl quota delete --model <model>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--model <model>` | string | 是 | 模型名称 |
| `--yes` | switch | 否 | 确认执行此高风险操作 |

> **警告**
>
> 该操作会永久清除指定模型的所有自定义 QPM/TPM 限流配置，且无法撤销。

**示例**：确认执行指定模型的限流配置清除

<a id="code-block-22"></a>

```bash
bl quota delete --model qwen-plus
```

<a id="bl-quota-history"></a>

### bl quota history

查看额度变更历史。

**语法**

<a id="code-block-23"></a>

```bash
bl quota history [flags]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--page <n>` | string | 否 | 页码（默认：1） |
| `--page-size <n>` | string | 否 | 每页数量（默认：10） |
| `--model <model>` | string | 否 | 按模型名称筛选 |

**示例**：预览第 2 页的额度变更历史

<a id="code-block-24"></a>

```bash
bl quota history --page 2
```

<a id="模型权限管理"></a>

## 模型权限管理

<a id="bl-permission-grant"></a>

### bl permission grant

授予模型权限（推理 / 微调 / 部署）。需要 API Key 鉴权。

**语法**

<a id="code-block-25"></a>

```bash
bl permission grant --model <models> [--action <actions>] | --all
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--model <models>` | string | 否 | 模型 ID，多个以逗号分隔（最多 20 个） |
| `--action <actions>` | string | 否 | 权限操作，多个以逗号分隔：inference、finetune、deploy（默认：inference） |
| `--all` | switch | 否 | 一键授予 Workspace 中所有模型的推理权限（包括未来新增模型） |

**示例**：授予指定模型的权限

<a id="code-block-26"></a>

```bash
bl permission grant --model qwen-plus
```

-   授权将应用于 API Key 所属的业务 Workspace。
-   \--all 对应服务端一键授权开关（access\_all\_entities: OPEN），仅涵盖推理权限。
-   未指定的操作将保留当前授权状态（服务端三态增量更新）。

<a id="bl-permission-list"></a>

### bl permission list

列出 Workspace 中的模型权限（推理 / 微调 / 部署）。需要 API Key 鉴权。

**语法**

<a id="code-block-27"></a>

```bash
bl permission list [--scope <scope>] [--model <model>] [--name <name>] [--page <n>] [--page-size <n>]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--scope <scope>` | string | 否 | 授权范围：authorizable（默认，完整目录）、authorized（已授权） |
| `--model <model>` | string | 否 | 模型 ID（精确匹配） |
| `--name <name>` | string | 否 | 按模型名称或 ID 模糊搜索 |
| `--page <n>` | number | 否 | 页码（默认：1） |
| `--page-size <n>` | number | 否 | 每页结果数（默认：20） |

**示例**：列出指定模型的权限信息

<a id="code-block-28"></a>

```bash
bl permission list --model qwen-plus
```

-   默认范围为 `authorizable`（完整可授权目录）；使用 `--scope authorized` 仅查看已授权模型。
-   默认输出 JSON；传入 `--output text` 可查看表格。权限值为三态：true / false / null（从未设置）。
-   这些值原样反映 API Key 所绑定 Workspace 的服务端授权记录。显示 false/null 的模型仍可能可以调用（访问权限可能来自其他渠道）；准确语义请参阅百炼模型授权文档。

<a id="bl-permission-revoke"></a>

### bl permission revoke

撤销模型权限（推理 / 微调 / 部署）。需要 API Key 鉴权。

**语法**

<a id="code-block-29"></a>

```bash
bl permission revoke --model <models> [--action <actions>] | --all [flags]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--model <models>` | string | 否 | 模型 ID，多个以逗号分隔（最多 20 个） |
| `--action <actions>` | string | 否 | 权限操作，多个以逗号分隔：inference、finetune、deploy（默认：inference） |
| `--all` | switch | 否 | 关闭一键授权并清除所有历史推理授权 |
| `--yes` | switch | 否 | 确认执行此高风险操作 |

> **警告**
>
> 该操作会撤销模型权限，可能导致推理、精调或部署任务中断；使用 --all 时会清除全部历史推理授权。

**示例**：确认执行撤销模型权限

<a id="code-block-30"></a>

```bash
bl permission revoke --model qwen-plus --yes
```

-   授权将应用于 API Key 所属的业务 Workspace。
-   所有撤权操作均需使用 --yes；可通过 --dry-run 免确认预览请求。
-   \--all 对应服务端一键授权开关（access\_all\_entities: CLOSE）：它会清除所有历史推理授权且无法撤销，因此必须同时传入 --yes。
-   未指定的操作将保留当前授权状态（服务端三态增量更新）。

<a id="token-plan"></a>

## Token Plan

<a id="bl-token-plan-list-seats"></a>

### bl token-plan list-seats

列出 Token Plan 订阅席位详情。

**语法**

<a id="code-block-31"></a>

```bash
bl token-plan list-seats [flags]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--page-no <n>` | number | 否 | 页码（默认：1） |
| `--page-size <n>` | number | 否 | 每页数量（默认：10） |
| `--caller-uac-account-id <id>` | string | 否 | 调用方 UAC 账号 ID |
| `--namespace-id <id>` | string | 否 | 产品 Namespace ID（Token Plan 默认：namespace-1） |
| `--status <status>` | array | 否 | 席位状态筛选（可重复）：CREATING、NORMAL、LIMIT、RELEASE、STOP、REFUNDED |
| `--status-list-str <json>` | string | 否 | JSON 字符串格式的 StatusList，例如 '\["NORMAL"\]' |
| `--seat-id <id>` | string | 否 | 按席位 ID 筛选 |
| `--seat-type <type>` | string | 否 | 席位档位：standard、pro 或 max |
| `--query-assigned <bool>` | string | 否 | 按分配状态筛选：true=已分配，false=未分配 |

**示例**：列出 Token Plan 席位详情

<a id="code-block-32"></a>

```bash
bl token-plan list-seats --page-size 20 --status NORMAL
```

<a id="bl-token-plan-add-member"></a>

### bl token-plan add-member

向 Token Plan 组织添加成员。

**语法**

<a id="code-block-33"></a>

```bash
bl token-plan add-member --account-name <name> --org-id <id> [flags]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--account-name <name>` | string | 是 | 成员显示名称 |
| `--org-id <id>` | string | 是 | 组织 ID |
| `--org-role-code <code>` | string | 否 | 组织角色：ORG\_ADMIN 或 ORG\_MEMBER（默认：ORG\_MEMBER） |
| `--spec-type <type>` | string | 否 | 创建时分配的席位档位：standard、pro 或 max |
| `--caller-uac-account-id <id>` | string | 否 | 调用方 UAC 账号 ID |
| `--namespace-id <id>` | string | 否 | 产品 Namespace ID（Token Plan 默认：namespace-1） |

**示例**：向组织添加成员

<a id="code-block-34"></a>

```bash
bl token-plan add-member --account-name dev_user --org-id org_123
```

<a id="bl-token-plan-assign-seats"></a>

### bl token-plan assign-seats

批量向成员分配 Token Plan 席位。

**语法**

<a id="code-block-35"></a>

```bash
bl token-plan assign-seats --workspace-id <id> --seat-type <type> --account-id <id> [flags]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--workspace-id <id>` | string | 否 | Workspace ID（环境变量：BAILIAN\_WORKSPACE\_ID，配置项：workspace\_id） |
| `--seat-type <type>` | string | 是 | 席位档位：standard、pro 或 max |
| `--account-id <id>` | array | 否 | 目标成员账号 ID（可重复） |
| `--caller-uac-account-id <id>` | string | 否 | 调用方 UAC 账号 ID |
| `--namespace-id <id>` | string | 否 | 产品 Namespace ID（Token Plan 默认：namespace-1） |
| `--locale <locale>` | string | 否 | 语言：zh-CN 或 en-US |

**示例**：批量分配席位给成员

<a id="code-block-36"></a>

```bash
bl token-plan assign-seats --workspace-id ws_456 --seat-type standard --account-id acc_123
```

<a id="bl-token-plan-create-key"></a>

### bl token-plan create-key

为席位创建 Token Plan API Key。

**语法**

<a id="code-block-37"></a>

```bash
bl token-plan create-key --account-id <id> --workspace-id <id> [flags]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--account-id <id>` | string | 是 | 目标成员账号 ID |
| `--workspace-id <id>` | string | 否 | Workspace ID（环境变量：BAILIAN\_WORKSPACE\_ID，配置项：workspace\_id） |
| `--description <text>` | string | 否 | API Key 描述 |
| `--caller-uac-account-id <id>` | string | 否 | 调用方 UAC 账号 ID |
| `--namespace-id <id>` | string | 否 | 产品 Namespace ID（Token Plan 默认：namespace-1） |

**示例**：为席位创建 API Key

<a id="code-block-38"></a>

```bash
bl token-plan create-key --account-id acc_123 --workspace-id ws_456
```
