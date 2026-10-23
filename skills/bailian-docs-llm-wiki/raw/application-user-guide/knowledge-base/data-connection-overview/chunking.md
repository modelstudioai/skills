# 切片与向量化

了解切片策略与嵌入模型如何影响检索质量。

切片和向量化在导入数据时自动完成。切片决定检索的最小单元，向量化决定语义匹配的精度。两者均在[导入数据](https://help.aliyun.com/zh/model-studio/rag/documents#h-ragdoc-import)的索引设置步骤中配置，创建后不可更改。

## 切片方式

导入数据时可选择以下切片方式：

切片方式

说明

适用场景

智能切分（默认）

自动识别章节、段落边界

大部分场景

按长度切分

按固定 token 数等距切分

对 token 数量有严格要求的场景

按页切分

按 PDF 页面边界切分

每页传达独立主题的文档

按标题切分

按 Markdown / HTML 标题层级切分

用标题划分独立主题的文档

按照正则切分

按自定义正则表达式匹配位置切分

有固定分隔标记的文本

按照符号切分

按指定分隔符切分

根据特定标识符区分内容的文档

**最大分段长度**：默认 600，范围 10–6000（token）。

## 切片选型建议

场景

推荐配置

原因

FAQ 文档

按长度切分，256 token

问答对短小独立

产品手册

智能切分，600 token（默认）

章节结构清晰

长篇报告

智能切分，2048 token

保留更多上下文

法律合同

按标题切分，512 token

条款层级分明

## 向量化

切片完成后，系统使用嵌入模型将文本转为向量写入索引。嵌入模型在创建知识库时选择，创建后不可更改。

导入数据时右侧费用详情会显示当前使用的嵌入模型和排序模型。

## 查看与管理切片

切片构建完成后，在知识库详情页的 **切片详情** Tab 中查看和管理切片。详见[文档管理 — 切片管理](https://help.aliyun.com/zh/model-studio/rag/documents#h-ragdoc-chunks)。

## API 管理

切片相关 API：

-   [查询切片列表](raw/application-api-reference/rag-api/rag-api-chunks/rag-api-list-chunks.md)
-   [更新切片](raw/application-api-reference/rag-api/rag-api-chunks/rag-api-update-chunk.md)
-   [删除切片](raw/application-api-reference/rag-api/rag-api-chunks/rag-api-delete-chunk.md)

**重要**切片与向量化配置好后，创建[知识检索服务](raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)开始联合检索。
