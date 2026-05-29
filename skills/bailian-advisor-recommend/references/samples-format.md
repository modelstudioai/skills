# 示例代码获取与输出规则

## samples 数据结构

每个模型的 `detailPath` 字段指向其 group 文件（如 `models/groups/qwen-plus.json`）。该文件中每个 item 有 `samples` 字段，结构如下：

```
samples:
  openai:                          # OpenAI 兼容接口（优先使用）
    completionsAPI / default:      # API 类型
      curl: "..."                  # curl 示例
      python: "..."               # Python 示例
      nodejs: "..."               # Node.js 示例
      docUrl: "..."               # 文档链接
  dashscope:                       # DashScope 原生接口
    default:
      curl: "..."
      python: "..."
      java: "..."
      docUrl: "..."
```

## 输出规则

1. 优先使用 `samples.openai` 下的代码（兼容性好，用户熟悉）
2. 如果没有 openai 兼容示例，使用 `samples.dashscope` 下的代码
3. 优先给 Python 示例，其次 curl
4. 示例代码中如果包含 `enable_thinking: true` 或深度思考相关逻辑，去掉这部分，给用户最简洁的调用方式
5. 如果 samples 字段不存在或为空，基于模型的 API 类型构造最简调用示例

## 推荐输出格式

每个推荐模型必须包含：

1. **模型名称和 ID**
2. **推荐理由** — 关联用户具体需求
3. **亮点** — 关键优势标签
4. **规格信息** — 上下文窗口、最大输出、定价（如有）
5. **调用示例代码** — 从 group 文件的 samples 字段获取

### pipeline 场景输出

```
方案概述：一句话描述

步骤 1：xxx
  推荐模型 + 理由 + 示例代码

步骤 2：xxx
  推荐模型 + 理由 + 示例代码
  （如有兼容性提示则说明）
```
