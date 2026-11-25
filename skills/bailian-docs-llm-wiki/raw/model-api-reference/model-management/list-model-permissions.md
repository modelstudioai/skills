# 查询模型授权

调用 GET /api/v1/models/permissions 接口查询当前业务空间下可授权或已授权的模型列表及其权限明细。

<a id="前提条件"></a>

<a id="lmp0000a010"></a>

<a id="prerequisite-section-lmp"></a>

## 前提条件

已创建 API Key 并配置为环境变量 `DASHSCOPE_API_KEY`。配置方法请参见[配置API Key到环境变量](../preparations/get-api-key.md)。

<a id="请求说明"></a>

<a id="43f31e8630lzd"></a>

<a id="request-section-lmp"></a>

## 请求说明

-   **HTTP 方法**：GET
    
-   **请求地址**
    
    > 调用时请将 `{WorkspaceId}` 替换为您的业务空间 ID。
    
    | 地域 | Endpoint |
    | --- | --- |
    | 华北2（北京） | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/models/permissions` |
    
-   **认证方式**
    
    在请求 Header 中设置 `Authorization: Bearer {API_KEY}`。
    

<a id="请求参数"></a>

<a id="lmp0000a100"></a>

<a id="request-params-section-lmp"></a>

## 请求参数

所有参数均通过 Query String 传递。

<table><thead><tr><th><p><strong>参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>必选</strong></p></th><th><p><strong>描述</strong></p></th></tr></thead><tbody><tr><td><p>name</p></td><td><p>String</p></td><td><p>否</p></td><td><p>模型名称模糊搜索，对 <code>name</code> 与 <code>model_id</code> 做模糊匹配。示例：<code>qwen</code></p></td></tr><tr><td><p>model</p></td><td><p>String</p></td><td><p>否</p></td><td><p>模型 ID 精确查询，对 <code>model_id</code> 做精确匹配。示例：<code>qwen-plus</code></p></td></tr><tr><td><p>page_no</p></td><td><p>Integer</p></td><td><p>否</p></td><td><p>页码，正整数，从 1 开始。默认值：<code>1</code>。</p></td></tr><tr><td><p>page_size</p></td><td><p>Integer</p></td><td><p>否</p></td><td><p>每页数量，取值范围 1~200，最大 200。默认值：<code>20</code>。</p></td></tr><tr><td><p>authorization_scope</p></td><td><p>String</p></td><td><p>否</p></td><td><p>授权范围筛选。可选值：</p><ul><li><p><code>AUTHORIZABLE</code>：可授权的模型（默认）。</p></li><li><p><code>AUTHORIZED</code>：已授权的模型。</p></li></ul><p>默认值：<code>AUTHORIZABLE</code>。示例：<code>AUTHORIZED</code></p></td></tr><tr><td><p>action</p></td><td><p>String</p></td><td><p>否</p></td><td><p>权限动作维度。可选值：<code>INFERENCE</code>-推理（当前仅支持此值）。仅在 <code>authorization_scope=AUTHORIZED</code> 时驱动过滤维度。默认值：<code>INFERENCE</code>。</p></td></tr></tbody></table>

<a id="返回参数"></a>

<a id="lmp0000a200"></a>

<a id="response-params-section-lmp"></a>

## 返回参数

<table><thead><tr><th><p><strong>参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>描述</strong></p></th></tr></thead><tbody><tr><td><p>request_id</p></td><td><p>String</p></td><td><p>请求 ID。示例：<code>d5f5201f-ee7a-9e3d-8569-bc0eedec21f9</code></p></td></tr><tr><td><p>code</p></td><td><p>String</p></td><td><p>错误码，成功为 <code>null</code>。</p></td></tr><tr><td><p>message</p></td><td><p>String</p></td><td><p>错误信息，成功为 <code>null</code>。</p></td></tr><tr><td><p>success</p></td><td><p>Boolean</p></td><td><p>是否成功。示例：<code>true</code></p></td></tr><tr><td><p>output.total</p></td><td><p>Number</p></td><td><p>总数。示例：<code>5</code></p></td></tr><tr><td><p>output.page_no</p></td><td><p>Number</p></td><td><p>页码。示例：<code>1</code></p></td></tr><tr><td><p>output.page_size</p></td><td><p>Number</p></td><td><p>每页数量。示例：<code>20</code></p></td></tr><tr><td><p>output.permissions</p></td><td><p>Array[Object]</p></td><td><p>权限列表，见返回示例。</p></td></tr><tr><td><p>output.model</p></td><td><p>String</p></td><td><p>模型 ID。示例：<code>qwen-plus</code></p></td></tr><tr><td><p>output.name</p></td><td><p>String</p></td><td><p>模型展示名。示例：<code>通义千问-Plus</code></p></td></tr><tr><td><p>output.permissions[].permissions</p></td><td><p>Object</p></td><td><p>权限明细。示例：<code>{&quot;inference&quot;:true,&quot;fine_tune&quot;:false,&quot;deploy&quot;:false}</code>。包含以下字段：</p><ul><li><p><code>inference</code>（Boolean）：是否具备模型调用权限。示例：<code>true</code></p></li><li><p><code>fine_tune</code>（Boolean）：是否具备模型训练权限。示例：<code>false</code></p></li><li><p><code>deploy</code>（Boolean）：是否具备模型部署权限。示例：<code>false</code></p></li></ul></td></tr></tbody></table>

<a id="请求示例"></a>

<a id="lmp0000a300"></a>

<a id="example-section-lmp"></a>

## 请求示例

<a id="code-block"></a>

```bash
curl "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/models/permissions?authorization_scope=AUTHORIZED&action=INFERENCE&page_no=1&page_size=20" \
    --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    --header 'Content-Type: application/json'
```

<a id="返回示例"></a>

<a id="lmp0000a400"></a>

<a id="response-example-section-lmp"></a>

## 返回示例

<a id="code-block-2"></a>

```json
{
    "code": null,
    "message": null,
    "success": true,
    "output": {
        "total": 1,
        "page_no": 1,
        "page_size": 20,
        "permissions": [
            {
                "model": "qwen-plus",
                "name": "通义千问-Plus",
                "permissions": {
                    "inference": true,
                    "fine_tune": false,
                    "deploy": false
                }
            }
        ]
    },
    "request_id": "d5f5201f-ee7a-9e3d-8569-bc0eedec21f9"
}
```

<a id="错误码"></a>

<a id="b1c2d3e4f5a500"></a>

<a id="4b2ee74018zzf"></a>

## 错误码

如果调用失败，会返回错误信息。更多错误码及解决方法，请参见[错误信息](../preparations/error-code.md)。
