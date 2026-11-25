# GetBillingTrend

查询指定时间范围内的账单趋势信息，支持按天或按月聚合，并按维度分组和筛选。

<a id="请求语法"></a>

<a id="api-detail-35"></a>

## 请求语法

<a id="code-block"></a>

```text
GET /modelstudio/billing/trend HTTP/1.1
```

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

<table><thead><tr><th><p><strong>名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>必填</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td>granularity</td><td><p>string</p></td><td><p>是</p></td><td><div><p>查询粒度，不能为空。取值：</p><ul><li><p>MONTH：按月</p></li><li><p>DAY：按天</p></li></ul></div></td><td><p>DAY</p></td></tr><tr><td>timePeriod</td><td><p>object</p></td><td><p>是</p></td><td><div><p>查询时间范围，包含开始和结束时间，不能为空。</p></div></td><td></td></tr><tr><td>timePeriod.start</td><td><p>string</p></td><td><p>是</p></td><td><div><p>开始时间，格式为 YYYY-MM-DD。</p></div></td><td><p>2026-08-01</p></td></tr><tr><td>timePeriod.end</td><td><p>string</p></td><td><p>是</p></td><td><div><p>结束时间，格式为 YYYY-MM-DD。</p></div></td><td><p>2026-08-31</p></td></tr><tr><td>groupBy</td><td><p>array&lt;object&gt;</p></td><td><p>是</p></td><td><div><p>分组条件，必须且只能包含一个元素。支持的维度 Code 见下方补充说明。</p></div></td><td></td></tr><tr><td>groupBy.code</td><td><p>string</p></td><td><p>是</p></td><td><div><p>维度 Code。</p></div></td><td><p>MAAS_TYPE</p></td></tr><tr><td>filter</td><td><p>object</p></td><td><p>否</p></td><td><div><p>维度过滤条件。</p></div></td><td></td></tr><tr><td>filter.dimensions</td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><div><p>筛选维度列表。</p></div></td><td></td></tr><tr><td>filter.dimensions.code</td><td><p>string</p></td><td><p>否</p></td><td><div><p>维度 Code。</p></div></td><td><p>BASE_MODEL</p></td></tr><tr><td>filter.dimensions.values</td><td><p>array&lt;string&gt;</p></td><td><p>否</p></td><td><div><p>筛选值列表。</p></div></td><td><p>[&quot;qwen-max&quot;]</p></td></tr><tr><td>filter.dimensions.selectType</td><td><p>string</p></td><td><p>否</p></td><td><div><p>筛选类型。取值：</p><ul><li><p>IN</p></li><li><p>NOT</p></li></ul></div></td><td><p>IN</p></td></tr><tr><td>topNum</td><td><p>integer</p></td><td><p>否</p></td><td><div><p>返回分组数量，范围为 1～20，默认 20。其余分组合并为&quot;其他&quot;。</p></div></td><td><p>20</p></td></tr><tr><td>zeroFilter</td><td><p>boolean</p></td><td><p>否</p></td><td><div><p>是否过滤金额为 0 的分组，默认 true。</p></div></td><td><p>true</p></td></tr><tr><td>regionId</td><td><p>string</p></td><td><p>否</p></td><td><div><p>地域 ID。</p></div></td><td><p>cn-beijing</p></td></tr><tr><td>locale</td><td><p>string</p></td><td><p>否</p></td><td><div><p>返回语言，默认 en-US。取值：</p><ul><li><p>en-US：英文</p></li><li><p>zh-CN：中文</p></li></ul></div></td><td><p>zh-CN</p></td></tr></tbody></table>

**补充说明**

`groupBy[].code` 和 `filter.dimensions[].code` 支持以下值，建议统一使用大写：

| 维度 Code | 含义 | filter.dimensions\[\].values 可传值 |
| --- | --- | --- |
| MAAS\_TYPE | MaaS 业务类型 | inference（模型调用）、training（模型训练）、model\_units（模型单元）、capacity\_reserved（容量预留） |
| BASE\_MODEL | 基础模型 | 账单数据中的基础模型原始值，例如 qwen-plus |
| API\_KEY\_ID | API Key ID | 账单数据中的 API Key ID 原始值 |
| WORKSPACE\_ID | 业务空间 ID | 账单数据中的 Workspace ID 原始值 |
| FEE\_TYPE | 费用类型 | billing（账单费用）、subscription（订阅购买费用） |
| CHARGE\_TYPE | 付费类型 | postpaid（后付费）、prepaid（预付费） |
| BUSINESS\_REGION | 业务地域 | cn-beijing、ap-southeast-1、cn-hongkong 等，取值以实际值为准 |
| SERVICE\_SITE | 服务站点 | asia-pacific-china、global、international 等，取值以实际值为准 |
| ARTICLE\_CODE | 商品 Code | sfm\_inferenceglobal\_public\_intl 等，取值以实际值为准 |

> **说明**
>
> 所有维度的 `filter.dimensions[].values` 均可传 `DIMENSION_FILTER_NULL_VALUE`，表示匹配字段为 NULL 或空字符串的数据。

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

| 名称 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
| requestId | string | 请求 ID。 | 099A671E-FA21-5A36-8A73-918572DDEF53 |
| code | string | 请求结果代码。 | 200 |
| message | string | 请求结果说明。 | null |
| success | boolean | 请求是否成功。 | true |
| data | object | 返回数据。 |  |
| data.costTotals | object | 整个查询时间范围内的费用合计，包含 TopN 和"其他"。 |  |
| data.costTotals.amount | string | 费用总金额 | 100 |
| data.costTotals.pretaxAmount | string | 不含税金额 | 94.34 |
| data.costTotals.taxAmount | string | 税费金额 | 5.66 |
| data.costTotals.currency | string | 金额币种 | CNY |
| data.groupByTotal | array<object> | 周期内 TopN 分组及可选"其他"分组的费用合计 |  |
| data.groupByTotal.key | string | 分组维度值 | qwen-plus |
| data.groupByTotal.name | string | 分组展示名称，受入参 locale 影响 | qwen-plus |
| data.groupByTotal.amount | string | 当前分组的总金额 | 60 |
| data.groupByTotal.pretaxAmount | string | 当前分组的不含税金额 | 56.60 |
| data.groupByTotal.taxAmount | string | 当前分组的税费金额 | 3.40 |
| data.resultByTime | array<object> | 按时间升序排列的费用趋势列表 |  |
| data.resultByTime.period | string | 统计周期。DAY 返回 yyyyMMdd，MONTH 返回 yyyyMM。 | 20260801 |
| data.resultByTime.total | object | 当前周期的费用合计 |  |
| data.resultByTime.total.amount | string | 当前周期的费用总金额 | 30 |
| data.resultByTime.total.pretaxAmount | string | 当前周期的不含税金额 | 28.30 |
| data.resultByTime.total.taxAmount | string | 当前周期的税费金额 | 1.70 |
| data.resultByTime.total.currency | string | 当前周期的金额币种 | CNY |
| data.resultByTime.periodDetails | array<object> | 当前周期实际存在的费用分组 |  |
| data.resultByTime.periodDetails.key | string | 分组维度值。TopN 以外的数据使用 DIMENSION\_GROUP\_OTHERS\_VALUE。 | qwen-plus |
| data.resultByTime.periodDetails.name | string | 分组展示名称，受入参 locale 影响。 | qwen-plus |
| data.resultByTime.periodDetails.amount | string | 当前周期内该分组的金额 | 20 |
| data.resultByTime.periodDetails.pretaxAmount | string | 当前周期内该分组的不含税金额 | 18.87 |
| data.resultByTime.periodDetails.taxAmount | string | 当前周期内该分组的税费金额 | 1.13 |
| data.resultByTime.periodDetails.percentage | string | 当前分组金额占当前周期总金额的比例 | 0.6667 |

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-2"></a>

```json
{
  "requestId": "099A671E-FA21-5A36-8A73-918572DDEF53",
  "code": "200",
  "message": "null",
  "success": true,
  "data": {
    "costTotals": {
      "amount": "100",
      "pretaxAmount": "94.34",
      "taxAmount": "5.66",
      "currency": "CNY"
    },
    "groupByTotal": [
      {
        "key": "qwen-plus",
        "name": "qwen-plus",
        "amount": "60",
        "pretaxAmount": "56.60",
        "taxAmount": "3.40"
      }
    ],
    "resultByTime": [
      {
        "period": "20260801",
        "total": {
          "amount": "30",
          "pretaxAmount": "28.30",
          "taxAmount": "1.70",
          "currency": "CNY"
        },
        "periodDetails": [
          {
            "key": "qwen-plus",
            "name": "qwen-plus",
            "amount": "20",
            "pretaxAmount": "18.87",
            "taxAmount": "1.13",
            "percentage": "0.6667"
          }
        ]
      }
    ]
  }
}
```
