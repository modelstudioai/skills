# 查询订阅席位明细

分页查询订阅席位明细。

## 前提条件

已获取阿里云账号或 RAM 用户的 AccessKey，并已为其授予调用本接口所需的 RAM 权限。建议将 AccessKey 配置为环境变量 `ALIBABA_CLOUD_ACCESS_KEY_ID` 和 `ALIBABA_CLOUD_ACCESS_KEY_SECRET`，避免明文写入代码。

## 请求说明

-   **HTTP 方法**：GET
    
-   **请求地址**
    
    **地域**
    
    **Endpoint**
    
    华北2（北京）
    
    `GET [https://modelstudio.cn-beijing.aliyuncs.com/tokenplan/subscription/seat-detail](https://modelstudio.cn-beijing.aliyuncs.com/tokenplan/subscription/seat-detail)`
    
-   **认证方式**
    
    本接口是阿里云 OpenAPI，采用 AccessKey 签名（签名算法 `ACS3-HMAC-SHA256`），不支持 `Authorization: Bearer {API_KEY}` 方式。请求需携带公共请求头 `x-acs-action: GetSubscriptionSeatDetails`、`x-acs-version: 2026-02-10`、`x-acs-date`、`x-acs-content-sha256`、`x-acs-signature-nonce` 以及 `Authorization`。
    
    推荐使用阿里云 SDK 或 [OpenAPI Explorer](https://api.aliyun.com/api/ModelStudio/2026-02-10/GetSubscriptionSeatDetails) 发起调用，可免去自行计算签名。
    

## 请求参数

所有参数均通过 Query String 传递。数组类型参数（StatusList）使用 Flat 格式：以 `参数名.序号` 逐个传递，序号从 1 开始，例如 `StatusList.1=NORMAL`、`StatusList.2=<第二个取值>`。

**参数**

**类型**

**必选**

**描述**

PageNo

integer

否

分页页号。默认值：1 取值范围：正整数。

PageSize

integer

否

分页参数：每页显示条数，默认值 10。

StatusList

Array

否

席位状态筛选列表

SeatId

string

否

席位 id

SeatType

string

否

席位类型（specType）  
standard - 标准席位  
pro - 高级席位  
max - 尊享席位

QueryAssigned

boolean

否

席位分配状态筛选项。true=已分配，false=未分配，null=全部

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

Items

Array\[Object\]

数据项

Array\[Object\]

数据项

InstanceCode

string

席位 instance code

EquityList

Array\[Object\]

当前生效的权益实例，对 TokenPlan 产品，该列表只会有一个生效的权益实例

object

EquityType

string

权益类型（如 CREDITS、SPN、资源包等）

CycleInstanceId

string

权益 code（订阅 code，credits 场景下不需要消费）

CycleStartTime

integer

当前周期开始时间，毫秒

CycleEndTime

integer

当前周期结束时间，毫秒

CycleTotalValue

number

当前周期的总额度

CycleSurplusValue

number

当前周期的剩余额度

CycleVersion

integer

当前周期的时序版本

EndTime

integer

席位过期时间

SeatId

string

席位 ID

SpecType

string

席位类型  
standard - 标准席位  
pro - 高级席位  
max - 尊享席位

StartTime

integer

席位开始时间

AssignedStatus

string

分配状态  
ASSIGNED  
UNASSIGNED

AccountId

string

绑定的成员账号 ID

AccountName

string

成员账号名称

AccountEmail

string

成员账号邮箱

Status

string

席位状态：  
CREATING —— 创建中  
NORMAL —— 有效状态  
LIMIT ——欠费受限  
RELEASE —— 到期释放  
STOP —— 到期停机  
REFUNDED —— 已退款

Total

integer

席位的总数量

PageNo

integer

页码，取值大于 0 且不超过 Integer 数据类型的最大值

PageSize

integer

每页条数。

## 请求示例

本接口使用阿里云 OpenAPI 签名，下例中 `${SIGNATURE}` 需按 `ACS3-HMAC-SHA256` 算法计算得出，`x-acs-date`、`x-acs-signature-nonce` 需替换为实际值。

```
curl -X GET "https://modelstudio.cn-beijing.aliyuncs.com/tokenplan/subscription/seat-detail?PageNo=1&PageSize=10&StatusList.1=NORMAL&SeatId=seat-123456&SeatType=standard&QueryAssigned=true" \
    --header "x-acs-action: GetSubscriptionSeatDetails" \
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
    "Items": [
      {
        "InstanceCode": "subs-1234567",
        "EquityList": [
          {
            "EquityType": "CREDITS",
            "CycleInstanceId": "123456",
            "CycleStartTime": 1788328800000,
            "CycleEndTime": 1790920800000,
            "CycleTotalValue": 100,
            "CycleSurplusValue": 40,
            "CycleVersion": 1
          }
        ],
        "EndTime": 1790920800000,
        "SeatId": "seat_123456",
        "SpecType": "standard",
        "StartTime": 1788328800000,
        "AssignedStatus": "ASSIGNED",
        "AccountId": "acc_123456789",
        "AccountName": "ExampleName",
        "AccountEmail": "test@email.com",
        "Status": "NORMAL"
      }
    ],
    "Total": 100,
    "PageNo": 1,
    "PageSize": 10
  }
}
```

## 错误码

如果调用失败，会返回错误信息。更多错误码及解决方法，请参见[错误信息](raw/model-api-reference/preparations/error-code.md)。
