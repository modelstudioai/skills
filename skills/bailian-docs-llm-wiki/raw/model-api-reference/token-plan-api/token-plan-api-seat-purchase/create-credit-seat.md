# 创建席位（新购）

创建一个或多个 Token Plan 团队版席位。

## 前提条件

已获取阿里云账号或 RAM 用户的 AccessKey，并已为其授予调用 BssOpenApi 所需的 RAM 权限。建议将 AccessKey 配置为环境变量 `ALIBABA_CLOUD_ACCESS_KEY_ID` 和 `ALIBABA_CLOUD_ACCESS_KEY_SECRET`，避免明文写入代码。

已通过 `QueryProductList` 获取 `ProductCode`、`ProductType` 和 `SubscriptionType`。Token Plan 团队版的示例取值为 `sfm`、`sfm_tokenplanteams_dp_cn` 和 `Subscription`。

## 请求说明

-   **HTTP 方法**：POST
    
-   **请求地址**
    
    **地域**
    
    **Endpoint**
    
    中国站
    
    `POST [https://business.aliyuncs.com/](https://business.aliyuncs.com/)`
    
-   **认证方式**
    
    本接口属于 BssOpenApi（版本 `2023-09-30`），采用 AccessKey 签名（RPC 签名，`HMAC-SHA1`），不支持 `Authorization: Bearer {API_KEY}` 方式。
    
    推荐使用阿里云 SDK 的 `CommonRequest` 发起调用，SDK 会自动生成公共参数并计算签名。
    

## 请求参数

全部参数通过表单或 Query String 传递。数组参数使用 Flat 格式：`SubscriptionConfigs.1.Seats`、`SubscriptionConfigs.1.Configs.1.Code`，序号从 1 开始。

**参数**

**类型**

**必选**

**描述**

ProductCode

string

是

产品代码。通过 `QueryProductList` 获取，例如 `sfm`。

ProductType

string

是

产品类型。通过 `QueryProductList` 获取，例如 `sfm_tokenplanteams_dp_cn`。

SubscriptionType

string

是

订阅类型。通过 `QueryProductList` 获取，例如 `Subscription`。

ClientToken

string

是

幂等性令牌。由客户端生成，需保证不同请求间唯一，最大 64 个 ASCII 字符。

Period

integer

是

付费周期数，至少为 1。

PeriodUnit

string

是

付费周期单位。取值：  
`Year`：年  
`Month`：月

AutoRenew

boolean

否

是否开启自动续费。

SubscriptionConfigs

Array

是

订阅规格列表，支持一次创建多种规格。

SubscriptionConfigs.N.Seats

long

是

席位数量，至少为 1。

SubscriptionConfigs.N.Configs

Array

是

模块属性列表。

SubscriptionConfigs.N.Configs.N.Code

string

否

模块属性 code，例如 `plan_type`。

SubscriptionConfigs.N.Configs.N.Value

string

否

模块属性 value，例如 `standard`、`pro`、`max`。

**说明**`Configs` 中的 `Code` 和 `Value` 需成对填写，取值以商品支持的属性为准。

## 返回参数

**参数**

**类型**

**描述**

RequestId

string

请求 ID。

Success

boolean

是否成功。

Code

string

结果码，成功为 `Success`。

Message

string

结果描述。

Data

object

业务数据。

Data.OrderId

long

订单 ID。

Data.InstanceId

Array\[string\]

实例 ID 列表。

Data.HostId

string

站点标识。中国站返回 `cn`；部分响应可能不返回该字段。

AccessDeniedDetail

string

RAM 权限被拒绝时的详细错误信息。

## 请求示例

本接口使用 BssOpenApi 的 RPC 签名。下例中 `${SIGNATURE}` 需按签名算法计算，`SignatureNonce` 和 `Timestamp` 需替换为实际值。使用阿里云 SDK 时会自动处理公共参数和签名。

```
curl -X POST "https://business.aliyuncs.com/" \
    --data-urlencode "Action=CreateCreditSeat" \
    --data-urlencode "Version=2023-09-30" \
    --data-urlencode "Format=JSON" \
    --data-urlencode "AccessKeyId=${ALIBABA_CLOUD_ACCESS_KEY_ID}" \
    --data-urlencode "SignatureMethod=HMAC-SHA1" \
    --data-urlencode "SignatureVersion=1.0" \
    --data-urlencode "SignatureNonce=${SIGNATURE_NONCE}" \
    --data-urlencode "Timestamp=2026-01-01T12:00:00Z" \
    --data-urlencode "Signature=${SIGNATURE}" \
    --data-urlencode "ProductCode=sfm" \
    --data-urlencode "ProductType=sfm_tokenplanteams_dp_cn" \
    --data-urlencode "SubscriptionType=Subscription" \
    --data-urlencode "ClientToken=example-client-token-001" \
    --data-urlencode "Period=1" \
    --data-urlencode "PeriodUnit=Month" \
    --data-urlencode "AutoRenew=false" \
    --data-urlencode "SubscriptionConfigs.1.Seats=1" \
    --data-urlencode "SubscriptionConfigs.1.Configs.1.Code=plan_type" \
    --data-urlencode "SubscriptionConfigs.1.Configs.1.Value=standard"
```

## 返回示例

```
{
  "RequestId": "request-id-example",
  "Success": true,
  "Code": "Success",
  "Message": "Successful!",
  "Data": {
    "OrderId": 1234567890123456,
    "InstanceId": ["subs-example0000000001"],
    "HostId": "cn"
  }
}
```

## 错误码

如果调用失败，会返回错误信息。更多错误码及解决方法，请参见 [BssOpenApi 错误码](https://help.aliyun.com/zh/user-center/developer-reference/api-bssopenapi-2017-12-14-error-codes)。
