# 更新模型授权

调用 POST /api/v1/models/permissions 接口更新指定业务空间下模型的授权（推理 / 微调 / 部署），支持逐模型授权与"一键授权"两种模式。

<a id="前提条件"></a>

<a id="ump0000a010"></a>

<a id="prerequisite-section-ump"></a>

## 前提条件

已创建 API Key 并配置为环境变量 `DASHSCOPE_API_KEY`。配置方法请参见[配置API Key到环境变量](../preparations/get-api-key.md)。

<a id="请求说明"></a>

<a id="43f31e8630lzd"></a>

<a id="request-section-ump"></a>

## 请求说明

-   **HTTP 方法**：POST
    
-   **请求地址**
    
    > 调用时请将 `{WorkspaceId}` 替换为您的业务空间 ID。
    
    | 地域 | Endpoint |
    | --- | --- |
    | 华北2（北京） | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/models/permissions` |
    
-   **认证方式**
    
    在请求 Header 中设置 `Authorization: Bearer {API_KEY}`。
    

<a id="请求参数"></a>

<a id="ump0000a100"></a>

<a id="request-params-section-ump"></a>

## 请求参数

所有参数均通过请求 Body 传递。

<table><thead><tr><th><p><strong>参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>必选</strong></p></th><th><p><strong>描述</strong></p></th></tr></thead><tbody><tr><td><p>models</p></td><td><p>Array[Object]</p></td><td><p>条件必填</p></td><td><p>逐模型授权项列表。当 <code>access_all_entities</code> 为 <code>OPEN</code>/<code>CLOSE</code> 时可空；为 <code>KEEP</code> 或不传时必填，且数量需为 1~20。示例：<code>[{&quot;model&quot;:&quot;qwen-plus&quot;,&quot;inference&quot;:true}]</code></p></td></tr><tr><td><p>models[].model</p></td><td><p>String</p></td><td><p>是</p></td><td><p>模型 ID，不能为空。如 <code>qwen-plus</code>、<code>qwen-max</code>。</p></td></tr><tr><td><p>models[].inference</p></td><td><p>Boolean</p></td><td><p>否</p></td><td><p>模型调用权限。<code>true</code>=授权推理，<code>false</code>=取消授权，不传=保持现状。默认值：null（不变更）。</p></td></tr><tr><td><p>models[].finetune</p></td><td><p>Boolean</p></td><td><p>否</p></td><td><p>模型训练权限。<code>true</code>=授权微调，<code>false</code>=取消，不传=保持现状。默认值：null（不变更）。</p></td></tr><tr><td><p>models[].deploy</p></td><td><p>Boolean</p></td><td><p>否</p></td><td><p>模型部署权限。<code>true</code>=授权部署，<code>false</code>=取消，不传=保持现状。默认值：null（不变更）。</p></td></tr><tr><td><p>access_all_entities</p></td><td><p>String</p></td><td><p>否</p></td><td><p>一键授权开关。可选值：</p><ul><li><p><code>OPEN</code>：一键授权当前空间全部推理模型（含后续新增）。</p></li><li><p><code>CLOSE</code>：取消一键授权并清空历史推理授权。</p></li><li><p><code>KEEP</code>：保持原逐模型授权行为（缺省）。</p></li></ul><p>传 <code>OPEN</code>/<code>CLOSE</code> 时 <code>models</code> 可不填。默认值：<code>KEEP</code>。示例：<code>OPEN</code></p></td></tr></tbody></table>

<a id="返回参数"></a>

<a id="ump0000a200"></a>

<a id="response-params-section-ump"></a>

## 返回参数

| 参数 | 类型 | 描述 |
| --- | --- | --- |
| request\_id | String | 请求 ID。示例：`d5f5201f-ee7a-9e3d-8569-bc0eedec21f9` |
| code | String | 错误码，成功为 `null`。 |
| message | String | 错误信息，成功为 `null`。 |
| success | Boolean | 是否成功。示例：`true` |
| output | Object | 业务数据，本接口为 `null`。 |

<a id="请求示例"></a>

<a id="ump0000a300"></a>

<a id="example-section-ump"></a>

## 请求示例

**示例一：逐模型授权**

<a id="code-block"></a>

```bash
curl -X POST "https://dashscope.aliyuncs.com/api/v1/models/permissions" \
    --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    --header 'Content-Type: application/json' \
    --data '{
        "models": [
            {"model": "qwen-plus", "inference": true, "fine_tune": true, "deploy": false},
            {"model": "qwen-max", "inference": true}
        ]
    }'
```

**示例二：一键授权**

<a id="code-block-2"></a>

```bash
curl -X POST "https://dashscope.aliyuncs.com/api/v1/models/permissions" \
    --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    --header 'Content-Type: application/json' \
    --data '{"access_all_entities": "OPEN"}'
```

<a id="返回示例"></a>

<a id="ump0000a400"></a>

<a id="response-example-section-ump"></a>

## 返回示例

**成功示例**

<a id="code-block-3"></a>

```json
{
    "code": null,
    "message": null,
    "success": true,
    "output": null,
    "request_id": "d5f5201f-ee7a-9e3d-8569-bc0eedec21f9"
}
```

**失败示例**

<a id="code-block-4"></a>

```json
{
    "code": "InvalidParameter",
    "message": "Model qwen-xxx is not authorized for Inference",
    "success": false,
    "output": null,
    "request_id": "d5f5201f-ee7a-9e3d-8569-bc0eedec21f9"
}
```

<a id="错误码"></a>

<a id="b1c2d3e4f5a500"></a>

<a id="error-section-ump"></a>

## 错误码

如果调用失败，会返回错误信息。更多错误码及解决方法，请参见[错误信息](../preparations/error-code.md)。
