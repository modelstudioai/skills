# 记忆库

大模型受上下文窗口限制，跨会话无法保留记忆，导致每次对话都从零开始。记忆库通过自动提取对话中的关键信息并持久化存储，使智能体能够跨会话持续引用用户偏好和历史信息，提供个性化、连贯的对话体验。

## 概述

记忆库是一种为大模型提供跨会话长期记忆的服务。它自动从对话中提取关键信息并持久化存储为**事实记忆**和**用户画像**，在后续对话中基于语义检索相关记忆并注入上下文，使智能体持续理解用户偏好和历史信息。

-   **事实记忆**：从对话中自动提取的关键事件和信息，如"用户每天上午 9 点需要喝水提醒"。适用于动态事件信息。
-   **用户画像**：基于自定义模板提取的结构化属性，如年龄、职业、爱好。适用于固定用户属性。

记忆库提供开放的 API 接口，可接入任意应用，也支持多应用共享同一记忆库。产品概念与工作原理详见[核心概念](raw/application-user-guide/memory-library-overview/memory/concepts.md)。

**警告**记忆库将于 **2026 年 8 月 20 日 10:00**（北京时间）正式开始商业化计费，Add 和 Search 调用区分 **Pro** 和 **Lite** 策略版本。详见[计费说明](raw/application-user-guide/memory-library-overview/integration-overview/billing.md)。

## 快速开始

通过 API 3 步即可完成记忆的写入、查看和检索，参见[快速开始](raw/application-user-guide/memory-library-overview/memory/quickstart.md)。写入的记忆可在[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list)默认记忆库的**记忆详情**标签页，输入记忆实体 ID（`user_id`）后点击**查看**进行确认。

## 创建记忆库

每个用户账号下自带一个默认记忆库，无需创建即可直接使用。默认记忆库无法删除，但可以编辑名称和描述、添加自定义记忆规则；它已预置一条"默认项目"事实记忆规则，默认有效期 180 天，可点击编辑调整。

如需自定义记忆规则或为不同业务场景分别管理记忆，可创建新的记忆库：

1.  **进入创建入口**：在[记忆库](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list)页面，点击右上角的**创建记忆库**。
2.  **填写基础信息**：填写**记忆库名称**和**记忆库描述**（可能用于指导智能体调用），点击**确定**完成创建。
3.  **配置记忆规则**：创建成功后，系统会提示**是否立即开始创建记忆规则**。推荐点击**立即创建**，跳转到记忆规则配置页面；也可点击**暂不**，后续通过记忆库卡片上的**查看详情**进入配置。

删除记忆库：在记忆库卡片上点击 `...` 图标，或在记忆库详情页右上角点击 `...` 图标，再点击**删除**。删除后记忆库中的所有记忆内容将被清除且不可恢复；默认记忆库不可删除。

详细说明参见[创建与删除记忆库](raw/application-user-guide/memory-library-overview/create-memory.md)。

## 配置记忆规则

记忆规则定义了如何从对话中提取、存储和检索记忆，包括**事实记忆规则**和**用户画像规则**。每个记忆库最多可配置 50 条事实记忆规则和 50 条用户画像规则。点击记忆库卡片的**查看详情**，进入记忆库详情页的**记忆规则**标签页进行配置。

-   **事实记忆规则**：从对话内容中提取关键事件和信息片段，可配置规则指令、自动更新、记忆过期时间和记忆抽取策略版本（Pro/Lite）。
-   **用户画像规则**：持久化存储用户的属性信息，需逐个定义画像字段的名称、描述、初始值和记忆抽取策略版本。

完整参数说明参见[配置记忆规则](raw/application-user-guide/memory-library-overview/create-memory/configure-rules.md)。

## 查看记忆与检索调试

在记忆库详情页的**记忆详情**标签页，可查看记忆库基本信息、统计数据和记忆实体列表，支持通过记忆实体 ID（`user_id`）筛选并查看记忆详情。

在**记忆检索**标签页可调试检索效果：调整最大召回数量、相似度阈值（建议 0.5~0.7），按需开启意图判别召回、改写和排序，优化召回准确性和相关性。

通过 API 管理记忆（列表、更新、删除）参见[管理记忆](raw/application-user-guide/memory-library-overview/create-memory/manage-memory.md)。

## 使用用户画像

通过 API 创建画像模板后，调用 `AddMemory` 时传入画像模板 ID（`profile_schema`），系统会自动从对话中提取结构化属性，再通过 `GetUserProfile` 获取用户画像。完整流程参见[使用用户画像](raw/application-user-guide/memory-library-overview/create-memory/user-profile.md)。

## 相关文档

-   [快速开始](raw/application-user-guide/memory-library-overview/memory/quickstart.md)
-   [核心概念](raw/application-user-guide/memory-library-overview/memory/concepts.md)
-   [集成方式概览](raw/application-user-guide/memory-library-overview/integration-overview.md)
-   [长期记忆 API](raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)
-   [长期记忆 API 参考](raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)
-   [计费说明](raw/application-user-guide/memory-library-overview/integration-overview/billing.md)
-   [常见问题](raw/application-user-guide/memory-library-overview/integration-overview/faq.md)
