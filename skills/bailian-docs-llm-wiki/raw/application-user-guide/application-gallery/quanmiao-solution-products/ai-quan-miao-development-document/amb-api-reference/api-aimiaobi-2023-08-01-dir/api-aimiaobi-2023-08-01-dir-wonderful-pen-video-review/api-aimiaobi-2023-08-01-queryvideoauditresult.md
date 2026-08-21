# QueryVideoAuditResult - 查询视频审校结果

查询视频审校结果

## 接口说明

根据任务 ID 查询视频审校结果，包含视频信息、分镜信息和审核结果

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/QueryVideoAuditResult)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/QueryVideoAuditResult)

## **授权信息**

下表是API对应的授权信息，可以在RAM权限策略语句的`Action`元素中使用，用来给RAM用户或RAM角色授予调用此API的权限。具体说明如下：

-   操作：是指具体的权限点。
    
-   访问级别：是指每个操作的访问级别，取值为写入（Write）、读取（Read）或列出（List）。
    
-   资源类型：是指操作中支持授权的资源类型。具体说明如下：
    
    -   对于必选的资源类型，用前面加 \* 表示。
        
    -   对于不支持资源级授权的操作，用`全部资源`表示。
        
-   条件关键字：是指云产品自身定义的条件关键字。
    
-   关联操作：是指成功执行操作所需要的其他权限。操作者必须同时具备关联操作的权限，操作才能成功。
    

**操作**

**访问级别**

**资源类型**

**条件关键字**

**关联操作**

aimiaobi:QueryVideoAuditResult

get

\*全部资源

`*`

无

无

## 请求语法

```
POST /quanmiao/aimiaobi/pop/videoAudit/queryVideoAuditResult HTTP/1.1
```

## 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

WorkspaceId

string

是

业务空间 ID

llm-xxxxx

TaskId

string

是

任务 ID

xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

## **返回参数**

**名称**

**类型**

**描述**

**示例值**

object

查询结果响应

RequestId

string

请求 ID

1813ceee-7fe5-41b4-87e5-982a4d18cca5

HttpStatusCode

integer

HTTP 状态码

200

Code

string

业务状态码

success

Message

string

返回信息

查询成功

Success

boolean

是否成功

true

Data

object

视频审校结果数据

Status

string

任务状态（PENDING：排队中、RUNNING： 执行中，SUCCESSED： 执行成功、 FAILED: 执行失败、 CANCELED：任务被取消）

SUCCESSED

ErrorMessage

string

错误信息

错误信息

Text

string

审校文本

视频审核完成

VideoUrl

string

视频 URL

https://example.com/video.mp4

VideoFileKey

string

视频 FileKey

video/test.mp4

Duration

number

视频时长

120.5

Width

integer

视频宽度

1920

Height

integer

视频高度

1080

Fps

number

视频帧率

30.0

TotalFrames

integer

总帧数

3615

TotalShots

integer

总分镜数

15

TotalFrameAudit

integer

待审核帧数

120

FrameAudited

integer

已审帧数

120

ImageUrls

array<object>

图片 URL 列表

object

Url

string

图片 URL

https://example.com/image1.jpg

Id

string

图片 ID（与 Results\[\].DataId 关联获取 审核结果信息）

img001

Timestamp

number

时间戳（毫秒级）

1000

Results

array<object>

审核结果列表

array<object>

ReqId

string

请求 ID

B5D1CF9E-0404-51E3-A28E-A5C7D95B6C71

DataId

string

图片 ID（与 ImageUrls\[\].Id 关联 获取图片信息）

d411ed15e8fc154fd0ef5addabfee04b

RiskLevel

string

风险等级

-   high: 高风险
    
-   medium：中风险
    
-   low：低风险
    
-   none：无风险
    

none

Result

array<object>

检测结果

object

Label

string

风险标签

图片内容检测运算后返回的标签，如：nonLabel（未检测出风险）

风险等级，根据设置的高低风险分返回，返回值包括： ● high：高风险 ● medium：中风险 ● low：低风险 ● none：未检测到风险

nonLabel

Confidence

number

置信分值 0 到 100 分，保留到小数点后 2 位，部分标签无置信分

99.5

Description

string

Label 字段的解释说明

未检测出风险

## 示例

正常返回示例

`JSON`格式

```
{
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "HttpStatusCode": 200,
  "Code": "success",
  "Message": "查询成功",
  "Success": true,
  "Data": {
    "Status": "SUCCESSED",
    "ErrorMessage": "错误信息",
    "Text": "视频审核完成",
    "VideoUrl": "https://example.com/video.mp4",
    "VideoFileKey": "video/test.mp4",
    "Duration": 120.5,
    "Width": 1920,
    "Height": 1080,
    "Fps": 30,
    "TotalFrames": 3615,
    "TotalShots": 15,
    "TotalFrameAudit": 120,
    "FrameAudited": 120,
    "ImageUrls": [
      {
        "Url": "https://example.com/image1.jpg",
        "Id": "img001",
        "Timestamp": 1000
      }
    ],
    "Results": [
      {
        "ReqId": "B5D1CF9E-0404-51E3-A28E-A5C7D95B6C71",
        "DataId": "d411ed15e8fc154fd0ef5addabfee04b",
        "RiskLevel": "none",
        "Result": [
          {
            "Label": "nonLabel",
            "Confidence": 99.5,
            "Description": "未检测出风险"
          }
        ]
      }
    ]
  }
}
```

## 错误码

访问[错误中心](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode)查看更多错误码。

## **变更历史**

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/QueryVideoAuditResult#workbench-doc-change-demo)。
