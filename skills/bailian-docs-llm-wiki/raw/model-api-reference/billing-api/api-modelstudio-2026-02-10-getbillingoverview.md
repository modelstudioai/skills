# GetBillingOverview

查询指定月份的账单总览信息，支持按维度分组聚合和筛选。

## 请求语法

```
GET /modelstudio/billing/overview HTTP/1.1
```

## 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

billMonth

string

是

账单月份，格式为 YYYY-MM，不能为空。

2026-08

groupBy

array<object>

是

分组条件列表。当前必须且只能传入一个分组维度。支持的维度 Code 见下方补充说明。

groupBy.code

string

是

维度 Code。

MAAS\_TYPE

filter

object

否

过滤条件。

filter.dimensions

array<object>

否

筛选维度列表。

filter.dimensions.code

string

否

维度 Code。

BASE\_MODEL

filter.dimensions.values

array<string>

否

筛选值列表。

\["qwen-max"\]

filter.dimensions.selectType

string

否

筛选类型。取值：

-   IN
    
-   NOT
    

IN

topNum

integer

否

返回分组数量，范围为 1～20，默认 20。

20

zeroFilter

boolean

否

是否过滤金额为 0 的分组，默认 true。

true

regionId

string

否

地域 ID。

cn-beijing

locale

string

否

返回语言，默认 en-US。取值：

-   en-US：英文
    
-   zh-CN：中文
    

zh-CN

**补充说明**

`groupBy[].code` 和 `filter.dimensions[].code` 支持以下值，建议统一使用大写：

**维度 Code**

**含义**

**filter.dimensions\[\].values 可传值**

MAAS\_TYPE

MaaS 业务类型

inference（模型调用）、training（模型训练）、model\_units（模型单元）、capacity\_reserved（容量预留）

BASE\_MODEL

基础模型

账单数据中的基础模型原始值，例如 qwen-plus

API\_KEY\_ID

API Key ID

账单数据中的 API Key ID 原始值

WORKSPACE\_ID

业务空间 ID

账单数据中的 Workspace ID 原始值

FEE\_TYPE

费用类型

billing（账单费用）、subscription（订阅购买费用）

CHARGE\_TYPE

付费类型

postpaid（后付费）、prepaid（预付费）

BUSINESS\_REGION

业务地域

cn-beijing、ap-southeast-1、cn-hongkong 等，取值以实际值为准

SERVICE\_SITE

服务站点

asia-pacific-china、global、international 等，取值以实际值为准

ARTICLE\_CODE

商品 Code

sfm\_inferenceglobal\_public\_intl 等，取值以实际值为准

**说明**所有维度的 `filter.dimensions[].values` 均可传 `DIMENSION_FILTER_NULL_VALUE`，表示匹配字段为 NULL 或空字符串的数据。

## 返回参数

**名称**

**类型**

**描述**

**示例值**

requestId

string

请求 ID。

BB521414-5D38-5E66-AA66-963B2B4200E2

code

string

请求结果代码。

200

message

string

请求结果说明。

null

success

boolean

请求是否成功。

true

data

object

账单费用概览数据。

data.currency

string

金额币种

USD

data.totalAmount

string

金额合计

31228.60

data.pretaxAmount

string

不含税金额合计

28729.32

data.taxAmount

string

税费合计

2499.28

data.groups

array<object>

按金额降序排列的 TopN 分组列表

data.groups.key

string

分组维度值。空值返回 DIMENSION\_FILTER\_NULL\_VALUE。

inference

data.groups.name

string

分组展示名称，受 locale 参数影响；空值展示为-。

模型调用

data.groups.articleCodes

array<string>

当前分组涉及的商品 Code 列表

data.groups.amount

string

当前分组金额

3000

data.groups.percentage

string

分组金额占 TopN 金额合计的比例

0.10

## 示例

正常返回示例

`JSON`格式

```
{
  "requestId": "BB521414-5D38-5E66-AA66-963B2B4200E2",
  "code": "200",
  "message": "null",
  "success": true,
  "data": {
    "currency": "USD",
    "totalAmount": "31228.60",
    "pretaxAmount": "28729.32",
    "taxAmount": "2499.28",
    "groups": [
      {
        "key": "inference",
        "name": "模型调用",
        "articleCodes": [
          "sfm_inferenceglobal_public_intl"
        ],
        "amount": "3000",
        "percentage": "0.10"
      }
    ]
  }
}
```
