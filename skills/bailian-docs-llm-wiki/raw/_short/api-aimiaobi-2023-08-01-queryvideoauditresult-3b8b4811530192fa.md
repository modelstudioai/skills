# QueryVideoAuditResult

查询视频审校结果

<a id="接口说明"></a>

<a id="api-detail-51"></a>

## 接口说明

根据任务 ID 查询视频审校结果，包含视频信息、分镜信息和审核结果

<a id="调试"></a>

<a id="api-doc-debug"></a>

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

<a id="授权信息"></a>

<a id="api-detail-32"></a>

## 授权信息

下表是API对应的授权信息，可以在RAM权限策略语句的`Action`元素中使用，用来给RAM用户或RAM角色授予调用此API的权限。具体说明如下：

-   操作：是指具体的权限点。
    
-   访问级别：是指每个操作的访问级别，取值为写入（Write）、读取（Read）或列出（List）。
    
-   资源类型：是指操作中支持授权的资源类型。具体说明如下：
    
    -   对于必选的资源类型，用前面加 \* 表示。
    -   对于不支持资源级授权的操作，用`全部资源`表示。
-   条件关键字：是指云产品自身定义的条件关键字。
    
-   关联操作：是指成功执行操作所需要的其他权限。操作者必须同时具备关联操作的权限，操作才能成功。
    

| 操作 | 访问级别 | 资源类型 | 条件关键字 | 关联操作 |
| --- | --- | --- | --- | --- |
| aimiaobi:QueryVideoAuditResult | get | \*全部资源<br><br>`*` | 无 | 无 |

<a id="请求语法"></a>

<a id="api-detail-53"></a>

## 请求语法

<a id="code-block"></a>

```text
POST /quanmiao/aimiaobi/pop/videoAudit/queryVideoAuditResult HTTP/1.1
```

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

| 名称 | 类型 | 必填 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| WorkspaceId | string | 是 | 业务空间 ID | llm-xxxxx |
| TaskId | string | 是 | 任务 ID | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx |

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

<table><thead><tr><th><p><strong>名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td></td><td><p>object</p></td><td><div><p>查询结果响应</p></div></td><td></td></tr><tr><td>RequestId</td><td><p>string</p></td><td><div><p>请求 ID</p></div></td><td><p>1813ceee-7fe5-41b4-87e5-982a4d18cca5</p></td></tr><tr><td>HttpStatusCode</td><td><p>integer</p></td><td><div><p>HTTP 状态码</p></div></td><td><p>200</p></td></tr><tr><td>Code</td><td><p>string</p></td><td><div><p>业务状态码</p></div></td><td><p>success</p></td></tr><tr><td>Message</td><td><p>string</p></td><td><div><p>返回信息</p></div></td><td><p>查询成功</p></td></tr><tr><td>Success</td><td><p>boolean</p></td><td><div><p>是否成功</p></div></td><td><p>true</p></td></tr><tr><td>Data</td><td><p>object</p></td><td><div><p>视频审校结果数据</p></div></td><td></td></tr><tr><td>Status</td><td><p>string</p></td><td><div><p>任务状态（PENDING：排队中、RUNNING： 执行中，SUCCESSED： 执行成功、 FAILED: 执行失败、 CANCELED：任务被取消）</p></div></td><td><p>SUCCESSED</p></td></tr><tr><td>ErrorMessage</td><td><p>string</p></td><td><div><p>错误信息</p></div></td><td><p>错误信息</p></td></tr><tr><td>Text</td><td><p>string</p></td><td><div><p>审校文本</p></div></td><td><p>视频审核完成</p></td></tr><tr><td>VideoUrl</td><td><p>string</p></td><td><div><p>视频 URL</p></div></td><td><p><a href="https://example.com/video.mp4">https://example.com/video.mp4</a></p></td></tr><tr><td>VideoFileKey</td><td><p>string</p></td><td><div><p>视频 FileKey</p></div></td><td><p>video/test.mp4</p></td></tr><tr><td>Duration</td><td><p>number</p></td><td><div><p>视频时长</p></div></td><td><p>120.5</p></td></tr><tr><td>Width</td><td><p>integer</p></td><td><div><p>视频宽度</p></div></td><td><p>1920</p></td></tr><tr><td>Height</td><td><p>integer</p></td><td><div><p>视频高度</p></div></td><td><p>1080</p></td></tr><tr><td>Fps</td><td><p>number</p></td><td><div><p>视频帧率</p></div></td><td><p>30.0</p></td></tr><tr><td>TotalFrames</td><td><p>integer</p></td><td><div><p>总帧数</p></div></td><td><p>3615</p></td></tr><tr><td>TotalShots</td><td><p>integer</p></td><td><div><p>总分镜数</p></div></td><td><p>15</p></td></tr><tr><td>TotalFrameAudit</td><td><p>integer</p></td><td><div><p>待审核帧数</p></div></td><td><p>120</p></td></tr><tr><td>FrameAudited</td><td><p>integer</p></td><td><div><p>已审帧数</p></div></td><td><p>120</p></td></tr><tr><td>ImageUrls</td><td><p>array&lt;object&gt;</p></td><td><div><p>图片 URL 列表</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td></td><td></td></tr><tr><td>Url</td><td><p>string</p></td><td><div><p>图片 URL</p></div></td><td><p><a href="https://example.com/image1.jpg">https://example.com/image1.jpg</a></p></td></tr><tr><td>Id</td><td><p>string</p></td><td><div><p>图片 ID（与 Results[].DataId 关联获取 审核结果信息）</p></div></td><td><p>img001</p></td></tr><tr><td>Timestamp</td><td><p>number</p></td><td><div><p>时间戳（毫秒级）</p></div></td><td><p>1000</p></td></tr><tr><td>Results</td><td><p>array&lt;object&gt;</p></td><td><div><p>审核结果列表</p></div></td><td></td></tr><tr><td></td><td><p>array&lt;object&gt;</p></td><td></td><td></td></tr><tr><td>ReqId</td><td><p>string</p></td><td><div><p>请求 ID</p></div></td><td><p>B5D1CF9E-0404-51E3-A28E-A5C7D95B6C71</p></td></tr><tr><td>DataId</td><td><p>string</p></td><td><div><p>图片 ID（与 ImageUrls[].Id 关联 获取图片信息）</p></div></td><td><p>d411ed15e8fc154fd0ef5addabfee04b</p></td></tr><tr><td>RiskLevel</td><td><p>string</p></td><td><div><p>风险等级</p><ul><li><p>high: 高风险</p></li><li><p>medium：中风险</p></li><li><p>low：低风险</p></li><li><p>none：无风险</p></li></ul></div></td><td><p>none</p></td></tr><tr><td>Result</td><td><p>array&lt;object&gt;</p></td><td><div><p>检测结果</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td></td><td></td></tr><tr><td>Label</td><td><p>string</p></td><td><div><p>风险标签</p><p>图片内容检测运算后返回的标签，如：nonLabel（未检测出风险）</p><p>风险等级，根据设置的高低风险分返回，返回值包括： ● high：高风险 ● medium：中风险 ● low：低风险 ● none：未检测到风险</p></div></td><td><p>nonLabel</p></td></tr><tr><td>Confidence</td><td><p>number</p></td><td><div><p>置信分值 0 到 100 分，保留到小数点后 2 位，部分标签无置信分</p></div></td><td><p>99.5</p></td></tr><tr><td>Description</td><td><p>string</p></td><td><div><p>Label 字段的解释说明</p></div></td><td><p>未检测出风险</p></td></tr></tbody></table>

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-2"></a>

```json
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

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

访问[错误中心](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode)查看更多错误码。

<a id="变更历史"></a>

<a id="workbench-doc-change-demo"></a>

## 变更历史

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/QueryVideoAuditResult#workbench-doc-change-demo)。
