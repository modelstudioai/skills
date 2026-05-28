# 生成临时 API Key

当应用需要在浏览器、移动 App 等不可信环境中调用模型服务时，为避免永久 API Key 泄露，应通过安全的后端服务来提供临时 API Key。

**重要**

临时 API Key 将继承生成它的 API Key 所拥有的权限。（例如：限制访问特定模型、知识库）

## **前提条件**

需要先在[密钥管理（北京）](https://bailian.console.aliyun.com/?tab=model#/api-key)或[密钥管理（新加坡）](https://modelstudio.console.aliyun.com/?tab=model#/api-key)或[密钥管理（弗吉尼亚）](https://modelstudio.console.aliyun.com/us-east-1?tab=model#/api-key)页面创建永久有效的 API-Key，并将其设置为环境变量 `DASHSCOPE_API_KEY`。配置方法请参见[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

## **请求示例**

临时 API Key 默认有效期为60秒，支持设置超时时间范围为\[1, 1800\]秒。

```
curl -X POST "https://dashscope.aliyuncs.com/api/v1/tokens?expire_in_seconds=1800" \
-H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

## **响应示例**

### **正常响应示例**

```
{  
    "token":"st-****",
    "expires_at":1744080369
}
```

### 响应参数

**参数名称**

**参数类型**

**说明**

**示例**

token

String

生成的临时 API Key。

st-\*\*\*\*

expires\_at

Number

过期时间，时间戳（Unix Timestamp），单位为秒。

1744080369

### **错误响应示例**

```
{  
    "code":"InvalidApiKey",
    "message":"Invalid API-key provided.",
    "request_id":"902fee3b-f7f0-9a8c-96a1-6b4ea25af114"
}
```

### 响应参数

**参数名称**

**参数类型**

**说明**

**示例**

code

String

错误码。

请前往[错误信息](https://help.aliyun.com/zh/model-studio/error-code)页面查询更多的原因和解决方法。

InvalidApiKey：无效API-Key错误码

message

String

错误消息。

Invalid API-key provided.

request\_id

String

请求ID。

902fee3b-f7f0-9a8c-96a1-6b4ea25af114

## **常见问题**

**问：我能手动删除一个已经创建的临时 API Key 吗？**

答：不能。临时 API Key 有固定的生命周期，到期后会自动失效。
