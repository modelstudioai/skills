# 获取RSA的公钥

本接口用于获取公钥ID及其对应的值。

## HTTP接口调用

### **功能描述**

在对input字段值加密前，需要通过此接口获取当前支持的最新公钥ID及其对应的值。

### **前提条件**

-   已开通百炼服务并获得API-KEY：[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。
    
-   我们推荐您将API-KEY配置到环境变量中以降低API-KEY的泄漏风险，配置方法可参考[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。您也可以在代码中配置API-KEY，但是泄漏风险会提高。
    

### **接口调用**

```
GET /api/v1/public-keys/latest
```

### **入参描述**

**传参方式**

**字段**

**数据类型**

**必选**

**描述**

**示例值**

Header

Authorization

String

是

鉴权使用的API-KEY。

"Authorization":"Bearer d1\*\*2a"

### **出参描述**

**字段**

**数据类型**

**必选**

**描述**

request\_id

String

是

请求ID

public\_key

String

否

RSA公钥的值

public\_key\_id

String

否

RSA公钥的ID

### **异常返回参数描述**

**名称**

**类型**

**必填**

描述

request\_id

String

是

请求ID

code

String

否

错误码及错误信息，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)

message

String

否

### **请求示例**

```
curl -X GET 'https://dashscope.aliyuncs.com/api/v1/public-keys/latest' \
--header 'Authorization: Bearer xxx'
```

### **正常响应示例**

```
{
    "request_id": "bcb3***",
    "data": {
        "public_key": "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnojrB579xgPQN5f46SvoRAiQBPWBaPzWh7hp51fWI+OsQk7KqH0qMcw8i0eK5rfOvJIPujOQgnes1ph9/gKAst9NzXVIl9JJYUSPtzTvOabhp4yvS3KBf9g3xHYVjYgW33SOY74Ue/tgbCXn717rV6gXb4sVvq9XK/1BrDcGbEOQEZEgBTFkm/g3lpWLQtACwwqHffoA9eQtkkz15ZFKosAgbR8LedfIvxAl2zk15REzxXiRcFgc9/tLF0U1t2Sxt9FkQefxYwn6EZawTsRJvf4kqF3MaPdTcDbOp0iSNvCl2qzPSf/F+Oll2CUM1tFAEu81oa4l0WaDR3UtvqOtyQIDAQAB",
        "public_key_id": "1"
    }
}
```

### **异常响应示例**

```
{
    "request_id": "bcb3***",
    "code": "InvalidParameter",
    "message": "Required parameter(s) missing or invalid, please check the request parameters."
}
```

## **错误码**

更多错误码详情，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。
