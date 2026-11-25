# 获取RSA的公钥

本接口用于获取公钥ID及其对应的值。

<a id="http接口调用"></a>

<a id="c3c19f7915c03"></a>

## HTTP接口调用

<a id="功能描述"></a>

<a id="05a51ae3d7inv"></a>

### 功能描述

在对input字段值加密前，需要通过此接口获取当前支持的最新公钥ID及其对应的值。

<a id="前提条件"></a>

<a id="158f5c6f7606t"></a>

### 前提条件

-   已开通百炼服务并获得API-KEY：[获取与配置 API Key](../../../model-api-reference/preparations/get-api-key.md)。
-   我们推荐您将API-KEY配置到环境变量中以降低API-KEY的泄漏风险，配置方法可参考[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。您也可以在代码中配置API-KEY，但是泄漏风险会提高。

<a id="接口调用"></a>

<a id="7124e5bb0d2in"></a>

### 接口调用

<a id="code-block"></a>

```json
GET /api/v1/public-keys/latest
```

<a id="入参描述"></a>

<a id="e710c0309dh68"></a>

### 入参描述

| 传参方式 | 字段 | 数据类型 | 必选 | 描述 | 示例值 |
| --- | --- | --- | --- | --- | --- |
| Header | Authorization | String | 是 | 鉴权使用的API-KEY。 | "Authorization":"Bearer d1\*\*2a" |

<a id="出参描述"></a>

<a id="3f76fb5305uer"></a>

### 出参描述

| 字段 | 数据类型 | 必选 | 描述 |
| --- | --- | --- | --- |
| request\_id | String | 是 | 请求ID |
| public\_key | String | 否 | RSA公钥的值 |
| public\_key\_id | String | 否 | RSA公钥的ID |

<a id="异常返回参数描述"></a>

<a id="9960fa9433xqn"></a>

### 异常返回参数描述

<table><thead><tr><th><p><strong>名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>必填</strong></p></th><th><p>描述</p></th></tr></thead><tbody><tr><td><p>request_id</p></td><td><p>String</p></td><td><p>是</p></td><td><p>请求ID</p></td></tr><tr><td><p>code</p></td><td><p>String</p></td><td><p>否</p></td><td rowspan="2"><p>错误码及错误信息，请参见<a href="../../../model-api-reference/preparations/error-code.md">错误码</a></p></td></tr><tr><td><p>message</p></td><td><p>String</p></td><td><p>否</p></td></tr></tbody></table>

<a id="请求示例"></a>

<a id="7a9f7cbedaj7e"></a>

### 请求示例

<a id="sec-tabs"></a>

<a id="curl"></a>

<a id="curl-h4"></a>

#### curl

<a id="code-block-2"></a>

```bash
curl -X GET 'https://dashscope.aliyuncs.com/api/v1/public-keys/latest' \
--header 'Authorization: Bearer xxx'
```

<a id="python-sdk"></a>

<a id="python-sdk-h4"></a>

#### Python SDK

使用 DashScope SDK 时无需手动调用本接口获取公钥。在调用模型时设置 `enable_encryption=True`，SDK 会自动获取最新的 RSA 公钥、生成 AES 密钥并对 input 加密，您无需关心公钥获取与加解密细节。

<a id="code-block-3"></a>

```python
import os
from dashscope import Generation

resp = Generation.call(
    model='qwen-plus',
    messages=[{'role': 'user', 'content': '你好'}],
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    enable_encryption=True,
)
print(resp)
```

<a id="正常响应示例"></a>

<a id="82de5cedafu9u"></a>

### 正常响应示例

<a id="code-block-4"></a>

```json
{
    "request_id": "bcb3***",
    "data": {
        "public_key": "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnojrB579xgPQN5f46SvoRAiQBPWBaPzWh7hp51fWI+OsQk7KqH0qMcw8i0eK5rfOvJIPujOQgnes1ph9/gKAst9NzXVIl9JJYUSPtzTvOabhp4yvS3KBf9g3xHYVjYgW33SOY74Ue/tgbCXn717rV6gXb4sVvq9XK/1BrDcGbEOQEZEgBTFkm/g3lpWLQtACwwqHffoA9eQtkkz15ZFKosAgbR8LedfIvxAl2zk15REzxXiRcFgc9/tLF0U1t2Sxt9FkQefxYwn6EZawTsRJvf4kqF3MaPdTcDbOp0iSNvCl2qzPSf/F+Oll2CUM1tFAEu81oa4l0WaDR3UtvqOtyQIDAQAB",
        "public_key_id": "1"
    }
}
```

<a id="异常响应示例"></a>

<a id="07a77cc3a9loh"></a>

### 异常响应示例

<a id="code-block-5"></a>

```json
{
    "request_id": "bcb3***",
    "code": "InvalidParameter",
    "message": "Required parameter(s) missing or invalid, please check the request parameters."
}
```

<a id="错误码"></a>

<a id="6e69a84f09oxc"></a>

## 错误码

更多错误码详情，请参见[错误码](../../../model-api-reference/preparations/error-code.md)。
