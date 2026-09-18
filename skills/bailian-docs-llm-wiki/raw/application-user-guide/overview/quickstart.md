# 快速开始

连接第一个 App，并在支持 MCP 的客户端中调用它的工具。

这篇指南用文件连接器走一遍完整流程：创建连接、确认自动生成的工具、把 Connector 接入客户端并发起第一次调用。全程大约 10 分钟。

## 前置条件

-   一个阿里云账号，且已开通阿里云百炼。
-   一个阿里云百炼业务空间，以及该空间的业务空间 ID，形如 `llm-xxxxxxxxxxxx`。
-   一个 DashScope API Key。在阿里云百炼控制台的 **API-KEY** 页面创建。
-   一个支持 MCP 的客户端，例如 Qoder。

**说明**RAM 用户需要主账号先完成授权才能使用 Connector。

## 第 1 步：创建连接

1.  **打开 Apps 目录**：进入 Connector 控制台，在左侧导航单击 **Apps**，页面会列出全部可连接的 App。
    
2.  **选择文件连接器**：找到 **文件连接器** 卡片，单击卡片上的 **连接**。
    
    文件连接器用于托管非结构化文档，例如 PDF、Word、Markdown。它不需要外部系统的凭证，最适合用来跑通第一次流程。
    
    **说明**语雀、Salesforce、MaxCompute 等 App 的连接对话框里只有一个身份验证配置下拉框，需要先创建配置才能连接。流程见[身份验证概览](raw/application-user-guide/overview/auth-guide/overview.md)。
    
3.  **填写连接信息**。在弹出的对话框中填写：
    
    字段
    
    是否必填
    
    说明
    
    连接器名称
    
    是
    
    用于区分同一 App 下的多个连接，最多 64 个字符。例如 `产品文档库`
    
    连接器描述
    
    否
    
    说明这个连接存了什么、用在什么场景。智能体会参考描述判断该不该调用，建议写清楚
    
    存储位置
    
    是
    
    只有 **使用平台存储** 一个选项，数据存放在平台提供的免费存储额度内
    
    **重要**描述不是摆设，它会影响智能体选择工具的准确度。只写文档两个字，智能体无法判断该不该调用；写成产品手册与发布说明，供回答产品功能问题时引用，效果要好得多。
    
4.  **确认创建**：单击 **确认**。返回 Apps 列表后，文件连接器卡片上会显示已连接的数量。
    

## 第 2 步：确认自动生成的工具

单击 **文件连接器** 卡片进入详情页，可以看到两块内容：

-   **已连接的用户**：列出该 App 下的所有连接实例，含名称、状态和创建时间。单击名称旁的编辑图标可以改名。
-   **可用的工具**：Connector 自动生成的工具。展开任一工具可查看入参与出参。

文件连接器固定生成 2 个工具：

工具

功能

入参

搜索文件

按文件标题的关键词查询文件列表，返回文件的下载链接

`keyWord`（string，必填）：文件标题的关键词  
`maxCount`（integer，可选）：返回数量，默认 5，最大 10

获取文件

按文件 ID 获取文件，返回文件的下载链接

`fileId`（string，必填）：文件 ID

**说明**工具是连接建立后自动生成的，数量和参数由 App 类型决定，不需要也无法手动配置。不同 App 生成的工具不同，详见[各 App 的说明](raw/application-user-guide/overview/apps-guide/overview.md)。

## 第 3 步：导入几个文件

工具能搜到内容，前提是连接器里有数据。文件连接器的数据通过类目组织。

1.  **新建类目**：进入连接器的文件管理页面，在左侧类目区域新建一个类目，例如 `产品手册`。
2.  **上传文件**：单击 **导入数据**，导入方式选择本地上传，选择几个 PDF 或 Word 文件。
3.  **等待解析完成**：平台会把文件转换成可检索的格式。文件较多或处于高峰时段时，解析可能需要较长时间。

完整的导入方式见[文件连接器](https://help.aliyun.com/zh/model-studio/connector/apps/file#%E5%AF%BC%E5%85%A5%E6%95%B0%E6%8D%AE)。

## 第 4 步：接入客户端

Connector 通过一个 MCP 地址对外提供服务，这个地址覆盖当前业务空间下全部已连接的 App。

1.  **找到 MCP 配置入口**：在你使用的客户端中找到 MCP 或连接器配置入口。
    
2.  **添加 MCP 服务器**。把下面的配置加入客户端的 MCP 配置文件：
    
    ```
    {
      "mcpServers": {
        "bailian-connector-mcp": {
          "type": "http",
          "url": "https://${workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/connector/mcp",
          "headers": {
            "Authorization": "Bearer ${DASHSCOPE_API_KEY}"
          }
        }
      }
    }
    ```
    
3.  **替换两个变量**：
    
    -   `${workspaceId}` 替换为你的阿里云百炼业务空间 ID。
    -   `${DASHSCOPE_API_KEY}` 替换为你的 DashScope API Key。
    
    **警告**API Key 属于敏感凭证，不要分享给他人或提交到代码仓库。如果客户端支持环境变量注入，优先使用该方式，避免密钥以明文形式保存在配置文件里。
    
4.  **验证连接**：保存配置并重启或刷新客户端。在 MCP 服务器列表中确认 `bailian-connector-mcp` 显示为已连接，展开后能看到 Connector 提供的工具。
    

如果使用 Qoder、Qoder Work 或 Qwen Work，可以在控制台的 **安装** 页面一键安装，不必手写配置。

## 第 5 步：发起第一次调用

在客户端里用自然语言提问，例如：

```
帮我在产品文档里找一下和计费相关的文件
```

客户端会调用搜索文件工具，返回匹配的文件列表和下载链接。

## 连接失败怎么排查

现象

可能原因

返回 401

鉴权请求头缺失，或 API Key 无效、已过期

返回 404

MCP 地址填写有误，检查路径是否为 `/api/v2/connector/mcp`

服务器列表中显示未连接

业务空间 ID 填错，或网络无法访问 `cn-beijing.maas.aliyuncs.com`

已连接但工具列表为空

当前业务空间下还没有任何已连接的 App

## 下一步

-   [核心概念](raw/application-user-guide/overview/concepts.md)：理解 App、连接器实例与工具的层级关系。
-   [连接更多 App](raw/application-user-guide/overview/apps-guide/overview.md)：连接钉钉、语雀、数据库等真实业务系统。
-   [身份验证](raw/application-user-guide/overview/auth-guide/overview.md)：连接语雀、Salesforce 前，先建好身份验证配置。
-   [管理文件与类目](raw/application-user-guide/overview/apps-guide/file.md)：用类目组织文件，按需从本地或 OSS 批量导入。
