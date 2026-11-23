# 模型部署

阿里云百炼 CLI 按文本、音频、图像模态创建和管理模型部署及吞吐预留容量的命令速查。

在终端管理模型部署全生命周期：按文本、音频、图像选择创建命令，管理部署、限流、扩缩容和吞吐预留容量。

**重要**任意命令追加 `--help` 可查看完整参数说明，例如 `bl deploy list --help`。本文命令明细以 bl 2.5.1 为基准核实。

## 按模态选择命令

模态

创建命令

说明

文本

`bl deploy text create`

文本模型部署，支持 lora、ptu、mu 计费方案

音频

`bl deploy audio create`

音频（TTS）模型部署

图像

`bl deploy image create`

图像生成模型部署

## 文本部署

### bl deploy text create

创建文本模型部署。需要 API Key 鉴权。

**语法**

```
bl deploy text create
```

参数

类型

必填

说明

`--model-name <model_name>`

string

是

要部署的模型：微调输出模型名称或模型目录中的模型

`--display-name <display_name>`

string

否

控制台显示名称（PTU 可选；其他方案必填）

`--plan <plan>`

string

否

计费方案：lora（默认，按 Token 计费）| ptu（吞吐预留）| mu

`--deploy-spec <id>`

string

否

部署规格（仅 plan=mu 使用；省略时自动选择）

`--capacity <n>`

number

否

资源单元数（仅 plan=mu；API 必填；默认为模板的单元数）

`--billing-method <m>`

string

否

计费方式（仅 plan=mu；默认且仅支持 "POST\_PAY"）

`--input-tpm <kTPM>`

number

否

输入绝对容量，单位 kTPM（1 kTPM = 1000 Tokens/分钟）

`--output-tpm <kTPM>`

number

否

输出绝对容量，单位 kTPM

`--thinking-output-tpm <n>`

number

否

旧版思考输出容量参数；PTU 不支持此参数

`--charge-type <type>`

string

否

PTU 付费方式（plan=ptu 必填）：pre\_paid 或 post\_paid

`--service-tier <tier>`

string

否

PTU 性能档位：ptu\_fast（默认高速）或 ptu\_default（标速，仅预付费）

`--suffix <suffix>`

string

否

可选 PTU ModelCode 后缀；省略时由服务端生成

`--duration <days>`

number

否

预付费购买或续订天数，正整数

`--auto-renewal <true|false>`

boolean

否

显式开启或关闭预付费自动续费

`--auto-renewal-duration <days>`

number

否

自动续费天数，开启自动续费时必填

`--auto-renewal-cycle <cycle>`

string

否

可选续费周期单位，按服务支持的值传入，如 Day

`--wait`

switch

否

等待返回的容量操作完成并刷新容量

`--interval <seconds>`

number

否

等待初始轮询间隔（1–3600，默认：2 秒）

`--poll-timeout <seconds>`

number

否

提交后的等待总时限（默认：600 秒）

`--yes`

switch

否

确认执行此高风险操作

**警告**创建部署会购买或开通资源，可能产生费用。

**示例**：创建名称为 my-qwen-sft 的文本模型部署

```
bl deploy text create --model-name my-qwen-sft --display-name my-sft-test
```

-   文本和图片部署默认使用 `lora`（按 Token 计费），音频（CosyVoice TTS）默认使用 `mu`（按模型单元计费）。可通过 --plan 覆盖。
-   plan=ptu 时，--charge-type、--input-tpm 和 --output-tpm 必填。容量单位为 kTPM（1 kTPM = 1000 Token/分钟），不支持单独的思考输出容量。预付费须提供 --duration 和显式 --auto-renewal true|false。
-   plan=mu 时，`capacity`、`billing_method` 和 `deploy_spec` 必填。billing\_method 默认且仅支持 POST\_PAY；省略 deploy\_spec 和 capacity 时，会从 GET /deployments/models 自动选择。
-   使用 `deploy models --source base` 查看可用模板。
-   PTU 创建即使指定 --quiet 也保留原始 JSON 和 operation\_id。--wait 仅查询返回的操作；待生效容量不等于已生效容量。调用模型前请确认实际状态。
-   \--model-name 标识源模型；返回的 deployed\_model 为调用标识（ModelCode），用于推理（`text chat --model <deployed_model>`）和部署生命周期命令。
-   首次创建 ModelCode 不支持 --request-id，也不承诺幂等。超时不代表失败：再次尝试前先确认部署是否已创建。本命令不会自动重新提交创建请求。
-   使用 --dry-run 离线预览；仅在确认费用后传入 --yes 执行。

## 音频部署

### bl deploy audio create

创建音频（TTS）模型部署。需要 API Key 鉴权。

**语法**

```
bl deploy audio create
```

参数

类型

必填

说明

`--model-name <model_name>`

string

是

要部署的模型：微调输出模型名称或模型目录中的模型

`--display-name <display_name>`

string

否

控制台显示名称（PTU 可选；其他方案必填）

`--plan <plan>`

string

否

计费方案：lora（默认，按 Token 计费）| ptu（吞吐预留）| mu

`--deploy-spec <id>`

string

否

部署规格（仅 plan=mu 使用；省略时自动选择）

`--capacity <n>`

number

否

资源单元数（仅 plan=mu；API 必填；默认为模板的单元数）

`--billing-method <m>`

string

否

计费方式（仅 plan=mu；默认且仅支持 "POST\_PAY"）

`--input-tpm <kTPM>`

number

否

输入绝对容量，单位 kTPM（1 kTPM = 1000 Tokens/分钟）

`--output-tpm <kTPM>`

number

否

输出绝对容量，单位 kTPM

`--thinking-output-tpm <n>`

number

否

旧版思考输出容量参数；PTU 不支持此参数

`--charge-type <type>`

string

否

PTU 付费方式（plan=ptu 必填）：pre\_paid 或 post\_paid

`--service-tier <tier>`

string

否

PTU 性能档位：ptu\_fast（默认高速）或 ptu\_default（标速，仅预付费）

`--suffix <suffix>`

string

否

可选 PTU ModelCode 后缀；省略时由服务端生成

`--duration <days>`

number

否

预付费购买或续订天数，正整数

`--auto-renewal <true|false>`

boolean

否

显式开启或关闭预付费自动续费

`--auto-renewal-duration <days>`

number

否

自动续费天数，开启自动续费时必填

`--auto-renewal-cycle <cycle>`

string

否

可选续费周期单位，按服务支持的值传入，如 Day

`--wait`

switch

否

等待返回的容量操作完成并刷新容量

`--interval <seconds>`

number

否

等待初始轮询间隔（1–3600，默认：2 秒）

`--poll-timeout <seconds>`

number

否

提交后的等待总时限（默认：600 秒）

`--yes`

switch

否

确认执行此高风险操作

**警告**创建部署会购买或开通资源，可能产生费用。

**示例**：创建名称为 my-cosyvoice-ft 的音频模型部署

```
bl deploy audio create --model-name my-cosyvoice-ft --display-name my-tts
```

-   文本和图片部署默认使用 `lora`（按 Token 计费），音频（CosyVoice TTS）默认使用 `mu`（按模型单元计费）。可通过 --plan 覆盖。
-   plan=ptu 时，--charge-type、--input-tpm 和 --output-tpm 必填。容量单位为 kTPM（1 kTPM = 1000 Token/分钟），不支持单独的思考输出容量。预付费须提供 --duration 和显式 --auto-renewal true|false。
-   plan=mu 时，`capacity`、`billing_method` 和 `deploy_spec` 必填。billing\_method 默认且仅支持 POST\_PAY；省略 deploy\_spec 和 capacity 时，会从 GET /deployments/models 自动选择。
-   使用 `deploy models --source base` 查看可用模板。
-   PTU 创建即使指定 --quiet 也保留原始 JSON 和 operation\_id。--wait 仅查询返回的操作；待生效容量不等于已生效容量。调用模型前请确认实际状态。
-   \--model-name 标识源模型；返回的 deployed\_model 为调用标识（ModelCode），用于推理（`text chat --model <deployed_model>`）和部署生命周期命令。
-   首次创建 ModelCode 不支持 --request-id，也不承诺幂等。超时不代表失败：再次尝试前先确认部署是否已创建。本命令不会自动重新提交创建请求。
-   使用 --dry-run 离线预览；仅在确认费用后传入 --yes 执行。

## 图像部署

### bl deploy image create

创建图片生成模型部署。需要 API Key 鉴权。

**语法**

```
bl deploy image create
```

参数

类型

必填

说明

`--model-name <model_name>`

string

是

要部署的模型：微调输出模型名称或模型目录中的模型

`--display-name <display_name>`

string

否

控制台显示名称（PTU 可选；其他方案必填）

`--plan <plan>`

string

否

计费方案：lora（默认，按 Token 计费）| ptu（吞吐预留）| mu

`--deploy-spec <id>`

string

否

部署规格（仅 plan=mu 使用；省略时自动选择）

`--capacity <n>`

number

否

资源单元数（仅 plan=mu；API 必填；默认为模板的单元数）

`--billing-method <m>`

string

否

计费方式（仅 plan=mu；默认且仅支持 "POST\_PAY"）

`--input-tpm <kTPM>`

number

否

输入绝对容量，单位 kTPM（1 kTPM = 1000 Tokens/分钟）

`--output-tpm <kTPM>`

number

否

输出绝对容量，单位 kTPM

`--thinking-output-tpm <n>`

number

否

旧版思考输出容量参数；PTU 不支持此参数

`--charge-type <type>`

string

否

PTU 付费方式（plan=ptu 必填）：pre\_paid 或 post\_paid

`--service-tier <tier>`

string

否

PTU 性能档位：ptu\_fast（默认高速）或 ptu\_default（标速，仅预付费）

`--suffix <suffix>`

string

否

可选 PTU ModelCode 后缀；省略时由服务端生成

`--duration <days>`

number

否

预付费购买或续订天数，正整数

`--auto-renewal <true|false>`

boolean

否

显式开启或关闭预付费自动续费

`--auto-renewal-duration <days>`

number

否

自动续费天数，开启自动续费时必填

`--auto-renewal-cycle <cycle>`

string

否

可选续费周期单位，按服务支持的值传入，如 Day

`--wait`

switch

否

等待返回的容量操作完成并刷新容量

`--interval <seconds>`

number

否

等待初始轮询间隔（1–3600，默认：2 秒）

`--poll-timeout <seconds>`

number

否

提交后的等待总时限（默认：600 秒）

`--yes`

switch

否

确认执行此高风险操作

**警告**创建部署会购买或开通资源，可能产生费用。

**示例**：创建名称为 my-wan-ft 的图片生成模型部署

```
bl deploy image create --model-name my-wan-ft --display-name my-wan
```

-   文本和图片部署默认使用 `lora`（按 Token 计费），音频（CosyVoice TTS）默认使用 `mu`（按模型单元计费）。可通过 --plan 覆盖。
-   plan=ptu 时，--charge-type、--input-tpm 和 --output-tpm 必填。容量单位为 kTPM（1 kTPM = 1000 Token/分钟），不支持单独的思考输出容量。预付费须提供 --duration 和显式 --auto-renewal true|false。
-   plan=mu 时，`capacity`、`billing_method` 和 `deploy_spec` 必填。billing\_method 默认且仅支持 POST\_PAY；省略 deploy\_spec 和 capacity 时，会从 GET /deployments/models 自动选择。
-   使用 `deploy models --source base` 查看可用模板。
-   PTU 创建即使指定 --quiet 也保留原始 JSON 和 operation\_id。--wait 仅查询返回的操作；待生效容量不等于已生效容量。调用模型前请确认实际状态。
-   \--model-name 标识源模型；返回的 deployed\_model 为调用标识（ModelCode），用于推理（`text chat --model <deployed_model>`）和部署生命周期命令。
-   首次创建 ModelCode 不支持 --request-id，也不承诺幂等。超时不代表失败：再次尝试前先确认部署是否已创建。本命令不会自动重新提交创建请求。
-   使用 --dry-run 离线预览；仅在确认费用后传入 --yes 执行。

## 部署管理

### bl deploy list

列出模型部署及吞吐预留。需要 API Key 鉴权。

**语法**

```
bl deploy list [--page <n>] [--page-size <n>] [--plan <plan>] [--status <status>]
```

参数

类型

必填

说明

`--page <n>`

number

否

页码（默认：1）

`--page-size <n>`

number

否

每页结果数（默认：10，最多：100）

`--plan <plan>`

string

否

服务端方案筛选；吞吐预留使用 ptu

`--status <status>`

string

否

仅在已获取的当前页本地筛选 ModelCode 状态；total 仍为筛选前总数

**示例**：列出 PTU 方案的模型部署及吞吐预留

```
bl deploy list --plan ptu
```

-   部署列表 API 支持 page\_no/page\_size/plan，不支持 status。--status 仅筛选所请求的当前页，不代表全账号筛选；当前页为空不代表后续页没有匹配项。total 是本地筛选前的服务端总数，local\_filter 给出当前页匹配数量。PTU 容量单位为 kTPM。

### bl deploy get

获取单个模型部署的详情。需要 API Key 鉴权。

**语法**

```
bl deploy get --deployed-model <id>
```

参数

类型

必填

说明

`--deployed-model <code>`

string

是

部署调用标识（ModelCode）

**示例**：获取部署标识为 qwen-plus-2025-12-01-b6d61c71 的模型详情

```
bl deploy get --deployed-model qwen-plus-2025-12-01-b6d61c71
```

-   保留部署字段，包括 ptu\_capacity（汇总生效容量，kTPM）、ptu\_service\_tier、overflow\_strategy 及 pre\_paid\_info。混合付费或多实例时，通过 capacity list/get 查询各实例状态、到期时间和容量；ModelCode 状态不等于实例状态。

### bl deploy update

更新部署的限流配置（rpm\_limit / tpm\_limit）。需要 API Key 鉴权。

**语法**

```
bl deploy update --deployed-model <id> [--rpm-limit <n>] [--tpm-limit <n>]
```

参数

类型

必填

说明

`--deployed-model <id>`

string

是

已部署模型标识

`--rpm-limit <n>`

number

否

每分钟请求数

`--tpm-limit <n>`

number

否

每分钟 Token 数

**示例**：更新 dep-... 部署的每分钟请求数限流配置

```
bl deploy update --deployed-model dep-... --rpm-limit 1000
```

-   \--rpm-limit / --tpm-limit 至少需要提供一个。

### bl deploy scale

调整部署容量。需要 API Key 鉴权。

**语法**

```
bl deploy scale --deployed-model <id> (--capacity <n> | --input-tpm <n> --output-tpm <n>) [--instance-id <id>] [flags]
```

参数

类型

必填

说明

`--deployed-model <id>`

string

是

已部署模型标识

`--capacity <n>`

number

否

MU 目标容量：非负整数，单位为方案单元；须满足 base\_capacity 约束

`--input-tpm <kTPM>`

number

否

输入绝对容量，单位 kTPM（1 kTPM = 1000 Tokens/分钟）

`--output-tpm <kTPM>`

number

否

输出绝对容量，单位 kTPM

`--instance-id <id>`

string

否

PTU 容量实例 ID；存在多个未释放实例时必填

`--duration <days>`

number

否

预付费购买或续订天数，正整数

`--auto-renewal <true|false>`

boolean

否

显式开启或关闭预付费自动续费

`--auto-renewal-duration <days>`

number

否

自动续费天数，开启自动续费时必填

`--auto-renewal-cycle <cycle>`

string

否

可选续费周期单位，按服务支持的值传入，如 Day

`--request-id <uuid>`

string

否

请求标识，省略时生成；仅重试同一容量操作时保持标识和参数一致

`--wait`

switch

否

等待返回的容量操作完成并刷新容量

`--interval <seconds>`

number

否

等待初始轮询间隔（1–3600，默认：2 秒）

`--poll-timeout <seconds>`

number

否

提交后的等待总时限（默认：600 秒）

`--order-type <UPGRADE|DOWNGRADE>`

string

否

可选变配方向，省略时由服务端判定

`--yes`

switch

否

确认执行此高风险操作

**警告**扩缩容会变更购买的容量，可能产生费用或降低服务容量。

**示例**：预览调整 dep-... 部署容量至 8 的操作

```
bl deploy scale --deployed-model dep-... --capacity 8 --dry-run
```

-   PTU 输入/输出值为选中实例的绝对目标容量，单位 kTPM（1 kTPM = 1000 Token/分钟），不是增量或部署总容量。允许同时为零，但不等于释放实例。PTU 参数不能与 --capacity 混用。
-   省略 --instance-id 时，执行前必须确认恰好一个未释放实例并复查 can\_scale。dry-run 不解析实例或验证其付费方式；仅在确认费用及目标后传入 --yes 执行。

### bl deploy delete

删除模型部署（PTU 须为 STOPPED 且已释放全部容量）。需要 API Key 鉴权。

**语法**

```
bl deploy delete --deployed-model <id> [--skip-precheck]
```

参数

类型

必填

说明

`--deployed-model <id>`

string

是

已部署模型标识

`--skip-precheck`

switch

否

仅跳过本地检查；服务端仍验证删除前提条件

`--yes`

switch

否

确认执行此高风险操作

**警告**该操作会永久删除指定的模型部署，且无法撤销。

**示例**：预览删除 dep-... 部署的操作

```
bl deploy delete --deployed-model dep-... --dry-run
```

-   PTU 删除要求状态为 STOPPED、全部容量实例已释放，且不存在执行中或排队的容量操作。暂停或缩容到零不等于释放实例；预付费容量可能需要先退订。
-   本地检查部署、未释放实例及返回的 operation\_id。没有公开的排队操作列表接口，因此无法在本地确认所有操作均已完成，最终以服务端裁决为准。--skip-precheck 仅省略本地检查，不绕过服务端验证或资源释放要求。

### bl deploy pause

暂停运行中的模型部署（mu/ptu 方案将停止计费）。

**语法**

```
bl deploy pause --deployed-model <id> [--skip-precheck]
```

参数

类型

必填

说明

`--deployed-model <id>`

string

是

已部署模型标识

`--skip-precheck`

switch

否

跳过本地 RUNNING/PENDING 状态预检查

**示例**：暂停运行中的 dep-... 模型部署

```
bl deploy pause --deployed-model dep-...
```

-   暂停期间，mu/ptu 方案将停止计费。使用 `deploy resume` 恢复服务，或使用 `deploy delete` 删除部署。
-   发起暂停前会预检查部署状态是否为 RUNNING/PENDING；可传入 --skip-precheck 跳过检查。

### bl deploy resume

恢复已暂停的模型部署（使服务重新上线）。

**语法**

```
bl deploy resume --deployed-model <id> [--skip-precheck]
```

参数

类型

必填

说明

`--deployed-model <id>`

string

是

已部署模型标识

`--skip-precheck`

switch

否

跳过本地 STOPPED 状态预检查

**示例**：恢复已暂停的 dep-... 模型部署

```
bl deploy resume --deployed-model dep-...
```

-   发起恢复前会预检查部署状态是否为 STOPPED；可传入 --skip-precheck 跳过检查。
-   对于 mu/ptu 方案，服务重新上线后将恢复计费。

### bl deploy instances

列出 Console 独立部署服务。需要 Console 鉴权。

**语法**

```
bl deploy instances [--page <n>] [--page-size <n>] [--keyword <keyword>] [--model-service-id <id>]
```

参数

类型

必填

说明

`--page <n>`

number

否

页码（默认：1）

`--page-size <n>`

number

否

每页结果数（默认：10）

`--keyword <keyword>`

string

否

按名称关键词筛选（服务端过滤）

`--model-service-id <id>`

string

否

按模型服务 ID 筛选（服务端过滤）

`--workspace-id <id>`

string

否

工作空间 ID（环境变量：BAILIAN\_WORKSPACE\_ID）

**示例**：列出 Console 独立部署服务

```
bl deploy instances --keyword example --model-service-id example-service-id
```

-   列出 Console 独立部署服务，不是容量实例或副本。仅获取请求的当前页；records 为列表，items 为服务端返回的总数。保留全部业务响应字段，不推断可调用状态。

### bl deploy models

列出可部署的模型。需要 API Key 鉴权。

**语法**

```
bl deploy models [--page <n>] [--page-size <n>] [--catalog-version <v>] [--source <custom|public>]
```

参数

类型

必填

说明

`--page <n>`

number

否

页码（默认：1）

`--page-size <n>`

number

否

每页结果数（默认：100）

`--catalog-version <v>`

string

否

模型目录版本筛选（默认：v1.0；新目录模型必填）

`--source <s>`

string

否

模型来源筛选：custom（微调模型）| base（模型目录）| public

**示例**：筛选并列出可部署的模型

```
bl deploy models --source base
```

## 吞吐预留容量

容量实例的购买、扩缩、续费、释放与溢出策略设置属于高风险操作：未加 `--yes` 时阻断执行，可先用 `--dry-run` 预览。

### bl deploy capacity list

查询吞吐预留容量实例列表。需要 API Key 鉴权。

**语法**

```
bl deploy capacity list --deployed-model <code> [--page <n>] [--page-size <n>] [--include-deleted <true|false>] [--statuses <status,...>] [--charge-types <pre_paid,post_paid>]
```

参数

类型

必填

说明

`--deployed-model <code>`

string

是

部署调用标识（ModelCode）

`--page <n>`

number

否

页码（默认：1）

`--page-size <n>`

number

否

每页条数（1–100，默认：20）

`--include-deleted <true|false>`

boolean

否

包含已释放实例（默认：true）

`--statuses <status,...>`

string

否

实例状态，逗号分隔（非 ModelCode 状态）

`--charge-types <pre_paid,post_paid>`

string

否

付费类型：pre\_paid、post\_paid，逗号分隔

**示例**：查询指定模型的容量实例列表

```
bl deploy capacity list --deployed-model example-model-code
```

-   保留 API 响应结构及 records/items/page/itemsPerPage/pageCount 分页字段。容量单位为 kTPM，区分生效、配置和目标容量。仅 STOPPED 不代表已释放，需检查 deleted。

### bl deploy capacity get

查询吞吐预留容量实例详情。需要 API Key 鉴权。

**语法**

```
bl deploy capacity get --deployed-model <code> --instance-id <id>
```

参数

类型

必填

说明

`--deployed-model <code>`

string

是

部署调用标识（ModelCode）

`--instance-id <id>`

string

是

接口返回的容量实例 ID

**示例**：获取指定容量实例的详细信息

```
bl deploy capacity get --deployed-model example-model-code --instance-id example-capacity-instance
```

-   只读查询，已释放实例也可查询。保留 API 响应结构、容量字段、can\_scale/can\_renew/can\_delete 和 deleted。容量单位为 kTPM，实例必须属于指定 ModelCode。

### bl deploy capacity create

为已有 ModelCode 叠加购买容量实例。需要 API Key 鉴权。

**语法**

```
bl deploy capacity create --deployed-model <code> --billing-method <PRE_PAY|POST_PAY> --input-tpm <kTPM> --output-tpm <kTPM> [--duration <days>] [--auto-renewal <true|false>] [--wait]
```

参数

类型

必填

说明

`--deployed-model <code>`

string

是

部署调用标识（ModelCode）

`--input-tpm <kTPM>`

number

否

输入绝对容量，单位 kTPM（1 kTPM = 1000 Tokens/分钟）

`--output-tpm <kTPM>`

number

否

输出绝对容量，单位 kTPM

`--duration <days>`

number

否

预付费购买或续订天数，正整数

`--auto-renewal <true|false>`

boolean

否

显式开启或关闭预付费自动续费

`--auto-renewal-duration <days>`

number

否

自动续费天数，开启自动续费时必填

`--auto-renewal-cycle <cycle>`

string

否

可选续费周期单位，按服务支持的值传入，如 Day

`--request-id <uuid>`

string

否

请求标识，省略时生成；仅重试同一容量操作时保持标识和参数一致

`--wait`

switch

否

等待返回的容量操作完成并刷新容量

`--interval <seconds>`

number

否

等待初始轮询间隔（1–3600，默认：2 秒）

`--poll-timeout <seconds>`

number

否

提交后的等待总时限（默认：600 秒）

`--billing-method <PRE_PAY|POST_PAY>`

string

是

容量实例付费方式（区分大小写）

`--yes`

switch

否

确认执行此高风险操作

**警告**该操作将购买额外吞吐容量，可能开启持续续费。

**示例**：预览为模型叠加购买容量实例的配置

```
bl deploy capacity create --deployed-model example-code --billing-method POST_PAY --input-tpm 10000 --output-tpm 1000 --dry-run
```

-   沿用原 ModelCode、模型和性能档位。同一 ModelCode 只允许一个未释放的后付费实例；购买资格和实例数量限制由服务端校验。

### bl deploy capacity scale

调整单个预留实例的绝对容量。需要 API Key 鉴权。

**语法**

```
bl deploy capacity scale --deployed-model <code> --instance-id <id> --input-tpm <kTPM> --output-tpm <kTPM> [--order-type <UPGRADE|DOWNGRADE>] [--wait]
```

参数

类型

必填

说明

`--deployed-model <code>`

string

是

部署调用标识（ModelCode）

`--instance-id <id>`

string

是

接口返回的容量实例 ID

`--input-tpm <kTPM>`

number

否

输入绝对容量，单位 kTPM（1 kTPM = 1000 Tokens/分钟）

`--output-tpm <kTPM>`

number

否

输出绝对容量，单位 kTPM

`--duration <days>`

number

否

预付费购买或续订天数，正整数

`--auto-renewal <true|false>`

boolean

否

显式开启或关闭预付费自动续费

`--auto-renewal-duration <days>`

number

否

自动续费天数，开启自动续费时必填

`--auto-renewal-cycle <cycle>`

string

否

可选续费周期单位，按服务支持的值传入，如 Day

`--order-type <UPGRADE|DOWNGRADE>`

string

否

可选变配方向，省略时由服务端判定

`--request-id <uuid>`

string

否

请求标识，省略时生成；仅重试同一容量操作时保持标识和参数一致

`--wait`

switch

否

等待返回的容量操作完成并刷新容量

`--interval <seconds>`

number

否

等待初始轮询间隔（1–3600，默认：2 秒）

`--poll-timeout <seconds>`

number

否

提交后的等待总时限（默认：600 秒）

`--yes`

switch

否

确认执行此高风险操作

**警告**该操作会变更购买容量、可能产生费用，也可能将服务容量降至零。

**示例**：预览调整容量实例的输入输出绝对容量

```
bl deploy capacity scale --deployed-model example-code --instance-id example-instance --input-tpm 20000 --output-tpm 2000 --dry-run
```

-   写入前刷新 can\_scale。未指定预付费参数时不发送该对象，由服务端复用已保存的信息。后付费实例不能携带预付费配置。

### bl deploy capacity renew

续订预付费容量实例，可同时变更容量。需要 API Key 鉴权。

**语法**

```
bl deploy capacity renew --deployed-model <code> --instance-id <id> --duration <days> --auto-renewal <true|false> [--is-change <true|false>] [--input-tpm <kTPM>] [--output-tpm <kTPM>] [--wait]
```

参数

类型

必填

说明

`--deployed-model <code>`

string

是

部署调用标识（ModelCode）

`--instance-id <id>`

string

是

接口返回的容量实例 ID

`--input-tpm <kTPM>`

number

否

输入绝对容量，单位 kTPM（1 kTPM = 1000 Tokens/分钟）

`--output-tpm <kTPM>`

number

否

输出绝对容量，单位 kTPM

`--duration <days>`

number

否

预付费购买或续订天数，正整数

`--auto-renewal <true|false>`

boolean

否

显式开启或关闭预付费自动续费

`--auto-renewal-duration <days>`

number

否

自动续费天数，开启自动续费时必填

`--auto-renewal-cycle <cycle>`

string

否

可选续费周期单位，按服务支持的值传入，如 Day

`--request-id <uuid>`

string

否

请求标识，省略时生成；仅重试同一容量操作时保持标识和参数一致

`--wait`

switch

否

等待返回的容量操作完成并刷新容量

`--interval <seconds>`

number

否

等待初始轮询间隔（1–3600，默认：2 秒）

`--poll-timeout <seconds>`

number

否

提交后的等待总时限（默认：600 秒）

`--is-change <true|false>`

boolean

否

续订时同时变更容量（默认：false）

`--yes`

switch

否

确认执行此高风险操作

**警告**该操作将付费续订容量实例，可能开启自动持续续费。

**示例**：预览续订容量实例并变更容量的配置

```
bl deploy capacity renew --deployed-model example-code --instance-id example-instance --duration 30 --auto-renewal false --dry-run
```

-   仅支持预付费，写入前刷新 can\_renew。变更容量必须指定 --is-change true；相同配置容量可随 false 发送。本接口不接受 order\_type。

### bl deploy capacity delete

释放容量实例，保留所属 ModelCode。需要 API Key 鉴权。

**语法**

```
bl deploy capacity delete --deployed-model <code> --instance-id <id> [--reason <text>] [--wait]
```

参数

类型

必填

说明

`--deployed-model <code>`

string

是

部署调用标识（ModelCode）

`--instance-id <id>`

string

是

接口返回的容量实例 ID

`--request-id <uuid>`

string

否

请求标识，省略时生成；仅重试同一容量操作时保持标识和参数一致

`--wait`

switch

否

等待返回的容量操作完成并刷新容量

`--interval <seconds>`

number

否

等待初始轮询间隔（1–3600，默认：2 秒）

`--poll-timeout <seconds>`

number

否

提交后的等待总时限（默认：600 秒）

`--reason <text>`

string

否

可选释放原因，以查询参数发送

`--yes`

switch

否

确认执行此高风险操作

**警告**该操作将释放服务容量，可能中断请求，不能通过本命令撤销。这不是预付费退订或退款操作。

**示例**：预览释放容量实例的配置

```
bl deploy capacity delete --deployed-model example-code --instance-id example-instance --dry-run
```

-   已生效预付费实例须通过 `deploy capacity unsubscribe` 获取费用中心退订链接完成退订，即使 can\_delete=true 也不能直接删除。失败的预付费实例可能尚未关联订单，能否直接释放由服务端裁决。释放是异步操作，须确认 deleted=true，不能只看 STOPPED 或零容量。

### bl deploy capacity unsubscribe

生成预付费容量实例在阿里云费用中心的退订链接。无需鉴权。

**语法**

```
bl deploy capacity unsubscribe --instance-id <id>
```

参数

类型

必填

说明

`--instance-id <id>`

string

是

接口返回的容量实例 ID

**示例**：生成容量实例的退订链接

```
bl deploy capacity unsubscribe --instance-id example-instance
```

-   本命令不调用任何接口，也不会执行退订，只生成费用中心退订页面链接。请用下单账号打开链接，在费用中心完成退订流程。
-   仅预付费实例通过此方式退订；后付费实例请使用 `deploy capacity delete` 释放。此处为容量实例 ID（见 `deploy capacity list` / `get`），不是 ModelCode。退订可能中断服务且不可撤销，退款规则以费用中心为准。

### bl deploy overflow

设置吞吐预留 ModelCode 的溢出策略。需要 API Key 鉴权。

**语法**

```
bl deploy overflow --deployed-model <code> --strategy <enable|disable>
```

参数

类型

必填

说明

`--deployed-model <code>`

string

是

部署调用标识（ModelCode）

`--strategy <enable|disable>`

string

是

允许按量溢出或将请求限制在预留容量内

`--yes`

switch

否

确认执行此高风险操作

**警告**开启溢出后，预留容量外的流量将产生按量费用；关闭后，超额请求会被限流。

**示例**：预览设置模型溢出策略的配置

```
bl deploy overflow --deployed-model example-code --strategy enable --dry-run
```

-   配置作用于整个 ModelCode，而非单个容量实例。提交一次更新后 GET 回读确认策略。不自动重试更新；回读失败不代表配置未生效。

### bl deploy operation get

单次查询吞吐预留容量操作。需要 API Key 鉴权。

**语法**

```
bl deploy operation get --deployed-model <code> --operation-id <id>
```

参数

类型

必填

说明

`--deployed-model <code>`

string

是

部署调用标识（ModelCode）

`--operation-id <id>`

string

是

写请求返回的容量操作 ID

**示例**：查询指定容量操作的详情

```
bl deploy operation get --deployed-model example-model-code --operation-id 100001
```

-   保留 API 响应结构，包括 FAILED 状态及错误字段；GET 请求成功即返回退出码 0，不以操作状态判断。需要等待成功或失败时非零退出，请使用 operation wait。操作 ID 必须使用实际返回值，不要自行构造。

### bl deploy operation wait

等待容量操作完成并刷新已确认容量。需要 API Key 鉴权。

**语法**

```
bl deploy operation wait --deployed-model <code> --operation-id <id> [--interval <seconds>] [--poll-timeout <seconds>]
```

参数

类型

必填

说明

`--deployed-model <code>`

string

是

部署调用标识（ModelCode）

`--operation-id <id>`

string

是

写请求返回的容量操作 ID

`--interval <seconds>`

number

否

初始轮询间隔（1–3600 秒，默认：2）；逐次翻倍至 max(初始值, 30)

`--poll-timeout <seconds>`

number

否

总等待时限，包含请求及刷新（默认：600 秒）

**示例**：等待容量操作完成并刷新确认容量

```
bl deploy operation wait --deployed-model example-model-code --operation-id 100001
```

-   只读 GET 轮询：PROCESSING 继续等待，FAILED 透传服务端错误并退出 1，SUCCEEDED 刷新实例（返回 ID 时）及部署。输出保留操作响应结构，追加 instance/deployment 响应结构。缺失或未知状态报错，不推定成功。
-   \--timeout 限制单次 HTTP 请求，--poll-timeout 限制整个等待过程（超时退出 5）。Ctrl-C 只停止本地等待，不取消远端操作。不重试任何写请求；超时或中断后仍使用原操作 ID 查询。
