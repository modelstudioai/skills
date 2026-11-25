# GetIndexMonitor - 获取知识库监控数据

调用GetIndexMonitor接口，查询指定知识库在特定时间范围内的监控数据。这些数据对于性能分析、容量规划和成本管理至关重要。 监控数据主要包含两大维度： 存储监控：获取知识库的索引存储限额和当前使用量。 检索（QPS）监控：获取查询时间段内总的及按时间窗口细分的检索性能指标，包括QPS峰值、总请求数、平均QPS，并细分为成功、失败和被限流的请求。

<a id="接口说明"></a>

<a id="api-detail-51"></a>

## 接口说明

-   RAM 用户（子账号）需要首先获取阿里云百炼的 [API 权限](../model-user-guide/security-and-compliance/permission-management-overview.md)（需要`AliyunBailianDataFullAccess`），并加入一个业务空间后，方可调用本接口。阿里云账号（主账号）可直接调用无须授权。建议您通过最新版[阿里云百炼 SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)来调用本接口。
-   调用本接口前，请确保您的知识库已经创建完成且未被删除（即知识库 ID `IndexId` 有效）。
-   本接口具有幂等性。
-   查询时间范围（`EndTimestamp` - `StartTimestamp`）最大支持 30 天。
-   返回数据中的时间窗口粒度会根据您查询的时间范围动态调整。

<a id="调试"></a>

<a id="api-detail-23"></a>

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

[调试](https://api.aliyun.com/api/bailian/2023-12-29/GetIndexMonitor)

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
    

<table><thead><tr><th>操作</th><th>访问级别</th><th>资源类型</th><th>条件关键字</th><th>关联操作</th></tr></thead><tbody><tr><td>sfm:GetIndexMonitor</td><td>get</td><td><div><div>*全部资源</div><div><code>*</code></div></div></td><td><ul>无</ul></td><td>无</td></tr></tbody></table>

<a id="请求语法"></a>

<a id="api-detail-53"></a>

## 请求语法

<a id="code-block"></a>

```text
GET /{WorkspaceId}/rag/index/monitor HTTP/1.1
```

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

| 名称 | 类型 | 必填 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| WorkspaceId | string | 是 | 知识库所在工作空间 ID | llm-3shx2gu255oqxxxx |
| IndexId | string | 是 | 目标知识库的唯一 ID | kb-123456xxxx |
| StartTimestamp | long | 是 | 查询起始时间，秒级 Unix 时间戳 | 1767604500 |
| EndTimestamp | long | 是 | 查询结束时间，最大支持起始时间+30d，秒级 Unix 时间戳 | 1767604500 |

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

<table><thead><tr><th><p>名称</p></th><th><p>类型</p></th><th><p>描述</p></th><th><p>示例值</p></th></tr></thead><tbody><tr><td></td><td><p>object</p></td><td><p>Schema of Response</p></td><td></td></tr><tr><td><p>RequestId</p></td><td><p>string</p></td><td><p>请求 ID</p></td><td><p>778C0B3B-xxxx-5FC1-A947-36EDD13606AB</p></td></tr><tr><td><p>Code</p></td><td><p>string</p></td><td><p>状态码</p></td><td><p>200</p></td></tr><tr><td><p>Data</p></td><td><p>any</p></td><td><p>响应的核心数据对象。</p><p><strong>pipelineCommercialType</strong>(String):知识库规格</p><ul><li>standard：标准版</li><li>enterprise：旗舰版</li></ul><p><strong>storageMonitorData</strong>(Object): 知识库的存储监控数据</p><ul><li>indexStorageLimit(Number): 知识库的索引存储限额，单位为 GB。</li><li>indexStorageUsage(Number): 知识库当前已占用的索引存储额度，单位为 GB。</li></ul><p><strong>pipelineCommercialCu</strong>（Integer）：表示旗舰版知识库的 RCU，如 2。</p><p><strong>qpsMonitorData</strong> (Object): 知识库在整个查询时间段内的检索（QPS）聚合监控数据</p><ul><li><p>peakQps(Integer): 整个时间段内的最高 QPS 峰值</p></li><li><p>totalRequests(Integer): 整个时间段内的总请求次数</p></li><li><p>avgQpsOfActiveSeconds(Number): 整个时间段内，所有活跃秒（即有调用的秒）的平均 QPS</p></li><li><p>monitorData(Array): 按时间窗口划分的详细监控数据数组。数组中的每个对象代表一个时间窗口的统计信息。</p><a id="accordion-details"></a><section><p>Details</p><div><strong>子属性</strong><ul><li>successData(Object):该窗口内请求成功的统计数据。</li><li>limitData(Object): 该窗口内被限流的统计数据。</li><li>failData(Object): 该窗口内调用失败的统计数据。</li><li>peakQpsInWindowRange(Integer): 该窗口内的总 QPS 峰值（成功+限流+失败）。</li><li>totalRequests(Integer): 该窗口内的总请求数（成功+限流+失败）。</li><li>windowRange(Integer): 时间窗口的开始时间（秒级 Unix 时间戳）。</li><li>windowRangeEnd(Integer): 时间窗口的结束时间（秒级 Unix 时间戳）。</li><li>avgQpsOfActiveSeconds(Number): 该窗口内活跃秒的平均 QPS。</li></ul><strong>successData, limitData, failData 这三个对象的内部结构完全相同，具体如下：</strong><ul><li>peakQpsInWindowRange(Integer): 对应状态下的 QPS 峰值。</li><li>totalRequests(Integer): 对应状态下的总请求数。</li><li>avgQpsOfActiveSeconds(Number): 对应状态下活跃秒的平均 QPS。</li></ul></div></section></li></ul></td><td><p>{ &quot;code&quot;: &quot;Success&quot;, &quot;status_code&quot;: 200, &quot;data&quot;: { &quot;pipelineCommercialType&quot;: &quot;standard&quot;, &quot;storageMonitorData&quot;: Object{...}, &quot;qpsMonitorData&quot;: Object{...} }, &quot;success&quot;: true, &quot;message&quot;: &quot;success&quot;, &quot;request_id&quot;: &quot;65d34b79-b97e-478e-a0a3-xxx&quot;, &quot;status&quot;: &quot;SUCCESS&quot; }</p></td></tr><tr><td><p>Message</p></td><td><p>string</p></td><td><p>状态信息</p></td><td><p>success</p></td></tr><tr><td><p>Success</p></td><td><p>boolean</p></td><td><p>请求是否成功</p></td><td><p>true</p></td></tr><tr><td><p>Status</p></td><td><p>integer</p></td><td><p>接口返回的状态码</p></td><td><p>SUCCESS</p></td></tr></tbody></table>

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-2"></a>

```text
{
  "RequestId": "778C0B3B-xxxx-5FC1-A947-36EDD13606AB",
  "Code": 200,
  "Data": "{\n    \"code\": \"Success\",\n    \"status_code\": 200,\n    \"data\": {\n\"pipelineCommercialType\": \"standard\",       \"storageMonitorData\": Object{...},\n        \"qpsMonitorData\": Object{...}\n    },\n    \"success\": true,\n    \"message\": \"success\",\n    \"request_id\": \"65d34b79-b97e-478e-a0a3-xxx\",\n    \"status\": \"SUCCESS\"\n}",
  "Message": "success",
  "Success": true,
  "Status": 0
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

访问[错误中心](https://api.aliyun.com/document/bailian/2023-12-29/errorCode)查看更多错误码。

<a id="变更历史"></a>

<a id="workbench-doc-change-demo"></a>

## 变更历史

| 变更时间 | 变更内容概要 | 操作 |
| --- | --- | --- |
| 2026-01-14 | 新增 OpenAPI | [查看变更详情](https://api.aliyun.com/document/bailian/2023-12-29/GetIndexMonitor?updateTime=2026-01-14#workbench-doc-change-demo) |
