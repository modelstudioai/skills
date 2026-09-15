# 批量回收席位

批量回收成员层席位

## 前提条件

已获取阿里云账号或 RAM 用户的 AccessKey，并已为其授予调用本接口所需的 RAM 权限。建议将 AccessKey 配置为环境变量 `ALIBABA_CLOUD_ACCESS_KEY_ID` 和 `ALIBABA_CLOUD_ACCESS_KEY_SECRET`，避免明文写入代码。

## 请求说明

-   **HTTP 方法**：POST
    
-   **请求地址**
    
    **地域**
    
    **Endpoint**
    
    华北2（北京）
    
    `POST [https://modelstudio.cn-beijing.aliyuncs.com/tokenplan/subscription/seat-revocations](https://modelstudio.cn-beijing.aliyuncs.com/tokenplan/subscription/seat-revocations)`
    
-   **认证方式**
    
    本接口是阿里云 OpenAPI，采用 AccessKey 签名（签名算法 `ACS3-HMAC-SHA256`），不支持 `Authorization: Bearer {API_KEY}` 方式。请求需携带公共请求头 `x-acs-action: BatchRevokeSeats`、`x-acs-version: 2026-02-10`、`x-acs-date`、`x-acs-content-sha256`、`x-acs-signature-nonce` 以及 `Authorization`。
    
    推荐使用阿里云 SDK 或 [OpenAPI Explorer](https://api.aliyun.com/api/ModelStudio/2026-02-10/BatchRevokeSeats) 发起调用，可免去自行计算签名。
    

## 请求参数

所有参数均通过 Query String 传递。数组类型参数 Items 的取值是一个 JSON 字符串，例如 `Items=[{"AccountId": "acc_123456789"}]`，实际发起请求时需对该取值做 URL 编码。

**参数**

**类型**

**必选**

**描述**

Items

Array\[Object\]

否

回收项列表，不可为空

Items\[\].AccountId

string

否

当前绑定的成员 ID

Locale

string

否

多语言信息 zh-CN/en-US

## 返回参数

**参数**

**类型**

**描述**

Success

boolean

是否成功

Code

string

错误码（成功时为空）

Message

string

错误信息（成功时为空）

## 请求示例

本接口使用阿里云 OpenAPI 签名，下例中 `${SIGNATURE}` 需按 `ACS3-HMAC-SHA256` 算法计算得出，`x-acs-date`、`x-acs-signature-nonce` 需替换为实际值。

```
curl -X POST "https://modelstudio.cn-beijing.aliyuncs.com/tokenplan/subscription/seat-revocations?Items=%5B%7B%22AccountId%22%3A%22acc_123456789%22%7D%5D&Locale=zh-CN" \
    --header "x-acs-action: BatchRevokeSeats" \
    --header "x-acs-version: 2026-02-10" \
    --header "x-acs-date: 2026-01-01T12:00:00Z" \
    --header "x-acs-content-sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855" \
    --header "x-acs-signature-nonce: 3e3b2a9f0c7d4f8e9a1b2c3d4e5f6a7b" \
    --header "Authorization: ACS3-HMAC-SHA256 Credential=${ALIBABA_CLOUD_ACCESS_KEY_ID},SignedHeaders=host;x-acs-action;x-acs-content-sha256;x-acs-date;x-acs-signature-nonce;x-acs-version,Signature=${SIGNATURE}"
```

## 返回示例

```
{
  "Success": true
}
```

## 错误码

如果调用失败，会返回错误信息。更多错误码及解决方法，请参见[错误信息](raw/model-api-reference/preparations/error-code.md)。
