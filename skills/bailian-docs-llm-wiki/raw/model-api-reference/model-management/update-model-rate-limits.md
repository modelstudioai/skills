# 更新模型限流

调用 POST /api/v1/models/limits 接口更新指定业务空间下模型的限流配额（QPM / TPM），支持"合并覆盖"与"删除限流"两种操作。

<a id="前提条件"></a>

<a id="uml0000a010"></a>

<a id="prerequisite-section-uml"></a>

## 前提条件

已创建 API Key 并配置为环境变量 `DASHSCOPE_API_KEY`。配置方法请参见[配置API Key到环境变量](../preparations/get-api-key.md)。

<a id="请求说明"></a>

<a id="43f31e8630lzd"></a>

<a id="request-section-uml"></a>

## 请求说明

-   **HTTP 方法**：POST
    
-   **请求地址**
    
    > 调用时请将 `{WorkspaceId}` 替换为您的业务空间 ID。
    
    | 地域 | Endpoint |
    | --- | --- |
    | 华北2（北京） | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/models/limits` |
    
-   **认证方式**
    
    在请求 Header 中设置 `Authorization: Bearer {API_KEY}`。
    

<a id="请求参数"></a>

<a id="uml0000a100"></a>

<a id="request-params-section-uml"></a>

## 请求参数

所有参数均通过请求 Body 传递。

<table><thead><tr><th><p><strong>参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>必选</strong></p></th><th><p><strong>描述</strong></p></th></tr></thead><tbody><tr><td><p>models</p></td><td><p>Array[Object]</p></td><td><p>是</p></td><td><p>逐模型限流项列表。必填，数量需为 1~200。示例：<code>[{&quot;model&quot;:&quot;qwen-plus&quot;,&quot;request_limit&quot;:60}]</code></p></td></tr><tr><td><p>models[].model</p></td><td><p>String</p></td><td><p>是</p></td><td><p>模型 ID，不能为空。如 <code>qwen-plus</code>、<code>qwen3.7-plus</code>。</p></td></tr><tr><td><p>models[].operation_type</p></td><td><p>String</p></td><td><p>否</p></td><td><p>操作类型。可选值：</p><ul><li><p><code>OVERLAY</code>：合并覆盖（只覆盖传入字段，未传字段回填当前值）。</p></li><li><p><code>DELETE</code>：删除限流（此时限流值字段需全部为空）。</p></li></ul><p>默认值：<code>OVERLAY</code>。</p></td></tr><tr><td><p>models[].request_limit</p></td><td><p>Number</p></td><td><p>否</p></td><td><p>请求次数上限（QPM），非负。每分钟最大请求数，单位次/分钟。<code>operation_type=DELETE</code> 时必须为空。默认值：null（不变更）。示例：<code>60</code></p></td></tr><tr><td><p>models[].request_limit_period</p></td><td><p>Number</p></td><td><p>否</p></td><td><p>请求限流时间周期，正整数，单位秒，如 <code>60</code>=1 分钟。默认值：null（不变更）。</p></td></tr><tr><td><p>models[].usage_limit</p></td><td><p>Number</p></td><td><p>否</p></td><td><p>用量上限（TPM），非负。每分钟最大 Token 用量。<code>operation_type=DELETE</code> 时必须为空。默认值：null（不变更）。示例：<code>100000</code></p></td></tr><tr><td><p>models[].usage_limit_period</p></td><td><p>Number</p></td><td><p>否</p></td><td><p>用量限流时间周期，正整数，单位秒，如 <code>60</code>=1 分钟。默认值：null（不变更）。</p></td></tr></tbody></table>

<a id="返回参数"></a>

<a id="uml0000a200"></a>

<a id="response-params-section-uml"></a>

## 返回参数

| 参数 | 类型 | 描述 |
| --- | --- | --- |
| request\_id | String | 请求 ID。示例：`d5f5201f-ee7a-9e3d-8569-bc0eedec21f9` |
| code | String | 错误码，成功为 `null`。 |
| message | String | 错误信息，成功为 `null`。 |
| success | Boolean | 是否成功。示例：`true` |
| output | Object | 业务数据，本接口为 `null`。 |

<a id="tpm-豁免场景"></a>

<a id="uml0000a600"></a>

<a id="tpm-exempt-section-uml"></a>

## TPM 豁免场景

若需"只限制 RPM、豁免 TPM"，推荐两步法——先调用本接口对目标模型传 `{"model":"X","operation_type":"DELETE"}` 删除全部限流，再传 `{"model":"X","operation_type":"OVERLAY","request_limit":60,"request_limit_period":60}` 只设置 QPM。两步非原子，中间有短暂无限制窗口。

<a id="请求示例"></a>

<a id="uml0000a300"></a>

<a id="example-section-uml"></a>

## 请求示例

**示例一：设置 QPM=60、TPM=100000**

<a id="code-block"></a>

```bash
curl -X POST "https://dashscope.aliyuncs.com/api/v1/models/limits" \
    --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    --header 'Content-Type: application/json' \
    --data '{
        "models": [
            {
                "model": "qwen-plus",
                "operation_type": "OVERLAY",
                "request_limit": 60,
                "request_limit_period": 60,
                "usage_limit": 100000,
                "usage_limit_period": 60
            }
        ]
    }'
```

**示例二：删除限流**

<a id="code-block-2"></a>

```bash
curl -X POST "https://dashscope.aliyuncs.com/api/v1/models/limits" \
    --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    --header 'Content-Type: application/json' \
    --data '{
        "models": [
            {"model": "qwen-plus", "operation_type": "DELETE"}
        ]
    }'
```

<a id="返回示例"></a>

<a id="uml0000a400"></a>

<a id="response-example-section-uml"></a>

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
    "message": "Cannot set TPM without QPM for model qwen-plus: no existing QPM limit, please set QPM first",
    "success": false,
    "output": null,
    "request_id": "d5f5201f-ee7a-9e3d-8569-bc0eedec21f9"
}
```

<a id="错误码"></a>

<a id="b1c2d3e4f5a500"></a>

<a id="error-section-uml"></a>

## 错误码

如果调用失败，会返回错误信息。更多错误码及解决方法，请参见[错误信息](../preparations/error-code.md)。
