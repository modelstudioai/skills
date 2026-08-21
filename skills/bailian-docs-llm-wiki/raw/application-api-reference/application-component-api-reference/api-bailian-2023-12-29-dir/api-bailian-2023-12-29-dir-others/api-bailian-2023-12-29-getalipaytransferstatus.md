# GetAlipayTransferStatus - 查询支付宝打赏状态

查询应用中绑定的支付宝钱包的打赏状态。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/bailian/2023-12-29/GetAlipayTransferStatus)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/bailian/2023-12-29/GetAlipayTransferStatus)

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

sfm:GetAlipayTransferStatus

none

\*全部资源

`*`

无

无

## 请求语法

```
GET /openapi/alipay/transfer/status HTTP/1.1
POST /openapi/alipay/transfer/status HTTP/1.1GET /openapi/alipay/transfer/status HTTP/1.1
POST /openapi/alipay/transfer/status HTTP/1.1
```

## 请求参数

名称

类型

必填

描述

示例值

workspace\_id

string

否

百炼工作空间 ID

llm-cxxxxxxb8d47ks

code

string

否

支付宝打赏链接请求返回的打赏 code

xxx-xxxx

## 返回参数

名称

类型

描述

示例值

object

Schema of Response

requestId

string

请求的唯一 ID

6a71f2d9-f1c9-913b-818b-11402910xxxx

data

object

打赏的结果数据

code

string

打赏对应的 code

0

walletItemCode

string

支付宝商品钱包 code

xsdfsdf

mainAccountId

string

主账号 id（API 忽略）

1007576424487905

accountId

string

子账号 id（API 忽略）

1348393307144609

alipayOrderId

string

支付宝的订单 id

1234234

status

long

打赏状态

-   1 （成功）
-   0 （删除）
-   2 （待打赏）
-   3 （取消）
-   4 （退款）
-   5（关闭）
-   6（失败）
-   7（纠纷、异常）

1

creator

string

创建者（API 忽略）

234234

modifier

string

修改者（API 忽略）

234234

alipayOrderDetail

string

支付细节（API 忽略）

{}

title

string

转账标题

test

qrURL

string

打赏链接（API 忽略）

https://xxx.aliyun.com

transAmount

string

订单总金额，单位为：元。

0.22

scope

string

打赏应用的所属状态

publish

## 示例

正常返回示例

`JSON`格式

```
{
  "requestId": "6a71f2d9-f1c9-913b-818b-11402910xxxx\n",
  "data": {
    "code": 0,
    "walletItemCode": "xsdfsdf",
    "mainAccountId": 1007576424487905,
    "accountId": 1348393307144609,
    "alipayOrderId": 1234234,
    "status": 1,
    "creator": 234234,
    "modifier": 234234,
    "alipayOrderDetail": {},
    "title": "test",
    "qrURL": "https://xxx.aliyun.com",
    "transAmount": 0.22,
    "scope": "publish"
  }
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/bailian/2023-12-29/errorCode>)查看更多错误码。
