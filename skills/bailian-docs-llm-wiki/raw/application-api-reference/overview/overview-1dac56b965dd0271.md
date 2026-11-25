# 版本管理

上传、查询和下载 Skill 版本。

版本管理接口用于为自定义 Skill 上传新版本，查询版本列表和详情，以及获取版本 ZIP 包的下载地址。

| 接口 | 方法 | 说明 |
| --- | --- | --- |
| [创建版本](overview/create-66b335d7c24c1f0f.md) | POST `/api/v1/skills/{skill_id}/versions` | 上传新版本 ZIP 包 |
| [列出版本](overview/list-ee346a0747aae1d4.md) | GET `/api/v1/skills/{skill_id}/versions` | 分页查询版本 |
| [获取版本详情](overview/get-2856ed31dd1c9b3d.md) | GET `/api/v1/skills/{skill_id}/versions/{version}` | 查询指定版本 |
| [下载版本 ZIP](overview/download.md) | GET `/api/v1/skills/{skill_id}/versions/{version}/content` | 获取 ZIP 包的临时下载地址 |

版本号格式为 `major.minor`，由服务端递增，不能指定。旧版本保留。挂载到智能体时必须指定具体版本，后续上传新版本不影响已挂载的智能体。
