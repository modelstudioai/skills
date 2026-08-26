# AddChunk

使用此API可为文档搜索类（document）、数据查询类（table）、图片问答类（image）知识库添加切片。

## 接口说明

-   对于文档搜索类（document）、数据查询类（table）、图片问答类（image）知识库，本接口可向指定知识库中添加切片内容；目前尚不支持对音视频搜索类（multimedia）知识库进行相关操作。仅当数据源为表格连接器(excel)时，对数据查询与图片问答类型知识库的操作方可生效。
-   RAM 用户（子账号）需要首先获取阿里云百炼的 [API 权限](https://help.aliyun.com/zh/model-studio/grant-data-access-permission-to-ram-user)（需要`AliyunBailianDataFullAccess`，已包括 sfm:ChunkList 权限点），并[加入一个业务空间](https://help.aliyun.com/zh/model-studio/grant-the-business-space-permission-to-ram-users)后，方可调用本接口。阿里云账号（主账号）可直接调用无须授权。建议您通过最新版[阿里云百炼 SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)[阿里云百炼 SDK](https://api.alibabacloud.com/api-tools/sdk/bailian?version=2023-12-29)来调用本接口。
-   调用本接口前，请确保您的知识库已经创建完成且未被删除（即知识库 ID`IndexId`有效）。
-   本接口具有幂等性。

**限流说明：** 本接口频繁调用会被限流，频率请勿超过 10 次/秒。如遇限流，请稍后重试。

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

## 授权信息

当前API暂无授权信息透出。

## 请求语法

```
POST /{WorkspaceId}/chunk/create HTTP/1.1
```

## 路径参数

**名称**

**类型**

**必填**

**描述**

**示例值**

WorkspaceId

string

是

工作区标识

llm-19hxxxxx7htdf9lh

## 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

PipelineId

string

是

知识库 id

79c0alxxxx

dataId

string

否

文件 id

doc\_xxx

field

object

否

插入的切片内容信息，以键值对形式传入。文档搜索类知识库使用固定 key 列表：

-   content（**String**）：**必填**，切片正文内容
    
-   title（**String**）**选填**，切片标题
    
-   image\_urls（**Array**）：**选填**，切片包含的图片链接，最多 10 张
    

数据查询类、图片问答类知识库 key 不固定，由该知识库的数据源表格决定：key 为 Excel 列标题，value 为对应列的值。

{ "content": "The Bailian platform supports parsing multiple document formats including PDF, Word, and PPT.", "title": "Document Parsing and Chunking", "image\_urls": \[ "[](https://example.com/images/chunk-flow.png)[https://example.com/images/chunk-flow.png](https://example.com/images/chunk-flow.png)", "[](https://example.com/images/parsing-result.png)[https://example.com/images/parsing-result.png](https://example.com/images/parsing-result.png)" \] }

any

否

插入切片的表头字段信息，仅数据查询类与图片问答类知识库支持。需要参与检索或参与回复的表头为必填。各类型取值要求：

-   **String 类型** ：最大长度 6000
    
-   **时间 类型**：13 位时间戳（毫秒）
    
-   **Long 类型**：整数，最大 2147483647
    
-   **Double 类型**：支持小数
    
-   **image\_url 类型**：最多 5 张，多张用英文逗号拼接为一个字符串
    

{"Product Name": "Wireless Bluetooth Headphones", "Publish Time": 1752624000000, "Stock Quantity": 1580, "Unit Price": 299.99, "image\_url":"[](https://example.com/images/headphones-front.jpg,https://example.com/images/headphones-side.jpg,https://example.com/images/headphones-package.jpg)[https://example.com/images/headphones-front.jpg,https://example.com/images/headphones-side.jpg,https://example.com/images/headphones-package.jpg](https://example.com/images/headphones-front.jpg,https://example.com/images/headphones-side.jpg,https://example.com/images/headphones-package.jpg)" }

## 返回参数

**名称**

**类型**

**描述**

**示例值**

object

Schema of Response

RequestId

string

请求 id

35A267BF-xxxx-54DB-8394-AA3B0742D833

Code

string

错误状态码

Index.InvalidParameter

Message

string

错误信息

Required parameter(%s) missing or invalid, please check the request parameters.

Success

boolean

接口调用是否成功

**枚举值：**

-   true :
    
    true
    
-   false :
    
    false
    

true

Data

boolean

请求成功返回的业务数据

**枚举值：**

-   true :
    
    true
    
-   false :
    
    false
    

true

Status

string

接口返回的状态码

200

## 示例

正常返回示例

`JSON`格式

```
{
  "RequestId": "35A267BF-xxxx-54DB-8394-AA3B0742D833",
  "Code": "Index.InvalidParameter",
  "Message": "Required parameter(%s) missing or invalid, please check the request parameters.",
  "Success": true,
  "Data": true,
  "Status": "200"
}
```

## 错误码

访问[错误中心](https://api.aliyun.com/document/bailian/2023-12-29/errorCode)查看更多错误码。

## 变更历史

更多信息，参考[变更详情](https://api.aliyun.com/document/bailian/2023-12-29/AddChunk#workbench-doc-change-demo)。
