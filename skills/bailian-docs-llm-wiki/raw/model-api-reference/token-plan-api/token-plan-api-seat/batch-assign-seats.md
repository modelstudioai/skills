# 批量分配席位

批量分配席位至成员层

## 前提条件

已获取阿里云账号或 RAM 用户的 AccessKey，并已为其授予调用本接口所需的 RAM 权限。建议将 AccessKey 配置为环境变量 `ALIBABA_CLOUD_ACCESS_KEY_ID` 和 `ALIBABA_CLOUD_ACCESS_KEY_SECRET`，避免明文写入代码。

## 请求说明

-   **HTTP 方法**：POST
    
-   **请求地址**
    
    **地域**
    
    **Endpoint**
    
    华北2（北京）
    
    `POST [https://modelstudio.cn-beijing.aliyuncs.com/tokenplan/subscription/seat-assignments](https://modelstudio.cn-beijing.aliyuncs.com/tokenplan/subscription/seat-assignments)`
    
-   **认证方式**
    
    本接口是阿里云 OpenAPI，采用 AccessKey 签名（签名算法 `ACS3-HMAC-SHA256`），不支持 `Authorization: Bearer {API_KEY}` 方式。请求需携带公共请求头 `x-acs-action: BatchAssignSeats`、`x-acs-version: 2026-02-10`、`x-acs-date`、`x-acs-content-sha256`、`x-acs-signature-nonce` 以及 `Authorization`。
    
    推荐使用阿里云 SDK 或 [OpenAPI Explorer](https://api.aliyun.com/api/ModelStudio/2026-02-10/BatchAssignSeats) 发起调用，可免去自行计算签名。
    

## 请求参数

所有参数均通过 Query String 传递。数组类型参数（AccountIds）使用 Flat 格式：以 `参数名.序号` 逐个传递，序号从 1 开始，例如 `AccountIds.1=acc_123456789`、`AccountIds.2=<第二个取值>`。

**参数**

**类型**

**必选**

**描述**

SeatType

string

是

席位类型  
standard - 标准席位  
pro - 高级席位  
max - 尊享席位

AccountIds

Array

否

目标成员 id 列表

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

响应状态码。

Message

string

响应信息。

## 请求示例

本接口使用阿里云 OpenAPI 签名，下例中 `${SIGNATURE}` 需按 `ACS3-HMAC-SHA256` 算法计算得出，`x-acs-date`、`x-acs-signature-nonce` 需替换为实际值。

```
curl -X POST "https://modelstudio.cn-beijing.aliyuncs.com/tokenplan/subscription/seat-assignments?SeatType=standard&AccountIds.1=acc_123456789&Locale=zh-CN" \
    --header "x-acs-action: BatchAssignSeats" \
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
