# 数据连接

数据连接是阿里云百炼平台管理外部数据源的统一入口。通过创建数据连接器，阿里云百炼应用可以安全地访问企业数据库、文档系统和对象存储中的数据，在对话中实时查询和引用这些数据。

### 连接器类型

数据连接器按数据的存储和访问方式，分为**平台托管**和**流处理**两大类：

**联通格式**

**连接器类型**

**数据存储方式**

**适用场景**

平台托管

文件

阿里云百炼平台或自有OSS

上传和管理非结构化文档（PDF、Word、Markdown等）

表格

阿里云百炼平台或自有OSS

导入和查询结构化表格数据（CSV、Excel等）

流处理

MySQL

数据保留在原数据库,实时访问

连接MySQL数据库

执行SQL查询（仅DMS导入数据源方式支持执行）

PostgreSQL

数据保留在原数据库,实时访问

连接PostgreSQL数据库

执行SQL查询（仅DMS导入数据源方式支持执行）

PolarDB-X 2.0

数据保留在原数据库,实时访问

连接阿里云 PolarDB-X 2.0 分布式数据库

执行SQL查询（仅DMS导入数据源方式支持执行）

语雀

数据保留在语雀,实时访问

访问语雀文档和知识库

OSS

数据保留在OSS,实时访问

访问对象存储中的文件

## **前置条件**

在创建数据连接器前，请确保满足以下条件：

-   **账号权限**：主账号或具有数据连接管理权限的 RAM 用户。RAM 用户需要主账号授权后才能使用数据连接功能。授权方法请参见[权限管理](https://help.aliyun.com/zh/model-studio/application-permission-management-overview)。
    
-   **数据源准备：**
    
    -   **文件/表格连接器：**已准备好要上传的文档或表格文件，或已创建OSS Bucket。
        
    -   **MySQL连接器：**已有MySQL数据库实例（阿里云RDS或自建），并确保网络可达（公网或私网）。
        
    -   **PostgreSQL连接器：**已有PostgreSQL数据库实例，且已将`wal_level`参数设置为`logical`。
        
    -   **PolarDB-X 2.0连接器：**已有阿里云 PolarDB-X 2.0 实例，且实例所在地域支持私网访问。如需通过 DMS 导入数据源，请先在 DMS 中完成 PolarDB-X 实例的录入。
        
    -   **语雀连接器：**已有语雀知识库（仅支持公网版本语雀），并获取了个人访问 Token。
        
    -   **OSS连接器：**已创建OSS Bucket，并开通了[向量检索服务](https://help.aliyun.com/zh/oss/user-guide/vector-retrieval/)。
        

## **创建连接器**

1.  访问[数据连接](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/connector/list)页面，单击右上角的**创建连接器**。
    
2.  选择连接器类型，填写基本信息和存储位置。
    
    ### 文件连接器
    
    文件连接器用于管理非结构化文档（PDF、Word等）。
    
    1.  在创建连接器页面，连接器类型选择文件。
        
    2.  **填写基本信息：**
        
        1.  **连接器名称：**使用易于识别的名称。
            
        2.  **描述：**填写连接器的用途说明。描述会用于指导应用调用的准确度,建议写明数据内容和用途。
            
    3.  选择**存储位置**：
        
        -   **使用平台存储：**数据存储在阿里云百炼平台提供的存储空间中,提供最大100，000个文件，1 TB 存储额度，**限时免费**。
            
        -   **使用自有OSS存储：**数据存储在您自己的OSS Bucket中，适用于大规模数据存储。
            
            **说明**
            
            -   首次使用需按界面提示完成授权。
                
            -   目标 Bucket 需要添加`bailian-connector-access`标签（值为`ReadAndWrite`）以供阿里云百炼访问。[添加标签](https://oss.console.aliyun.com/bucket)
                
            
    
    ## 表格连接器
    
    表格连接器用于管理结构化数据（CSV、Excel等）。
    
    1.  在创建连接器页面，连接器类型选择表格**。**
        
    2.  **填写基本信息：**
        
        1.  **连接器名称：**使用易于识别的名称。
            
        2.  **描述：**填写连接器的用途说明。描述会用于指导智能体调用的准确度,建议写明数据内容和用途。
            
    3.  **选择存储位置**：
        
        -   **使用平台存储：**数据存储在阿里云百炼平台提供的存储空间中,提供1 TB免费额度,额度用完后自动转为按量付费。适用于小规模数据存储。
            
        -   **使用自有OSS存储：**数据存储在您自己的OSS Bucket中，适用于大规模数据存储。
            
            **说明**
            
            -   首次使用需按界面提示完成授权。
                
            -   目标 Bucket 需要添加`bailian-connector-access`标签（值为`ReadAndWrite`）以供阿里云百炼访问。[添加标签](https://oss.console.aliyun.com/bucket)
                
            
    
    ### MySQL连接器
    
    MySQL连接器属于**流处理**类型,用于连接MySQL数据库,使应用可以执行SQL查询获取实时数据。
    
    **说明**
    
    仅通过**从DMS导入数据源**方式创建的MySQL连接器支持执行SQL查询。通过**创建自定义数据源**方式添加的MySQL连接器不支持直接执行SQL。
    
    1.  在创建连接器页面,选择**MySQL**类型。
        
    2.  填写**连接器名称**和**描述**。
        
    3.  **配置数据来源信息**:
        
        -   **创建自定义数据源：**手动配置数据库连接信息,通过公网或私网连接阿里云RDS或自建MySQL数据库。
            
            -   **阿里云RDS MySQL：**通过SLR授权,关联阿里云RDS服务下的MySQL数据库。选择后,**数据库地址**和**端口**会根据实例ID自动获取,无需手动输入。
                
            -   **自建MySQL：**手动配置远端MySQL数据库的连接信息。需要手动输入**数据库地址**和**端口**。
                
        -   **从DMS导入数据源：**快速导入DMS（数据管理服务）中已创建的数据源。首次使用需完成SLR授权,包括EventBridge服务关联角色、RDS服务管理角色和DMS服务管理角色的授权。
            
    4.  **选择网络类型**:
        
        -   **公网**（默认）:通过公网连接数据库。选择公网时,请务必将指定IP段加入数据库实例的白名单中。
            
        -   **私网**:通过内网连接数据库,需要额外选择**所属地域**。适用于生产环境,连接更稳定安全。
            
        -   **填写数据库连接信息**:
            
            配置项
            
            说明
            
            **数据库实例**
            
            仅阿里云RDS MySQL时显示。输入RDS实例ID,例如`rm-******adq7`。
            
            **数据库地址**
            
            阿里云RDS MySQL时自动获取（禁用输入）;自建MySQL时需手动输入。
            
            **数据库端口**
            
            阿里云RDS MySQL时自动填充为3306（禁用输入）;自建MySQL时需手动输入。
            
            **数据库用户名**
            
            必填。输入数据库用户名,用于鉴权连接。
            
            **数据库密码**
            
            必填。输入数据库密码。请确保该用户具备数据库的读取权限。
            
        -   （可选）单击**开始检测**,验证数据库连通性。
            
            系统通过EventBridge服务检测连通性,检测不收取费用。检测通过后,可以从**选择DB**下拉列表中选择要连接的数据库。
            
    
    ### PostgreSQL连接器
    
    PostgreSQL连接器支持连接阿里云RDS PostgreSQL实例或自建PostgreSQL数据库。
    
    **说明**
    
    仅通过**从DMS导入数据源**方式创建的PostgreSQL连接器支持执行SQL查询。通过**创建自定义数据源**方式添加的PostgreSQL连接器不支持直接执行SQL。
    
    **前置条件**
    
    -   数据库账号必须具有高权限（Superuser或具有REPLICATION权限）。
        
    -   已将实例系统参数`wal_level`设置为`logical`（默认为replica）。
        
    -   （仅自建实例）已配置`listen_addresses`参数，允许100.64.0.0/16网段访问。配置方法：
        
        1.  编辑配置文件：`sudo vim /etc/postgresql/[版本]/main/pg_hba.conf`
            
        2.  在文件顶部添加规则：`host [数据库名] [用户名] 100.64.0.0/16 md5`
            
        3.  重载配置：`sudo systemctl reload postgresql`
            
    
    1.  在创建连接器页面，选择**PostgreSQL**类型。
        
    2.  **填写基本信息**：连接器名称、描述（建议说明数据内容和用途）。
        
    3.  **配置数据库连接：**
        
        -   **主机地址：**数据库实例的连接地址（公网或私网）。
            
        -   **端口**：默认5432。
            
        -   **数据库名称（dbName）**：必填字段，指定要连接的数据库。
            
        -   **用户名**：具有高权限的数据库账号。
            
        -   **密码**：数据库密码。
            
    4.  单击测试连通性，确保配置正确。PostgreSQL连接器使用DTS（数据传输服务）进行连通性检测。
        
    
    MySQL与PostgreSQL差异对比：
    
    差异项
    
    MySQL
    
    PostgreSQL
    
    默认端口
    
    3306
    
    5432
    
    额外必填字段
    
    无
    
    需额外填写dbName（数据库名称）
    
    连通性检测服务
    
    EventBridge
    
    DTS（数据传输服务）
    
    特殊配置要求
    
    无
    
    需将实例系统参数`wal_level`修改为`logical`
    
    ### PolarDB-X 2.0连接器
    
    PolarDB-X 2.0连接器属于**流处理**类型,用于连接阿里云 PolarDB-X 2.0 分布式数据库,使应用可以执行SQL查询获取实时数据。
    
    **说明**
    
    仅通过**从DMS导入数据源**方式创建的PolarDB-X 2.0连接器支持执行SQL查询。通过**创建自定义数据源**方式添加的PolarDB-X 2.0连接器不支持直接执行SQL。
    
    1.  在创建连接器页面,选择**PolarDB-X 2.0**类型。
        
    2.  填写**连接器名称**和**描述**。
        
    3.  **配置数据来源信息**:
        
        -   **创建自定义数据源：**通过 SLR 授权,关联阿里云 RDS 服务下的 PolarDB-X 2.0 数据库。**数据库地址**和**端口**会根据所选实例自动获取,无需手动输入。
            
            首次使用需在弹窗中完成两个服务关联角色的授权:DTS 服务管理角色（`AliyunServiceRoleForSFMConnectorAccessDTS`）和 PolarDB-X 服务管理角色（`AliyunServiceRoleForSFMAccessPolarDBX`）。
            
        -   **从DMS导入数据源：**快速导入 DMS（数据管理服务）中已创建的 PolarDB-X 数据源。首次使用需完成 DMS、DTS 和 PolarDB-X 三个服务管理角色的 SLR 授权。
            
    4.  **选择网络类型**:仅支持**私网**。需要选择**所属地域**,通过内网连接 PolarDB-X 实例,适用于生产环境。
        
    5.  **填写数据库连接信息**:
        
        配置项
        
        说明
        
        **数据库实例**
        
        仅**创建自定义数据源**方式显示。从下拉列表中选择当前账号在所选地域下的 PolarDB-X 2.0 实例。
        
        **选择数据源**
        
        仅**从DMS导入数据源**方式显示。从 DMS 数据源列表中选择 1 个 PolarDB-X 数据源,数据源连通性由 DMS 保障。
        
        **数据库地址**
        
        **创建自定义数据源**方式根据所选实例自动获取（禁用输入）;**从DMS导入数据源**方式需手动输入或确认。
        
        **数据库端口**
        
        **创建自定义数据源**方式根据所选实例自动获取（禁用输入）;**从DMS导入数据源**方式需手动输入或确认。
        
        **数据库用户名**
        
        必填。输入数据库用户名,用于鉴权连接。
        
        **数据库密码**
        
        必填。输入数据库密码。请确保该用户具备数据库的读取权限。
        
    6.  （可选）单击**开始检测**,验证数据库连通性。检测通过后,可以从**选择DB**下拉列表中选择要连接的数据库。
        
    
    与 MySQL 连接器的主要差异:
    
    -   **网络类型**:仅支持私网,不支持公网。
        
    -   **数据源**:仅支持阿里云 PolarDB-X 2.0 实例,不支持自建数据库。
        
    -   **SLR 授权**:首次使用时需在弹窗中显式同意 DTS 与 PolarDB-X 服务管理角色（DMS 方式还需 DMS 角色）的授权。
        
    
    ### 语雀连接器
    
    语雀连接器用于访问语雀文档和知识库，使智能体可以检索和引用企业在语雀中的知识内容。
    
    > 仅支持公网版本语雀。
    
    1.  在创建连接器页面，选择**语雀**。
        
    2.  填写**连接器名称**和**描述**。
        
    3.  访问[语雀开放 API](https://www.yuque.com/yuque/developer/api)获取Tenant access token并填入在连接信息区域。
        
    4.  单击**连接检测**,验证Token有效性。输入Token后该按钮自动启用。
        
    
    ### OSS连接器
    
    OSS连接器用于访问对象存储中的文件,使应用可以读取和处理OSS中存储的各类文件。
    
    1.  在创建连接器页面,选择**OSS**类型。
        
    2.  填写**连接器名称**和**描述**。
        
    3.  在**存储Bucket选择**下拉列表中,选择要连接的OSS Bucket。
        
    
    **说明**
    
    -   首次使用，需按界面提示完成授权。
        
    -   目标 Bucket 需添加`bailian-datahub-access`标签（值为`read`）以供阿里云百炼访问。[添加标签](https://oss.console.aliyun.com/bucket)
        
    -   如果下拉列表中没有显示Bucket,请确认已创建OSS Bucket,且当前账号拥有该Bucket的访问权限。
        
    -   使用OSS连接器需要开通[向量检索服务](https://help.aliyun.com/zh/oss/user-guide/vector-retrieval/)。如果未开通，调用工具时会返回相应的错误提示信息。
        
    
    > 不支持归档、冷归档或深度冷归档存储类型的 Bucket。
    
    > 支持内容加密的 Bucket。支持私有的 Bucket。
    
    > 如需使用开启[Referer防盗链](https://help.aliyun.com/zh/oss/configure-referer-policy-to-prevent-other-websites-from-referring-to-oss-files)的Bucket，须参考[防盗链](https://help.aliyun.com/zh/oss/user-guide/hotlink-protection#8a560a5cc91od)将域名`*.console.aliyun.com`添加到白名单Referer中。
    
3.  单击**确认**，完成创建。
    

## **导入数据**

## 导入文件

点击文件连接器卡片**详情**，进入文件管理页面。

1.  在左侧**类目**下，选择一个现有类目，或点击![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0077764271/p839829.png)图标新建类目。
    
    > 阿里云百炼通过类目管理导入的文件。
    
2.  点击**导入数据，**进入**导入数据**界面**。**导入方式选择**本地上传**。
    
    > 目前平台不支持直接导入JSON、CSV、YAML格式文件。请自行用相应工具将其转换为XLSX或XLS格式再导入。
    
3.  **解析方式**可选**默认设置**或**自定义设置**（**自定义设置**可针对不同格式配置解析规则，以提升解析效果）。
    
    **解析方式说明**
    
    请根据实际需求配置解析策略，如不确定建议保持默认设置。有关**文档智能解析**、**大模型文档解析**和**电子文档解析**的详细说明，请参阅[文档理解](https://help.aliyun.com/zh/document-mind/product-overview/overview-of-document-understanding#9a4f5fb91fpps)。
    
    > 可选的解析方式取决于选择的文件类型（文档、图像、音频、视频）。
    
    -   **电子文档解析**：不支持解析文件中的插图与图表。
        
    -   **文档智能解析：**对于文件中的插图，解析器会识别并提取图中的文本，并生成文本摘要。这些摘要将与文件中其它非图片内容一起被切分并转换为向量，参与知识库的检索。
        
    -   **大模型文档解析：**使用[选择模型](https://help.aliyun.com/zh/model-studio/models#3f1f1c8913fvo)模型的智能体应用支持用户对文件中插图和图表的内容进行提问。如需识别和理解文件中的插图与图表，请选择**大模型文档解析**。
        
    -   **Qwen VL解析：**仅支持解析图片格式。可自主选择千问VL模型，并通过传入Prompt指定模型需要识别的版面、元素及内容，其余功能与大模型文档解析一致。
        
    -   **音视频解析：**对文件进行语音识别、视频帧提取（仅限视频）和剧情解析（仅限视频），最终将所有声画信息按时间轴结构化对齐。
        
        -   **语音识别：**字幕内容解析器通过[录音文件识别](https://help.aliyun.com/zh/model-studio/recording-file-recognition)将人类语音转为文本。暂不支持识别音乐或自然环境声（如喇叭声、钟声、雷声等）。
            
        -   **视频帧提取：**从原始视频中抽取有代表性的视觉画面，并生成相应的文本描述。
            
        -   **剧情解析（需手动开启）：**分析视频内容，定位具体事件并标注时间戳，同时生成相应的文本描述。
            
    
4.  为文件**配置标签**（可选）。
    
    > [通过API调用应用](https://help.aliyun.com/zh/model-studio/application-calling-guide#4100253b7chc3)时，可以在请求参数`tags`中指定标签。应用在检索知识库时，会先根据标签筛选相关文件，从而提高检索效率。对于[智能体应用](https://help.aliyun.com/zh/model-studio/single-agent-application)，可在控制台调试知识库时设置标签。
    
5.  点击**确认**，系统将开始解析和导入，可在页面查看任务进度。
    
    > 文件将被转换成阿里云百炼可处理的格式。在请求高峰时段，该过程可能需要数小时，请耐心等待。
    
6.  导入完成后，点击相应文件右侧的**详情**即可查看导入的文件。
    
    > 文件导入阿里云百炼后，将作为独立副本（与原始数据没有关联）存储在平台提供的免费空间中，当前无容量限制。
    
    > 仅支持查看最近**90**天内导入的文件。超过此时间范围后，导入的文件将无法查看，但不会被删除。
    
    > 导入的文件仅供当前业务空间的用户使用。阿里云百炼不会将其用于任何商业用途或对外公开。
    

## 导入表格

点击表格连接器卡片**详情**，进入数据管理页面。

在左侧**数据表管理**下，选择一个现有数据表，或点击![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0077764271/p839829.png)图标新建数据表。

> 阿里云百炼通过数据表管理导入的数据。

### **导入到新数据表**

1.  输入**数据表名称**。并配置数据表，选择可**直接上传Excel**或**自定义表头**。
    
    -   **直接上传Excel：**阿里云百炼将自动识别上传文件中的表头，并据此来创建数据表结构，并将其余内容作为数据记录导入该表。
        
    -   **自定义表头：****列名**为必填参数，**描述**为选填参数，**类型**为必填参数。
        
        **重要**
        
        -   数据表的结构（列名、描述以及类型）一旦确定，无法修改。
            
        -   上传文件的表结构必须与待导入数据文件的结构（列数、列名）完全一致，否则导入会失败。例如，待导入的数据表有2列，这里的表结构必须配置2个字段，且列名需一一对应。可通过点击**新增字段**或**操作**列的**删除**，来增加或删减字段。
            
        -   为帮助模型理解各字段含义（如 `age` 表示年龄），请在“描述”中提供清晰的自然语言说明。
            
        -   若字段类型设为 `image_url`，请确保链接是**公开可访问**的图片URL。知识库会用此链接抓取图片并为其生成向量索引，用于以图搜图等场景。
            
            > image\_url格式示例：https://example.com/downloads/pic.jpg
            
            > 创建知识库时，image\_url类型字段用于生成**图片索引**。阿里云百炼会访问目标图片并提取其特征，然后通过图片Embedding转换为向量并保存。知识库检索时，会用该向量与用户上传图片的向量进行相似度比对。
            
        
2.  点击![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2312799171/p816622.png)图标选择并上传文件（XLSX或XLS格式）。
    
    > 文件必须包含表头，否则会导入失败。
    
    > 目前平台不支持直接导入JSON、CSV、YAML格式文件。请自行用相应工具将其转换为XLSX或XLS格式再导入。
    
3.  点击**确定**，开始导入。完成后，左侧的**数据表**导航树中将出现新数据表。
    

### **导入到现有数据表**

1.  在左侧的**数据表**列表中选择相应的数据表，然后点击**导入数据**。
    
2.  导入类型选择**覆盖上传**或**增量上传**。
    
    > 点击界面上的**下载模板**，可获取一个仅包含表头的空白文件。您可直接在该文件中插入新数据，然后将其用于覆盖上传或增量上传。
    
3.  点击![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2312799171/p816622.png)图标选择并上传文件（XLSX或XLS格式）。
    
    > 文件必须包含表头，且与当前数据表的表头结构一致，否则会导入失败。
    
    > 目前平台不支持直接导入JSON、CSV、YAML格式文件。请自行用相应工具将其转换为XLSX或XLS格式再导入。
    

## 导入OSS文件

-   **OSS连接器**：点击卡片**详情**，进入工具页签，可搜索或获取OSS的指定文件下载链接。使用工具需开通[向量检索服务](https://help.aliyun.com/zh/oss/user-guide/vector-retrieval/)。
    
-   **文件连接器**或**表格连接器**：点击卡片**详情**，进入文件或表格管理页面。
    
    1.  在左侧**类目**下，选择一个现有类目，或点击![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0077764271/p839829.png)图标新建类目。
        
        > 阿里云百炼通过类目管理导入的文件。
        
    2.  点击**导入数据，**进入**导入数据**界面**。**导入方式选择**OSS**。
        
        > 首次从 OSS 向阿里云百炼导入数据，需按界面提示完成授权，并为目标 Bucket 添加`bailian-datahub-access`标签以供阿里云百炼访问。
        
        > 不支持归档、冷归档或深度冷归档存储类型的 Bucket。
        
        > 不支持访问 Bucket 根目录下的文件，请选择已有的子目录或新建一个子目录供阿里云百炼访问。
        
        > 支持内容加密的 Bucket。支持私有的 Bucket。
        
        > 如需使用开启[Referer防盗链](https://help.aliyun.com/zh/oss/configure-referer-policy-to-prevent-other-websites-from-referring-to-oss-files)的Bucket，须参考[防盗链](https://help.aliyun.com/zh/oss/user-guide/hotlink-protection#8a560a5cc91od)将域名`*.console.aliyun.com`添加到白名单Referer中。
        
    3.  **解析方式**可选**默认设置**或**自定义设置**（**自定义设置**可针对不同格式配置解析规则，以提升解析效果）。
        
        **解析方式说明**
        
        请根据实际需求配置解析策略，如不确定建议保持默认设置。有关**文档智能解析**、**大模型文档解析**和**电子文档解析**的详细说明，请参阅[文档理解](https://help.aliyun.com/zh/document-mind/product-overview/overview-of-document-understanding#9a4f5fb91fpps)。
        
        -   **电子文档解析**：不支持解析文件中的插图与图表。
            
        -   **文档智能解析：**对于文件中的插图，解析器会识别并提取图中的文本，并生成文本摘要。这些摘要将与文件中其它非图片内容一起被切分并转换为向量，参与知识库的检索。
            
        -   **大模型文档解析：**使用[选择模型](https://help.aliyun.com/zh/model-studio/models#3f1f1c8913fvo)模型的应用支持用户对文件中插图和图表的内容进行提问。如需识别和理解文件中的插图与图表，请选择**大模型文档解析**。
            
        -   **Qwen VL解析：**仅支持解析图片格式。可自主选择千问VL模型，并通过传入Prompt指定模型需要识别的版面、元素及内容，其余功能与大模型文档解析一致。
            
        -   **音视频解析：**对文件进行语音识别、视频帧提取（仅限视频）和剧情解析（仅限视频），最终将所有声画信息按时间轴结构化对齐。
            
            -   **语音识别：**字幕内容解析器通过[录音文件识别](https://help.aliyun.com/zh/model-studio/recording-file-recognition)将人类语音转为文本。暂不支持识别音乐或自然环境声（如喇叭声、钟声、雷声等）。
                
            -   **视频帧提取：**从原始视频中抽取有代表性的视觉画面，并生成相应的文本描述。
                
            -   **剧情解析（需手动开启）：**分析视频内容，定位具体事件并标注时间戳，同时生成相应的文本描述。
                
        
    4.  为文件**配置标签**（可选）。
        
        > [通过API调用应用](https://help.aliyun.com/zh/model-studio/application-calling-guide#4100253b7chc3)时，可以在请求参数`tags`中指定标签。应用在检索知识库时，会先根据标签筛选相关文件，从而提高检索效率。对于[智能体应用](https://help.aliyun.com/zh/model-studio/single-agent-application)，可在控制台编辑应用时直接设置标签（启用**知识库** > **+知识库** > **知识库高级配置** > **标签过滤**）。
        
    5.  点击**确认**，系统将开始解析和导入，可在页面查看任务进度。
        
        > 文件将被转换成阿里云百炼可处理的格式。在请求高峰时段，该过程可能需要数小时，请耐心等待。
        
    6.  导入完成后，点击相应文件右侧的**详情**即可查看导入的文件。
        
        > 文件导入阿里云百炼后，将作为独立副本（与原始数据没有关联）存储在平台提供的免费空间中，当前无容量限制。
        
        > 导入的文件仅供当前业务空间的用户使用。阿里云百炼不会将其用于任何商业用途或对外公开。
        

## 导入RDS MySQL数据

**重要**

-   新建数据源前需开通阿里云事件总线[EventBridge](https://eventbridge.console.aliyun.com/)服务。
    
-   阿里云百炼与RDS实例**必须归属同一阿里云账号**。否则请按照**导入自建MySQL数据**中步骤操作。
    
-   导入大数据表（**1,000,000**行以上）时，耗时可能超过数据库本地日志的保留时长，造成数据重复导入。[如何解决](#b44fa3ac75xg6)
    

> **RDS实例限制：**目前只支持**MySQL**引擎（版本无限制），暂不支持**PostgreSQL**等其它引擎；实例地域不限；只支持**基础系列**和**高可用系列**；创建RDS实例时，网络类型必须是**专有网络**，加入白名单需选**是**（将VPC网段加入到RDS实例白名单中）。

> **数据库和表限制：**知识库只能关联单个数据库中的一张表，不支持多表关联；关联表中的数据量最大为**10,000,000**行，且每一行记录的大小必须控制在**100**KB以内（超出将被截断）。

**网络类型**选择**公网**或**私网**。

> 私网数据源[仅支持部分地域](#b44fa3ac75xg6)的RDS实例；其他地域请选择公网数据源。私网数据源在安全性和性能方面更具优势。

## 新建公网数据源

1.  为确保知识库能正常接收RDS数据，请为RDS实例设置EventBridge白名单。
    
    > 若未正确设置白名单，创建数据源时会提示`Communications link failure`。
    
    **如何设置EventBridge白名单**
    
    1.  访问[RDS控制台](https://rdsnext.console.aliyun.com/)，点击左侧导航栏中的**实例列表**，然后点击包含数据表的RDS实例。接着，点击左侧导航栏中的**数据库连接**，点击外网地址旁的**设置白名单**。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8520240571/p960931.png)
        
    2.  点击**添加白名单分组**，并将以下 EventBridge 公网 IP 地址**全部添加**至白名单分组中。
        
        -   39.105.55.188,39.105.110.43,47.95.35.213,47.95.33.100,39.106.255.198,47.93.177.159,47.95.32.154,39.107.99.72
            
    3.  点击**确定**，白名单生效。
        
    
2.  填写数据源相关配置：
    
    **配置项**
    
    **说明**
    
    **数据源名称**
    
    数据源名称在同一个[业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)中应是唯一的。即使数据源创建失败，该名称也无法再次使用。
    
    **数据库实例**
    
    填写RDS实例ID。请前往[RDS控制台](https://rdsnext.console.aliyun.com/)，点击左侧导航栏中的**实例列表**获取。
    
    **数据库地址**
    
    填写RDS实例的外网地址。您可以在RDS实例的**数据库连接**界面获取该信息：前往[RDS控制台](https://rdsnext.console.aliyun.com/)，点击左侧导航栏中的**实例列表**，然后点击包含数据表的RDS实例。接着，点击左侧导航栏中的**数据库连接**，即可查看该实例对应的外网地址。
    
    > 若该 RDS 实例未开通外网地址，请先按照界面指引完成 RDS 外网地址开通。
    
    > 高可用系列RDS请勿使用**数据库代理连接**区域的**代理连接地址**或**内网地址**。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8520240571/p961377.png)
    
    **数据库端口**
    
    填写RDS实例的外网端口。该信息同样可以在RDS实例的**数据库连接**界面获取。
    
    **数据库用户名**
    
    数据库账号类型需为**高权限账号**，关于账号说明和获取方式请参见[创建账号](https://help.aliyun.com/zh/rds/apsaradb-rds-for-mysql/create-an-account-on-an-apsaradb-rds-for-mysql-instance#section-b3f-whz-q2b)。
    
    > 使用普通账号创建数据源时会提示`There is no permission:RELOAD`。
    
3.  点击**创建数据源**，提交新建任务。系统将自动配置 RDS 数据源，期间业务空间将被锁定，无法同时创建其他数据源。
    
    > 首次提交任务时，请根据界面指引开通EventBridge服务关联角色，请使用[主账号](https://help.aliyun.com/zh/model-studio/permission-management-overview#24ca2dad7djzs)操作。如需使用RAM用户，需主账号为该RAM用户[配置必要权限](https://help.aliyun.com/zh/model-studio/data-import-instructions#b0cbc9b177wvb)。
    
    > 在请求高峰时段，创建数据源过程可能需要几分钟，请耐心等待。
    
    **状态**
    
    **说明**
    
    **创建成功**
    
    表示数据源创建成功。请选择该数据源并执行[下一步](https://help.aliyun.com/zh/model-studio/data-import-instructions#fe7af7262307m)。
    
    **创建失败**
    
    表示数据源创建失败。请检查各项参数是否正确，修改后点击**重试**重新创建数据源。您可点击**删除**，删除创建失败的数据源。
    

## 新建私网数据源

1.  填写数据源相关配置：
    
    **配置项**
    
    **说明**
    
    **数据源名称**
    
    数据源名称在同一个[业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)中应是唯一的。即使数据源创建失败，该名称也无法再次使用。
    
    **所属地域**
    
    选择RDS实例[所在地域](https://help.aliyun.com/zh/model-studio/data-import-instructions#6e4bedffaedcy)。请前往[RDS控制台](https://rdsnext.console.aliyun.com/)，点击左侧导航栏中的**实例列表**获取。
    
    **数据库实例**
    
    填写RDS实例ID。请前往[RDS控制台](https://rdsnext.console.aliyun.com/)，点击左侧导航栏中的**实例列表**获取。
    
    **数据库地址**
    
    填写RDS实例的**内网地址**。您可以在RDS实例的**数据库连接**界面获取该信息：前往[RDS控制台](https://rdsnext.console.aliyun.com/)，点击左侧导航栏中的**实例列表**，然后点击包含数据表的RDS实例。接着，点击左侧导航中的**数据库连接**，即可查看该实例对应的**内网地址**。
    
    > 高可用系列RDS请勿使用**数据库代理连接**区域的**代理连接地址**或**内网地址**。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9520240571/p961406.png)
    
    **数据库端口**
    
    填写RDS实例的**内网端口**。该信息同样可以在RDS实例的**数据库连接**界面获取。
    
    **数据库用户名**
    
    数据库账号类型需为**高权限账号**，关于账号说明和获取方式请参见[创建账号](https://help.aliyun.com/zh/rds/apsaradb-rds-for-mysql/create-an-account-on-an-apsaradb-rds-for-mysql-instance#section-b3f-whz-q2b)。
    
    > 使用普通账号创建数据源时会提示`There is no permission:RELOAD`。
    
2.  连通性检测：点击**开始检测**，对阿里云百炼与数据源之间的网络连通性进行检查。
    
    > 首次检测时，请根据界面指引开通EventBridge服务关联角色，请使用[主账号](https://help.aliyun.com/zh/model-studio/permission-management-overview#24ca2dad7djzs)操作。如需使用RAM用户，需主账号为该RAM用户[配置必要权限](https://help.aliyun.com/zh/model-studio/data-import-instructions#b0cbc9b177wvb)。
    
    **VPC ID**
    
    应填写RDS实例的**VPC ID**。该信息同样可以在RDS实例的**数据库连接**界面获取。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8520240571/p961413.png)
    
    **VSwitch ID**
    
    将鼠标悬浮于RDS实例的VPC ID上即可显示VSwitch ID。
    
    > RDS MySQL高可用系列实例可能拥有多个 VSwitch ID，请完整填写该实例关联的所有 VSwitch ID。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8520240571/p961526.png)
    
    **安全组ID**
    
    可直接**使用托管安全组**；如需使用指定安全组，该安全组应为直接创建，非由第三方产品或服务间接创建。您可以前往[ECS控制台](https://ecs.console.aliyun.com/home)的**安全组**界面创建安全组。该安全组需满足以下要求：
    
    -   安全组的地域需与上方**所属地域**保持一致；
        
    -   安全组的网络需选择RDS所在的VPC；
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1538323571/p988790.png)
        
    -   安全组类型支持普通安全组和企业级安全组。
        
    -   安全组的网络**入方向**未设置任何访问限制；
        
        -   **正确示例：**
            
            ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8520240571/p961532.png)
            
        -   **错误示例：**![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9520240571/p961531.png)
            
    
3.  连通性检测通过后，点击**确认**，提交新建任务。系统将为您自动配置RDS数据源，期间当前业务空间会被锁定，禁止同时创建其他数据源。
    
    > 在请求高峰时段，创建数据源过程可能需要几分钟，请耐心等待。
    
    **状态**
    
    **说明**
    
    **创建成功**
    
    表示数据源创建成功。请选择该数据源并执行[下一步](https://help.aliyun.com/zh/model-studio/data-import-instructions#fe7af7262307m)。
    
    **创建失败**
    
    表示数据源创建失败。请检查各项参数是否正确，修改后点击**重试**重新创建数据源。您可点击**删除**，删除创建失败的数据源。
    

## 导入自建MySQL数据

**重要**

-   新建数据源前需开通阿里云事件总线[EventBridge](https://eventbridge.console.aliyun.com/)服务。
    
-   导入大数据表（**1,000,000**行以上）时，耗时可能超过数据库本地日志的保留时长，造成数据重复导入。[如何解决](https://help.aliyun.com/zh/model-studio/data-import-instructions#d152117985mus)
    

> **自建MySQL限制：**必须部署在阿里云ECS实例（地域不限）上；目前只支持MySQL 5.6、5.7和8.0；不支持MySQL代理Proxy。

> **数据库和表限制：**知识库只能关联单个数据库中的一张表，不支持多表关联；关联表中的数据量最大为**10,000,000**行，且每一行记录的大小必须控制在**100**KB以内（超出将被截断）。若最大行数限制无法满足实际业务需求，可提交工单申请调整。

**网络类型**选择**公网**或**私网**。

> 私网数据源[仅支持部分地域](https://help.aliyun.com/zh/model-studio/data-import-instructions#6e4bedffaedcy)的ECS实例；其他地域请选择公网数据源。私网数据源在安全性和性能方面更具优势。

## 新建公网数据源

1.  为确保知识库能正常接收数据，请为您的自建MySQL配置EventBridge白名单。
    
    > 若未正确配置白名单，创建数据源时会提示`Communications link failure`。
    
    **如何设置EventBridge白名单**
    
    1.  访问[ECS控制台](https://ecs.console.aliyun.com/home)，点击左侧导航栏中的**安全组**，找到与您自建MySQL关联的安全组，然后点击**操作**栏中的**管理规则。**
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8520240571/p968572.png)
        
    2.  在安全组详情页，点击**增加规则**，将以下EventBridge公网IP地址**全部添加**至该安全组中，并且需要放行**所有流量**和**全部端口**。
        
        > 不可使用由第三方产品或服务间接创建的安全组。
        
        -   39.105.55.188,39.105.110.43,47.95.35.213,47.95.33.100,39.106.255.198,47.93.177.159,47.95.32.154,39.107.99.72
            
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9520240571/p968577.png)
        
    3.  点击**确定**，安全组生效。
        
    4.  在您的MySQL中，创建一个允许全部来源流量的数据库账号（也可以使用已有账号）然后执行以下GRANT授权命令。
        
        > 请根据您的实际情况，将下方命令中的user1替换为您的实际数据库账号。
        
        ```
        -- 创建用户（合并为单条语句），请将user1替换为您的实际数据库账号
        CREATE USER 'user1'@'%' IDENTIFIED BY 'user1的密码';
        
        -- 授予基础权限（合并为单条语句），请将user1替换为您的实际数据库账号
        GRANT ALL PRIVILEGES ON *.* TO 'user1'@'%' WITH GRANT OPTION;
        
        -- 刷新权限（仅需一次）
        FLUSH PRIVILEGES;
        ```
        
    5.  通过修改MySQL配置文件开启Binlog和GTID。以Linux系统为例，MySQL配置文件一般位于：/etc/my.cnf 或 /etc/mysql/my.cnf。
        
        ```
        [mysqld]
        log-bin=mysql-bin
        server-id=1
        binlog_format=ROW
        gtid_mode=ON
        enforce_gtid_consistency=ON
        ```
        
    6.  重启MySQL，配置文件生效。
        
    
2.  填写数据源相关配置：
    
    **配置项**
    
    **说明**
    
    **数据源名称**
    
    数据源名称在同一个[业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)中应是唯一的。即使数据源创建失败，该名称也无法再次使用。
    
    **数据库地址**
    
    填写您自建MySQL的公网地址。
    
    **数据库端口**
    
    填写您自建MySQL的端口。
    
    **数据库用户名**
    
    填写您在前面加白步骤中执行过GRANT授权的数据库账号。
    
3.  点击**创建数据源**，提交新建任务。系统将为您自动配置自建MySQL数据源，期间当前业务空间会被锁定，禁止同时创建其他数据源。
    
    > 首次提交任务时，请根据界面指引开通EventBridge服务关联角色，请使用[主账号](https://help.aliyun.com/zh/model-studio/permission-management-overview#24ca2dad7djzs)操作。如需使用RAM用户，需主账号为该RAM用户[配置必要权限](https://help.aliyun.com/zh/model-studio/data-import-instructions#b0cbc9b177wvb)。
    
    > 在请求高峰时段，创建数据源过程可能需要几分钟，请耐心等待。
    
    **状态**
    
    **说明**
    
    **创建成功**
    
    表示数据源创建成功。请选择该数据源并执行[下一步](https://help.aliyun.com/zh/model-studio/data-import-instructions#fe7af7262307m)。
    
    **创建失败**
    
    表示数据源创建失败。请检查各项参数是否正确，修改后点击**重试**重新创建数据源。您可点击**删除**，删除创建失败的数据源。
    

## 新建私网数据源

1.  为确保知识库能正常接收数据，请为您的自建MySQL配置EventBridge白名单。
    
    > 若未正确配置白名单，创建数据源时会提示`Communications link failure`。
    
    **如何设置EventBridge白名单**
    
    1.  在您的MySQL中，创建一个允许全部来源流量的数据库账号（也可以使用已有账号）然后执行以下GRANT授权命令。
        
        > 请根据您的实际情况，将下方命令中的user1替换为您的实际数据库账号。
        
        ```
        -- 创建用户（合并为单条语句），请将user1替换为您的实际数据库账号
        CREATE USER 'user1'@'%' IDENTIFIED BY 'user1的密码';
        
        -- 授予基础权限（合并为单条语句），请将user1替换为您的实际数据库账号
        GRANT ALL PRIVILEGES ON *.* TO 'user1'@'%' WITH GRANT OPTION;
        
        -- 刷新权限（仅需一次）
        FLUSH PRIVILEGES;
        ```
        
    2.  通过修改MySQL配置文件开启Binlog和GTID。以Linux系统为例，MySQL配置文件一般位于：/etc/my.cnf 或 /etc/mysql/my.cnf。
        
        ```
        [mysqld]
        log-bin=mysql-bin
        server-id=1
        binlog_format=ROW
        gtid_mode=ON
        enforce_gtid_consistency=ON
        ```
        
    3.  重启MySQL，配置文件生效。
        
    
2.  填写数据源相关配置：
    
    **配置项**
    
    **说明**
    
    **数据源名称**
    
    数据源名称在同一个[业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)中应是唯一的。即使数据源创建失败，该名称也无法再次使用。
    
    **所属地域**
    
    请选择您自建MySQL所部署ECS实例所在地域。该信息可以前往[ECS控制台](https://ecs.console.aliyun.com/home)获取。
    
    **数据库地址**
    
    填写您自建MySQL的**私网地址**。您可以在ECS的**实例**界面获取该信息：前往[ECS控制台](https://ecs.console.aliyun.com/home)，点击左侧导航栏中的**实例**，即可查看对应实例的**私网地址**。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8520240571/p968587.png)
    
    **数据库端口**
    
    填写您自建MySQL的端口。
    
    **数据库用户名**
    
    填写您在前面加白步骤中执行过GRANT授权的数据库账号。
    
3.  连通性检测：点击**开始检测**，对阿里云百炼与数据源之间的网络连通性进行检查。
    
    > 首次提交任务时，请根据界面指引开通EventBridge服务关联角色，请使用[主账号](https://help.aliyun.com/zh/model-studio/permission-management-overview#24ca2dad7djzs)操作。如需使用RAM用户，需主账号为该RAM用户[配置必要权限](https://help.aliyun.com/zh/model-studio/data-import-instructions#b0cbc9b177wvb)。
    
    **VPC ID**
    
    填写您自建MySQL所部署ECS实例所在VPC的**实例ID**（vpc-xxxxxx）。该信息同样可以前往[ECS控制台](https://ecs.console.aliyun.com/home)获取。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8520240571/p968620.png)
    
    **VSwitch ID**
    
    实例VPC ID下方即是VSwitch ID（vsw-xxxxxx）。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9520240571/p968618.png)
    
    **安全组ID**
    
    可直接**使用托管安全组**；如需使用指定安全组，该安全组应为直接创建，非由第三方产品或服务间接创建。您可以前往[ECS控制台](https://ecs.console.aliyun.com/home)的**安全组**界面创建安全组。该安全组需满足以下要求：
    
    -   安全组的地域需与上方**所属地域**保持一致；
        
    -   安全组的网络需选择ECS所在的VPC；
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1538323571/p988802.png)
        
    -   安全组类型支持普通安全组和企业级安全组。
        
    -   **入方向**未设置任何访问限制；
        
        -   **正确示例：**
            
            ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8520240571/p961532.png)
            
        -   **错误示例：**![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9520240571/p961531.png)
            
    
4.  连通性检测通过后，点击**创建数据源**，提交新建任务。系统将为您自动配置MySQL数据源，期间当前业务空间会被锁定，禁止同时创建其他数据源。
    
    > 在请求高峰时段，创建数据源过程可能需要几分钟，请耐心等待。
    
    **状态**
    
    **说明**
    
    **创建成功**
    
    表示数据源创建成功。请选择该数据源并执行[下一步](https://help.aliyun.com/zh/model-studio/data-import-instructions#fe7af7262307m)。
    
    **创建失败**
    
    表示数据源创建失败。请检查各项参数是否正确，修改后点击**重试**重新创建数据源。您可点击**删除**，删除创建失败的数据源。
    

## **导入自建PostgreSQL数据**

**重要**

新建数据源前需开通[数据传输服务DTS](https://help.aliyun.com/zh/dts/product-overview/what-is-dts)。

> **自建PostgreSQL限制：**

> 必须部署在阿里云ECS实例（地域不限）上。

> **数据库和表限制：**

> 知识库只能关联单个数据库中的一张表，不支持多表关联；关联表中的数据量最大为10,000,000行，且每一行记录的大小必须控制在100 KB以内（超出将被截断）。若最大行数限制无法满足实际业务需求，可提交工单申请调整。

网络类型选择**私网**。

> 仅支持部分地域的ECS实例。私网数据源在安全性和性能方面更具优势。

**新建私网数据源**

1\. **填写数据源相关配置：**

**配置项**

**说明**

所属地域

请选择您自建PostgreSQL所部署ECS实例所在地域。该信息可以前往ECS控制台获取。

数据库地址

填写您自建PostgreSQL的内网IP地址。您可以在ECS的实例界面获取该信息：前往ECS控制台，单击左侧导航栏中的实例，即可查看对应实例的内网IP地址。

数据库端口

填写您自建PostgreSQL的端口。默认为5432。

数据库用户名

填写您在前面配置步骤中授权的数据库账号。

数据库密码

填写数据库密码。

数据库名称

必填字段，指定要连接的数据库名称（dbName）。

ecsId

用于自建的pgsql实例的ecs实例的Id。

2\. **连通性检测**：单击**开始检测**，对阿里云百炼与数据源之间的网络连通性进行检查。

> 首次提交任务时，请根据界面指引开通DTS服务关联角色，请使用主账号操作。如需使用RAM用户，需主账号为该RAM用户配置必要权限。

**配置项**

**说明**

VPC ID

填写您自建PostgreSQL所部署ECS实例所在VPC的ID（vpc-xxxxxx）。该信息同样可以前往ECS控制台获取。

VSwitch ID

实例VPC ID下方即是VSwitch ID（vsw-xxxxxx）。

安全组

可直接使用托管安全组；如需使用指定安全组，该安全组应为直接创建，非由第三方产品或服务间接创建。您可以前往ECS控制台的安全组界面创建安全组。该安全组需满足以下要求：

\- 安全组的地域需与上方所属地域保持一致；

\- 安全组的网络需选择ECS所在的VPC；

\- 安全组类型支持普通安全组和企业级安全组。

\- 入方向未设置任何访问限制。

3\. 连通性检测通过后，单击**确认**，提交任务。系统将为您自动配置PostgreSQL数据源，期间当前业务空间会被锁定，禁止同时创建其他数据源。

> 在请求高峰时段，创建数据源过程可能需要几分钟，请耐心等待。

**状态**

**说明**

创建成功

表示数据源创建成功。请选择该数据源并执行选择数据表。

创建失败

表示数据源创建失败。请检查各项参数是否正确，修改后单击重新创建数据源。您可单击删除，删除创建失败的数据源。

## **查看连接器详情**

在[连接器列表页](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/connector/list)，单击目标连接器的**详情**按钮，进入连接器详情页。详情页包含以下标签页：

-   **概览**:显示连接器的基本信息（名称、描述、类型、创建时间、存储配额等）和自动生成的工具列表。
    
-   **文件/表格**（仅平台托管类型）：管理连接器中的文件或表格数据。
    
-   **工具：**查看连接器自动生成的工具详情,包括参数说明和在线测试。
    

您可以在连接器详情页展开工具,填写参数后单击**运行**按钮，在线测试工具的返回结果。

## **管理连接器**

-   **编辑**：点击卡片进入连接器详情页,单击右上角的**编辑**按钮，可以修改连接器的**名称**和**描述**。连接器类型和存储方式创建后不可更改。
    
-   **复制**：在连接器列表页或详情页，单击**复制**按钮，可以基于当前连接器的配置快速创建一个新的连接器。
    
-   **删除**：在连接器列表页，单击目标连接器卡片上的**更多**图标（`···`），选择**删除**；或在连接器详情页单击**删除**按钮。
    
    **重要**
    
    删除前需确认，**删除后无法恢复**。
    

## **在智能体中使用数据连接器**

创建连接器后，在智能体应用中配置数据连接器工具，使智能体在对话中自动调用这些工具来查询和引用外部数据。

1.  在智能体配置页面左侧,单击**技能**，找到**数据连接器**区域。
    
2.  单击数据连接器区域的**+**按钮,在弹出的**选择数据连接器**对话框中：
    
    1.  浏览或搜索目标连接器，支持按连接器类型筛选。
        
    2.  单击目标连接器的**添加**按钮。
        

-   添加后，连接器的工具会自动显示在配置列表中。您可以单击工具右侧的设置按钮调整参数。
    
-   **发布**智能体，即可在对话中自动调用这些工具。
    

## **在工作流中使用数据连接器**

创建连接器后，您可以在工作流应用中添加数据连接器节点，使工作流在执行过程中调用连接器工具来查询外部数据，并将结果传递给下游节点处理。

1.  在工作流画布配置页面，展开左侧**节点库**，在**工具**分类下找到**数据连接器**，将其拖拽到画布中。
    
2.  在弹出的**选择数据连接器**对话框中：
    
    -   浏览或搜索目标连接器，支持按连接器类型（文件、表格、MySQL、PostgreSQL、语雀、OSS）筛选。
        
    -   展开连接器，选择要使用的工具（如 searchFile、getFile），然后单击**确定**。
        
3.  配置节点输入：在节点配置面板的**输入**区域，为工具参数设置引用方式，将上游节点的输出或内置变量映射到工具所需的参数（如 fileId）。
    
4.  连接节点：将数据连接器节点与上下游节点通过连线连接，确保数据流向正确。
    
5.  节点输出为 result 对象，包含 content（Array<Object>，返回内容）和 isError（Boolean，是否发生错误）两个字段，供下游节点引用。
    

**说明**

工作流中每个数据连接器节点只能关联一个工具。如需使用同一连接器的多个工具，请添加多个数据连接器节点。

## **相关文档**

创建知识库导入数据源内容，用于后续检索：[创建和使用知识库](https://help.aliyun.com/zh/model-studio/rag-knowledge-base)。

应用配置和使用指南：[应用类型介绍](https://help.aliyun.com/zh/model-studio/application-introduction)。

## **常见问题**

### **权限与安全**

-   **数据导入时，遇到报错“缺少该模块的权限”，应如何处理？**
    
    [RAM用户](https://help.aliyun.com/zh/model-studio/permission-management-overview#24ca2dad7djzs)需主账号授予`管理员`权限，参见[页面权限](https://help.aliyun.com/zh/model-studio/member-management#febd776ce5lbx)。
    

### **导入OSS文件**

-   **从OSS导入文件配置说明**
    
    首次从OSS导入文件时，需要授权阿里云百炼访问OSS资源。[主账号](https://help.aliyun.com/zh/model-studio/permission-management-overview#24ca2dad7djzs)与子账号的授权流程不同。
    
    ## 主账号授权
    
    1.  在导入数据页面，点击**前往授权**。
        
    2.  在弹出的对话框中，点击**确认授权**，系统将自动创建[OSS服务关联角色](https://help.aliyun.com/zh/model-studio/bailian-service-linked-role#32a41eac73z64)，允许阿里云百炼访问OSS资源。
        
        > 通常秒级生效（高峰期可能延迟）。
        
    3.  为目标 OSS Bucket 添加`bailian-datahub-access`标签（值为`read`）。
        
        > 该标签用于标记阿里云百炼可访问的 Bucket，未标记的 Bucket 阿里云百炼无法访问。
        
        1.  访问[OSS管理控制台](https://oss.console.aliyun.com/)，点击左侧导航栏中的**Bucket 列表**，找到目标 Bucket。
            
        2.  悬停鼠标在其![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0707990571/p978639.png)图标上，点击**编辑**（若未设置过标签）或**前往编辑**。
            
        3.  在Bucket标签页面，点击**创建标签**（若未设置过标签）或**设置**。
            
        4.  点击**标签**，添加标签名为`bailian-datahub-access`，标签值为`read`的标签，然后点击**保存**。
            
    4.  返回**导入数据**页面，重新选择目标 Bucket 再尝试导入。
        
        > **注意：阿里云百炼不支持访问 Bucket 根目录下的文件**，请选择已有的子目录或新建一个子目录供阿里云百炼访问。
        
    
    ## **子账号授权**
    
    1.  在导入数据页面，点击**前往授权**。
        
    2.  在弹出的对话框中，点击**确认授权**。若界面提示**授权失败**、**当前用户没有创建服务关联角色的权限**，需先授予子账号创建服务关联角色的权限。
        
        1.  **需主账号登录**[RAM控制台](https://ram.console.aliyun.com/)，在左侧导航栏，选择**权限管理** > **权限策略**，然后点击页面上的**创建权限策略**。
            
        2.  点击**脚本编辑**，将下方提供的完整JSON策略复制并粘贴至编辑框，点击**确定**。
            
            ```
            {
                "Action": [
                    "ram:CreateServiceLinkedRole"
                ],
                "Resource": "*",
                "Effect": "Allow",
                "Condition": {
                    "StringEquals": {
                        "ram:ServiceName": "datahub.sfm.aliyuncs.com"
                    }
                }
            }
            ```
            
        3.  输入权限策略名称（如服务关联角色）后，点击**确定**。
            
        4.  在左侧导航栏，选择**身份管理** > **用户**。在页面列表中找到待授权的子账号，然后点击子账号**操作**列的**添加权限**。
            
        5.  在权限策略中选择刚才创建的权限策略（自定义策略），点击**确认新增授权**。至此，子账号拥有了创建服务关联角色的权限。
            
    3.  授权子账号通过阿里云百炼访问OSS。
        
        1.  返回**导入数据**页面，点击**前往授权**。
            
        2.  在弹出的对话框中，点击**确认授权**，系统将自动创建[OSS服务关联角色](https://help.aliyun.com/zh/model-studio/bailian-service-linked-role#32a41eac73z64)（必要条件）。
            
            > 通常秒级生效（高峰期可能延迟）。
            
    4.  为目标 OSS Bucket 添加`bailian-datahub-access`标签，值为`read`。
        
        > 该标签用于标记阿里云百炼可访问的 Bucket，未标记的 Bucket 阿里云百炼无法访问。
        
        1.  访问[OSS管理控制台](https://oss.console.aliyun.com/)，点击左侧导航栏中的****Bucket 列表****，找到目标Bucket。
            
        2.  悬停鼠标在其![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0707990571/p978639.png)图标上，点击**编辑**（若未设置过标签）或**前往编辑**。
            
        3.  在Bucket标签页面，点击**创建标签**（若未设置过标签）或**设置**。
            
        4.  点击**标签**，添加标签名为`bailian-datahub-access`，标签值为`read`的标签，然后点击**保存**。
            
    5.  返回**导入数据**页面，重新选择目标 Bucket 再尝试导入。
        
        > **注意：阿里云百炼不支持访问 Bucket 根目录下的文件**，请选择已有的子目录或新建一个子目录供阿里云百炼访问。
        
    
-   **导入OSS文件遇到“10041495”报错，应如何处理？**
    
    通常是主账号未开通OSS服务，处理步骤：
    
    1.  需主账号前往[OSS管理控制台](https://oss.console.aliyun.com/)，按界面指引开通 OSS。
        
    2.  返回阿里云百炼页面，再尝试授权。
        
    

### **导入MySQL数据**

-   **私网数据源支持哪些地域的RDS与ECS实例？**
    
    -   华东1（杭州）
        
    -   华东2（上海）
        
    -   华南1（深圳）
        
    -   华南2（河源）
        
    -   华南3（广州）
        
    -   华北1（青岛）
        
    -   华北2（北京）
        
    -   华北3（张家口）
        
    -   华北5（呼和浩特）
        
    -   华北6（乌兰察布）
        
    -   西南1（成都）
        
    

-   **我想使用RAM用户开通EventBridge服务关联角色，应如何为该RAM用户配置权限？**
    
    1.  主账号为RAM用户配置如下三个系统策略：`AliyunBailianFullAccess`、`AliyunEventBridgeFullAccess`和`AliyunRDSReadOnlyAccess`。具体操作请参考[为RAM用户授权](https://help.aliyun.com/zh/ram/user-guide/grant-permissions-to-the-ram-user)。
        
    2.  主账号为RAM用户配置**创建服务关联角色**系统策略。
        
        1.  使用主账号登录[RAM控制台](https://ram.console.aliyun.com/)，在左侧导航栏，选择**权限管理** > **权限策略**，然后点击页面上的**创建权限策略**。
            
        2.  在**脚本编辑**的`Effect`、`Action`、`Resource`、`Condition`中分别输入以下脚本中的对应内容后，点击**确定**。
            
            ```
            {
                "Version": "1",
                "Statement": [
                    {
                        "Action": "ram:CreateServiceLinkedRole",
                        "Resource": "*",
                        "Effect": "Allow"
                    }
                ]
            }
            ```
            
        3.  输入权限策略名称`CreateServiceLinkedRole`后，点击**确定**。
            
        4.  在左侧导航栏，选择**身份管理** > **用户**。从页面列表中找到待授权的RAM 用户，然后点击RAM 用户**操作**列的**添加权限**。
            
        5.  从**权限策略**列表中，选择刚创建的权限策略（CreateServiceLinkedRole），然后点击**确认新增授权**。至此，RAM 用户拥有了创建服务关联角色的权限。
            
    3.  完成以上步骤1和2后，返回**创建数据源**界面，使用RAM用户再尝试开通**EventBridge服务关联角色**。
        
    

-   **系统提示“数据库配置校验不通过，您选择的表数据量较大”，应如何处理？**
    
    ## 阿里云RDS MySQL
    
    上方仅为示意图，提示中的建议项和建议值会根据您表中数据量不同而不同。若无对应建议项，则无需调整。
    
    以下步骤请使用阿里云账号（主账号）操作。
    
    -   **如何配置本地日志保留时长：**
        
        1.  前往[RDS控制台](https://rdsnext.console.aliyun.com/)，点击左侧导航栏中的**实例列表**，然后点击包含该数据表的RDS实例。接着点击左侧导航栏中的**备份恢复**，再点击**备份策略**选项卡，即可看到**保留时长**设置项。
            
        2.  修改**保留时长**为提示中提供的建议值。
            
    -   **如何配置wait\_timeout：**
        
        1.  前往[RDS控制台](https://rdsnext.console.aliyun.com/)，点击左侧导航栏中的**实例列表**，然后点击包含数据表的RDS实例。接着点击左侧导航栏中的**参数设置**，再点击**可修改参数**选项卡，即可看到`wait_timeout`设置项。
            
        2.  改为提示中提供的建议值。
            
    
    ## 自建MySQL
    
    > 仅为示意图，提示中的建议项和建议值会根据您表中数据量不同而不同。若无对应建议项，则无需调整。
    
    -   **如何设置本地日志保留时长：**
        
        -   方式一（临时生效）：通过执行SET GLOBAL命令修改`expire_logs_days`（MySQL 5.7及以下版本）或`binlog_expire_logs_seconds`（MySQL 8.0及以上版本），该修改将在下次MySQL重启后失效。
            
            ## MySQL 5.7及以下版本
            
            1.  执行命令：
                
                > 请将下方参数值 15 替换为提示中提供的建议值。
                
                ```
                SET GLOBAL expire_logs_days = 15;
                ```
                
            2.  验证修改是否已生效，执行命令：
                
                ```
                SHOW VARIABLES LIKE 'expire_logs_days';
                ```
                
            
            ## MySQL 8.0及以上版本
            
            1.  执行命令：
                
                > 请将下方参数值 1296000 替换为提示中提供的建议值。
                
                ```
                SET GLOBAL binlog_expire_logs_seconds = 1296000;
                ```
                
            2.  验证修改是否已生效，执行命令：
                
                ```
                SHOW VARIABLES LIKE 'binlog_expire_logs_seconds';
                ```
                
            
        -   方式二（永久生效）：通过MySQL配置文件设置`expire_logs_days`（MySQL 5.7及以下版本）或`binlog_expire_logs_seconds`（MySQL 8.0及以上版本），但该方式需重启MySQL服务。
            
            ## MySQL 5.7及以下版本
            
            1.  以Linux系统为例，MySQL配置文件一般位于：/etc/my.cnf 或 /etc/mysql/my.cnf。若文件中已包含`expire_logs_days`，可直接修改；若不存在，请手动添加。
                
                > 请将下方参数值 15 替换为提示中提供的建议值。
                
                ```
                [mysqld]
                expire_logs_days = 15
                ```
                
            2.  保存配置文件后，请您手动重启MySQL服务。
                
            3.  验证修改是否已生效，执行命令：
                
                ```
                SHOW VARIABLES LIKE 'expire_logs_days';
                ```
                
            
            ## MySQL 8.0及以上版本
            
            1.  以Linux系统为例，MySQL配置文件一般位于：/etc/my.cnf 或 /etc/mysql/my.cnf。若文件中已包含`binlog_expire_logs_seconds`，可直接修改；若不存在，请手动添加。
                
                > 请将下方参数值 15 替换为提示中提供的建议值。
                
                ```
                [mysqld]
                binlog_expire_logs_seconds = 1296000
                ```
                
            2.  保存配置文件后，请您手动重启MySQL服务。
                
            3.  验证修改是否已生效，执行命令：
                
                ```
                SHOW VARIABLES LIKE 'binlog_expire_logs_seconds';
                ```
                
            
    -   **如何设置wait\_timeout：**
        
        -   方式一（临时生效）：通过执行SET GLOBAL命令修改`wait_timeout`（单位是秒），该修改将在下次MySQL重启后失效。
            
            1.  执行命令：
                
                > 请将下方参数值 1159200 替换为提示中提供的建议值。
                
                > 该命令将影响所有新建立的连接。已存在的连接不受此设置影响。
                
                ```
                SET GLOBAL wait_timeout = 1159200;
                ```
                
            2.  验证修改是否已生效，执行命令：
                
                ```
                SHOW VARIABLES LIKE 'wait_timeout';
                ```
                
        -   方式二（永久生效）：通过MySQL配置文件设置`wait_timeout`（单位是秒），但该方式需重启MySQL服务。
            
            1.  以Linux系统为例，MySQL配置文件一般位于：/etc/my.cnf 或 /etc/mysql/my.cnf。若文件中已包含`wait_timeout`，可直接修改；若不存在，请手动添加。
                
                > 请将下方参数值 1159200 替换为提示中提供的`wait_timeout`建议值。
                
                ```
                [mysqld]
                wait_timeout = 1159200
                ```
                
            2.  保存配置文件后，请您手动重启MySQL服务。
                
            3.  验证修改是否已生效，执行命令：
                
                ```
                SHOW VARIABLES LIKE 'wait_timeout';
                ```
