# 查询成员列表

查询组织成员列表（含席位信息），支持按名称、状态、是否分配席位过滤，支持分页。

## 前提条件

已获取阿里云账号或 RAM 用户的 AccessKey，并已为其授予调用本接口所需的 RAM 权限。建议将 AccessKey 配置为环境变量 `ALIBABA_CLOUD_ACCESS_KEY_ID` 和 `ALIBABA_CLOUD_ACCESS_KEY_SECRET`，避免明文写入代码。

## 请求说明

-   **HTTP 方法**：GET
    
-   **请求地址**
    
    **地域**
    
    **Endpoint**
    
    华北2（北京）
    
    `GET [https://modelstudio.cn-beijing.aliyuncs.com/tokenplan/organization/members](https://modelstudio.cn-beijing.aliyuncs.com/tokenplan/organization/members)`
    
-   **认证方式**
    
    本接口是阿里云 OpenAPI，采用 AccessKey 签名（签名算法 `ACS3-HMAC-SHA256`），不支持 `Authorization: Bearer {API_KEY}` 方式。请求需携带公共请求头 `x-acs-action: ListOrganizationMembers`、`x-acs-version: 2026-02-10`、`x-acs-date`、`x-acs-content-sha256`、`x-acs-signature-nonce` 以及 `Authorization`。
    
    推荐使用阿里云 SDK 或 [OpenAPI Explorer](https://api.aliyun.com/api/ModelStudio/2026-02-10/ListOrganizationMembers) 发起调用，可免去自行计算签名。
    

## 请求参数

所有参数均通过 Query String 传递。

**参数**

**类型**

**必选**

**描述**

Name

string

否

成员名称模糊过滤（匹配 accountName 或 email，忽略大小写）

Status

string

否

成员状态过滤（如 ACTIVE、FROZEN），null 表示不过滤

HasSeat

boolean

否

是否已分配席位过滤：

PageNum

integer

否

页码，从 1 开始，默认 1

PageSize

integer

否

每页条数，默认 20，最大 100

## 返回参数

**参数**

**类型**

**描述**

PageNo

integer

当前页码

PageSize

integer

每页数量

Total

integer

总记录数

Success

boolean

是否成功

Code

string

响应状态码。

Message

string

响应信息。

Data

Array\[Object\]

业务数据

Array\[Object\]

操作结果

AccountId

string

成员账号 ID

AccountName

string

成员账号名称

AccountBizId

string

成员业务 ID

Email

string

成员邮箱

OrgId

string

组织 ID

Status

string

成员状态

Roles

Array

成员角色列表

string

成员角色

GmtCreate

string

加入时间

SeatId

string

席位资源分配 ID

SpecType

string

席位规格类型  
standard - 标准席位  
pro - 高级席位  
max - 尊享席位

ApiKeyId

string

API Key ID

MaskedApiKey

string

脱敏 API Key

PackLimitInfo

object

HasShareLimit

boolean

UpperLimit

number

UsedCredits

number

AvailableLimit

number

FrozenCredits

number

IsAvailable

boolean

CycleStartTime

integer

CycleEndTime

integer

LastConfirmedTime

integer

SubscriptionInfo

object

InstanceCode

string

ProductCode

string

SpecType

string

PayMode

string

Status

string

StartTime

integer

EndTime

integer

EquityList

Array\[Object\]

object

EquityType

string

CycleStartTime

integer

CycleEndTime

integer

CycleTotalValue

number

CycleSurplusValue

number

EquityUnit

string

## 请求示例

本接口使用阿里云 OpenAPI 签名，下例中 `${SIGNATURE}` 需按 `ACS3-HMAC-SHA256` 算法计算得出，`x-acs-date`、`x-acs-signature-nonce` 需替换为实际值。示例 URL 中的中文取值为便于阅读未做编码；实际计算签名时，规范化请求（CanonicalRequest）的 Query String 需按 RFC 3986 对键和取值做百分号编码，否则会返回 `SignatureDoesNotMatch`。使用阿里云 SDK 时会自动处理。

```
curl -X GET "https://modelstudio.cn-beijing.aliyuncs.com/tokenplan/organization/members?Name=成员名称&Status=ACTIVE&HasSeat=true&PageNum=1&PageSize=20" \
    --header "x-acs-action: ListOrganizationMembers" \
    --header "x-acs-version: 2026-02-10" \
    --header "x-acs-date: 2026-01-01T12:00:00Z" \
    --header "x-acs-content-sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855" \
    --header "x-acs-signature-nonce: 3e3b2a9f0c7d4f8e9a1b2c3d4e5f6a7b" \
    --header "Authorization: ACS3-HMAC-SHA256 Credential=${ALIBABA_CLOUD_ACCESS_KEY_ID},SignedHeaders=host;x-acs-action;x-acs-content-sha256;x-acs-date;x-acs-signature-nonce;x-acs-version,Signature=${SIGNATURE}"
```

## 返回示例

```
{
  "PageNo": 18,
  "PageSize": 20,
  "Total": 1,
  "Success": true,
  "Data": [
    {
      "AccountId": "acc_123456789",
      "AccountName": "test_001",
      "AccountBizId": "112233",
      "Email": "test@email.com",
      "OrgId": "org_123456789",
      "Status": "ACTIVE",
      "Roles": [
        "ORG_MEMBER"
      ],
      "GmtCreate": "2026-06-10T11:57:42.000+00:00",
      "SeatId": "seat_123456",
      "SpecType": "standard",
      "ApiKeyId": "key_123456789",
      "MaskedApiKey": "prefix.abc****456",
      "PackLimitInfo": {
        "HasShareLimit": true,
        "UpperLimit": 0,
        "UsedCredits": 0,
        "AvailableLimit": 0,
        "FrozenCredits": 0,
        "IsAvailable": true,
        "CycleStartTime": 0,
        "CycleEndTime": 0,
        "LastConfirmedTime": 0
      },
      "SubscriptionInfo": {
        "InstanceCode": "",
        "ProductCode": "",
        "SpecType": "",
        "PayMode": "",
        "Status": "",
        "StartTime": 0,
        "EndTime": 0,
        "EquityList": [
          {
            "EquityType": "",
            "CycleStartTime": 0,
            "CycleEndTime": 0,
            "CycleTotalValue": 0,
            "CycleSurplusValue": 0,
            "EquityUnit": ""
          }
        ]
      }
    }
  ]
}
```

## 错误码

如果调用失败，会返回错误信息。更多错误码及解决方法，请参见[错误信息](raw/model-api-reference/preparations/error-code.md)。
