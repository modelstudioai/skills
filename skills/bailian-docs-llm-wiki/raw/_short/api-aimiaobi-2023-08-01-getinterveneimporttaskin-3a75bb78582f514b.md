# GetInterveneImportTaskInfo - 获得干预项目导入任务信息

获得导入任务信息。

<a id="调试"></a>

<a id="api-detail-23"></a>

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

[调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetInterveneImportTaskInfo)

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
    

<table><thead><tr><th>操作</th><th>访问级别</th><th>资源类型</th><th>条件关键字</th><th>关联操作</th></tr></thead><tbody><tr><td>aimiaobi:GetInterveneImportTaskInfo</td><td>get</td><td><div><div>*全部资源</div><div><code>*</code></div></div></td><td><ul>无</ul></td><td>无</td></tr></tbody></table>

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

| 名称 | 类型 | 必填 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| AgentKey | string | 是 | 业务空间唯一标识： [AgentKey](https://help.aliyun.com/zh/model-studio/get-accesskey-appid-and-agentkey) | 67c520d1fa43455ea44fb69fa402d54d\_p\_beebot\_public |
| TaskId | string | 否 | 任务唯一标识<br><br>**说明** TaskId 默认无需填写，系统将自动生成。当后续任务填写的 TaskId 相同时，表示这些任务属于同一组对话。 | 19162157 |

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

<table><thead><tr><th>名称</th><th>类型</th><th>描述</th><th>示例值</th></tr></thead><tbody><tr><td></td><td>object</td><td><div><p>PlainResult</p></div></td><td></td></tr><tr><td>Code</td><td>string</td><td><div><p>状态码</p></div></td><td>0</td></tr><tr><td>Data</td><td>object</td><td><div><p>业务数据</p></div></td><td></td></tr><tr><td>Status</td><td>object</td><td><div><p>任务状态信息</p></div></td><td></td></tr><tr><td>Msg</td><td>string</td><td><div><p>任务信息</p></div></td><td>success</td></tr><tr><td>Percentage</td><td>integer</td><td><div><p>完成百分比</p></div></td><td>80</td></tr><tr><td>Status</td><td>integer</td><td><div><p>任务状态</p></div><div><div>枚举值：</div><ul><li>3-超时：3-超时。</li><li>2-错误：2-错误。</li><li>1-进行中 ： 1-进行中 。</li><li>0-结束：0-结束。</li></ul></div></td><td>0</td></tr><tr><td>TaskId</td><td>string</td><td><div><p>任务 Id</p></div></td><td>41405255</td></tr><tr><td>TaskName</td><td>string</td><td><div><p>任务名字</p></div></td><td>ft-task-20190101m8rnK</td></tr><tr><td>HttpStatusCode</td><td>integer</td><td><div><p>http 状态码</p></div></td><td>200</td></tr><tr><td>Message</td><td>string</td><td><div><p>错误说明</p></div></td><td>Success</td></tr><tr><td>RequestId</td><td>string</td><td><div><p>请求唯一标识</p></div></td><td>1813ceee-7fe5-41b4-87e5-982a4d18cca5</td></tr><tr><td>Success</td><td>boolean</td><td><div><p>是否成功：true 成功，false 失败</p></div></td><td>true</td></tr></tbody></table>

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block"></a>

```text
{
  "Code": 0,
  "Data": {
    "Status": {
      "Msg": "success",
      "Percentage": 80,
      "Status": 0,
      "TaskId": 41405255,
      "TaskName": "ft-task-20190101m8rnK"
    },
    "Code": 0
  },
  "HttpStatusCode": 200,
  "Message": "Success",
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "Success": true
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

访问[错误中心](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode)查看更多错误码。
