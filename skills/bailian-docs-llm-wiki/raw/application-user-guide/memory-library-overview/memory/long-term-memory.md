# 长期记忆

阿里云百炼的智能体应用在和您进行对话时，能够记住一定长度的对话记录，但由于大模型注意力机制的限制，可能会忘记某些信息。为了解决这个问题，您可以将对话过程中的特定信息（主要是用户个性化信息，例如用户特征、用户偏好等）存储到长期记忆体中，使智能体应用持续学习，帮助其更好地记住用户偏好等。在后续对话中，智能体应用将持续引用这些信息，提升交互体验。

## 功能介绍

在智能体应用中启用长期记忆功能后，将自动创建长期记忆体（Memory）。长期记忆体通过记忆片段和记忆变量实现记忆管理。在调用智能体应用时，系统会根据传入的长期记忆体ID（Memory ID），自动召回记忆体内容（记忆片段和记忆变量），并将其与当前用户提问一起传递给模型生成答案。

-   **记忆片段（即MemoryNode）**：
    
    阿里云百炼会自动提取对话中的用户个性化信息存储到记忆片段中（如用户说“我喜欢吃辣的”会存储为“用户喜辣”），用于后续对话推荐。但其易受临时性信息干扰（如用户临时提及“尝试素食”），需通过记忆变量校准。
    
-   **记忆变量**：
    
    记忆变量是以键值对形式存在的，需手动定义字段，值可通过模型推理（基于用户提问生成）或人工输入（如录入外部用户行为数据）获取。其权重高于记忆片段，可弥补记忆片段的不完整性和即时偏差，确保推荐准确性。
    

## 场景示例

-   智能导购助手：收集并记住顾客的预算范围、品牌偏好、关注的具体功能等信息，提供个性化的购买建议。
-   健身教练助手：收集并记住用户的身体状况、健身目标和可用设备等信息，提供个性化的锻炼计划和饮食建议。
-   旅游规划助手：收集并记住用户的预算、兴趣爱好和旅行时间等信息，推荐合适的目的地、景点和行程安排。
-   学习辅导助手：收集并记住学生的年级、知识水平和薄弱科目等信息，提供有针对性的学习资料和练习题。

您也可以手动将特定信息添加到长期记忆中，例如添加“语言：中文”的键值对，这样智能体应用在后续对话中就会持续用中文回复。

## 如何使用长期记忆

### 步骤1：创建长期记忆体并获取长期记忆体ID

可以通过以下两种方式创建长期记忆体，长期记忆体ID在同一阿里云账号（UID）下是唯一的。

#### 通过控制台创建

1.  创建长期记忆体。
    
    在[阿里云百炼应用](https://bailian.console.aliyun.com/#/app-center)的智能体应用中启用长期记忆功能时（下图位置①），会自动创建一个长期记忆体。当前应用默认与该长期记忆体绑定，并通过此长期记忆体进行记忆的检索和存储。如果您需要绑定其他长期记忆体，请参考[在应用中调用长期记忆体](https://help.aliyun.com/zh/model-studio/long-term-memory#ef7ad60fe1c3k)。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0337013671/p1026804.png)
2.  获取当前应用绑定的长期记忆ID。
    
    在页面右侧单击![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0760734571/p975487.png)图标（上图位置②），再单击**Memory ID**（下图位置③），记录当前应用绑定的Memory ID（下图位置④）用于后续调用。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0760734571/p975488.png)
3.  记忆片段信息的存储以Memory ID作为隔离。如需实现更细粒度的记忆隔离，灵活地管理不同的长期记忆体，避免不同场景或用户之间的记忆混淆，您可单击**创建Memory ID**（上图位置⑤）手动创建Memory ID，并[在应用中调用长期记忆体](https://help.aliyun.com/zh/model-studio/long-term-memory#ef7ad60fe1c3k)时传入。
    

#### 通过API创建

方式一：调用[CreateMemory - 创建长期记忆体](raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-creatememory.md)接口新建长期记忆体，并记录返回参数中的`memoryId`（即长期记忆体ID）用于后续调用。

方式二：调用[ListMemories - 获取长期记忆体列表](raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-listmemories.md)接口获取已有的长期记忆体，并记录返回参数中的`memoryId`（即长期记忆体ID）用于后续调用。

### 步骤2：在长期记忆体中创建记忆变量和记忆片段

新建的长期记忆体中未包含任何有用信息，您需要将对话过程中的特定信息存储到长期记忆体中（即记忆片段和记忆变量），智能体应用才能在后续对话中持续引用这些信息。

#### 通过控制台创建

1.  单击**长期记忆**开关后![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0337013671/p1026801.png)图标，在右侧**记忆变量**面板中，单击**添加字段**，配置记忆变量字段。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0337013671/p1026799.png)
    
    **参数名称**
    
    **参数说明**
    
    **配置示例**
    
    **字段名称**
    
    记忆变量的字段名称，自定义填写。
    
    记忆变量字段要语义化，确保使用者能快速理解字段的含义，机器能方便地做标签提取、聚合分析。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2912801471/p923303.png)
    
    **字段描述**
    
    对记忆变量字段的自然语言描述，用于提示大模型该字段的作用。
    
    自定义填写。
    
    **是否通过模型推理**
    
    是否通过模型推理自动更新该字段的值。开关状态不影响提取到记忆片段中的内容。
    
    开关打开![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4064206271/p838877.png)：从记忆片段中提取该记忆变量的值。随着对话中用户信息的更新，这个值也会自动更新。
    
    当字段名称为用户偏好等主观信息时，建议选择此设置。例如，饮食偏好、运动偏好等信息。这些信息不是单一且固定的，可能会随着时间变化，因此系统应具备动态更新的能力。通过定期询问或分析用户行为，确保存储的信息是最新的。
    
    开关关闭![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3064206271/p838879.png)：该记忆变量对应的值不会自动更新。可手动输入或从API中传入该记忆变量的值。
    
    当字段名称为用户特征等客观信息时，建议选择此设置。例如，性别、姓名等。这些信息通常不会频繁更改，并且相对稳定。因此，应定期进行审查和清理，以确保其准确性和时效性。对于不再相关或过时的信息，应及时更新或删除，以避免误导系统的决策过程。
    
2.  单击**确定**，完成配置。在**长期记忆**区域中，可以看到已配置的记忆变量字段。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0760734571/p975499.png)
3.  单击**发布**，发布应用。
    
    > 新增记忆变量字段后，需要发布应用才能生效。
    
4.  分别输入以下用户提问发起对话。等待1分钟左右，在页面右侧单击![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0760734571/p975500.png)图标，查看基于用户提问自动提取的记忆片段和记忆变量。
    
    **用户提问**
    
    **记忆片段中的内容**
    
    **记忆变量的值**
    
    我喜欢吃海鲜。
    
    用户喜欢吃海鲜。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0760734571/p975504.png)
    
    “饮食偏好”字段打开了**是否通过模型推理**开关，可以基于记忆片段自动提取记忆变量的值“海鲜, 面食, 不吃米饭, 不吃辣, 尤其是川菜”。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2912801471/p923332.png)
    
    我爱吃面食，不吃米饭。
    
    用户爱吃面食，不吃米饭。
    
    川菜太辣了，我受不了。
    
    用户不喜欢吃辣，尤其是川菜。
    
    我习惯每周末都去打羽毛球。
    
    用户习惯每周末都去打羽毛球。
    
    “运动偏好”和“年龄”字段关闭了**是否通过模型推理**开关，不能自动提取对应的值，显示为空。
    
    可在“运动偏好”中手动输入对应的值，比如“游泳”。在后续的对话中，将召回记忆片段和记忆变量，由模型判断并生成回答。使用示例请参考[修改“运动偏好”对应的值。](raw/application-user-guide/memory-library-overview/memory/long-term-memory.md)
    
    我今年20岁。
    
    用户出生于2005年。（推断时间：2005年）
    
    今天下大雨了。
    
    不是用户个性化数据，不提取内容。
    
5.  用户输入新的提问时，基于记忆变量结合Prompt来回答问题。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0760734571/p975506.png)
6.  手动输入“运动偏好”对应的值，清空记录重新开始对话。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2912801471/p919386.png)
    
    **“运动偏好”中不输入值，大模型回答时以记忆片段中的内容为准。**
    
    **“运动偏好”中手动输入“游泳”，在后续的对话中，将召回记忆片段和记忆变量，由模型判断并生成回答。**
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0760734571/p975512.png)
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0760734571/p975511.png)
    

#### 通过API创建

**方式一：**调用[CreateMemoryNode - 创建记忆片段](raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-creatememorynode.md)接口，在参数`content`中分别输入下述示例创建记忆片段。如果传入的长期记忆体ID已经绑定了控制台中的应用，则创建后可在控制台的记忆片段中查看其内容。否则只能通过[GetMemoryNode - 获取记忆片段](raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-getmemorynode.md)或[ListMemoryNodes - 获取记忆片段列表](raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-listmemorynodes.md)接口进行查看。

示例：

-   用户喜欢吃海鲜。
-   用户喜欢吃面食，不吃米饭。
-   用户不能吃太辣的食物。
-   用户习惯每周末都去打羽毛球。
-   用户今年20岁。

**方式二：**在[工作流与旧版智能体应用 API应用 DashScope API 参考](raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)时，传入长期记忆体ID，在`prompt`中输入下述示例，系统会根据`prompt`，在指定长期记忆体下自动创建记忆片段。请在[工作流与旧版智能体应用 API应用 DashScope API 参考](raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)中搜索“长期记忆”查看代码示例及详细的调用方法。创建后，可在控制台的记忆片段中查看其内容。

示例：

-   我喜欢吃海鲜。
-   我爱吃面食，不吃米饭。
-   川菜太辣了，我受不了。
-   我习惯每周末都去打羽毛球。
-   我今年20岁。

### 步骤3：在应用中调用长期记忆体

应用需通过绑定长期记忆体实现记忆能力。在应用中调用长期记忆体，可以将不同的记忆片段和记忆变量数据整合到应用中。在每轮发起对话时，将基于MemoryID进行存储和检索，从而提供更全面的用户画像。同时，还可以确保不同应用间的用户信息一致，提升智能体的个性化服务能力，优化用户体验，避免产生矛盾信息。

#### 在控制台调用

1.  在[阿里云百炼应用](https://bailian.console.aliyun.com/#/app-center)中找到目标智能体应用，单击**配置**。
    
2.  由于启用长期记忆功能时，该长期记忆体已经默认与当前应用绑定。因此，如果您想继续使用此长期记忆体进行记忆的检索和存储则无需重新绑定，直接发起会话即可。如果需要绑定其他长期记忆体，单击![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0760734571/p975538.png)图标，再单击**Memory ID**，在列表中选择Memory ID单击**确定**。
    
    > 已经在其他应用中使用的Memory ID不能删除。
    
3.  发布应用。
    
4.  重新发起会话时，系统会根据应用绑定的记忆体ID，自动召回相关记忆体内容，然后将其与当前用户提问一起传递给模型生成答案。
    

#### 通过API调用

1.  获取长期记忆体ID。
    
    获取方法请参见[步骤1：创建长期记忆体并获取长期记忆体ID](https://help.aliyun.com/zh/model-studio/long-term-memory#09a3b95cb2gp8)。
    
2.  在[工作流与旧版智能体应用 API应用 DashScope API 参考](raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)中搜索参数“长期记忆”查看代码示例及详细的调用方法。
    
    调用智能体应用时，系统会根据传入的长期记忆体ID，自动召回相关记忆体内容，然后将其与当前用户提问一起传递给模型生成答案。
    
    由于启用长期记忆功能时，该长期记忆体已经默认与当前应用绑定。因此，如果您没有传入记忆体ID，则默认继续使用此长期记忆体进行记忆的检索和存储。
    

## 相关API

您可以使用[长期记忆（旧）](raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory.md)中的API来管理长期记忆体及记忆体内容。

## 常见问题

1.  **记忆体内容（记忆片段和记忆变量）会存储多长时间？**
    
    阿里云百炼不会保存原始对话记录，仅按照客户配置的记忆变量字段进行内容提取，该信息目前暂无失效日期。您可以自行删除不需要的记忆体内容：
    
    -   仅删除一条记忆片段：使用[CreateMemoryNode](raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-creatememorynode.md)创建的记忆片段可通过[DeleteMemoryNode](raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-deletememorynode.md)删除。在阿里云百炼控制台界面创建的记忆片段和记忆变量，仅支持在界面上逐条删除。
    -   删除记忆体中的所有内容：使用[CreateMemory](raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-creatememory.md)创建的长期记忆体，可通过[DeleteMemory](raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-deletememory.md)删除该记忆体，从而移除其中的所有内容。
2.  **长期记忆功能如何收费？**
    
    数据存储不收费。
    
    在调用应用进行问答时，记忆体内容会合并到Prompt传递给大模型，从而增加Token消耗。目前，被记忆体内容占用的Token暂不计费。
    
3.  **调用智能体时，如何实现记忆隔离？**
    
    记忆片段信息（MemoryNode）的存储以Memory ID作为隔离。
    
    您可使用[CreateMemory - 创建长期记忆体](raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-others/api-bailian-2023-12-29-dir-long-term-memory/api-bailian-2023-12-29-creatememory.md)创建长期记忆体，获取新的Memory ID。通过API调用时传入指定Memory ID，即可实现记忆隔离。如不传入，则默认使用应用所绑定的默认Memory ID。
