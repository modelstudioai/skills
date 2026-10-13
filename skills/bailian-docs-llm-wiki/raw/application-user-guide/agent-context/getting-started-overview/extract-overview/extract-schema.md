# Schema规则参考

说明文档抽取服务的 \`extract\_schema\`（抽取 schema）参数规则、限制与使用方法

## 概述

`schema` 用于定义「从文档中抽取哪些字段、每个字段是什么类型」，是抽取请求的必传参数。

本服务的 schema 兼容 LlamaIndex 的 JSON Schema 格式，但**使用限制与 LlamaIndex 不完全相同**（如嵌套深度、字段数、大小上限），以本文档为准。

## JSON Schema 格式

### 基本结构

```
{
  "description": "发票信息抽取",
  "type": "object",
  "properties": {
    "invoice_number": {"description": "发票号码", "type": "string"},
    "invoice_date": {"description": "开票日期，格式 YYYY-MM-DD", "type": "string"},
    "total_amount": {"description": "价税合计金额，单位元", "type": "number"},
    "is_electronic": {"description": "是否电子发票", "type": "boolean"},
    "buyer": {
      "description": "购方信息",
      "type": "object",
      "properties": {
        "name": {"description": "购方名称", "type": "string"},
        "tax_id": {"description": "购方税号", "type": "string"}
      },
      "required": ["name"]
    },
    "line_items": {
      "description": "明细行",
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "item_name": {"description": "项目名称", "type": "string"},
          "quantity": {"description": "数量", "type": "integer"},
          "amount": {"description": "金额，单位元", "type": "number"}
        }
      }
    }
  },
  "required": ["invoice_number", "total_amount"]
}
```

### 格式判定

以下任一情况，schema 会按 JSON Schema 格式解析：

1.  顶层同时包含 `description`、`properties`、`required` 三个键；
2.  `type` 为 `"object"` 且 `properties` 为非空对象、其中每个字段定义都是对象（即标准 JSON Schema 形态，如 Pydantic 生成的结果）。

其余情况按旧版描述串格式解析。为避免歧义，建议始终在顶层写明 `"type": "object"`。

### 支持的类型

类型

说明

结果值示例

`string`

文本

`"12345"`

`integer`

整数

`12`

`number`

数字（整数或小数）

`12.5`

`boolean`

布尔

`true`

`object`

嵌套对象，必须有 `properties`

`{"name": "xx"}`

`array`

数组，必须有 `items`

`[{"amount": 1}]`

### 常用写法

**可空字段**（两种写法均可）：

```
"start_date": {
    "anyOf": [
        {
            "type": "string"
        },
        {
            "type": "null"
        }
    ],
    "description": "开始日期"
}
```
```
"start_date": {
    "type": [
        "string",
        "null"
    ],
    "description": "开始日期"
}
```

**枚举值**（结果会尽量匹配枚举项）：

```
"payment_type": {
    "description": "付款方式",
    "type": "string",
    "enum": [
        "电汇",
        "承兑汇票",
        "支票"
    ]
}
```

**默认值**（字段未抽到且非必填时填入）：

```
"currency": {
    "description": "币种",
    "type": "string",
    "default": "CNY"
}
```

**复用字段定义**（`$ref` 仅支持 `#/$defs/xxx` 形式）：

```
{
  "type": "object",
  "properties": {
    "seller": {"$ref": "#/$defs/Company"},
    "buyer": {"$ref": "#/$defs/Company"}
  },
  "$defs": {
    "Company": {
      "type": "object",
      "properties": {
        "name": {"description": "公司名称", "type": "string"},
        "tax_id": {"description": "税号", "type": "string"}
      }
    }
  }
}
```

### 不支持的关键字

仅支持 `type`、`description`、`title`、`properties`、`items`、`required`、`enum`、`default`、`$defs`、`$ref`、`anyOf`。其余 JSON Schema 关键字（如 `format`、`pattern`、`minLength`、`minItems` 等）**不支持，会被忽略**。如需格式约束（如日期格式），请写入字段的 `description`。

### 结果自动纠正

抽取结果会按 schema 声明自动纠正，无需额外处理：

-   类型纠正：值不符合声明类型时尽力转换，如 `"12"` → `12`（integer）、`"12.5"` → `12.5`（number）、`"true"` → `true`（boolean）；转换失败保留原值；`object`/`array` 类型不做转换。
-   枚举匹配：值与 `enum` 失配时依次按精确匹配、忽略大小写、相似度匹配，仍不匹配则取枚举第一项。
-   默认值填充：字段值为 `null` 且声明了 `default` 时填入默认值。
-   数组抽取：数组整体作为一个字段返回 JSON 数组，数组内各字段同样按 `items` 中的类型纠正。

## 限制

项目

限制

说明

schema 大小

序列化后 UTF-8 编码 ≤ 600 KB

超限报错 4013

嵌套深度

≤ 6 层

口径见下，超限报错 4012

叶子字段数

≤ 100

超限报错 4011

根节点

必须为 JSON 对象

数组、字符串等报错 4011

`object` 字段

必须有非空 `properties`

缺失或为空报错 4011

`array` 字段

必须有非空 `items`

缺失或为空报错 4011

**深度口径**（JSON Schema 格式）：

-   根级 `properties` 下的字段是第 1 层；
-   每进入一层嵌套 `object` 的子字段，层数 +1；
-   数组的 `items` 整体 +1 层（`items` 为 object 时，其内部字段再 +1）。

以数据路径表示：`a.b.c.d.e.f` 为 6 层（合法），`a.b.c.d.e.f.g` 为 7 层（超限）；`a[ ].b` 为 3 层（a 1 层、items 1 层、b 1 层）。

**叶子字段数口径**：

-   JSON Schema 格式：object 递归展开计数，array 整体算 1 个字段（其内部字段不计入）；
-   旧版格式：字符串叶子数。

**建议**：嵌套尽量控制在 3~4 层以内；字段数较多时拆分为多次抽取再合并。

## Schema校验工具

提交前可用校验脚本离线自查（脚本见：[schema校验工具](https://prism-data.oss-cn-hangzhou.aliyuncs.com/tools/doc-extract/validate_extract_schema.py)，与服务端校验规则一致）：

```
python3 validate_extract_schema.py schema.json
python3 validate_extract_schema.py --json '{"type":"object","properties":{"a":{"type":"string"}}}'
```

通过时输出：

```
[通过] 格式=llama，叶子字段数=3，最大深度=3，大小=336 字节
```

失败时输出错误码、原因与出错位置：

```
[失败] 错误码 4011：type 为 object 但 properties 缺失或为空（位置：properties.buyer）
[失败] 错误码 4012：extract_schema 嵌套层数超过上限 6（位置：properties.a.b.c.d.e.f.g）
```

## 问题排查

[schema校验工具](https://prism-data.oss-cn-hangzhou.aliyuncs.com/tools/doc-extract/validate_extract_schema.py)返回错误码为下表之一时，说明 schema 未通过校验：

错误码

错误名

含义

常见原因与修复

9004

参数错误

`extract_schema` 未传或为空

请求体中补充非空的 `extract_schema`

4011

EXTRACT\_SCHEMA\_ERROR

不允许的 schema 格式

见下方常见 4011 场景

4012

EXTRACT\_SCHEMA\_DEPTH\_ERROR

嵌套层数超过 6 层

减少嵌套层级、扁平化结构

4013

EXTRACT\_SCHEMA\_SIZE\_ERROR

schema 大小超过 600 KB

精简描述文字、减少字段或拆分抽取

常见 4011 场景：

报错信息

原因

修复

type 为 object 但 properties 缺失或为空

object 字段未声明子字段

补充非空 `properties`，或将该字段改为 `string`

type 为 array 但 items 缺失或为空

array 字段未声明元素结构

补充 `items`，如 `"items": {"type": "string"}`

字段数超过上限

叶子字段数超 100（生产 1500）

拆分为多次抽取再合并

properties 为空

未声明任何字段

至少声明一个字段

字段描述必须是字符串或对象

旧格式叶子值不是字符串/对象（如数字、数组）

叶子值改为描述字符串，或改用 JSON Schema 格式

字段路径异常（如出现 `a.description`、`a.type` 成为抽取字段）

schema 缺少顶层 `type: "object"` 且不满足三字段判定，被当作旧格式解析

顶层补充 `"type": "object"`

其他自查建议：

1.  用校验脚本本地验证，报错会给出具体出错位置；
2.  确认 JSON 本身合法（无多余逗号、中文引号等）；
3.  确认 `required` 中列出的字段名在 `properties` 中存在；
4.  `$ref` 仅支持 `#/$defs/xxx` 形式，被引用的定义需放在顶层 `$defs` 中。
