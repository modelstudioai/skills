# AsyncUploadVideo - 异步上传视频剪辑素材

上传剪辑素材

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/AsyncUploadVideo)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/AsyncUploadVideo)

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

aimiaobi:AsyncUploadVideo

create

\*全部资源

`*`

无

无

## 请求语法

```
POST  HTTP/1.1
```

## 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

SourceVideos

array<object>

是

剪辑素材结构

object

否

剪辑素材结构

VideoName

string

是

视频名称

123.mp4

VideoUrl

string

是

视频地址。

http://123.mp4 目前该接口只进行视频理解额和分析，并没有对文件进行转存。请保证视频地址在任务执行期间有效。

VideoExtraInfo

string

否

视频额外描述

视频中有一个房子

AnlysisPrompt

string

否

视频理解 prompt

重点理解视频中的风景信息

WorkspaceId

string

是

[百炼工作空间 Id](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

llm-xxxx

ReferenceVideo

object

否

参考视频信息

VideoName

string

否

参考视频名字

refvideo.mp4

VideoUrl

string

否

视频地址。

http://viapi-customer-pop.oss-cn-shanghai.aliyuncs.com/d71e\_208334498220521996\_51298e0a909d457693166eb883768c7a

VideoExtraInfo

string

否

视频理解附加信息

手机cpu采用3纳米技术

SplitInterval

integer

否

视频理解镜头时间间隔

默认1

VideoRoles

array<object>

否

角色人脸信息

array<object>

否

角色名字

RoleName

string

否

角色名字

李晓明

RoleInfo

string

否

角色信息

李晓明是一位警察

RoleUrls

array<object>

否

角色照片地址

object

否

角色图片文件信息

RoleFileName

string

否

角色面部图片文件名字

王小明.jpeg

RoleFileUrl

string

否

角色面部图片公网地址

http://xxx/xxx.jpeg

FaceIdentitySimilarityMinScore

number

否

人物识别相似度阈值

0.7

VideoShotFaceIdentityCount

integer

否

人物匹配时，单镜头(分镜)，参与匹配的抽帧（图片）数量

2

RemoveSubtitle

boolean

否

去除素材字幕

TaskName

string

否

任务名字

task001

TaskType

string

否

任务类型

type001

AdaptiveThreshold

number

否

分镜阈值，越小分镜越敏感，取值 1·10，默认是 3

3.0

## **返回参数**

**名称**

**类型**

**描述**

**示例值**

object

Schema of Response

RequestId

string

Id of the request

94512A33-8EC1-5452-A793-5C91F18ED2F0

Code

string

请求返回 Code

successful

Data

object

业务数据

TaskId

string

任务 ID

3f7045e099474ba28ceca1b4eb6d6e21

VideoInfos

array<object>

视频信息

object

视频信息

VideoId

string

视频 Id

60616fad41b171f0bb4b4531948c0102

VideoName

string

视频名称

123.mp4

VideoUrl

string

视频 URL

http://123.mp4

VideoExtraInfo

string

视频额外信息

视频中有一个房子

HttpStatusCode

integer

http 状态码

200

Message

string

错误说明

success

Success

boolean

是否成功：true 成功，false 失败

true

## 示例

正常返回示例

`JSON`格式

```
{
  "RequestId": "94512A33-8EC1-5452-A793-5C91F18ED2F0",
  "Code": "successful",
  "Data": {
    "TaskId": "3f7045e099474ba28ceca1b4eb6d6e21",
    "VideoInfos": [
      {
        "VideoId": "60616fad41b171f0bb4b4531948c0102",
        "VideoName": "123.mp4",
        "VideoUrl": "http://123.mp4",
        "VideoExtraInfo": "视频中有一个房子"
      }
    ]
  },
  "HttpStatusCode": 200,
  "Message": "success",
  "Success": true
}
```

## 错误码

   

**HTTP status code**

**错误码**

**错误信息**

**描述**

403

NoPermission

You are not authorized to perform this action.

请检查workspaceId的赋值

访问[错误中心](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode)查看更多错误码。

## **变更历史**

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/AsyncUploadVideo#workbench-doc-change-demo)。
