# 版本管理

上传、查询和下载 Skill 版本。

版本管理接口用于为自定义 Skill 上传新版本，查询版本列表和详情，以及获取版本 ZIP 包的下载地址。

接口

方法

说明

[创建版本](raw/application-api-reference/overview/overview/create.md)

POST `/api/v1/skills/{skill_id}/versions`

上传新版本 ZIP 包

[列出版本](raw/application-api-reference/overview/overview/list.md)

GET `/api/v1/skills/{skill_id}/versions`

分页查询版本

[获取版本详情](raw/application-api-reference/overview/overview/get.md)

GET `/api/v1/skills/{skill_id}/versions/{version}`

查询指定版本

[下载版本 ZIP](raw/application-api-reference/overview/overview/download.md)

GET `/api/v1/skills/{skill_id}/versions/{version}/content`

获取 ZIP 包的临时下载地址

版本号格式为 `major.minor`，由服务端递增，不能指定。旧版本保留。挂载到智能体时必须指定具体版本，后续上传新版本不影响已挂载的智能体。
