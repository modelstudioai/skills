# 析言GBI产品简介

析言GBI是基于阿里云千问大语言模型的数据分析助理，通过将自然语言转化为准确SQL，实现数据查询、分析与报告生成。

## 产品演示

## 产品版本对比

析言GBI提供三款版本，以满足不同业务场景的需求。

**标准版Turbo**和**标准版Mix**

-   **部署方式：**部署于公共云，**不支持微调**。
    
-   [计费方式](raw/application-user-guide/application-gallery/xiyan-gbi/xiyangbi-billing-description.md)**：按每月每RPM计费，支持**[**试用**](https://bailian.console.aliyun.com/xiyan?switchAgent=12473251#/home)**（各200个查询）。**
    
-   **版本特点：**
    -   **标准版Turbo：**响应迅速，适合开箱即用的通用查询，允许通过规则干预输出。
    -   **标准版Mix：**支持业务定制和结果干预，精度更高，允许通过案例学习提升处理能力。

**定制版Turbo**

-   **部署方式：**支持公共云、公共云与本地混合部署（**服务在云、数据在地**），支持模型微调。
-   [计费方式](raw/application-user-guide/application-gallery/xiyan-gbi/xiyangbi-billing-description.md)**：**仅用于定制化项目交付**。**
-   **核心优势：**专为特定业务需求设计，兼具低时延与高精度，能深度理解并融合您的专属业务逻辑，以应对复杂查询。

## 产品能力

### 数据库支持

支持联接公网可访问的MySQL或PostgreSQL协议数据库，以及联接阿里云云上内网数据库，ADB-PG、Hologres、PolarDB，详情参见[支持的数据库类型](https://help.aliyun.com/zh/model-studio/xiyan-gbi-user-guide#7f32fcc1d4hbz)。

### 数据问答

通过多智能体协同，将自然语言查询自动转换为SQL语句并执行，返回精确数据结果。

1.  **意图理解：**通过交互澄清模糊表述，理解用户真实意图。
2.  **问题转译：**根据领域术语和库表结构，将问题专业化，并映射到相关表与字段。
3.  **SQL生成：**协同生成SQL，并校验SQL逻辑和语法。

### 数据分析

自动拆解问题，执行多步查询，生成可视化图表和分析报告。

1.  **任务规划：**理解问题语义，拆解为清晰的子任务及依赖关系。
2.  **数据查询：**从数据库检索所需数据，并完成必要的清洗与对齐。
3.  **报告撰写：**将数据可视化，并撰写包含结论、方法与依据的分析报告。

### 配置企业知识管理

-   [知识名词解释](https://help.aliyun.com/zh/model-studio/xiyan-gbi-user-guide#e04a91677eu7x)：配置业务场景的专有名词，定义相关术语的计算方式。
    
-   [同义词解释](https://help.aliyun.com/zh/model-studio/xiyan-gbi-user-guide#aeebcd11a0f3y)：配置同义词列表，提高模型对不同询问方式的理解能力。
    
-   [业务逻辑解释](https://help.aliyun.com/zh/model-studio/xiyan-gbi-user-guide#df3c04eff2gee)：配置特定业务逻辑，支持全局和智能模型，可让配置根据用户问题内容选择性生效。
    
-   更多功能：
    
    -   [模型输出干预](https://help.aliyun.com/zh/model-studio/xiyan-gbi-user-guide#64a0fc168bmn0)**（标准版Turbo）**：设置特定问法描述和对应SQL对来干预模型输出。
    -   [优化案例管理](https://help.aliyun.com/zh/model-studio/xiyan-gbi-user-guide#3d8cae4fcdr98)**（标准版Mix）**：通过添加问答案例，指导模型进行自主学习，提升特定问题类型的处理能力，相较于模型输出干预更具有泛化性。

## 使用指南

使用方法和详细配置步骤参见[使用指南](raw/application-user-guide/application-gallery/xiyan-gbi/xiyan-gbi-user-guide.md)，更多信息可参考[Endpoint](https://api.aliyun.com/product/DataAnalysisGBI) 和 [API概览](raw/application-user-guide/application-gallery/xiyan-gbi/api-reference-4/api-dataanalysisgbi-2024-08-23-overview.md)。
