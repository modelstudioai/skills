# 模型部署 API 参考

本文档以千问模型的部署为例进行说明，使用 API（HTTP）调用方式帮助您使用阿里云百炼提供的模型部署功能。

> **重要**
>
> 模型部署 API 的开放地域因部署方式而异——模型单元（MU）与 独占吞吐（DTU）支持华北2（北京）。

<a id="前提条件"></a>

<a id="654cb090c6wkd"></a>

## 前提条件

-   您已经阅读了[模型部署](../../../model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md)和[使用 API 进行模型部署](../../../model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-quick-start.md)的相关内容，掌握了模型部署 API 的使用方法，并熟悉了在阿里云百炼平台上进行模型部署的基本步骤。
-   已配置百炼的 API-KEY， 请参考[获取与配置 API Key](../../preparations/get-api-key.md)。
-   DTU（DTU 独占算力）部署使用同一组部署接口，请求中以 `plan="dtu"` 区分部署形式。DTU 部署的请求需使用部署所在业务空间、地域对应的 `maas.aliyuncs.com` 业务空间域名（例如 `ws-vxxx.cn-beijing.maas.aliyuncs.com`）和该业务空间的 API Key，而不是 `dashscope.aliyuncs.com`。
-   智能路由（mr）服务同样调用本页的部署接口（请求以 `plan="mr"` 区分，仅支持后付费），完整接口说明独立成篇，请参见[智能路由 API 参考](../model-routing-api-reference.md)。
-   请求域名因地域而异：北京地域使用 `dashscope.aliyuncs.com`，新加坡地域使用 `dashscope-intl.aliyuncs.com`；业务空间专属域名（`{WorkspaceId}.{region}.maas.aliyuncs.com`）各地域均可用。各地域完整域名信息请参见[各地域接入信息](../../../model-user-guide/get-started-with-models/regions.md#h2_cc92e61c)。
-   DTU 部署仅支持预付费（`charge_type="pre_paid"`），不支持后付费创建；续费与自动续费变更目前仅支持在控制台操作。DTU 接口不支持 `AssumedRoleUser` 角色身份。使用 DTU 前需在控制台开通 DTU 功能并申请资源额度，详见[独占吞吐（DTU）](../../../model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/dtu-model-deployment.md)。

<a id="获取可以部署的模型列表"></a>

<a id="dc35528058t0d"></a>

## 获取可以部署的模型列表

<a id="code-block"></a>

```bash
GET https://dashscope.aliyuncs.com/api/v1/deployments/models
```

<a id="请求示例"></a>

<a id="4d68f79558lqs"></a>

### 请求示例

通过下面的命令可以查询支持部署的模型，推荐使用`version=v1.0`获取包含部署方案和模板信息的完整响应。

<a id="code-block-2"></a>

```bash
curl "https://dashscope.aliyuncs.com/api/v1/deployments/models?page_no=1&page_size=100&version=v1.0&model_source=base" \
    --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    --header 'Content-Type: application/json'
```

查询用户微调模型：

<a id="code-block-3"></a>

```bash
curl "https://dashscope.aliyuncs.com/api/v1/deployments/models?page_no=1&page_size=100&version=v1.0&model_source=custom" \
    --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    --header 'Content-Type: application/json'
```

查询 DTU 部署方案（传 `plan=dtu` 时仅返回 DTU 预付费模板，无需 `version` 参数；DTU 需使用业务空间域名）：

<a id="code-block-4"></a>

```bash
curl "https://ws-vxxx.cn-beijing.maas.aliyuncs.com/api/v1/deployments/models?plan=dtu&model_source=base&page_no=1&page_size=100" \
    --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    --header 'Content-Type: application/json'
```

<a id="请求参数"></a>

<a id="f37ec75058pia"></a>

### 请求参数

| 参数 | 类型 | 传参方式 | 必选 | 说明 |
| --- | --- | --- | --- | --- |
| page\_no | Number | query | 否 | 页码，默认值为1。 |
| page\_size | Number | query | 否 | 页大小，默认为50，最大值为100，最小值为1。 |
| model\_source | String | query | 否 | 模型来源。`base`表示系统模型（默认），`custom`表示用户微调模型。 |
| version | String | query | 否 | API 版本，推荐使用`v1.0`。使用`v1.0`时，响应中将包含完整的部署方案和模板信息。 |
| plan | String | query | 否 | 查询 DTU 部署方案时传`dtu`，仅返回 DTU 预付费模板（返回结构见下文 DTU 模板字段说明）。省略时保持原有模型目录行为，不返回 DTU 方案。 |

<a id="响应示例-参数"></a>

<a id="4d68f79858ncx"></a>

### 响应示例&参数

<a id="accordion-点击此处查看"></a>

点击此处查看

命令执行完成后，获得以下结果：

<a id="code-block-5"></a>

```json
{
    "request_id": "f7da015c-ea90-4d96-af89-2f8d7604026a",
    "output": {
        "page_no": 1,
        "page_size": 100,
        "total": 5,
        "models": [
            {
                "model_name": "qwen3-8b",
                "plans": [
                    {
                        "plan": "mu",
                        "templates": [
                            {
                                "template_id": "MU1",
                                "template_name": "单机部署-标准推理型",
                                "template_type": "COUPLED",
                                "template_version": "v1",
                                "template_desc": "适用于标准推理场景",
                                "roles": {
                                    "unified": {
                                        "model_unit_spec": "MU1",
                                        "capacity_unit_per_instance": 4
                                    }
                                }
                            },
                            {
                                "template_id": "MU1-PD",
                                "template_name": "PD分离部署-标准推理型",
                                "template_type": "SEPERATED",
                                "template_version": "v1",
                                "template_desc": "适用于PD分离推理场景",
                                "roles": {
                                    "prefill": {
                                        "model_unit_spec": "MU1",
                                        "capacity_unit_per_instance": 4
                                    },
                                    "decode": {
                                        "model_unit_spec": "MU1",
                                        "capacity_unit_per_instance": 4
                                    }
                                }
                            }
                        ]
                    },
                    {
                        "plan": "lora"
                    }
                ]
            }
        ]
    }
}
```

<a id="488bb28058j01"></a>

#### 响应参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| models | Array | 可部署模型列表。 |
| models\[\].model\_name | String | 模型名称。 |
| models\[\].plans | Array | 该模型支持的部署方案列表。使用`version=v1.0`时返回。 |
| models\[\].plans\[\].plan | String | 部署方案类型：`mu`（模型单元）、`cu`（算力单元）、`dtu`（DTU 独占算力）、`ptu_v2`（预置吞吐量V2，等效取值 `ptu`）、`lora`（LoRA共享部署）。 |
| models\[\].plans\[\].templates | Array | 部署模板列表（`plan=mu`时返回）。 |
| page\_no | Number | 查询页码。 |
| page\_size | Number | 查询页大小。 |
| total | Long | 满足查询条件的所有模型个数。 |

<a id="na10h1"></a>

#### 模板字段说明（templates）

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| template\_id | String | 模板 ID，在创建模型部署任务时作为`template_id`参数传入。 |
| template\_name | String | 模板显示名称。 |
| template\_type | String | 模板类型：`COUPLED`（非 PD 分离，使用`capacity`参数）、`SEPERATED`（PD 分离，使用`prefill_capacity`和`decode_capacity`参数）。 |
| template\_version | String | 模板版本。 |
| template\_desc | String | 模板描述。 |
| roles | Object | 节点角色配置。COUPLED 模式包含`unified`节点，SEPERATED 模式包含`prefill`和`decode`节点。 |

<a id="na18h1"></a>

#### roles 节点字段说明

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| model\_unit\_spec | String | 模型单元规格。 |
| capacity\_unit\_per\_instance | Number | 单实例容量单元数，即 base\_capacity。创建部署时`capacity`必须是该值的整数倍。 |

<a id="na20h1"></a>

#### DTU 模板字段说明（plan=dtu 时返回）

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| charge\_type | String | 固定为`pre_paid`（预付费）。 |
| sku\_code | String | 创建部署时使用的商品 SKU。 |
| template\_code | String | 创建部署时使用的部署模板，需与`sku_code`为同一模板项。 |
| input\_tpm\_quota | Object | 输入 TPM 的可购买范围与步长，字段见下表。 |
| output\_tpm\_quota | Object | 输出 TPM 的可购买范围与步长，字段见下表。 |
| display\_meta | Object | 方案名称、描述、标签等展示信息，有值时返回。 |
| standard\_workload | Object | 模板提供的标准工况（TPM 单位与工况档位），有值时返回。 |

`input_tpm_quota` 与 `output_tpm_quota` 分别表示输入、输出 TPM 的购买规则，容量单位为 tokens/min，包含以下字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| init | Integer | 该维度的最低起购 TPM，购买容量不得小于此值。 |
| max | Integer | 当前可购买的 TPM 上限。**任一维度 max=0 表示当前没有可购买额度，请联系商务申请资源；0 不代表不限量。** |
| step | Integer | 该维度的购买步长，购买的 TPM 必须是该步长的整数倍（不是在 init 上累加的偏移量）。 |

创建或扩缩容 DTU 部署时，传入的 `dtu_capacity.input_tpm` 与 `dtu_capacity.output_tpm` 须同时满足：

-   输入、输出 TPM 分别位于各自的 \[init, max\] 范围内；
-   输入 TPM 是 `input_tpm_quota.step` 的整数倍，输出 TPM 是 `output_tpm_quota.step` 的整数倍；
-   **输入、输出的步长倍数必须相同**：`input_tpm / input_tpm_quota.step = output_tpm / output_tpm_quota.step = n`（n 为正整数），不能独立选择不同倍数。

例如，输入范围为 `init=10000, max=100000, step=10000`、输出范围为 `init=1000, max=10000, step=1000` 时：购买输入 30000、输出 3000（均为 3 倍，满足）；购买输入 30000、输出 2000（倍数 3 和 2，不满足）；购买输入 15000、输出 1500（非步长整数倍，不满足）。

<a id="创建模型部署任务"></a>

<a id="13f7a7d05829h"></a>

## 创建模型部署任务

<a id="code-block-6"></a>

```bash
POST https://dashscope.aliyuncs.com/api/v1/deployments
```

<a id="请求示例-2"></a>

<a id="13f81d0d58x09"></a>

### 请求示例

<a id="sec-tabs"></a>

<a id="独占吞吐-dtu"></a>

<a id="独占吞吐-dtu-h4"></a>

#### 独占吞吐（DTU）

预付费，按输入/输出 TPM 购买容量（需使用业务空间域名；`sku_code`、`template_code` 及容量范围通过获取可以部署的模型列表 `plan=dtu` 查询）。DTU 为模型单元（MU）的继任方案，新购独占部署优先选择 DTU：

<a id="code-block-7"></a>

```bash
curl "https://ws-vxxx.cn-beijing.maas.aliyuncs.com/api/v1/deployments" \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model_name": "your-supported-model",
    "display_name": "业务模型服务",
    "suffix": "production",
    "plan": "dtu",
    "sku_code": "your-prepaid-sku",
    "template_code": "your-template",
    "charge_type": "pre_paid",
    "pre_paid_info": {
        "pricing_cycle": "Month",
        "duration": 1,
        "auto_renewal": false
    },
    "dtu_capacity": {"input_tpm": 10000, "output_tpm": 10000}
}'
```

<a id="模型单元部署-coupled-模式"></a>

<a id="模型单元部署-coupled-模式-h4"></a>

#### 模型单元部署（COUPLED 模式）

使用 `template_id` 指定 MU1 规格，`capacity` 为资源单元数量：

<a id="code-block-8"></a>

```bash
curl "https://dashscope.aliyuncs.com/api/v1/deployments" \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model_name": "qwen3-8b",
    "plan": "mu",
    "template_id": "MU1",
    "capacity": 4
}'
```

<a id="模型单元部署-pd-分离模式"></a>

<a id="模型单元部署-pd-分离模式-h4"></a>

#### 模型单元部署（PD 分离模式）

使用 `MU1-PD` 模板，分别指定 `prefill_capacity` 和 `decode_capacity`：

<a id="code-block-9"></a>

```bash
curl "https://dashscope.aliyuncs.com/api/v1/deployments" \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model_name": "qwen3-8b",
    "plan": "mu",
    "template_id": "MU1-PD",
    "prefill_capacity": 4,
    "decode_capacity": 8
}'
```

<a id="lora-共享部署"></a>

<a id="lora-共享部署-h4"></a>

#### LoRA 共享部署

按 Token 用量计费：

<a id="code-block-10"></a>

```bash
curl "https://dashscope.aliyuncs.com/api/v1/deployments" \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model_name": "qwen3-8b-ft-202511132025-0260",
    "plan": "lora"
}'
```

<a id="请求参数-2"></a>

<a id="13f7a7d4582to"></a>

### 请求参数

| 参数 | 类型 | 传参方式 | 必选 | 说明 |
| --- | --- | --- | --- | --- |
| model\_name | String | body | 是 | 待部署的模型名称。 |
| plan | String | body | 是 | 部署方案：`dtu`（DTU 独占算力，仅预付费）、`mu`（模型单元）、`cu`（算力单元）、`lora`（LoRA共享部署）。 |
| template\_id | String | body | 条件必填 | 部署模板 ID，对应获取可以部署的模型列表接口返回的 `template_id`。设置 `plan` 为 `mu` 时必须填写。推荐使用此参数指定模型单元规格。 |
| deploy\_spec（旧） | String | body | 否 | 模型单元规格，已废弃。 |
| capacity | Number | body | 条件必填 | 资源单元数量。COUPLED 模式（非 PD 分离）必填，必须是 `capacity_unit_per_instance` 的整数倍。按 Token 用量计费（`plan` 为 `lora`）时该参数设置无效但必须填写。 |
| prefill\_capacity | Number | body | 条件必填 | Prefill 容量。PD 分离模式（`template_type` 为 `SEPERATED`）时必填。 |
| decode\_capacity | Number | body | 条件必填 | Decode 容量。PD 分离模式（`template_type` 为 `SEPERATED`）时必填。 |
| name | String | body | 否 | 服务显示名称。 |
| suffix | String | body | 否 | 模型部署后将生成新的模型名称，suffix 用于指定新模型名称的后缀，最大长度为8个字符且需全局唯一。每个模型在首次部署时可以不指定后缀，多次部署同一模型时必须设置。 |
| charge\_type | String | body | 否 | 付费方式：`post_paid`（后付费，默认）、`pre_paid`（预付费）。 |
| pre\_paid\_info | Object | body | 条件必填 | 预付费信息，`charge_type` 为 `pre_paid` 时必填。包含字段：`auto_renewal`（Boolean，是否自动续费）、`duration`（Number，购买时长/月）、`auto_renewal_duration`（Number，自动续费时长）。 |
| pre\_paid\_info.auto\_renewal | Boolean | body | 是 | 是否自动续费 |
| pre\_paid\_info.duration | Integer | body | 是 | 购买时长（月） |
| pre\_paid\_info.auto\_renewal\_duration | Integer | body | 条件必填 | 自动续费时长（autoRenewal=true时必填） |
| enable\_thinking | Boolean | body | 否 | 是否启用思考模式，部分模型支持。 |
| max\_context\_length | Number | body | 否 | 最大上下文长度，部分模型支持。 |
| quantization\_precision | String | body | 否 | 量化精度。 |
| qpm\_limit | Number | body | 否 | QPM 限流，每分钟请求数限制。仅 `plan` 为 `mu` 的部分模型支持。 |
| tpm\_limit | Number | body | 否 | TPM 限流，每分钟 Token 使用量限制。仅 `plan` 为 `mu` 的部分模型支持。 |
| display\_name | String | body | 条件必填 | 服务展示名称，最多 50 个字符。`plan` 为 `dtu` 时使用（其他方案使用 `name`）。 |
| sku\_code | String | body | 条件必填 | 当前模型可用的预付费 SKU，`plan` 为 `dtu` 时必填。 |
| template\_code | String | body | 条件必填 | 与模型和 SKU 匹配的部署模板，`plan` 为 `dtu` 时必填。 |
| dtu\_capacity | Object | body | 条件必填 | DTU 购买容量，`plan` 为 `dtu` 时必填，须同时提供 `input_tpm` 与 `output_tpm`，规则见获取可以部署的模型列表的 TPM 购买范围与步长。 |
| dtu\_capacity.input\_tpm | Integer | body | 是 | 购买的输入 TPM（tokens/min），非负整数，最大值为 2147483647。 |
| dtu\_capacity.output\_tpm | Integer | body | 是 | 购买的输出 TPM（tokens/min），非负整数，最大值为 2147483647。 |
| pre\_paid\_info.pricing\_cycle | String | body | 是 | 计费周期，DTU 固定传 `Month`（省略或传其他值将返回 InvalidParameter）。 |
| pre\_paid\_info.auto\_renewal\_cycle | String | body | 条件必填 | 自动续费周期，开启自动续费时必填，应符合商品规则。 |

> **说明**
>
> `plan` 为 `dtu` 时的补充说明：`suffix` 最多 24 个字符，生成的完整部署标识不超过 100 个字符；不支持 `name`、`random_suffix`、`deploy_spec`、MU/PTU 容量字段、模型路由、限流或发布参数，限流请在部署就绪后通过修改限流接口设置；创建成功仅表示请求已受理（预付费订单处理中），需轮询详情至 `RUNNING`；续费与自动续费变更请在控制台操作。

<a id="支持的模型"></a>

<a id="184f7297e8ekv"></a>

### 支持的模型

<a id="accordion-模型单元-部署模式下-限流-推理加速等功能的-支持情况"></a>

模型单元 部署模式下，限流、推理加速等功能的 支持情况 。

<a id="sec-tabs-2"></a>

<a id="文本生成"></a>

<a id="文本生成-h4"></a>

#### 文本生成

<a id="sec-tabs-3"></a>

<a id="千问"></a>

<a id="千问-h4"></a>

#### 千问

<table><thead><tr><th><p><strong>模型名称</strong></p></th><th><p><strong>模型代码</strong></p></th><th><p><strong>模型单元规格</strong></p></th><th><p><strong>小时单价（元）</strong></p><p><strong>最小计费：分钟</strong></p></th><th><p><strong>包月单价（元）</strong></p><p><strong>最小计费：天</strong></p></th></tr></thead><tbody><tr><td rowspan="4"><p>千问3.6-35B-A3B</p></td><td rowspan="4"><p>qwen3.6-35b-a3b</p></td><td><p>MU1 x 8</p></td><td><p>¥432</p></td><td><p>¥208,944</p></td></tr><tr><td><p>MU2 x 8</p></td><td><p>¥504</p></td><td><p>¥240,288</p></td></tr><tr><td><p>MU3 x 8</p></td><td><p>¥1,096</p></td><td><p>¥527,752</p></td></tr><tr><td><p>MU9 x 1</p></td><td><p>¥51</p></td><td><p>¥24,600</p></td></tr><tr><td><p>千问3.6-27B</p></td><td><p>qwen3.6-27b</p></td><td><p>MU9 x 1</p></td><td><p>¥51</p></td><td><p>¥24,600</p></td></tr><tr><td rowspan="2"><p>千问3.6-Flash-2026-04-16</p></td><td rowspan="2"><p>qwen3.6-flash-2026-04-16</p></td><td><p>MU1 x 2</p></td><td><p>¥108</p></td><td><p>¥52,236</p></td></tr><tr><td><p>MU3 x 8</p></td><td><p>¥1,096</p></td><td><p>¥527,752</p></td></tr><tr><td><p>千问3.6-Plus-2026-04-02</p></td><td><p>qwen3.6-plus-2026-04-02</p></td><td><p>MU1 x 8</p><p>MU1 x 16（PD分离模式）</p></td><td><p>¥432</p><p>PD分离模式：¥864</p></td><td><p>¥208,944</p><p>PD分离模式：¥417,888</p></td></tr><tr><td colspan="5"><p></p></td></tr><tr><td rowspan="2"><p>千问3.5-397B-A17B</p></td><td rowspan="2"><p>qwen3.5-397b-a17b</p></td><td><p>MU3 x 8</p><p>MU3 x 16（PD分离模式）</p></td><td><p>¥1,096</p><p>PD分离模式：¥2,192</p></td><td><p>¥527,752</p><p>PD分离模式：¥1,055,504</p></td></tr><tr><td><p>MU6 x 16</p></td><td><p>¥400</p></td><td><p>¥193,424</p></td></tr><tr><td rowspan="2"><p>千问3.5-122B-A10B</p></td><td rowspan="2"><p>qwen3.5-122b-a10b</p></td><td><p>MU1 x 4</p></td><td><p>¥216</p></td><td><p>¥104,472</p></td></tr><tr><td><p>MU6 x 16</p></td><td><p>¥400</p></td><td><p>¥193,424</p></td></tr><tr><td rowspan="4"><p>千问3.5-35B-A3B</p></td><td rowspan="4"><p>qwen3.5-35b-a3b</p></td><td><p>MU1 x 2</p></td><td><p>¥108</p></td><td><p>¥52,236</p></td></tr><tr><td><p>MU2 x 8</p></td><td><p>¥504</p></td><td><p>¥240,288</p></td></tr><tr><td><p>MU3 x 8</p></td><td><p>¥1,096</p></td><td><p>¥527,752</p></td></tr><tr><td><p>MU9 x 1</p></td><td><p>¥51</p></td><td><p>¥24,600</p></td></tr><tr><td rowspan="4"><p>千问3.5-27B</p></td><td rowspan="4"><p>qwen3.5-27b</p></td><td><p>MU2 x 8</p></td><td><p>¥504</p></td><td><p>¥240,288</p></td></tr><tr><td><p>MU3 x 8</p></td><td><p>¥1,096</p></td><td><p>¥527,752</p></td></tr><tr><td><p>MU8 x 1</p></td><td><p>¥47</p></td><td><p>¥22,400</p></td></tr><tr><td><p>MU9 x 1</p></td><td><p>¥51</p></td><td><p>¥24,600</p></td></tr><tr><td><p>千问3.5-9B</p></td><td><p>qwen3.5-9b</p></td><td><p>MU2 x 2</p></td><td><p>¥126</p></td><td><p>¥60,072</p></td></tr><tr><td><p>千问3.5-Flash-2026-02-23</p></td><td><p>qwen3.5-flash-2026-02-23</p></td><td><p>MU1 x 2</p></td><td><p>¥108</p></td><td><p>¥52,236</p></td></tr><tr><td rowspan="3"><p>千问3.5-Plus-2026-02-15</p></td><td rowspan="3"><p>qwen3.5-plus-2026-02-15</p></td><td><p>MU1 x 8</p><p>MU1 x 16（PD分离模式）</p></td><td><p>¥432</p><p>PD分离模式：¥864</p></td><td><p>¥208,944</p><p>PD分离模式：¥417,888</p></td></tr><tr><td><p>MU2 x 8</p></td><td><p>¥504</p></td><td><p>¥240,288</p></td></tr><tr><td><p>MU3 x 8</p><p>MU3 x 16（PD分离模式）</p></td><td><p>¥1,096</p><p>PD分离模式：¥2,192</p></td><td><p>¥527,752</p><p>PD分离模式：¥1,055,504</p></td></tr><tr><td colspan="5"><p></p></td></tr><tr><td rowspan="3"><p>千问3-235B-A22B-Instruct-2507</p></td><td rowspan="3"><p>qwen3-235b-a22b-instruct-2507</p></td><td><p>MU1 x 4</p></td><td><p>¥216</p></td><td><p>¥104,472</p></td></tr><tr><td><p>MU2 x 8</p></td><td><p>¥504</p></td><td><p>¥240,288</p></td></tr><tr><td><p>MU3 x 8</p></td><td><p>¥1,096</p></td><td><p>¥527,752</p></td></tr><tr><td><p>千问3-32B</p></td><td><p>qwen3-32b</p></td><td><p>MU6 x 16</p></td><td><p>¥400</p></td><td><p>¥193,424</p></td></tr><tr><td><p>千问3-30B-A3B-Thinking-2507</p></td><td><p>qwen3-30b-a3b-thinking-2507</p></td><td><p>MU1 x 2</p></td><td><p>¥108</p></td><td><p>¥52,236</p></td></tr><tr><td rowspan="2"><p>千问3-8B</p></td><td rowspan="2"><p>qwen3-8b</p></td><td><p>MU1 x 2</p></td><td><p>¥108</p></td><td><p>¥52,236</p></td></tr><tr><td><p>MU2 x 2</p></td><td><p>¥126</p></td><td><p>¥60,072</p></td></tr><tr><td rowspan="2"><p>千问3-4B</p></td><td rowspan="2"><p>qwen3-4b</p></td><td><p>MU1 x 2</p></td><td><p>¥108</p></td><td><p>¥52,236</p></td></tr><tr><td><p>MU5 x 1</p></td><td><p>¥21</p></td><td><p>¥10,139</p></td></tr><tr><td rowspan="2"><p>千问3-Embedding-0.6B</p></td><td rowspan="2"><p>qwen3-embedding-0.6b</p></td><td><p>MU5 x 1</p></td><td><p>¥21</p></td><td><p>¥10,139</p></td></tr><tr><td><p>MU6 x 1</p></td><td><p>¥25</p></td><td><p>¥12,089</p></td></tr><tr><td><p>千问3-MoE-Rerank-0.6B</p></td><td><p>qwen3-moe-rerank-0.6b</p></td><td><p>MU5 x 1</p></td><td><p>¥21</p></td><td><p>¥10,139</p></td></tr><tr><td rowspan="2"><p>千问3-Rerank-0.6B</p></td><td rowspan="2"><p>qwen3-rerank-0.6b</p></td><td><p>MU5 x 1</p></td><td><p>¥21</p></td><td><p>¥10,139</p></td></tr><tr><td><p>MU6 x 1</p></td><td><p>¥25</p></td><td><p>¥12,089</p></td></tr><tr><td rowspan="2"><p>千问3-Max-2025-09-23</p></td><td rowspan="2"><p>qwen3-max-2025-09-23</p></td><td><p>MU2 x 8</p></td><td><p>¥504</p></td><td><p>¥240,288</p></td></tr><tr><td><p>MU3 x 8</p></td><td><p>¥1,096</p></td><td><p>¥527,752</p></td></tr><tr><td><p>千问3-Rerank</p></td><td><p>qwen3-rerank</p></td><td><p>MU5 x 1</p></td><td><p>¥21</p></td><td><p>¥10,139</p></td></tr><tr><td colspan="5"><p></p></td></tr><tr><td><p>千问2.5-开源版-72B</p></td><td><p>qwen2.5-72b-instruct</p></td><td><p>MU1 x 8</p></td><td><p>¥432</p></td><td><p>¥208,944</p></td></tr><tr><td><p>千问2.5-开源版-14B</p></td><td><p>qwen2.5-14b-instruct</p></td><td><p>MU1 x 2</p></td><td><p>¥108</p></td><td><p>¥52,236</p></td></tr><tr><td rowspan="2"><p>千问2.5-开源版-7B</p></td><td rowspan="2"><p>qwen2.5-7b-instruct</p></td><td><p>MU1 x 2</p></td><td><p>¥108</p></td><td><p>¥52,236</p></td></tr><tr><td><p>MU5 x 1</p></td><td><p>¥21</p></td><td><p>¥10,139</p></td></tr><tr><td colspan="5"><p></p></td></tr><tr><td><p>千问-Plus-2025-07-28</p></td><td><p>qwen-plus-2025-07-28</p></td><td><p>MU1 x 4</p><p>MU1 x 16（PD分离模式）</p></td><td><p>¥216</p><p>PD分离模式：¥864</p></td><td><p>¥104,472</p><p>PD分离模式：¥417,888</p></td></tr><tr><td><p>千问-Plus-2025-12-01</p></td><td><p>qwen-plus-2025-12-01</p></td><td><p>MU1 x 4</p></td><td><p>¥216</p></td><td><p>¥104,472</p></td></tr><tr><td><p>Qwen-Plus-Character-2025-11-06</p></td><td><p>qwen-plus-character-2025-11-06</p></td><td><p>MU1 x 4</p></td><td><p>¥216</p></td><td><p>¥104,472</p></td></tr></tbody></table>

<a id="glm"></a>

<a id="glm-h4"></a>

#### GLM

<table><thead><tr><th><p><strong>模型名称</strong></p></th><th><p><strong>模型代码</strong></p></th><th><p><strong>模型单元规格</strong></p></th><th><p><strong>小时单价（元）</strong></p><p><strong>最小计费：分钟</strong></p></th><th><p><strong>包月单价（元）</strong></p><p><strong>最小计费：天</strong></p></th></tr></thead><tbody><tr><td rowspan="3"><p>GLM-5.1</p></td><td rowspan="3"><p>glm-5.1</p></td><td><p>MU2 x 8</p></td><td><p>¥504</p></td><td><p>¥240,288</p></td></tr><tr><td><p>MU3 x 16（PD分离模式）</p></td><td><p>PD分离模式：¥2,192</p></td><td><p>PD分离模式：¥1,055,504</p></td></tr><tr><td><p>MU6 x 16</p></td><td><p>¥400</p></td><td><p>¥193,424</p></td></tr><tr><td><p>GLM-5</p></td><td><p>glm-5</p></td><td><p>MU3 x 16（PD分离模式）</p></td><td><p>PD分离模式：¥2,192</p></td><td><p>PD分离模式：¥1,055,504</p></td></tr><tr><td><p>GLM-4.7</p></td><td><p>glm-4.7</p></td><td><p>MU6 x 32（PD分离模式）</p></td><td><p>PD分离模式：¥800</p></td><td><p>PD分离模式：¥386,848</p></td></tr></tbody></table>

<a id="deepseek"></a>

<a id="deepseek-h4"></a>

#### DeepSeek

<table><thead><tr><th><p><strong>模型名称</strong></p></th><th><p><strong>模型代码</strong></p></th><th><p><strong>模型单元规格</strong></p></th><th><p><strong>小时单价（元）</strong></p><p><strong>最小计费：分钟</strong></p></th><th><p><strong>包月单价（元）</strong></p><p><strong>最小计费：天</strong></p></th></tr></thead><tbody><tr><td rowspan="2"><p>DeepSeek-v4-Flash</p></td><td rowspan="2"><p>deepseek-v4-flash</p></td><td><p>MU1 x 8</p></td><td><p>¥432</p></td><td><p>¥208,944</p></td></tr><tr><td><p>MU3 x 8</p></td><td><p>¥1,096</p></td><td><p>¥527,752</p></td></tr><tr><td><p>DeepSeek-v3.2</p></td><td><p>deepseek-v3.2</p></td><td><p>MU2 x 16（PD分离模式）</p></td><td><p>PD分离模式：¥1,008</p></td><td><p>PD分离模式：¥480,576</p></td></tr></tbody></table>

<a id="更多模型"></a>

<a id="更多模型-h4"></a>

#### 更多模型

| 模型名称 | 模型代码 | 模型单元规格 | **小时单价（元）**<br><br>**最小计费：分钟** | **包月单价（元）**<br><br>**最小计费：天** |
| --- | --- | --- | --- | --- |
| Kimi-K2.5 | kimi-k2.5 | MU2 x 8 | ¥504 | ¥240,288 |

模型类型：

-   Instruct - 模型部署后以**非思考模式**进行推理。
-   Thinking - 模型部署后以思考模式进行推理。

模型部署类型：

-   PD 分离模式 - **降低首 Token 延迟、提高吞吐。** 该部署模式部署的模型在进行模型推理时，将首 Token 计算（Prefill）和后续 Token 计算（Decode）两个计算阶段，拆到不同的计算节点执行。

<a id="多模态"></a>

<a id="多模态-h4"></a>

#### 多模态

<a id="sec-tabs-4"></a>

<a id="千问vl"></a>

<a id="千问vl-h4"></a>

#### 千问VL

<table><thead><tr><th><p><strong>模型名称</strong></p></th><th><p><strong>模型代码</strong></p></th><th><p><strong>模型单元规格</strong></p></th><th><p><strong>小时单价（元）</strong></p><p><strong>最小计费：分钟</strong></p></th><th><p><strong>包月单价（元）</strong></p><p><strong>最小计费：天</strong></p></th></tr></thead><tbody><tr><td rowspan="3"><p>千问3-VL-235B-A22B-Thinking</p></td><td rowspan="3"><p>qwen3-vl-235b-a22b-thinking</p></td><td><p>MU1 x 8</p></td><td><p>¥432</p></td><td><p>¥208,944</p></td></tr><tr><td><p>MU2 x 8</p></td><td><p>¥504</p></td><td><p>¥240,288</p></td></tr><tr><td><p>MU3 x 8</p></td><td><p>¥1,096</p></td><td><p>¥527,752</p></td></tr><tr><td rowspan="2"><p>千问3-VL-32B-Instruct</p></td><td rowspan="2"><p>qwen3-vl-32b-instruct</p></td><td><p>MU2 x 8</p></td><td><p>¥504</p></td><td><p>¥240,288</p></td></tr><tr><td><p>MU3 x 8</p></td><td><p>¥1,096</p></td><td><p>¥527,752</p></td></tr><tr><td rowspan="2"><p>千问3-VL-8B-Instruct</p></td><td rowspan="2"><p>qwen3-vl-8b-instruct</p></td><td><p>MU1 x 2</p></td><td><p>¥108</p></td><td><p>¥52,236</p></td></tr><tr><td><p>MU5 x 1</p></td><td><p>¥21</p></td><td><p>¥10,139</p></td></tr><tr><td><p>千问3-VL-4B-Instruct</p></td><td><p>qwen3-vl-4b-instruct</p></td><td><p>MU1 x 2</p></td><td><p>¥108</p></td><td><p>¥52,236</p></td></tr><tr><td><p>千问3-VL-2B-Instruct</p></td><td><p>qwen3-vl-2b-instruct</p></td><td><p>MU5 x 1</p></td><td><p>¥21</p></td><td><p>¥10,139</p></td></tr><tr><td><p>千问3-VL-Embedding-2B</p></td><td><p>qwen3-vl-embedding-2b</p></td><td><p>MU5 x 1</p></td><td><p>¥21</p></td><td><p>¥10,139</p></td></tr><tr><td><p>千问3-VL-Flash-2025-10-15</p></td><td><p>qwen3-vl-flash-2025-10-15</p></td><td><p>MU1 x 4</p></td><td><p>¥216</p></td><td><p>¥104,472</p></td></tr><tr><td><p>千问3-VL-Plus-2025-09-23</p></td><td><p>qwen3-vl-plus-2025-09-23</p></td><td><p>MU1 x 4</p></td><td><p>¥216</p></td><td><p>¥104,472</p></td></tr><tr><td colspan="5"><p></p></td></tr><tr><td><p>千问VL-Max-2025-08-13</p></td><td><p>qwen-vl-max-2025-08-13</p></td><td><p>MU6 x 4</p></td><td><p>¥100</p></td><td><p>¥48,356</p></td></tr></tbody></table>

<a id="千问-omni"></a>

<a id="千问-omni-h4"></a>

#### 千问 Omni

| 模型名称 | 模型代码 | 模型单元规格 | **小时单价（元）**<br><br>**最小计费：分钟** | **包月单价（元）**<br><br>**最小计费：天** |
| --- | --- | --- | --- | --- |
| 千问3.5-Omni-Flash | qwen3.5-omni-flash | MU9 x 1 | ¥51 | ¥24,600 |

模型类型：

-   Instruct - 模型部署后以**非思考模式**进行推理。
-   Thinking - 模型部署后以思考模式进行推理。
-   Instruct/Thinking - 可在模型部署时**选择是否开启思考模式**。

<a id="语音合成"></a>

<a id="语音合成-h4"></a>

#### 语音合成

**CosyVoice**

| 模型名称 | 模型代码 | 模型单元规格 | 小时单价（元） | 包月单价（元） |
| --- | --- | --- | --- | --- |
| cosyvoice-v3-flash | cosyvoice-v3-flash | MU5 | ¥21 | ¥10,139 |

<a id="响应示例-参数-2"></a>

<a id="28762b1a7bbjn"></a>

### 响应示例&参数

<a id="accordion-点击此处查看-2"></a>

点击此处查看

命令执行完成后，获得以下结果：

<a id="code-block-11"></a>

```json
{
    "request_id": "f2ae64f7-83cc-410c-bc0b-840443f7eb86",
    "output": {
        "deployed_model": "qwen3-8b-20260115-abcd",
        "name": "我的模型服务",
        "model_name": "qwen3-8b",
        "base_model": "qwen3-8b",
        "status": "PENDING",
        "capacity": 4,
        "ready_capacity": 0,
        "base_capacity": 4,
        "workspace_id": "llm-8v53e*******",
        "charge_type": "post_paid",
        "plan": "mu",
        "model_unit_spec": "MU1",
        "creator": "16542902******",
        "modifier": "16542902******",
        "qpm_limit": 100000000,
        "tpm_limit": 3600000,
        "mu_capacity": {
            "unified": {
                "base_capacity": 4,
                "model_unit_spec": "MU1",
                "ready_capacity": 0,
                "capacity": 4
            }
        },
        "gmt_create": "2026-01-15T10:00:00",
        "gmt_modified": "2026-01-15T10:00:00"
    }
}
```

<table><thead><tr><th><p><strong>参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p>request_id</p></td><td><p>String</p></td><td><p>本次请求的 ID。</p></td></tr><tr><td><p>output</p></td><td><p>Object</p></td><td><p>本次部署任务的详细信息。</p></td></tr><tr><td><p>deployed_model</p></td><td><p>String</p></td><td><p>新模型的唯一标识，在发起模型调用请求时需要在 SDK 参数传入。</p></td></tr><tr><td><p>name</p></td><td><p>String</p></td><td><p>服务显示名称。</p></td></tr><tr><td><p>model_name</p></td><td><p>String</p></td><td><p>部署任务使用的模型名称。</p></td></tr><tr><td><p>base_model</p></td><td><p>String</p></td><td><p>部署任务使用的模型对应的基础模型 ID。</p></td></tr><tr><td><p>status</p></td><td><p>String</p></td><td><p>部署任务的状态。</p><ul><li><p>PENDING：正在创建部署任务。</p></li><li><p>DEPLOYING：部署中。</p></li><li><p>WAIT_PRE_PAID_BILLING_TO_DEPLOYING：创建处于预付费订单处理阶段（DTU）。</p></li><li><p>WAIT_PRE_PAID_BILLING_TO_SCALING：扩缩容处于预付费订单处理阶段（DTU）。</p></li><li><p>RUNNING：部署任务正在运行，可正常处理请求。</p></li><li><p>SCALING：扩缩容中。</p></li><li><p>UPDATING：正在更新部署任务。</p></li><li><p>UPDATING_PAUSED：更新已暂停。</p></li><li><p>SUSPENDING：暂停中（欠费）。</p></li><li><p>SUSPENDED：已暂停（欠费）。</p></li><li><p>STOPPING：停止中。</p></li><li><p>STOPPED：已停止，不再计费。</p></li><li><p>STARTING：启动中（从 STOPPED/FAILED 状态重新启动）。</p></li><li><p>FAILED：部署任务创建或更新失败。</p></li><li><p>DELETING：正在删除部署任务。</p></li></ul></td></tr><tr><td><p>capacity</p></td><td><p>Number</p></td><td><p>部署任务的目标资源单元数量。</p></td></tr><tr><td><p>ready_capacity</p></td><td><p>Number</p></td><td><p>已就绪并可立即处理请求的资源单元数量。</p></td></tr><tr><td><p>base_capacity</p></td><td><p>Number</p></td><td><p>单实例基础容量。</p></td></tr><tr><td><p>workspace_id</p></td><td><p>String</p></td><td><p>部署任务所属的业务空间 ID。</p></td></tr><tr><td><p>charge_type</p></td><td><p>String</p></td><td><p><code>post_paid</code>：后付费；<code>pre_paid</code>：预付费。</p></td></tr><tr><td><p>plan</p></td><td><p>String</p></td><td><p>部署任务的计费模式。</p></td></tr><tr><td><p>model_unit_spec</p></td><td><p>String</p></td><td><p>模型单元规格。</p></td></tr><tr><td><p>gmt_create</p></td><td><p>String</p></td><td><p>创建部署任务的时间。</p></td></tr><tr><td><p>gmt_modified</p></td><td><p>String</p></td><td><p>修改部署任务的时间。</p></td></tr><tr><td><p>creator</p></td><td><p>String</p></td><td><p>该部署任务创建人 UID。</p></td></tr><tr><td><p>modifier</p></td><td><p>String</p></td><td><p>对该部署任务进行最后一次操作的账号 UID。</p></td></tr><tr><td><p>fail_reason</p></td><td><p>String</p></td><td><p>失败原因（仅 FAILED 状态返回）。</p></td></tr><tr><td><p>enable_thinking</p></td><td><p>Boolean</p></td><td><p>是否开启思考模式，部分模型支持。</p></td></tr><tr><td><p>max_context_length</p></td><td><p>Number</p></td><td><p>最大上下文长度限制。</p></td></tr><tr><td><p>qpm_limit</p></td><td><p>Number</p></td><td><p>QPM 限流，每分钟请求数。</p></td></tr><tr><td><p>tpm_limit</p></td><td><p>Number</p></td><td><p>TPM 限流，每分钟 Token 使用量。</p></td></tr><tr><td><p>quantization_precision</p></td><td><p>String</p></td><td><p>量化精度。</p></td></tr><tr><td colspan="3"><p>仅 DTU（dtu）部署方式响应</p></td></tr><tr><td><p>dtu_capacity</p></td><td><p>Object</p></td><td><p>部署记录中的购买容量；扩缩容期间可能仍为原容量，不能据此认为目标已生效。</p></td></tr><tr><td><p>dtu_capacity.input_tpm</p></td><td><p>Integer</p></td><td><p>购买的输入 Token 容量（tokens/min）。</p></td></tr><tr><td><p>dtu_capacity.output_tpm</p></td><td><p>Integer</p></td><td><p>购买的输出 Token 容量（tokens/min）。</p></td></tr><tr><td><p>pre_paid_info.pricing_cycle</p></td><td><p>String</p></td><td><p>返回的购买计费周期（如 <code>Month</code>）；可能为 <code>null</code>，表示本响应未提供该值，不代表下单失败或购买时长为 0。</p></td></tr><tr><td><p>pre_paid_info.auto_renewal_cycle</p></td><td><p>String</p></td><td><p>返回的自动续费周期，有值时返回。</p></td></tr><tr><td><p>pre_paid_instance_id</p></td><td><p>String</p></td><td><p>预付费实例标识，有值时返回。不是部署标识，不能替代 <code>deployed_model</code>。</p></td></tr><tr><td colspan="3"><p>仅模型单元（mu）部署方式响应</p></td></tr><tr><td><p>mu_capacity</p></td><td><p>Object</p></td><td><p>MU 容量详情。COUPLED 模式包含 <code>unified</code> 节点，SEPERATED 模式包含 <code>prefill</code> 和 <code>decode</code> 节点。每个节点包含：base_capacity、model_unit_spec、ready_capacity、capacity。</p></td></tr><tr><td><p>pre_paid_info</p></td><td><p>Object</p></td><td><p>预付费信息。</p></td></tr><tr><td><p>pre_paid_info.auto_renewal</p></td><td><p>Boolean</p></td><td><p>是否自动续费</p></td></tr><tr><td><p>pre_paid_info.duration</p></td><td><p>Integer</p></td><td><p>购买时长（月）</p></td></tr><tr><td><p>pre_paid_info.auto_renewal_duration</p></td><td><p>Integer</p></td><td><p>自动续费时长</p></td></tr><tr><td><p>pre_paid_instance_id</p></td><td><p>String</p></td><td><p>预付费实例 ID。</p></td></tr><tr><td><p>pre_paid_gmt_expired</p></td><td><p>String</p></td><td><p>预付费过期时间。</p></td></tr><tr><td colspan="3"><p>仅预置吞吐量V2（ptu_v2）部署方式响应</p></td></tr><tr><td><p>ptu_capacity</p></td><td><p>Object</p></td><td><p>PTU V2 容量信息。包含字段：</p><ul><li><p><code>input_tpm_quota</code>（Number，输入 TPM 配额）</p></li><li><p><code>output_tpm_quota</code>（Number，输出 TPM 配额）</p></li></ul></td></tr><tr><td><p>pre_paid_info</p></td><td><p>Object</p></td><td><p>预付费信息。</p></td></tr><tr><td><p>pre_paid_info.auto_renewal</p></td><td><p>Boolean</p></td><td><p>是否自动续费</p></td></tr><tr><td><p>pre_paid_info.duration</p></td><td><p>Integer</p></td><td><p>购买时长（月）</p></td></tr><tr><td><p>pre_paid_info.auto_renewal_duration</p></td><td><p>Integer</p></td><td><p>自动续费时长</p></td></tr><tr><td><p>pre_paid_instance_id</p></td><td><p>String</p></td><td><p>预付费实例 ID。</p></td></tr><tr><td><p>pre_paid_gmt_expired</p></td><td><p>String</p></td><td><p>预付费过期时间。</p></td></tr></tbody></table>

DTU 部署的 `qpm_limit`、`tpm_limit` 为网关限流设置（64 位整数，可能超过修改接口的请求上限），默认 `qpm_limit=600000`、`tpm_limit=output_tpm × 100`，不等于购买的输入/输出 TPM，也不表示实际推理吞吐保证。`gmt_create`、`gmt_modified` 字符串不包含时区偏移，请勿自行当作 UTC 时间。

<a id="查询模型部署任务"></a>

<a id="be373c3fb0bx2"></a>

## 查询模型部署任务

<a id="code-block-12"></a>

```bash
GET https://dashscope.aliyuncs.com/api/v1/deployments/{deployed_model}
```

<a id="请求示例-3"></a>

<a id="f6eee4dbadjhp"></a>

### 请求示例

<a id="code-block-13"></a>

```bash
curl "https://dashscope.aliyuncs.com/api/v1/deployments/qwen3-8b-20260115-abcd" \
    --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    --header 'Content-Type: application/json'
```

<a id="请求参数-3"></a>

<a id="e3998e5959dl5"></a>

### 请求参数

| 参数 | 类型 | 传参方式 | 必选 | 说明 |
| --- | --- | --- | --- | --- |
| deployed\_model | String | path | 是 | 部署模型的唯一标识，可通过创建模型部署任务或列举模型部署任务获取。 |

<a id="响应示例-参数-3"></a>

<a id="7c4cfdd7f6jlh"></a>

### 响应示例&参数

<a id="accordion-点击此处查看-3"></a>

点击此处查看

命令执行完成后，获得以下结果：

<a id="code-block-14"></a>

```json
{
    "request_id": "d8b8c47b-ae32-4c41-b9f4-9a1e2b3c4d5e",
    "output": {
        "deployed_model": "qwen3-8b-20260115-abcd",
        "name": "我的模型服务",
        "model_name": "qwen3-8b",
        "base_model": "qwen3-8b",
        "status": "RUNNING",
        "capacity": 4,
        "ready_capacity": 4,
        "base_capacity": 4,
        "workspace_id": "llm-8v53e*******",
        "charge_type": "post_paid",
        "plan": "mu",
        "model_unit_spec": "MU1",
        "creator": "16542902******",
        "modifier": "16542902******",
        "qpm_limit": 100000000,
        "tpm_limit": 3600000,
        "mu_capacity": {
            "unified": {
                "base_capacity": 4,
                "model_unit_spec": "MU1",
                "ready_capacity": 4,
                "capacity": 4
            }
        },
        "gmt_create": "2026-01-15T10:00:00",
        "gmt_modified": "2026-01-15T10:30:00"
    }
}
```

<a id="be0baabef41ed"></a>

#### 响应参数

响应参数与创建模型部署任务的响应参数一致，请参考创建模型部署任务的响应参数说明。

<a id="列举模型部署任务"></a>

<a id="14574383a2j2f"></a>

## 列举模型部署任务

<a id="code-block-15"></a>

```bash
GET https://dashscope.aliyuncs.com/api/v1/deployments
```

<a id="请求示例-4"></a>

<a id="4594b88224x2o"></a>

### 请求示例

<a id="code-block-16"></a>

```bash
curl "https://dashscope.aliyuncs.com/api/v1/deployments?page_no=1&page_size=10" \
    --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    --header 'Content-Type: application/json'
```

<a id="请求参数-4"></a>

<a id="d43648b210xk1"></a>

### 请求参数

| 参数 | 类型 | 传参方式 | 必选 | 说明 |
| --- | --- | --- | --- | --- |
| page\_no | Number | query | 否 | 页码，默认值为1。 |
| page\_size | Number | query | 否 | 页大小，默认为10，最大值为100。 |
| plan | String | query | 否 | 传`dtu`查询 DTU 部署；DTU 部署不支持状态过滤。 |

<a id="响应示例-参数-4"></a>

<a id="fd5f1061e9wqi"></a>

### 响应示例&参数

<a id="accordion-点击此处查看-4"></a>

点击此处查看

命令执行完成后，获得以下结果：

<a id="code-block-17"></a>

```json
{
    "request_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "output": {
        "page_no": 1,
        "page_size": 10,
        "total": 2,
        "deployments": [
            {
                "deployed_model": "qwen3-8b-20260115-abcd",
                "name": "我的模型服务",
                "model_name": "qwen3-8b",
                "base_model": "qwen3-8b",
                "status": "RUNNING",
                "capacity": 4,
                "ready_capacity": 4,
                "base_capacity": 4,
                "workspace_id": "llm-8v53e*******",
                "charge_type": "post_paid",
                "plan": "mu",
                "model_unit_spec": "MU1",
                "creator": "16542902******",
                "modifier": "16542902******",
                "qpm_limit": 100000000,
                "tpm_limit": 3600000,
                "mu_capacity": {
                    "unified": {
                        "base_capacity": 4,
                        "model_unit_spec": "MU1",
                        "ready_capacity": 4,
                        "capacity": 4
                    }
                },
                "gmt_create": "2026-01-15T10:00:00",
                "gmt_modified": "2026-01-15T10:30:00"
            }
        ]
    }
}
```

<a id="66f59fe166mp8"></a>

#### 响应参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| page\_no | Number | 查询页码。 |
| page\_size | Number | 查询页大小。 |
| total | Long | 满足查询条件的所有部署任务总数。 |
| deployments | Array | 部署任务列表。每个元素的字段与创建模型部署任务的响应参数一致，请参考创建模型部署任务的响应参数说明。 |

<a id="更新模型部署任务"></a>

<a id="e14811ebe1tvg"></a>

## 更新模型部署任务

<a id="sec-tabs-5"></a>

<a id="扩缩容"></a>

<a id="扩缩容-h4"></a>

#### 扩缩容

> **说明**
>
> 更新模型部署任务即对部署服务进行扩缩容操作。仅当服务状态为 RUNNING 或 SCALING 时可调用，其他状态调用将返回 OperationDenied 错误。DTU 部署通过本接口传入 `dtu_capacity` 扩缩容：输入、输出 TPM 须同增同减（范围与组合限制与创建相同），成功仅表示请求已受理（状态先变为 `WAIT_PRE_PAID_BILLING_TO_SCALING`），需轮询详情至 `RUNNING` 且输入、输出容量均达到目标值。

<a id="code-block-18"></a>

```bash
PUT https://dashscope.aliyuncs.com/api/v1/deployments/{deployed_model}/scale
```

<a id="84a6cd6709az5"></a>

### 请求示例

COUPLED 模式扩缩容：

<a id="code-block-19"></a>

```bash
curl -X PUT "https://dashscope.aliyuncs.com/api/v1/deployments/qwen3-8b-20260115-abcd/scale" \
    --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    --header 'Content-Type: application/json' \
    --data '{
    "capacity": 8
}'
```

PD 分离模式扩缩容：

<a id="code-block-20"></a>

```bash
curl -X PUT "https://dashscope.aliyuncs.com/api/v1/deployments/qwen3-8b-20260115-abcd/scale" \
    --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    --header 'Content-Type: application/json' \
    --data '{
    "prefill_capacity": 4,
    "decode_capacity": 8
}'
```

DTU 部署扩缩容（需使用业务空间域名，请求体可省略 `plan`）：

<a id="code-block-21"></a>

```bash
curl -X PUT "https://ws-vxxx.cn-beijing.maas.aliyuncs.com/api/v1/deployments/your-deployment-id/scale" \
    --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    --header 'Content-Type: application/json' \
    --data '{
    "dtu_capacity": {"input_tpm": 20000, "output_tpm": 20000}
}'
```

<a id="87d0d7c0c3zv1"></a>

### 请求参数

| 参数 | 类型 | 传参方式 | 必选 | 说明 |
| --- | --- | --- | --- | --- |
| deployed\_model | String | path | 是 | 部署模型的唯一标识。 |
| capacity | Number | body | 条件必填 | 扩缩容的目标资源单元数量。COUPLED 模式（非 PD 分离）时必填，必须是 `base_capacity` 的整数倍。 |
| prefill\_capacity | Number | body | 条件必填 | Prefill 目标容量。PD 分离模式时必填。 |
| decode\_capacity | Number | body | 条件必填 | Decode 目标容量。PD 分离模式时必填。 |
| dtu\_capacity | Object | body | 条件必填 | DTU 目标容量，`plan` 为 `dtu` 时必填，须同时提供 `input_tpm` 与 `output_tpm`（均必填）；范围与组合限制与创建时相同，输入、输出需同增同减。本接口仅修改容量，不支持同时修改模型、SKU、模板、购买周期、自动续费或限流。 |

<a id="f448b3a19f69u"></a>

### 响应示例&参数

<a id="accordion-点击此处查看-5"></a>

点击此处查看

命令执行完成后，获得以下结果：

<a id="code-block-22"></a>

```json
{
    "request_id": "e5f6a7b8-c9d0-1234-5678-abcdef012345",
    "output": {
        "deployed_model": "qwen3-8b-20260115-abcd",
        "name": "我的模型服务",
        "model_name": "qwen3-8b",
        "base_model": "qwen3-8b",
        "status": "SCALING",
        "capacity": 8,
        "ready_capacity": 4,
        "base_capacity": 4,
        "workspace_id": "llm-8v53e*******",
        "charge_type": "post_paid",
        "plan": "mu",
        "model_unit_spec": "MU1",
        "creator": "16542902******",
        "modifier": "16542902******",
        "qpm_limit": 100000000,
        "tpm_limit": 3600000,
        "mu_capacity": {
            "unified": {
                "base_capacity": 4,
                "model_unit_spec": "MU1",
                "ready_capacity": 4,
                "capacity": 8
            }
        },
        "gmt_create": "2026-01-15T10:00:00",
        "gmt_modified": "2026-01-15T11:00:00"
    }
}
```

<a id="64d367c8f3fgv"></a>

#### 响应参数

响应参数与创建模型部署任务的响应参数一致，请参考创建模型部署任务的响应参数说明。

<a id="修改-dtu-部署的限流"></a>

<a id="修改-dtu-部署的限流-h4"></a>

#### 修改 DTU 部署的限流

> **说明**
>
> 仅 DTU（dtu）部署支持本接口。部署须处于空闲的 RUNNING 状态；请求必须同时提供 `qpm_limit` 与 `tpm_limit` 两个正整数，范围 1-2147483647；`rpm_limit` 可作为 `qpm_limit` 的别名，请只选择一个名称。限流值不适用购买容量的步长及输入/输出相同倍数规则。

<a id="code-block-23"></a>

```bash
PUT https://ws-vxxx.cn-beijing.maas.aliyuncs.com/api/v1/deployments/{deployed_model}/config
```

<a id="dtu-config-req-h3"></a>

### 请求示例

<a id="code-block-24"></a>

```bash
curl -X PUT "https://ws-vxxx.cn-beijing.maas.aliyuncs.com/api/v1/deployments/your-deployment-id/config" \
    --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    --header 'Content-Type: application/json' \
    --data '{
    "qpm_limit": 600,
    "tpm_limit": 100000
}'
```

成功时返回当前部署详情（响应参数与创建模型部署任务一致），顶层 message 为 `DTU rate limit configuration updated.`。本接口只修改限流阈值，不改变购买的输入、输出 TPM，也不支持同时更新模型或扩缩容。

<a id="更新-dtu-部署的模型"></a>

<a id="更新-dtu-部署的模型-h4"></a>

#### 更新 DTU 部署的模型

> **说明**
>
> 仅 DTU（dtu）部署支持本接口，且仅支持将微调模型更新为另一个微调模型：目标模型与当前模型的基础模型名称及版本必须相同。部署须处于空闲的 RUNNING 状态，且模板支持模型更新；相同模型、并发变更或其他不满足条件的请求会报错。

<a id="code-block-25"></a>

```bash
PUT https://ws-vxxx.cn-beijing.maas.aliyuncs.com/api/v1/deployments/{deployed_model}/update
```

<a id="dtu-update-req-h3"></a>

### 请求示例

<a id="code-block-26"></a>

```bash
curl -X PUT "https://ws-vxxx.cn-beijing.maas.aliyuncs.com/api/v1/deployments/your-deployment-id/update" \
    --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    --header 'Content-Type: application/json' \
    --data '{
    "new_model_name": "your-new-finetuned-model"
}'
```

<a id="dtu-update-reqparam-h3"></a>

### 请求参数

| 参数 | 类型 | 传参方式 | 必选 | 说明 |
| --- | --- | --- | --- | --- |
| deployed\_model | String | path | 是 | 部署模型的唯一标识。 |
| new\_model\_name | String | body | 是 | 目标微调模型名称，必须是当前业务空间内可见且有权限使用的模型。 |

> **警告**
>
> 更新按模板允许的最小批次策略连续发布，不进行首批暂停验收。更新期间可服务容量可能下降，新旧模型可能同时提供服务，可能出现延迟增加、限流或请求失败；最小批次发布不保证无损或零停机。请在发起前确认目标模型可用，并选择可接受这些影响的时间窗口。

本接口只更新模型，不支持修改限流、容量、SKU、模板、购买信息、发布比例或暂停参数。成功响应表示请求已受理（顶层 message 为 `DTU model update request accepted. The model is published continuously without pausing. Poll deployment details to confirm completion.`），需轮询详情，确认 `status` 为 `RUNNING` 且 `model_name` 已变为目标模型；仅恢复 `RUNNING` 不足以证明更新成功——更新失败并回退时可能仍使用旧模型。

<a id="停止部署的模型"></a>

<a id="b9b44525c2xha"></a>

## 停止部署的模型

> **说明**
>
> 仅模型单元（mu）部署方式支持停止服务。仅当服务状态为 RUNNING 或 SCALING 时可调用。cu、ptu\_v2、lora、dtu 方式调用此接口将返回 UnsupportedOperation 错误。停止后服务不再计费，可通过API 详情 API 重新启动。DTU 部署不支持 API 启停。

<a id="code-block-27"></a>

```bash
POST https://dashscope.aliyuncs.com/api/v1/deployments/{deployed_model}/stop
```

<a id="请求示例-5"></a>

<a id="557f02aa779ls"></a>

### 请求示例

<a id="code-block-28"></a>

```bash
curl -X POST "https://dashscope.aliyuncs.com/api/v1/deployments/qwen3-8b-20260115-abcd/stop" \
    --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    --header 'Content-Type: application/json'
```

<a id="请求参数-5"></a>

<a id="0470e7a0b3crx"></a>

### 请求参数

| 参数 | 类型 | 传参方式 | 必选 | 说明 |
| --- | --- | --- | --- | --- |
| deployed\_model | String | path | 是 | 部署模型的唯一标识。 |

<a id="响应示例-参数-5"></a>

<a id="ba259639072pq"></a>

### 响应示例&参数

<a id="accordion-点击此处查看-6"></a>

点击此处查看

命令执行完成后，获得以下结果：

<a id="code-block-29"></a>

```json
{
    "request_id": "f1a2b3c4-d5e6-7890-abcd-ef1234567890",
    "output": {
        "deployed_model": "qwen3-8b-20260115-abcd",
        "name": "我的模型服务",
        "model_name": "qwen3-8b",
        "base_model": "qwen3-8b",
        "status": "STOPPING",
        "capacity": 4,
        "ready_capacity": 4,
        "base_capacity": 4,
        "workspace_id": "llm-8v53e*******",
        "charge_type": "post_paid",
        "plan": "mu",
        "model_unit_spec": "MU1",
        "creator": "16542902******",
        "modifier": "16542902******",
        "qpm_limit": 100000000,
        "tpm_limit": 3600000,
        "mu_capacity": {
            "unified": {
                "base_capacity": 4,
                "model_unit_spec": "MU1",
                "ready_capacity": 4,
                "capacity": 4
            }
        },
        "gmt_create": "2026-01-15T10:00:00",
        "gmt_modified": "2026-01-15T12:00:00"
    }
}
```

<a id="5aeb1bec25dpt"></a>

#### 响应参数

响应参数与创建模型部署任务的响应参数一致，请参考创建模型部署任务的响应参数说明。

<a id="重新启动部署的模型"></a>

<a id="fe31838d7fevi"></a>

## 重新启动部署的模型

> **说明**
>
> DTU（dtu）部署暂不支持通过本接口启动服务。

<a id="code-block-30"></a>

```bash
POST https://dashscope.aliyuncs.com/api/v1/deployments/{deployed_model}/start
```

<a id="请求示例-6"></a>

<a id="578af53278lpw"></a>

### 请求示例

<a id="code-block-31"></a>

```bash
curl -X POST "https://dashscope.aliyuncs.com/api/v1/deployments/qwen3-8b-20260115-abcd/start" \
    --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    --header 'Content-Type: application/json'
```

<a id="请求参数-6"></a>

<a id="5f86b188550uz"></a>

### 请求参数

| 参数 | 类型 | 传参方式 | 必选 | 说明 |
| --- | --- | --- | --- | --- |
| deployed\_model | String | path | 是 | 部署模型的唯一标识，可通过创建模型部署任务或列举模型部署任务获取。 |

<a id="响应示例-参数-6"></a>

<a id="2eba7d3b00hcp"></a>

### 响应示例&参数

<a id="accordion-点击此处查看-7"></a>

点击此处查看

命令执行完成后，获得以下结果：

> 启动后状态为 `STARTING`，模型可调用后变为 `RUNNING`

<a id="code-block-32"></a>

```json
{
  "request_id": "xxx-xxx-xxx",
  "output": {
    "deployed_model": "qwen-7b-chat-ft-20240101-abcd",
    "model_name": "qwen-7b-chat-ft",
    "base_model": "qwen-7b-chat",
    "status": "STARTING",
    "capacity": 1,
    "ready_capacity": 0,
    "base_capacity": 1,
    "plan": "mu",
    "model_unit_spec": "MU5",
    "workspace_id": "workspace-xxx",
    "charge_type": "post_paid",
    "creator": "user123",
    "modifier": "user123",
    "qpm_limit": 100000000,
    "tpm_limit": 3600000,
    "mu_capacity": {
      "unified": {
        "base_capacity": 1,
        "model_unit_spec": "",
        "ready_capacity": 0,
        "capacity": 1
      }
    },
    "gmt_create": "2024-01-01T10:00:00",
    "gmt_modified": "2024-01-01T13:00:00"
  }
}
```

<a id="0ffb9c955772y"></a>

#### 响应参数

响应参数与创建模型部署任务的响应参数一致，请参考创建模型部署任务的响应参数说明。

<a id="删除模型部署任务"></a>

<a id="a526c00058g7g"></a>

## 删除模型部署任务

> **说明**
>
> 仅当服务状态为 STOPPED 或 FAILED 时可调用删除。RUNNING 状态的服务需先调用API 详情接口。DTU（dtu）部署暂不支持通过本接口删除，请在控制台退订，详见[独占吞吐（DTU）](../../../model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/dtu-model-deployment.md)。

<a id="code-block-33"></a>

```http
DELETE https://dashscope.aliyuncs.com/api/v1/deployments/{deployed_model}
```

<a id="请求示例-7"></a>

<a id="ng01h32"></a>

### 请求示例

<a id="code-block-34"></a>

```bash
curl -X DELETE "https://dashscope.aliyuncs.com/api/v1/deployments/qwen3-8b-20260115-abcd" \
    --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    --header 'Content-Type: application/json'
```

<a id="请求参数-7"></a>

<a id="ng01h33"></a>

### 请求参数

| 参数 | 类型 | 传参方式 | 必选 | 说明 |
| --- | --- | --- | --- | --- |
| deployed\_model | String | path | 是 | 部署模型的唯一标识。 |

<a id="响应示例-参数-7"></a>

<a id="276c2c8778l63"></a>

### 响应示例&参数

<a id="accordion-点击此处查看-8"></a>

点击此处查看

命令执行完成后，获得以下结果：

<a id="code-block-35"></a>

```json
{
    "request_id": "g1h2i3j4-k5l6-7890-mnop-qr1234567890",
    "output": {
        "deployed_model": "qwen3-8b-20260115-abcd",
        "name": "我的模型服务",
        "model_name": "qwen3-8b",
        "base_model": "qwen3-8b",
        "status": "DELETING",
        "capacity": 4,
        "ready_capacity": 0,
        "base_capacity": 4,
        "workspace_id": "llm-8v53e*******",
        "charge_type": "post_paid",
        "plan": "mu",
        "model_unit_spec": "MU1",
        "creator": "16542902******",
        "modifier": "16542902******",
        "gmt_create": "2026-01-15T10:00:00",
        "gmt_modified": "2026-01-15T14:00:00"
    }
}
```

<a id="52b85ccfd1fir"></a>

#### 响应参数

响应参数与创建模型部署任务的响应参数一致，请参考创建模型部署任务的响应参数说明。

<a id="异常响应"></a>

<a id="ee7c8dc058j9j"></a>

## 异常响应

<a id="code-block-36"></a>

```json
{
    "request_id": "6fec0a3f-a1df-4f89-8c8f-33cb0db9f5b0",
    "code": "InvalidParameter",
    "message": "capacity is required when template_type is COUPLED"
}
```

<a id="响应参数"></a>

<a id="nh02h3"></a>

### 响应参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| request\_id | String | 本次请求的系统生成 ID。 |
| code | String | 错误码，标识错误类型。 |
| message | String | 错误详情，用于问题排查。 |

<a id="常见错误"></a>

<a id="nh03h3"></a>

### 常见错误

| 错误原因 | 说明 |
| --- | --- |
| `InvalidParameter` | 参数错误，如缺少必填参数、参数值不合法、template\_id 和 deploy\_spec 同时传入等。 |
| `AccessDenied` | 权限不足或资源不存在。 |
| `OperationDenied` | 当前状态不允许执行该操作，如在非 RUNNING 状态下执行扩缩容，或在非 STOPPED/FAILED 状态下删除。 |
| `UnsupportedOperation` | 当前部署方案不支持该操作，如 cu 方式不支持停止服务。 |
| `StockLimit` | 资源库存不足，无法完成扩容或部署。 |
| `InternalError` | 内部错误。 |
| `NotFound` | 指定的部署任务不存在。 |
| `Conflict` | 操作冲突，如服务正在进行其他操作。 |
| `QuotaExceeded` | 配额不足（DTU 预付费购买常见），请检查可用配额或联系服务支持。 |
| `InsufficientResource` | 资源不足，无法完成部署或扩容，可调整容量或联系服务支持。 |
| `ServiceUnavailable` | 服务暂时不可用，请退避后重试。 |
