# 模型数据

数据管理是百炼平台对训练集和评测集的统一管理功能，支持数据集的创建、导入、版本管理、发布与删除，以及通过数据流进行数据清洗和增强。

## 功能概述

阿里云百炼**数据管理**功能对您业务空间下所有大模型相关数据集进行统一管理。访问[百炼控制台·数据管理](https://bailian.console.aliyun.com/cn-beijing/model/data)页面，页面顶部提供**数据集**和**数据流**两个 Tab：

-   **数据集** Tab：以列表形式展示所有数据集，包含数据集名称、类型、最新版本、数据量、导入状态、发布状态、存储位置、导入方式和操作等列。页面右上角提供**创建数据集**按钮，操作列支持新增版本、发布和删除。
-   **数据流** Tab：用于数据清洗和数据增强，通过可视化数据流画布搭建处理流程。详见[数据清洗或增强](https://help.aliyun.com/zh/model-studio/data-processing)。

数据集分为**训练集**（用于[模型调优](https://help.aliyun.com/zh/model-studio/model-training-overview)）和**评测集**（用于[模型评测](https://help.aliyun.com/zh/model-studio/model-evaluation-overview)）。数据集的创建、版本管理和发布等操作详见[训练集与评测集](https://help.aliyun.com/zh/model-studio/training-set-and-evaluation-set)。

## 相关文档

-   [训练集与评测集](https://help.aliyun.com/zh/model-studio/training-set-and-evaluation-set)
-   [数据清洗或增强](https://help.aliyun.com/zh/model-studio/data-processing)
-   [日志回流](https://help.aliyun.com/zh/model-studio/model-log-backflow)
