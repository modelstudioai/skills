# 部署模型管理

部署模型管理接口， 适用于文本、图像、视频、语音等所有模型类型 。支持查询部署状态、获取可部署模型列表与部署列表、修改限流、扩缩容及删除部署。

<a id="适用范围"></a>

<a id="634380ea1e3am"></a>

## 适用范围

-   **适用地域**：本文描述的功能仅在**华北2（北京）地域**可用，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。
-   已成功[获取 API Key](../../preparations/get-api-key.md)并[配置到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
-   已阅读[模型部署](../../../model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md)和[使用 API 进行模型部署](../../../model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-quick-start.md)，了解模型部署的基本步骤。

> **说明**
>
> DTU 计费模式的部署使用同一组部署接口创建与管理，请求中以
>
> `plan="dtu"` 区分部署形式（创建、查询、扩缩容、修改限流与更新模型），DTU 相关参数、状态与域名说明详见 [模型部署 API 参考](model-deployment-api-reference.md)。续费与自动续费变更请在控制台操作，详见 [独占吞吐（DTU）](../../../model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/dtu-model-deployment.md)。

<a id="查询部署模型状态"></a>

<a id="09893a6ec96xp"></a>

## 查询部署模型状态

查询指定部署模型的详细信息和运行状态。可轮询此接口，当任务状态`status`变为**RUNNING**时，表示模型已部署成功。

> **说明**
>
> 模型部署过程预计需要 **5～10分钟**。

<a id="地址"></a>

<a id="8d5ac8fa87gs1"></a>

### 地址

<a id="code-block"></a>

```http
GET https://dashscope.aliyuncs.com/api/v1/deployments/{deployed_model}
```

<a id="请求示例"></a>

<a id="47484707ccxid"></a>

### 请求示例

通过以下命令可以查询指定专属服务的详细信息：

<a id="code-block-2"></a>

```bash
curl "https://dashscope.aliyuncs.com/api/v1/deployments/qwen-plus-202305099980-fac9-sample" \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --header 'Content-Type: application/json'
```

<a id="请求参数"></a>

<a id="3fb55f3ca72xp"></a>

### 请求参数

| 参数 | 类型 | 传参方式 | 必选 | 说明 |
| --- | --- | --- | --- | --- |
| deployed\_model | String | path | 是 | 部署模型的唯一标识，可通过[部署模型](model-deployment-text-generation-api/create-deployment-api.md)或查询部署模型列表接口获取。 |

<a id="响应示例"></a>

<a id="1c84778940gx9"></a>

### 响应示例

关注`status`字段。当状态变为 **RUNNING** 时，表示模型已部署成功，可以开始调用。

<a id="code-block-3"></a>

```json
{
  "request_id": "66a855f0-a6fe-4b05-9786-fb30c7c6782d",
  "output": {
    "deployed_model": "emo-35b3f106-sample01",
    "gmt_create": "2025-06-17T11:00:38",
    "gmt_modified": "2025-06-17T11:06:13",
    "status": "RUNNING",
    "model_name": "emo",
    "base_model": "emo",
    "base_capacity": 1,
    "capacity": 1,
    "ready_capacity": 1,
    "workspace_id": "llm-v71tlv3***",
    "charge_type": "post_paid",
    "creator": "175805416***",
    "modifier": "175805416***"
  }
}
```

<a id="响应参数"></a>

<a id="8567c7ddfbosd"></a>

### 响应参数

<table><thead><tr><th><p><strong>字段</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>描述</strong></p></th></tr></thead><tbody><tr><td><p>request_id</p></td><td><p>String</p></td><td><p>请求的唯一标识符。</p></td></tr><tr><td><p>output</p></td><td><p>Object</p></td><td><p>任务详情。</p></td></tr><tr><td><p>output.deployed_model</p></td><td><p>String</p></td><td><p>部署模型的唯一标识。用于查询模型部署状态和调用模型。</p></td></tr><tr><td><p>output.model_name</p></td><td><p>String</p></td><td><p>模型标识名。</p></td></tr><tr><td><p>output.base_model</p></td><td><p>String</p></td><td><p>使用的基准模型。</p></td></tr><tr><td><p>output.status</p></td><td><p>String</p></td><td><p>部署状态：</p><ul><li><p>PENDING：正在创建部署任务。</p></li><li><p>RUNNING：部署任务正在运行，模型可正常处理请求。</p></li><li><p>UPDATING：变配中。</p></li><li><p>UPDATING_FAILED：变配失败。</p></li><li><p>DELETING：正在删除部署任务。</p></li><li><p>DELETED：已删除。</p></li><li><p>FAILED：部署任务创建或更新失败。</p></li><li><p>STOPPED：部署任务已停止，不会被计费。</p></li><li><p>ARREARS_DOWN：欠费停服。</p></li><li><p>ARREARS_RECOVERING：欠费停服恢复中。</p></li><li><p>OFFLINING：服务下线中。</p></li></ul></td></tr><tr><td><p>output.base_capacity</p></td><td><p>Number</p></td><td><p>基础资源单元数量。</p></td></tr><tr><td><p>output.capacity</p></td><td><p>Number</p></td><td><p>当前资源单元数量。</p></td></tr><tr><td><p>output.ready_capacity</p></td><td><p>Number</p></td><td><p>已就绪的资源单元数量。</p></td></tr><tr><td><p>output.workspace_id</p></td><td><p>String</p></td><td><p>阿里云百炼 API Key 所属的业务空间 ID。请参见<a href="../../../application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md#732535cfc959h">获取Workspace ID</a>。</p></td></tr><tr><td><p>output.charge_type</p></td><td><p>String</p></td><td><p>付费模式。post_paid 表示后付费。</p></td></tr><tr><td><p>output.gmt_create</p></td><td><p>String</p></td><td><p>部署任务创建时间。</p></td></tr><tr><td><p>output.gmt_modified</p></td><td><p>String</p></td><td><p>部署任务更新时间。</p></td></tr><tr><td><p>output.creator</p></td><td><p>String</p></td><td><p>创建人的阿里云账号 ID。</p></td></tr><tr><td><p>output.modifier</p></td><td><p>String</p></td><td><p>修改人的阿里云账号 ID。</p></td></tr><tr><td><p>output.plan</p></td><td><p>String</p></td><td><p>部署方式。</p></td></tr></tbody></table>

<a id="获取可部署模型列表"></a>

<a id="9e9287b2fd629"></a>

## 获取可部署模型列表

获取百炼平台上**有资格部署的候选模型**清单，即哪些模型可以用来创建部署。

<a id="地址-2"></a>

<a id="28112bfa68m02"></a>

### 地址

<a id="code-block-4"></a>

```http
GET https://dashscope.aliyuncs.com/api/v1/deployments/models
```

<a id="请求示例-2"></a>

<a id="23ff587743990"></a>

### 请求示例

通过下面的命令可以查询支持部署的模型，推荐使用`version=v1.0`获取包含部署方案和模板信息的完整响应。

<a id="code-block-5"></a>

```bash
curl "https://dashscope.aliyuncs.com/api/v1/deployments/models?page_no=1&page_size=100&version=v1.0&model_source=base" \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --header 'Content-Type: application/json'
```

查询用户调优模型：

<a id="code-block-6"></a>

```bash
curl "https://dashscope.aliyuncs.com/api/v1/deployments/models?page_no=1&page_size=100&version=v1.0&model_source=custom" \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --header 'Content-Type: application/json'
```

<a id="请求参数-2"></a>

<a id="74d15d8f07mgq"></a>

### 请求参数

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| page\_no | Number | 否 | 页码，默认值为1。 |
| page\_size | Number | 否 | 页大小，默认为50，最大值为100，最小值为1。 |
| model\_source | String | 否 | 模型来源。`base`表示系统模型（默认），`custom`表示用户调优模型。 |
| version | String | 否 | API 版本，推荐使用`v1.0`。使用`v1.0`时，响应中将包含完整的部署方案和模板信息。 |

<a id="响应示例-2"></a>

<a id="365997715fjsj"></a>

### 响应示例

命令执行完成后，获得以下结果：

<a id="code-block-7"></a>

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

<a id="响应参数-2"></a>

<a id="a553eb467d50a"></a>

### 响应参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| models | Array | 可部署模型列表。 |
| models\[\].model\_name | String | 模型名称。 |
| models\[\].plans | Array | 该模型支持的部署方案列表。使用`version=v1.0`时返回。 |
| models\[\].plans\[\].plan | String | 部署方案类型：`mu`（模型单元）、`cu`（算力单元）、`ptu`（预置吞吐量）、`lora`（LoRA共享部署）。 |
| models\[\].plans\[\].templates | Array | 部署模板列表（`plan=mu`时返回）。 |
| models\[\].plans\[\].templates\[\].template\_id | String | 模板 ID，在[创建模型部署任务](https://help.aliyun.com/zh/model-studio/model-deployment-api)时作为`deploy_spec`参数传入。 |
| models\[\].plans\[\].templates\[\].template\_name | String | 模板显示名称。 |
| models\[\].plans\[\].templates\[\].template\_type | String | 模板类型：`COUPLED`（非 PD 分离，使用`capacity`参数）、`SEPERATED`（PD 分离，使用`prefill_capacity`和`decode_capacity`参数）。 |
| models\[\].plans\[\].templates\[\].template\_version | String | 模板版本。 |
| models\[\].plans\[\].templates\[\].template\_desc | String | 模板描述。 |
| models\[\].plans\[\].templates\[\].roles | Object | 节点角色配置。COUPLED 模式包含`unified`节点，SEPERATED 模式包含`prefill`和`decode`节点。 |
| models\[\].plans\[\].templates\[\].roles.{role}.model\_unit\_spec | String | 模型单元规格。 |
| models\[\].plans\[\].templates\[\].roles.{role}.capacity\_unit\_per\_instance | Number | 单实例容量单元数，即 base\_capacity。创建部署时`capacity`必须是该值的整数倍。 |
| page\_no | Number | 查询页码。 |
| page\_size | Number | 查询页大小。 |
| total | Long | 满足查询条件的所有模型个数。 |

<a id="获取已部署模型列表"></a>

<a id="ce0559e5a4fd2"></a>

## 获取已部署模型列表

获取**已创建的部署实例**列表，即当前工作空间下实际运行或已部署的模型服务。

<a id="地址-3"></a>

<a id="e23d1647eb97y"></a>

### 地址

<a id="code-block-8"></a>

```http
GET https://dashscope.aliyuncs.com/api/v1/deployments
```

<a id="请求示例-3"></a>

<a id="efc71e867awoi"></a>

### 请求示例

通过以下命令可以获取专属服务列表：

<a id="code-block-9"></a>

```bash
curl "https://dashscope.aliyuncs.com/api/v1/deployments?page_no=1&page_size=100" \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --header 'Content-Type: application/json'
```

<a id="请求参数-3"></a>

<a id="baf571b2e1761"></a>

### 请求参数

| 参数 | 类型 | 传参方式 | 必选 | 说明 |
| --- | --- | --- | --- | --- |
| page\_no | Number | query | 否 | 页码，默认值为1。 |
| page\_size | Number | query | 否 | 页大小，默认为50，最大值为200，最小值为1。 |

<a id="响应示例-3"></a>

<a id="dd0b4db7ffhz6"></a>

### 响应示例

命令执行完成后，返回以下结果：

<a id="code-block-10"></a>

```json
{
  "request_id": "7efdd3a7-a90d-96c6-b477-70055d59edf7",
  "output": {
    "page_no": 1,
    "page_size": 10,
    "total": 1,
    "deployments": [
      {
        "deployed_model": "emo-35b3f106-sample01",
        "gmt_create": "2025-06-17T11:00:38",
        "gmt_modified": "2025-06-17T11:06:13",
        "status": "RUNNING",
        "model_name": "emo",
        "base_model": "emo",
        "base_capacity": 1,
        "capacity": 1,
        "ready_capacity": 1,
        "workspace_id": "llm-v71tlv3d***",
        "charge_type": "post_paid",
        "creator": "175805416***",
        "modifier": "175805416***"
      }
    ]
  }
}
```

<a id="响应参数-3"></a>

<a id="b0bf8aed91j5n"></a>

### 响应参数

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| request\_id | String | 本次请求的系统唯一码。 |
| output.page\_no | Number | 当前页码。 |
| output.page\_size | Number | 每页数量。 |
| output.total | Number | 部署总数。 |
| output.deployments | Array | 部署模型列表，每个元素的字段与[查询部署模型状态](get-deployment-api.md#09893a6ec96xp)的 output 字段一致。 |

<a id="修改部署模型的限流"></a>

<a id="6d45b3880clmz"></a>

## 修改部署模型的限流

修改指定部署模型的 RPM（每分钟请求数）和 TPM（每分钟 Token 数）限流设置。

> **说明**
>
> 仅模型单元部署方式的[部分模型](model-deployment-text-generation-api/create-deployment-api.md)支持修改设置 rpm 和 tpm。

<a id="地址-4"></a>

<a id="4298a93855qnc"></a>

### 地址

<a id="code-block-11"></a>

```http
PUT https://dashscope.aliyuncs.com/api/v1/deployments/{deployed_model}/update
```

<a id="请求示例-4"></a>

<a id="c6c9b012e9idg"></a>

### 请求示例

通过以下命令可以修改指定部署的限流设置：

<a id="code-block-12"></a>

```bash
curl -X PUT "https://dashscope.aliyuncs.com/api/v1/deployments/qwen-plus-2025-12-01-b6d61c71/update" \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "rpm_limit": 1000,
    "tpm_limit": 200
}'
```

<a id="请求参数-4"></a>

<a id="11a1929f74zjo"></a>

### 请求参数

<table><thead><tr><th><p><strong>参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>传参方式</strong></p></th><th><p><strong>必选</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p>deployed_model</p></td><td><p>String</p></td><td><p>path</p></td><td><p>是</p></td><td><p>部署模型的唯一标识，可通过<a href="model-deployment-text-generation-api/create-deployment-api.md">部署模型</a>或查询部署模型列表接口获取。</p></td></tr><tr><td><p>rpm_limit</p></td><td><p>Number</p></td><td><p>body</p></td><td rowspan="2"><p>至少填写一个参数</p></td><td><p>Requests per minute，每分钟请求数。</p></td></tr><tr><td><p>tpm_limit</p></td><td><p>Number</p></td><td><p>body</p></td><td><p>Token per minute，每分钟 Token 使用量。</p></td></tr></tbody></table>

<a id="响应示例-4"></a>

<a id="11a4eece2eole"></a>

### 响应示例

命令执行完成后，返回如下结果：

<a id="code-block-13"></a>

```json
{
    "request_id": "1d121fd9-876c-40ad-bc40-a9e68ef3b986",
    "output":
    {
        "deployed_model": "qwen-plus-2025-12-01-b6d61c71",
        "gmt_create": "2026-01-07T13:52:44",
        "gmt_modified": "2026-01-07T14:01:41",
        "status": "PENDING",
        "model_name": "qwen-plus-2025-12-01",
        "base_model": "qwen-plus-2025-12-01",
        "base_capacity": 4,
        "capacity": 4,
        "ready_capacity": 0,
        "workspace_id": "llm-8v53e*******",
        "charge_type": "post_paid",
        "creator": "16542902******",
        "modifier": "16542902********",
        "plan": "mu",
        "model_unit_spec": "MU1",
        "enable_thinking": true,
        "max_context_length": 1,
        "rpm_limit": 1000,
        "tpm_limit": 200
    }
}
```

<a id="响应参数-4"></a>

<a id="c8690122eepu5"></a>

### 响应参数

除[查询部署模型状态](get-deployment-api.md#09893a6ec96xp)中列出的基础字段外，还可能包含以下字段：

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| output.plan | String | 部署方式。 |
| output.model\_unit\_spec | String | 模型单元部署模板，如 MU1。 |
| output.enable\_thinking | Boolean | 是否开启思考模式。 |
| output.max\_context\_length | Number | 最大上下文长度。 |
| output.rpm\_limit | Number | 每分钟请求数限制。 |
| output.tpm\_limit | Number | 每分钟 Token 数限制。 |

<a id="扩缩容部署服务"></a>

<a id="870260a9eeeyz"></a>

## 扩缩容部署服务

通过更新操作调整专属服务使用的资源单元数量。

<a id="地址-5"></a>

<a id="f8bc6bdbda9f3"></a>

### 地址

<a id="code-block-14"></a>

```http
PUT https://dashscope.aliyuncs.com/api/v1/deployments/{deployed_model}/scale
```

<a id="请求示例-5"></a>

<a id="eddff8dbb963q"></a>

### 请求示例

通过以下命令可以将指定的服务进行扩缩容：

<a id="code-block-15"></a>

```bash
curl --request PUT "https://dashscope.aliyuncs.com/api/v1/deployments/emo-35b3f106-sample01/scale" \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --header 'Content-Type: application/json' \
    --data '{
                "capacity":2
            }'
```

<a id="请求参数-5"></a>

<a id="6d783b4ffa9mv"></a>

### 请求参数

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| deployed\_model | String | 是 | 部署模型的唯一标识（path 参数），可通过[部署模型](model-deployment-text-generation-api/create-deployment-api.md)或查询部署模型列表接口获取。 |
| capacity | Integer | 条件必选 | 仅`"plan": "mu"`时生效。具体支持情况请参考[模型单元部署的功能支持情况](model-deployment-text-generation-api/create-deployment-api.md)。<br><br>更新后模型所使用的资源单元数量，**必须**是`base_capacity`的整数倍。 |
| ptu\_capacity | Object | 条件必选 | 仅`"plan": "ptu"`时生效。具体支持情况请参考[PTU部署的功能支持情况](model-deployment-text-generation-api/create-deployment-api.md)。<br><br>样例：`"ptu_capacity": { "input_tpm": 10000, "output_tpm": 1000 }`。 |
| ptu\_capacity.input\_tpm | Number | 条件必选 | 仅`"plan": "ptu"`时生效。具体支持情况请参考[PTU部署的功能支持情况](model-deployment-text-generation-api/create-deployment-api.md)。<br><br>部署的模型每分钟支持的最大输入 Token 量（input tokens per minute）。所有模型支持。 |
| ptu\_capacity.output\_tpm | Number | 条件必选 | 仅`"plan": "ptu"`时生效。具体支持情况请参考[PTU部署的功能支持情况](model-deployment-text-generation-api/create-deployment-api.md)。<br><br>部署的模型每分钟支持的最大输出 Token 量（output tokens per minute）。所有模型支持。 |
| ptu\_capacity.thinking\_output\_tpm | Number | 否 | 仅`"plan": "ptu"`时生效。具体支持情况请参考[PTU部署的功能支持情况](model-deployment-text-generation-api/create-deployment-api.md)。<br><br>部署的模型每分钟支持的预置思考最大输出 Token 量（thinking output tokens per minute）。部分模型支持。 |

<a id="响应示例-5"></a>

<a id="92f969029777u"></a>

### 响应示例

命令执行完成后，返回以下结果：

<a id="code-block-16"></a>

```json
{
  "request_id": "6c6b7676-3fea-423b-bc26-c9e2337e1142",
  "output": {
    "deployed_model": "emo-35b3f106-sample01",
    "gmt_create": "2025-06-17T11:00:38",
    "gmt_modified": "2025-06-17T11:42:02.311",
    "status": "UPDATING",
    "model_name": "emo",
    "base_model": "emo",
    "base_capacity": 1,
    "capacity": 2,
    "ready_capacity": 1,
    "workspace_id": "llm-v71tlv3dezezp2en",
    "charge_type": "post_paid",
    "creator": "17580541***",
    "modifier": "17580541***"
  }
}
```

<a id="响应参数-5"></a>

<a id="8ccb319fa1l7f"></a>

### 响应参数

响应字段与[查询部署模型状态](get-deployment-api.md#09893a6ec96xp)一致，请参考查询部署模型状态的响应参数。

<a id="删除部署"></a>

<a id="4984b6ab4bz05"></a>

## 删除部署

删除指定的部署模型，释放对应的计算资源。

> **重要**
>
> 执行该操作后，模型部署服务将立即下线且**不可恢复**：
>
> 1.  模型将无法调用。
> 2.  部署服务停止计费。

<a id="地址-6"></a>

<a id="7de1d2d10f3tn"></a>

### 地址

<a id="code-block-17"></a>

```http
DELETE https://dashscope.aliyuncs.com/api/v1/deployments/{deployed_model}
```

<a id="请求示例-6"></a>

<a id="8d81e6bebbfgm"></a>

### 请求示例

通过以下命令可以删除指定的部署任务。

<a id="code-block-18"></a>

```bash
curl --request DELETE "https://dashscope.aliyuncs.com/api/v1/deployments/emo-35b3f106-sample01" \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --header 'Content-Type: application/json'
```

<a id="请求参数-6"></a>

<a id="f5f3c56c6coq7"></a>

### 请求参数

| 参数 | 类型 | 传参方式 | 必选 | 说明 |
| --- | --- | --- | --- | --- |
| deployed\_model | String | path | 是 | 部署模型的唯一标识，可通过[部署模型](model-deployment-text-generation-api/create-deployment-api.md)或查询部署模型列表接口获取。 |

<a id="响应示例-6"></a>

<a id="c4d4a4d586yli"></a>

### 响应示例

关注`status`字段。当状态变为 **DELETING** 时，表示正在删除部署任务。

<a id="code-block-19"></a>

```json
{
  "request_id": "5378b78b-8564-481f-a3e0-580e551df22c",
  "output": {
    "deployed_model": "emo-35b3f106-sample01",
    "gmt_create": "2025-06-17T11:00:38",
    "gmt_modified": "2025-06-17T11:42:02",
    "status": "DELETING",
    "model_name": "emo",
    "base_model": "emo",
    "base_capacity": 1,
    "capacity": 2,
    "ready_capacity": 1,
    "workspace_id": "llm-v71tlv3***",
    "charge_type": "post_paid",
    "creator": "175805416***",
    "modifier": "175805416***"
  }
}
```

之后，再调用[查询部署模型状态](get-deployment-api.md#09893a6ec96xp)进行验证。若返回如下内容，说明部署的服务已不存在，删除成功。

<a id="code-block-20"></a>

```json
{
    "request_id": "eb619064-0c4f-4d29-aa49-xxxxxx",
    "message": "Not found.",
    "code": "NotFound"
}
```

<a id="响应参数-6"></a>

<a id="9d4ea4f7e6rfw"></a>

### 响应参数

响应字段与[查询部署模型状态](get-deployment-api.md#09893a6ec96xp)一致，请参考查询部署模型状态的响应参数。

<a id="异常响应"></a>

<a id="3a46ae96013z6"></a>

## 异常响应

<a id="响应示例-7"></a>

<a id="081e84fe38xxt"></a>

### 响应示例

<a id="code-block-21"></a>

```json
{
    "request_id": "ca218d57-b91b-46b2-bd35-c41c6287bcf4",
    "message": "Model: qwen-plus-20230703-cx7f not found!",
    "code": "NotFound"
}
```

<a id="响应参数-7"></a>

<a id="208c7caff7i9c"></a>

### 响应参数

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| request\_id | String | 本次请求的系统唯一码。 |
| code | String | 错误码。 |
| message | String | 错误信息。 |

当请求出错时，可能返回以下错误：

<table><thead><tr><th><p><strong>错误码</strong></p></th><th><p><strong>错误信息</strong></p></th><th><p><strong>错误原因</strong></p></th></tr></thead><tbody><tr><td><p><strong>NotFound</strong></p></td><td><p>Model: xxx not found!</p></td><td><ul><li><p>创建部署任务时指定了不存在的模型。</p></li><li><p>查询/更新/删除部署任务时指定了不存在的模型。</p></li></ul></td></tr><tr><td><p><strong>Conflict</strong></p></td><td><p>Deployed model xxx already exists, please specify a suffix.</p></td><td><p>创建部署任务时使用了已使用过的suffix。</p></td></tr><tr><td><p><strong>InvalidParameter</strong></p></td><td><p>Invalid capacity (xx), capacity must be larger than or equal to 0 and multiples of 1 and less than 1000!</p></td><td><p>创建/更新部署任务时指定了无效的算力单元数量。</p></td></tr></tbody></table>
