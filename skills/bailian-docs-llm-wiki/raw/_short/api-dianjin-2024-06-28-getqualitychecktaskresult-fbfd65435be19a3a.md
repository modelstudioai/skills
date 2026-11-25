# GetQualityCheckTaskResult - 获取质检结果

获取质检结果。

<a id="调试"></a>

<a id="api-detail-23"></a>

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

[调试](https://api.aliyun.com/api/DianJin/2024-06-28/GetQualityCheckTaskResult)

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
    

<table><thead><tr><th>操作</th><th>访问级别</th><th>资源类型</th><th>条件关键字</th><th>关联操作</th></tr></thead><tbody><tr><td>dianjin:GetQualityCheckTaskResult</td><td>get</td><td><div><div>*全部资源</div><div><code>*</code></div></div></td><td><ul>无</ul></td><td>无</td></tr></tbody></table>

<a id="请求语法"></a>

<a id="api-detail-53"></a>

## 请求语法

<a id="code-block"></a>

```text
GET /{workspaceId}/api/qualitycheck/task/query HTTP/1.1
```

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

| 名称 | 类型 | 必填 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| workspaceId | string | 是 | 业务空间 Id | llm-xxxxx |
| taskId | string | 是 | 任务 ID | 17071319 |

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

<table><thead><tr><th>名称</th><th>类型</th><th>描述</th><th>示例值</th></tr></thead><tbody><tr><td></td><td>object</td><td><div><p>ResultCode</p></div></td><td></td></tr><tr><td>cost</td><td>long</td><td><div><p>耗时</p></div></td><td>null</td></tr><tr><td>data</td><td>object</td><td><div><p>响应数据</p></div></td><td></td></tr><tr><td>conversationList</td><td>object</td><td><div><p>原始会话内容</p></div></td><td></td></tr><tr><td>callType</td><td>string</td><td><div><p>呼叫类型:</p></div><div><div>枚举值：</div><ul><li>1：呼入。</li><li>2：呼出。</li></ul></div></td><td>1</td></tr><tr><td>customerId</td><td>string</td><td><div><p>客户 ID</p></div></td><td>234234</td></tr><tr><td>customerName</td><td>string</td><td><div><p>客户名称</p></div></td><td>张三</td></tr><tr><td>customerServiceId</td><td>string</td><td><div><p>客服 ID</p></div></td><td>23984763826</td></tr><tr><td>customerServiceName</td><td>string</td><td><div><p>客服名称</p></div></td><td>李四</td></tr><tr><td>dialogueList</td><td>array&lt;object&gt;</td><td><div><p>对话明细列表</p></div></td><td></td></tr><tr><td>dialogueList</td><td>object</td><td><div><p>对话明细</p></div></td><td></td></tr><tr><td>begin</td><td>integer</td><td><div><p>本句话的开始时间，相对于会话开始点的偏移时间 ms</p></div></td><td>0</td></tr><tr><td>beginTime</td><td>string</td><td><div><p>这句话的开始时间</p></div></td><td>2024-09-27 11:23:20</td></tr><tr><td>content</td><td>string</td><td><div><p>对话的具体内容</p></div></td><td>您好，我是2001，很高兴为您服务！</td></tr><tr><td>customerId</td><td>string</td><td><div><p>对话角色的唯一标识</p></div></td><td>null</td></tr><tr><td>customerServiceId</td><td>string</td><td><div><p>客服 ID</p></div></td><td>李四</td></tr><tr><td>customerServiceType</td><td>string</td><td><div><p>坐席类型</p></div><div><div>枚举值：</div><ul><li>0：机器人。</li><li>1：人工。</li></ul></div></td><td>0</td></tr><tr><td>end</td><td>integer</td><td><div><p>本句话的结束时间，相对于会话开始点的偏移时间 ms</p></div></td><td>0</td></tr><tr><td>id</td><td>integer</td><td><div><p>本句话的唯一标识,内部赋值</p></div></td><td>1</td></tr><tr><td>role</td><td>string</td><td><div><p>角色</p></div><div><div>枚举值：</div><ul><li>0：客户。</li><li>1：坐席。</li></ul></div></td><td>0</td></tr><tr><td>type</td><td>string</td><td><div><p>对话内容的类型</p></div><div><div>枚举值：</div><ul><li>IMAGE：图片。</li><li>TEXT：文本。</li><li>AUDIO：语音。</li></ul></div></td><td>TEXT</td></tr><tr><td>gmtService</td><td>string</td><td><div><p>会话时间</p></div></td><td>2024-09-27 11:23:20</td></tr><tr><td>gmtCreate</td><td>string</td><td><div><p>任务创建时间，提交任务的时间</p></div></td><td>2024-09-27 11:23:20</td></tr><tr><td>gmtEnd</td><td>string</td><td><div><p>系统执行结束时间</p></div></td><td>2024-09-27 11:23:20</td></tr><tr><td>gmtStart</td><td>string</td><td><div><p>系统执行开始时间</p></div></td><td>2024-09-27 11:23:20</td></tr><tr><td>qualityCheckList</td><td>array&lt;object&gt;</td><td><div><p>质检结果集</p></div></td><td></td></tr><tr><td>qualityCheckList</td><td>object</td><td><div><p>质检结果</p></div></td><td></td></tr><tr><td>checkExplanation</td><td>string</td><td><div><p>通过或者不通过的原因解释</p></div></td><td>暂无</td></tr><tr><td>checkPassed</td><td>string</td><td><div><p>是否质检通过</p></div><div><div>枚举值：</div><ul><li>NOT_PASSED：不通过。</li><li>PASSED：通过。</li></ul></div></td><td>PASSED</td></tr><tr><td>checkProcess</td><td>string</td><td><div><p>质检过程描述</p></div></td><td>暂无</td></tr><tr><td>checked</td><td>string</td><td><div><p>是否命中</p></div><div><div>枚举值：</div><ul><li>HIT：命中。</li><li>NOT_HIT：未命中。</li></ul></div></td><td>HIT</td></tr><tr><td>gmtEnd</td><td>string</td><td><div><p>质检完成时间</p></div></td><td>2024-05-23 14:57:50</td></tr><tr><td>gmtStart</td><td>string</td><td><div><p>质检开始时间</p></div></td><td>2024-05-23 14:57:50</td></tr><tr><td>mode</td><td>string</td><td><div><p>内部质检模式</p></div><div><div>枚举值：</div><ul><li>0：大模型质检。</li></ul></div></td><td>0</td></tr><tr><td>originDialogue</td><td>array&lt;object&gt;</td><td><div><p>原始对话列表</p></div></td><td></td></tr><tr><td>originDialogue</td><td>object</td><td><div><p>原始对话</p></div></td><td></td></tr><tr><td>begin</td><td>integer</td><td><div><p>本句话的开始时间，相对于会话开始点的偏移时间 ms</p></div></td><td>0</td></tr><tr><td>beginTime</td><td>string</td><td><div><p>这句话的开始时间</p></div></td><td>2024-05-23 14:57:50</td></tr><tr><td>content</td><td>string</td><td><div><p>对话的具体内容</p></div></td><td>您好，我是2001，很高兴为您服务！</td></tr><tr><td>customerId</td><td>string</td><td><div><p>对话角色的唯一标识</p></div></td><td>xxx</td></tr><tr><td>customerServiceId</td><td>string</td><td><div><p>客服 ID</p></div></td><td>23876432</td></tr><tr><td>customerServiceType</td><td>string</td><td><div><p>坐席类型</p></div><div><div>枚举值：</div><ul><li>0：机器人。</li><li>1：人工。</li></ul></div></td><td>0</td></tr><tr><td>end</td><td>integer</td><td><div><p>本句话的结束时间，相对于会话开始点的偏移时间 ms</p></div></td><td>0</td></tr><tr><td>id</td><td>integer</td><td><div><p>本句话的唯一标识，内部赋值</p></div></td><td>1</td></tr><tr><td>role</td><td>string</td><td><div><p>角色</p></div><div><div>枚举值：</div><ul><li>0：客户。</li><li>1：坐席。</li></ul></div></td><td>0</td></tr><tr><td>type</td><td>string</td><td><div><p>对话内容的类型</p></div><div><div>枚举值：</div><ul><li>IMAGE：图片。</li><li>TEXT：文本。</li><li>AUDIO：语音。</li></ul></div></td><td>TEXT</td></tr><tr><td>qualityGroupId</td><td>string</td><td><div><p>质检组 ID</p></div></td><td>warning_customers</td></tr><tr><td>ruleDescription</td><td>string</td><td><div><p>质检项描述</p></div></td><td>进入检测预警客户流程</td></tr><tr><td>ruleId</td><td>string</td><td><div><p>质检项 ID</p></div></td><td>wcm_start</td></tr><tr><td>bizType</td><td>string</td><td><div><p>规则业务类型</p></div></td><td>No</td></tr><tr><td>ruleType</td><td>string</td><td><div><p>规则正负向类型 0：负向，1：正向。</p></div></td><td>0</td></tr><tr><td>subNodeCol</td><td>array</td><td><div><p>子节点</p></div></td><td></td></tr><tr><td>subNodeCol</td><td>any</td><td><div><p>子节点的质检结果，结构与 qualityCheckList 相同</p></div></td><td>{ &quot;ruleId&quot;: &quot;wxx_regulatory_authorities&quot;, &quot;ruleDescription&quot;: &quot;具体某机构预警&quot;, &quot;checked&quot;: &quot;HIT&quot;, &quot;checkProcess&quot;: &quot;通过审查对话记录，客户主要询问了关于贷款资方信息和结清证明的问题，并表达了想要注销账户的意愿。在整个对话过程中，客户并未提及任何具体的部门名称，也没有明确表示要向部门投诉的意图。&quot;, &quot;originDialogue&quot;: null, &quot;checkPassed&quot;: &quot;NOT_PASSED&quot;, &quot;checkExplanation&quot;: null, &quot;mode&quot;: &quot;0&quot;, &quot;gmtStart&quot;: &quot;2024-12-02 10:38:39&quot;, &quot;gmtEnd&quot;: &quot;2024-12-02 10:38:43&quot;, &quot;qualityGroupId&quot;: &quot;warning_customers&quot;, &quot;bizType&quot;: null, &quot;ruleType&quot;: &quot;0&quot;, &quot;subNodeCol&quot;: null }</td></tr><tr><td>status</td><td>string</td><td><div><p>任务状态</p></div><div><div>枚举值：</div><ul><li>CANCELLED：已取消。</li><li>INIT：初始化。</li><li>COMPLETED：已结束。</li><li>PROCESSING：进行中。</li><li>FAIL：失败。</li></ul></div></td><td>INIT</td></tr><tr><td>taskId</td><td>string</td><td><div><p>任务 ID</p></div></td><td>1703557101831</td></tr><tr><td>dataType</td><td>string</td><td><div><p>数据类型</p></div></td><td>null</td></tr><tr><td>errCode</td><td>string</td><td><div><p>错误码</p></div></td><td>0</td></tr><tr><td>message</td><td>string</td><td><div><p>错误信息</p></div></td><td>ok</td></tr><tr><td>requestId</td><td>string</td><td><div><p>请求 id</p></div></td><td>67C7021A-D268-553D-8C15-A087B9604028</td></tr><tr><td>success</td><td>boolean</td><td><div><p>是否成功</p></div></td><td>true</td></tr><tr><td>time</td><td>string</td><td><div><p>时间戳</p></div></td><td>2024-01-01 00:00:00</td></tr></tbody></table>

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-2"></a>

```text
{
  "cost": 0,
  "data": {
    "conversationList": {
      "callType": 1,
      "customerId": 234234,
      "customerName": "张三",
      "customerServiceId": 23984763826,
      "customerServiceName": "李四",
      "dialogueList": [
        {
          "begin": 0,
          "beginTime": "2024-09-27 11:23:20",
          "content": "您好，我是2001，很高兴为您服务！",
          "customerId": null,
          "customerServiceId": "李四",
          "customerServiceType": 0,
          "end": 0,
          "id": 1,
          "role": 0,
          "type": "TEXT"
        }
      ],
      "gmtService": "2024-09-27 11:23:20"
    },
    "gmtCreate": "2024-09-27 11:23:20",
    "gmtEnd": "2024-09-27 11:23:20",
    "gmtStart": "2024-09-27 11:23:20",
    "qualityCheckList": [
      {
        "checkExplanation": "暂无",
        "checkPassed": "PASSED",
        "checkProcess": "暂无",
        "checked": "HIT",
        "gmtEnd": "2024-05-23 14:57:50",
        "gmtStart": "2024-05-23 14:57:50",
        "mode": 0,
        "originDialogue": [
          {
            "begin": 0,
            "beginTime": "2024-05-23 14:57:50",
            "content": "您好，我是2001，很高兴为您服务！",
            "customerId": "xxx",
            "customerServiceId": 23876432,
            "customerServiceType": 0,
            "end": 0,
            "id": 1,
            "role": 0,
            "type": "TEXT"
          }
        ],
        "qualityGroupId": "warning_customers",
        "ruleDescription": "进入检测预警客户流程",
        "ruleId": "wcm_start",
        "bizType": "No",
        "ruleType": 0,
        "subNodeCol": [
          {
            "ruleId": "wxx_regulatory_authorities",
            "ruleDescription": "具体某机构预警",
            "checked": "HIT",
            "checkProcess": "通过审查对话记录，客户主要询问了关于贷款资方信息和结清证明的问题，并表达了想要注销账户的意愿。在整个对话过程中，客户并未提及任何具体的部门名称，也没有明确表示要向部门投诉的意图。",
            "originDialogue": null,
            "checkPassed": "NOT_PASSED",
            "checkExplanation": null,
            "mode": 0,
            "gmtStart": "2024-12-02 10:38:39",
            "gmtEnd": "2024-12-02 10:38:43",
            "qualityGroupId": "warning_customers",
            "bizType": null,
            "ruleType": 0,
            "subNodeCol": null
          }
        ]
      }
    ],
    "status": "INIT",
    "taskId": 1703557101831
  },
  "dataType": null,
  "errCode": 0,
  "message": "ok",
  "requestId": "67C7021A-D268-553D-8C15-A087B9604028",
  "success": true,
  "time": "2024-01-01 00:00:00"
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

访问[错误中心](https://api.aliyun.com/document/DianJin/2024-06-28/errorCode)查看更多错误码。

<a id="变更历史"></a>

<a id="workbench-doc-change-demo"></a>

## 变更历史

| 变更时间 | 变更内容概要 | 操作 |
| --- | --- | --- |

暂无变更历史
