# 数字人wan2.2-s2v图像检测API参考

数字人wan2.2-s2v-detect 模型，用于检测输入图片是否符合 wan2.2-s2v 模型的输入规范。

**重要**本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。

## 模型与价格

**模型名称**

**计费单价**

**限流（主账号与RAM子账号共用）**

**免费额度**[（查看）](raw/model-user-guide/test-1/new-free-quota.md)

**任务下发接口RPS限制**

**同时处理中任务数量**

wan2.2-s2v-detect

0.004元/张

5

同步接口无限制

200张

-   **计费项**：无论检测是否通过，只要请求成功就计费；请求失败不计费。
    
    > 当图像因不合规而导致检测不通过时，本次API调用仍会正常计费，因为模型已经执行了完整的检测流程。
    
-   **抵扣顺序**：优先消耗免费额度。额度用尽后，默认转为按量付费。您可开启“免费额度用完即停”功能，以避免免费额度耗尽后产生额外费用。详情请参见[免费额度](raw/model-user-guide/test-1/new-free-quota.md)。
    

## HTTP调用接口

该模型用于检测输入的图片是否满足“wan2.2-s2v”所需的人物肖像图片规范。

### 前提条件

-   已开通服务并获得API-KEY：[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)。
-   配置环境变量：[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

### 图像检测接口

```
POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image2video/face-detect
```

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

#### 入参描述

**字段**

**类型**

**传参方式**

**必选**

**描述**

**示例值**

Content-Type

String

Header

是

请求类型：application/json。

application/json

Authorization

String

Header

是

API-Key，格式为 Bearer sk-xxx。

Bearer sk-1a\*\*2b

model

String

Body

是

指定调用的模型名称。

wan2.2-s2v-detect

input.image\_url

String

Body

是

待检测的图像 URL。

-   图像格式：支持jpg，jpeg，png，bmp，webp。
    
-   图像分辨率：图像的宽度和高度范围为\[400, 7000\]像素。
    
-   上传图片仅支持公网可访问的 HTTP/HTTPS 链接。本地文件可通过[上传文件获取临时URL](raw/model-api-reference/more-about-models/get-temporary-file-url.md)。
    

http://aaa/bbb.jpg

#### 出参描述

**字段**

**类型**

**描述**

**示例值**

output.check\_pass

Bool

检测结果。true 表示通过，false 表示不通过。

true

output.humanoid

Bool

是否检测到人像：true 表示是，false 表示否。

true

usage.image\_count

Integer

本次请求检测图像数量，固定为 1 张，用于计费。无论检测是否通过，只要请求成功就计费；请求失败不计费。

> 当图像因不合规而导致检测不通过时，本次API调用仍会正常计费，因为模型已经执行了完整的检测流程。

1

request\_id

String

本次请求的唯一ID。

7574ee8f-38a3-4b1e-9280-11c33ab46e51

#### 请求示例

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

```
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

#### 响应示例（通过）

```
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

#### 响应示例（不通过）

```
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

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](raw/model-api-reference/preparations/error-code.md)进行解决。
