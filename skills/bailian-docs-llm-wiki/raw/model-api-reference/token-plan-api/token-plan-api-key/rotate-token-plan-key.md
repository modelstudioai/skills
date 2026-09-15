# 重置 API Key

重置 UAC API Key

## 前提条件

已获取阿里云账号或 RAM 用户的 AccessKey，并已为其授予调用本接口所需的 RAM 权限。建议将 AccessKey 配置为环境变量 `ALIBABA_CLOUD_ACCESS_KEY_ID` 和 `ALIBABA_CLOUD_ACCESS_KEY_SECRET`，避免明文写入代码。

## 请求说明

-   **HTTP 方法**：POST
    
-   **请求地址**
    
    **地域**
    
    **Endpoint**
    
    华北2（北京）
    
    `POST [https://modelstudio.cn-beijing.aliyuncs.com/tokenplan/api-key-rotations](https://modelstudio.cn-beijing.aliyuncs.com/tokenplan/api-key-rotations)`
    
-   **认证方式**
    
    本接口是阿里云 OpenAPI，采用 AccessKey 签名（签名算法 `ACS3-HMAC-SHA256`），不支持 `Authorization: Bearer {API_KEY}` 方式。请求需携带公共请求头 `x-acs-action: RotateTokenPlanKey`、`x-acs-version: 2026-02-10`、`x-acs-date`、`x-acs-content-sha256`、`x-acs-signature-nonce` 以及 `Authorization`。
    
    推荐使用阿里云 SDK 或 [OpenAPI Explorer](https://api.aliyun.com/api/ModelStudio/2026-02-10/RotateTokenPlanKey) 发起调用，可免去自行计算签名。
    

仅 API Key 变化，API Key ID 不变。

## 请求参数

所有参数均通过 Query String 传递。

**参数**

**类型**

**必选**

**描述**

ApiKeyId

string

是

API Key ID

## 返回参数

**参数**

**类型**

**描述**

Success

boolean

调用接口是否成功：  
true：成功  
false：失败

Code

string

响应状态码。

Message

string

响应信息。

Data

object

业务数据

ApiKeyId

string

API Key ID（系统生成）

SourceId

string

BaiLian 返回的 source\_id

PlainApiKey

string

BaiLian 返回的新明文 API Key（只在重置时返回一次）

MaskedApiKey

string

BaiLian 返回的新 masked\_api\_key（如 sk\_\*\*\*cdef）

ResetAt

string

重置时间

## 请求示例

本接口使用阿里云 OpenAPI 签名，下例中 `${SIGNATURE}` 需按 `ACS3-HMAC-SHA256` 算法计算得出，`x-acs-date`、`x-acs-signature-nonce` 需替换为实际值。

```
curl -X POST "https://modelstudio.cn-beijing.aliyuncs.com/tokenplan/api-key-rotations?ApiKeyId=ak_123456" \
    --header "x-acs-action: RotateTokenPlanKey" \
    --header "x-acs-version: 2026-02-10" \
    --header "x-acs-date: 2026-01-01T12:00:00Z" \
    --header "x-acs-content-sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855" \
    --header "x-acs-signature-nonce: 3e3b2a9f0c7d4f8e9a1b2c3d4e5f6a7b" \
    --header "Authorization: ACS3-HMAC-SHA256 Credential=${ALIBABA_CLOUD_ACCESS_KEY_ID},SignedHeaders=host;x-acs-action;x-acs-content-sha256;x-acs-date;x-acs-signature-nonce;x-acs-version,Signature=${SIGNATURE}"
```

## 返回示例

```
{
  "Success": true,
  "Data": {
    "ApiKeyId": "ak_123456",
    "SourceId": "123456",
    "PlainApiKey": "sk-ws.abc123456",
    "MaskedApiKey": "sk_***6",
    "ResetAt": "2025-07-18T03:19:17Z"
  }
}
```

## 错误码

如果调用失败，会返回错误信息。更多错误码及解决方法，请参见[错误信息](raw/model-api-reference/preparations/error-code.md)。
