# GetImageTranslateTask - 获取图片翻译任务结果

通义多模态翻译获取图片翻译结果

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AnyTrans/2025-07-07/GetImageTranslateTask)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AnyTrans/2025-07-07/GetImageTranslateTask)

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

anytrans:GetImageTranslateTask

none

\*全部资源

`*`

无

无

## 请求语法

```
POST /anytrans/translate/image/get HTTP/1.1
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

业务空间 Id

llm-kqtrcpdee4xm29xx

taskId

string

是

图片翻译任务 id

2746f4be-cff2-465e-a2c6-12bff30ce0f9

## 返回参数

名称

类型

描述

示例值

object

Schema of Response

code

string

响应状态码

success

message

string

响应信息

success

requestId

string

请求 id，用于追溯 API 调用链路

377A48D7-7CFA-53F9-8CA2-14FE3F2774B6

success

boolean

接口调用是否成功

true

httpStatusCode

string

http 响应码

200

synchro

boolean

是否同步

true

data

object

返回数据

traceId

string

链路 Id

213e391517328463424251152ec9fb

translation

object

翻译结果

angle

long

图片旋转角度

0

width

long

图片旋转后宽度

800

height

long

图片旋转后高度

800

orgWidth

long

原始图片宽度

800

orgHeight

long

原始图片高度

800

boxesCount

long

字块数量

13

boundingBoxes

array<object>

字块详情列表

boundingBoxes

object

字块详情

upLeft

object

左上角位置

x

long

x 坐标

10

y

long

y 坐标

66

upRight

object

右上角位置

x

long

x 坐标

328

y

long

y 坐标

69

downLeft

object

左下角位置

x

long

x 坐标

9

y

long

y 坐标

145

downRight

object

右下角位置

x

long

x 坐标

327

y

long

y 坐标

148

confidence

float

标签置信度，取值范围为 0（表示置信度最低）~1（表示置信度最高）

0.99

text

string

图片识别出的文字块的源语言文案

修护头皮

direction

long

文字方向 0 为横向 1 为竖行

0

tableId

long

文字块所属的表格 id 如果不在表格内值为-1

1

tableCellId

long

文字块所属的单元格 id 如果不在表格内 值为-1

1

translation

object

翻译结果

{ "en": "Restore Scalp Health" }

tableInfos

array<object>

表格信息列表

tableInfos

object

表格信息

tableId

long

源表 ID

1

xCellSize

long

横向单元格长度

50

yCellSize

long

纵向单元格长度

50

cellInfos

array<object>

单元格信息列表

cellInfos

object

单元格信息

tableCellId

long

单元格 Id

1

text

string

图片文字块中待翻译的文本

活动价

xsc

long

横轴方向该单元格起始在第几个单元格

1

xec

long

横轴方向该单元格结束在第几个单元格

2

ysc

long

纵轴方向该单元格起始在第几个单元格

3

yec

long

纵轴方向该单元格结束在第几个单元格

1

pos

array<object>

单元格位置列表

pos

object

单元格位置

x

long

x 坐标

33

y

long

y 坐标

11

## 示例

正常返回示例

`JSON`格式

```
{
  "code": "success",
  "message": "success",
  "requestId": "377A48D7-7CFA-53F9-8CA2-14FE3F2774B6",
  "success": true,
  "httpStatusCode": 200,
  "synchro": true,
  "data": {
    "traceId": "213e391517328463424251152ec9fb",
    "translation": {
      "angle": 0,
      "width": 800,
      "height": 800,
      "orgWidth": 800,
      "orgHeight": 800,
      "boxesCount": 13,
      "boundingBoxes": [
        {
          "upLeft": {
            "x": 10,
            "y": 66
          },
          "upRight": {
            "x": 328,
            "y": 69
          },
          "downLeft": {
            "x": 9,
            "y": 145
          },
          "downRight": {
            "x": 327,
            "y": 148
          },
          "confidence": 0.99,
          "text": "修护头皮",
          "direction": 0,
          "tableId": 1,
          "tableCellId": 1,
          "translation": {
            "en": "Restore Scalp Health"
          }
        }
      ],
      "tableInfos": [
        {
          "tableId": 1,
          "xCellSize": 50,
          "yCellSize": 50,
          "cellInfos": [
            {
              "tableCellId": 1,
              "text": "活动价",
              "xsc": 1,
              "xec": 2,
              "ysc": 3,
              "yec": 1,
              "pos": [
                {
                  "x": 33,
                  "y": 11
                }
              ]
            }
          ]
        }
      ]
    }
  }
}
```

## 错误码

HTTP status code

错误码

错误信息

400

IdempotentParameterMismatch

The request uses the same client token as a previous, but non-identical request. Do not reuse a client token with different requests, unless the requests are identical.

访问[错误中心](< https://api.aliyun.com/document/AnyTrans/2025-07-07/errorCode>)查看更多错误码。

## 变更历史

变更时间

变更内容概要

操作

暂无变更历史
