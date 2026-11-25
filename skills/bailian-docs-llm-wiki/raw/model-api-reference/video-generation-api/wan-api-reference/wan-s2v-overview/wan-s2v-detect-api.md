# 数字人wan2.2-s2v图像检测API参考

数字人wan2.2-s2v-detect 模型，用于检测输入图片是否符合 wan2.2-s2v 模型的输入规范。

> **重要**
>
> 本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。

<a id="http调用接口"></a>

<a id="2f67df3cf92ii"></a>

## HTTP调用接口

该模型用于检测输入的图片是否满足“wan2.2-s2v”所需的人物肖像图片规范。

<a id="前提条件"></a>

<a id="4325f8ce6amyc"></a>

### 前提条件

-   已开通服务并获得API-KEY：[获取与配置 API Key](../../../preparations/get-api-key.md)。
-   配置环境变量：[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

<a id="图像检测接口"></a>

<a id="31d1727a4ejzu"></a>

### 图像检测接口

<a id="code-block"></a>

```http
POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image2video/face-detect
```

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="入参描述"></a>

<a id="9ee77439ecy5y"></a>

#### 入参描述

<table><thead><tr><th><p><strong>字段</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>传参方式</strong></p></th><th><p><strong>必选</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td><p>Content-Type</p></td><td><p>String</p></td><td><p>Header</p></td><td><p>是</p></td><td><p>请求类型：application/json。</p></td><td><p>application/json</p></td></tr><tr><td><p>Authorization</p></td><td><p>String</p></td><td><p>Header</p></td><td><p>是</p></td><td><p>API-Key，格式为 Bearer sk-xxx。</p></td><td><p>Bearer sk-1a**2b</p></td></tr><tr><td><p>model</p></td><td><p>String</p></td><td><p>Body</p></td><td><p>是</p></td><td><p>指定调用的模型名称。</p></td><td><p>wan2.2-s2v-detect</p></td></tr><tr><td><p>input.image_url</p></td><td><p>String</p></td><td><p>Body</p></td><td><p>是</p></td><td><p>待检测的图像 URL。</p><ul><li><p>图像格式：支持jpg，jpeg，png，bmp，webp。</p></li><li><p>图像分辨率：图像的宽度和高度范围为[400, 7000]像素。</p></li><li><p>上传图片仅支持公网可访问的 HTTP/HTTPS 链接。本地文件可通过<a href="../../../more-about-models/get-temporary-file-url.md">上传文件获取临时URL</a>。</p></li></ul></td><td><p>http://aaa/bbb.jpg</p></td></tr></tbody></table>

<a id="出参描述"></a>

<a id="5cb0f3560c2xb"></a>

#### 出参描述

<table><thead><tr><th><strong>字段</strong></th><th><strong>类型</strong></th><th><strong>描述</strong></th><th><strong>示例值</strong></th></tr></thead><tbody><tr><td><p>output.check_pass</p></td><td><p>Bool</p></td><td><p>检测结果。true 表示通过，false 表示不通过。</p></td><td><p>true</p></td></tr><tr><td><p>output.humanoid</p></td><td><p>Bool</p></td><td><p>是否检测到人像：true 表示是，false 表示否。</p></td><td><p>true</p></td></tr><tr><td><p>usage.image_count</p></td><td><p>Integer</p></td><td><p>本次请求检测图像数量，固定为 1 张，用于计费。无论检测是否通过，只要请求成功就计费；请求失败不计费。</p><blockquote><p>当图像因不合规而导致检测不通过时，本次API调用仍会正常计费，因为模型已经执行了完整的检测流程。</p></blockquote></td><td><p>1</p></td></tr><tr><td><p>request_id</p></td><td><p>String</p></td><td><p>本次请求的唯一ID。</p></td><td><p>7574ee8f-38a3-4b1e-9280-11c33ab46e51</p></td></tr></tbody></table>

<a id="请求示例"></a>

<a id="a4441af7ade5m"></a>

#### 请求示例

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="code-block-2"></a>

```bash
curl 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image2video/face-detect' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data-raw '{
    "model": "wan2.2-s2v-detect",
    "input": {
        "image_url": "https://img.alicdn.com/imgextra/i3/O1CN011FObkp1T7Ttowoq4F_!!6000000002335-0-tps-1440-1797.jpg"
        }
    }'
```

<a id="响应示例-通过"></a>

<a id="c1a5d31e34jqm"></a>

#### 响应示例（通过）

<a id="code-block-3"></a>

```json
{
    "output":{
        "check_pass": true,
        "humanoid": true
    },
    "usage":{
        "image_count":1
    },
    "request_id":"c56f62df-724e-9c19-96bd-xxxxxx"
}
```

<a id="响应示例-不通过"></a>

<a id="800bb54a9folx"></a>

#### 响应示例（不通过）

<a id="code-block-4"></a>

```json
{
    "output":{
        "check_pass": false,
        "code": "",
        "message": ""
    },
    "usage":{
        "image_count":1
    },
    "request_id":"c56f62df-724e-9c19-96bd-xxxxxx"
}
```

<a id="错误码"></a>

<a id="0d0a562d05nkh"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](../../../preparations/error-code.md)进行解决。
