# 生成临时API Key

在浏览器、移动 App 等不可信环境中调用模型服务时，通过安全的后端服务生成临时API Key，避免永久API Key 泄露。

> **重要**
>
> 临时API Key 继承生成它的API Key 所拥有的全部权限，包括对特定模型或知识库的访问限制。

<a id="前提条件"></a>

<a id="prerequisite-title"></a>

## 前提条件

在[密钥管理（北京）](https://bailian.console.aliyun.com/?tab=model#/api-key)、[密钥管理（新加坡）](https://bailian.console.aliyun.com/?tab=model#/api-key)或[密钥管理（弗吉尼亚）](https://bailian.console.aliyun.com/us-east-1?tab=model#/api-key)或[密钥管理（中国香港）](https://bailian.console.aliyun.com/cn-hongkong?tab=globalset#/efm/api_key)页面创建永久API Key，并将其配置为环境变量 `DASHSCOPE_API_KEY`。配置方法请参见[配置API Key 到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

<a id="请求示例"></a>

<a id="a983ecd685kjl"></a>

## 请求示例

临时API Key 默认有效期为 60 秒，支持通过 `expire_in_seconds` 参数设置有效期（TTL），范围为 \[1, 1800\] 秒。

<a id="code-block"></a>

```bash
curl -X POST "https://dashscope.aliyuncs.com/api/v1/tokens?expire_in_seconds=1800" \
-H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

> 各地域的API Key 不同。

> 以下示例使用新加坡地域的 Endpoint。如需使用北京地域，请将URL替换为：[https://dashscope.aliyuncs.com/api/v1/tokens?expire\_in\_seconds=1800](https://dashscope.aliyuncs.com/api/v1/tokens?expire_in_seconds=1800)

<a id="响应示例"></a>

<a id="a8b797d312yzo"></a>

## 响应示例

<a id="sec-tabs"></a>

<a id="正常响应示例"></a>

<a id="正常响应示例-h4"></a>

#### 正常响应示例

<a id="code-block-2"></a>

```json
{
    "token":"st-****",
    "expires_at":1744080369
}
```

<a id="6995707ed2t3w"></a>

### 响应参数

| 参数名称 | 参数类型 | 说明 | 示例 |
| --- | --- | --- | --- |
| token | String | 生成的临时API Key。 | st-\*\*\*\* |
| expires\_at | Number | 过期时间，UNIX 时间戳，单位为秒。 | 1744080369 |

<a id="错误响应示例"></a>

<a id="错误响应示例-h4"></a>

#### 错误响应示例

<a id="code-block-3"></a>

```json
{
    "code":"InvalidApiKey",
    "message":"Invalid API-key provided.",
    "request_id":"902fee3b-f7f0-9a8c-96a1-6b4ea25af114"
}
```

<a id="cd5ad1efc01q6"></a>

### 响应参数

| 参数名称 | 参数类型 | 说明 | 示例 |
| --- | --- | --- | --- |
| code | String | 错误码。更多错误原因及解决方法，请前往[错误码](../../model-api-reference/preparations/error-code.md)页面查询。 | InvalidApiKey：无效API Key |
| message | String | 错误信息。 | Invalid API-key provided. |
| request\_id | String | 请求 ID。 | 902fee3b-f7f0-9a8c-96a1-6b4ea25af114 |

<a id="常见问题"></a>

## 常见问题

**问：能否手动删除已创建的临时API Key？**

答：不能。临时API Key 具有固定的生命周期，到期后自动失效，无法提前删除。
