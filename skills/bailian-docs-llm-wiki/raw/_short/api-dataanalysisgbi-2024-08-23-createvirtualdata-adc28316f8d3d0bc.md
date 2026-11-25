# CreateVirtualDatasourceInstance - 创建虚拟数据源实例

在您指定的业务空间创建虚拟数据源实例，虚拟数据源实例代表着一个虚拟的数据库，可以向虚拟数据源中添加ddl语句，来完成您构建虚拟数据库，数据表的能力。

<a id="调试"></a>

<a id="api-detail-23"></a>

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

[调试](https://api.aliyun.com/api/DataAnalysisGBI/2024-08-23/CreateVirtualDatasourceInstance)

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
    

<table><thead><tr><th>操作</th><th>访问级别</th><th>资源类型</th><th>条件关键字</th><th>关联操作</th></tr></thead><tbody><tr><td>dataanalysisgbi:CreateVirtualDatasourceInstance</td><td>none</td><td><div><div>*全部资源</div><div><code>*</code></div></div></td><td><ul>无</ul></td><td>无</td></tr></tbody></table>

<a id="请求语法"></a>

<a id="api-detail-53"></a>

## 请求语法

<a id="code-block"></a>

```text
POST /gbi/virtualDatasource/createVirtualDatasourceInstance HTTP/1.1
```

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

<table><thead><tr><th>名称</th><th>类型</th><th>必填</th><th>描述</th><th>示例值</th></tr></thead><tbody><tr><td>workspaceId</td><td>string</td><td>是</td><td><div><p>当前请求所使用的阿里云百炼业务空间 id</p></div></td><td>llm-2v3934xtp49esw64</td></tr><tr><td>body</td><td>object</td><td>否</td><td><div><p>请求体参数</p></div></td><td></td></tr><tr><td>name</td><td>string</td><td>否</td><td><div><p>虚拟数据源实例的名字</p></div></td><td>virtual-instance-1</td></tr><tr><td>description</td><td>string</td><td>否</td><td><div><p>虚拟数据源实例的描述</p></div></td><td>虚拟数据源实例的描述</td></tr><tr><td>type</td><td>integer</td><td>否</td><td><div><p>当前虚拟数据源的类型</p></div><div><div>枚举值：</div><ul><li>51：mysql类型虚拟数据源。</li><li>52：postgresql类型虚拟数据源。</li></ul></div></td><td>51</td></tr></tbody></table>

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

| 名称 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
|  | object | Result |  |
| data | any | 响应数据。即成功与否。 | true |
| errorMsg | string | 错误信息 | NoAuth |
| code | string | 错误码。 | NoAuth |
| success | boolean | true 接口调用成功，false 接口调用失败 | true |
| requestId | string | 请求 id，每次请求都是唯一值，便于后续排查问题 | D02D895A-5E58-5A9F-963D-D8B027AB7AE2 |

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-2"></a>

```text
{
  "data": true,
  "errorMsg": "NoAuth",
  "code": "NoAuth",
  "success": true,
  "requestId": "D02D895A-5E58-5A9F-963D-D8B027AB7AE2"
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

| HTTP status code | 错误码 | 错误信息 | 描述 |
| --- | --- | --- | --- |
| 401 | NoAuth | Bad Request: Workspace.Illegal.Auth. | 当前所使用的账号无所指定业务空间的权限 |
| 401 | Internal.Error | Bad Request: Internal Error. | 内部错误，请联系客服人员排查 |

访问[错误中心](https://api.aliyun.com/document/DataAnalysisGBI/2024-08-23/errorCode)查看更多错误码。
