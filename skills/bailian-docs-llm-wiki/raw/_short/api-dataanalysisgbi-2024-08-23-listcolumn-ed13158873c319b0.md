# ListColumn - 数据表下的数据列集合

获取当前指定业务空间，指定表下面的列信息。

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

[调试](https://api.aliyun.com/api/DataAnalysisGBI/2024-08-23/ListColumn)

## 授权信息

下表是API对应的授权信息，可以在RAM权限策略语句的`Action`元素中使用，用来给RAM用户或RAM角色授予调用此API的权限。具体说明如下：

-   操作：是指具体的权限点。
    
-   访问级别：是指每个操作的访问级别，取值为写入（Write）、读取（Read）或列出（List）。
    
-   资源类型：是指操作中支持授权的资源类型。具体说明如下：
    
    -   对于必选的资源类型，用前面加 \* 表示。
    -   对于不支持资源级授权的操作，用`全部资源`表示。
-   条件关键字：是指云产品自身定义的条件关键字。
    
-   关联操作：是指成功执行操作所需要的其他权限。操作者必须同时具备关联操作的权限，操作才能成功。
    

操作

访问级别

资源类型

条件关键字

关联操作

dataanalysisgbi:ListColumn

none

\*全部资源

`*`

无

无

## 请求语法

```
POST /gbi/list/column HTTP/1.1
```

## 请求参数

名称

类型

必填

描述

示例值

workspaceId

string

是

当前请求所使用的阿里云百炼业务空间 id

llm-2v3934xtp49esw64

body

object

否

请求体参数

tableIdKey

string

是

数据表的唯一标识符 id

table-AAAAAAAAFQBwSLJkUj4CYg

nextToken

integer

否

分页游标。

-   如果是首次调用，该参数不传。
    
-   如果是非首次调用，该参数传上传调用时返回的 nextToken。
    

e8Z0nRyY51ZQmYljqGNK

maxResults

integer

否

每页最大条目数

10

## 返回参数

名称

类型

描述

示例值

object

Result

data

any

返回信息

{ "data": { "data": \[ { "tableIdKey": "table-AAAAAAAAFQBwSLJkUj4CYg", "initializationData": "{\\"description\\":\\"下单客户的ID\\",\\"enumType\\":0,\\"gmtCreate\\":1734059103879,\\"name\\":\\"customer\_id\\",\\"samples\\":\\"\[\]\\",\\"tableId\\":5376,\\"type\\":\\"number\\"}", "enumType": 0, "name": "customer\_id", "description": "下单客户的ID", "gmtCreate": 1734059104000, "type": "number", "samples": \[\], "columnIdKey": "column-AAAAAAAAh6Q9ERazKYFvkA", "enumValues": \[\] }, { "tableIdKey": "table-AAAAAAAAFQBwSLJkUj4CYg", "initializationData": "{\\"description\\":\\"下单日期，格式为YYYY-MM-DD\\",\\"enumType\\":0,\\"gmtCreate\\":1734059103913,\\"name\\":\\"order\_date\\",\\"samples\\":\\"\[\]\\",\\"tableId\\":5376,\\"type\\":\\"date\\"}", "enumType": 0, "name": "order\_date", "description": "下单日期，格式为YYYY-MM-DD", "gmtCreate": 1734059104000, "type": "date", "samples": \[\], "columnIdKey": "column-AAAAAAAAh6XbT54v-8NjeA", "enumValues": \[\] }, { "tableIdKey": "table-AAAAAAAAFQBwSLJkUj4CYg", "initializationData": "{\\"description\\":\\"订单ID\\",\\"enumType\\":0,\\"gmtCreate\\":1734059103946,\\"name\\":\\"order\_id\\",\\"samples\\":\\"\[\]\\",\\"tableId\\":5376,\\"type\\":\\"number\\"}", "enumType": 0, "name": "order\_id", "description": "订单ID", "gmtCreate": 1734059104000, "type": "number", "samples": \[\], "columnIdKey": "column-AAAAAAAAh6avEvz8bdb30Q", "enumValues": \[\] }, { "tableIdKey": "table-AAAAAAAAFQBwSLJkUj4CYg", "initializationData": "{\\"description\\":\\"订单状态（例如：待发货、已发货、已送达）\\",\\"enumType\\":0,\\"gmtCreate\\":1734059103980,\\"name\\":\\"order\_status\\",\\"samples\\":\\"\[\]\\",\\"tableId\\":5376,\\"type\\":\\"text\\"}", "enumType": 0, "name": "order\_status", "description": "订单状态（例如：待发货、已发货、已送达）", "gmtCreate": 1734059104000, "type": "text", "samples": \[\], "columnIdKey": "column-AAAAAAAAh6cWOUPagYstkg", "enumValues": \[\] }, { "tableIdKey": "table-AAAAAAAAFQBwSLJkUj4CYg", "initializationData": "{\\"description\\":\\"所订购产品的ID\\",\\"enumType\\":0,\\"gmtCreate\\":1734059104013,\\"name\\":\\"product\_id\\",\\"samples\\":\\"\[\]\\",\\"tableId\\":5376,\\"type\\":\\"number\\"}", "enumType": 0, "name": "product\_id", "description": "所订购产品的ID", "gmtCreate": 1734059104000, "type": "number", "samples": \[\], "columnIdKey": "column-AAAAAAAAh6hFxzroVe3k4Q", "enumValues": \[\] }, { "tableIdKey": "table-AAAAAAAAFQBwSLJkUj4CYg", "initializationData": "{\\"description\\":\\"订购产品的数量\\",\\"enumType\\":0,\\"gmtCreate\\":1734059104046,\\"name\\":\\"quantity\\",\\"samples\\":\\"\[\]\\",\\"tableId\\":5376,\\"type\\":\\"number\\"}", "enumType": 0, "name": "quantity", "description": "订购产品的数量", "gmtCreate": 1734059104000, "type": "number", "samples": \[\], "columnIdKey": "column-AAAAAAAAh6ncfHPApl0elQ", "enumValues": \[\] } \], "nextToken": "T65g+mLhrbH14+IU/ABI3Q==", "totalCount": 0 } }

errorMsg

string

错误描述信息。

NoAuth

code

string

错误码

NoAuth

success

boolean

true 接口调用成功，false 接口调用失败

true

requestId

string

请求 id，每次请求都是唯一值，便于后续排查问题

FB11F719-9AC8-5C99-AB0A-4709D437FCFC

## 示例

正常返回示例

`JSON`格式

```
{
  "data": {
    "data": {
      "data": [
        {
          "tableIdKey": "table-AAAAAAAAFQBwSLJkUj4CYg",
          "initializationData": {
            "description": "下单客户的ID",
            "enumType": 0,
            "gmtCreate": 1734059103879,
            "name": "customer_id",
            "samples": [],
            "tableId": 5376,
            "type": "number"
          },
          "enumType": 0,
          "name": "customer_id",
          "description": "下单客户的ID",
          "gmtCreate": 1734059104000,
          "type": "number",
          "samples": [],
          "columnIdKey": "column-AAAAAAAAh6Q9ERazKYFvkA",
          "enumValues": []
        },
        {
          "tableIdKey": "table-AAAAAAAAFQBwSLJkUj4CYg",
          "initializationData": {
            "description": "下单日期，格式为YYYY-MM-DD",
            "enumType": 0,
            "gmtCreate": 1734059103913,
            "name": "order_date",
            "samples": [],
            "tableId": 5376,
            "type": "date"
          },
          "enumType": 0,
          "name": "order_date",
          "description": "下单日期，格式为YYYY-MM-DD",
          "gmtCreate": 1734059104000,
          "type": "date",
          "samples": [],
          "columnIdKey": "column-AAAAAAAAh6XbT54v-8NjeA",
          "enumValues": []
        },
        {
          "tableIdKey": "table-AAAAAAAAFQBwSLJkUj4CYg",
          "initializationData": {
            "description": "订单ID",
            "enumType": 0,
            "gmtCreate": 1734059103946,
            "name": "order_id",
            "samples": [],
            "tableId": 5376,
            "type": "number"
          },
          "enumType": 0,
          "name": "order_id",
          "description": "订单ID",
          "gmtCreate": 1734059104000,
          "type": "number",
          "samples": [],
          "columnIdKey": "column-AAAAAAAAh6avEvz8bdb30Q",
          "enumValues": []
        },
        {
          "tableIdKey": "table-AAAAAAAAFQBwSLJkUj4CYg",
          "initializationData": {
            "description": "订单状态（例如：待发货、已发货、已送达）",
            "enumType": 0,
            "gmtCreate": 1734059103980,
            "name": "order_status",
            "samples": [],
            "tableId": 5376,
            "type": "text"
          },
          "enumType": 0,
          "name": "order_status",
          "description": "订单状态（例如：待发货、已发货、已送达）",
          "gmtCreate": 1734059104000,
          "type": "text",
          "samples": [],
          "columnIdKey": "column-AAAAAAAAh6cWOUPagYstkg",
          "enumValues": []
        },
        {
          "tableIdKey": "table-AAAAAAAAFQBwSLJkUj4CYg",
          "initializationData": {
            "description": "所订购产品的ID",
            "enumType": 0,
            "gmtCreate": 1734059104013,
            "name": "product_id",
            "samples": [],
            "tableId": 5376,
            "type": "number"
          },
          "enumType": 0,
          "name": "product_id",
          "description": "所订购产品的ID",
          "gmtCreate": 1734059104000,
          "type": "number",
          "samples": [],
          "columnIdKey": "column-AAAAAAAAh6hFxzroVe3k4Q",
          "enumValues": []
        },
        {
          "tableIdKey": "table-AAAAAAAAFQBwSLJkUj4CYg",
          "initializationData": {
            "description": "订购产品的数量",
            "enumType": 0,
            "gmtCreate": 1734059104046,
            "name": "quantity",
            "samples": [],
            "tableId": 5376,
            "type": "number"
          },
          "enumType": 0,
          "name": "quantity",
          "description": "订购产品的数量",
          "gmtCreate": 1734059104000,
          "type": "number",
          "samples": [],
          "columnIdKey": "column-AAAAAAAAh6ncfHPApl0elQ",
          "enumValues": []
        }
      ],
      "nextToken": "T65g+mLhrbH14+IU/ABI3Q==",
      "totalCount": 0
    }
  },
  "errorMsg": "NoAuth",
  "code": "NoAuth",
  "success": true,
  "requestId": "FB11F719-9AC8-5C99-AB0A-4709D437FCFC"
}
```

## 错误码

HTTP status code

错误码

错误信息

描述

401

Internal.Error

Bad Request: Internal Error.

内部错误，请联系客服人员排查

401

NoAuth

Bad Request: Workspace.Illegal.Auth.

当前所使用的账号无所指定业务空间的权限

401

NoResourceAuth

Bad Request: Resource Auth Error.

没有请求的资源的权限，请确保所请求的资源属于当前参数中的业务空间

访问[错误中心](https://api.aliyun.com/document/DataAnalysisGBI/2024-08-23/errorCode)查看更多错误码。
