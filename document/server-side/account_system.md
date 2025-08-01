# 用户体系集成

<Toc />

环信即时通讯 RESTful API 可实现用户体系建立和管理，包括用户注册、获取、修改、删除、封禁、解禁、强制下线等。

## 公共参数

以下表格列举了环信 IM 的 RESTful 接口的公共请求参数和响应参数：

#### 请求参数 

| 参数       | 类型   | 是否必需 | 描述         |
| :--------- | :----- | :------- | :------------------------- |
| `host`     | String | 是       | 环信即时通讯 IM 分配的用于访问 RESTful API 的域名。详见 [获取环信即时通讯 IM 的信息](enable_and_configure_IM.html#获取环信即时通讯-im-的信息)。 |
| `org_name` | String | 是       | 环信即时通讯 IM 为每个公司（组织）分配的唯一标识。详见 [获取环信即时通讯 IM 的信息](enable_and_configure_IM.html#获取环信即时通讯-im-的信息)。  |
| `app_name` | String | 是       | 你在环信即时通讯云控制台创建应用时填入的应用名称。详见 [获取环信即时通讯 IM 的信息](enable_and_configure_IM.html#获取环信即时通讯-im-的信息)。  |

#### 响应参数

| 参数                 | 类型   | 描述            |
| :------------------- | :----- | :-------------------------------------------- |
| `action`             | String | 请求方法。                                   |
| `organization`       | String | 环信即时通讯 IM 为每个公司（组织）分配的唯一标识，与请求参数 `org_name` 相同。          |
| `application`        | String | 系统内为应用生成的唯一标识，开发者无需关心。          |
| `applicationName`    | String | 你在环信即时通讯云控制台创建应用时填入的应用名称，与请求参数 `app_name` 相同。    |
| `uri`                | String | 请求 URL。                |
| `path`               | String | 请求路径，属于请求 URL 的一部分，开发者无需关注。       |
| `entities`           | JSON Array | 响应实体。          |
|  - `uuid`      | String | 用户的 UUID。即时通讯服务为该请求中的 app 或用户生成的唯一内部标识，用于生成 User Token。      |
|  - `type`      | String | 对象类型，无需关注。             |
|  - `created`   | Long   | 注册用户的 Unix 时间戳，单位为毫秒。      |
|  - `modified`  | Long   | 最近一次修改用户信息的 Unix 时间戳，单位为毫秒。       |
|  - `username`  | String | 用户 ID。            |
|  - `nickname`  | String | 推送消息时，在消息推送通知栏内显示的昵称。     |
|  - `activated` | Bool   | 用户是否为正常状态：<br/> - `true`：用户为正常状态。<br/> - `false`：用户为封禁状态。如要使用已被封禁的用户账户，你需要调用[解禁用户](#账号解禁)方法解除封禁。 |
| `data`               | JSON   | 实际获取的数据详情。            |
| `timestamp`          | Long   | HTTP 响应的 Unix 时间戳，单位为毫秒。       |
| `duration`           | Long   | 从发送 HTTP 请求到响应的时长, 单位为毫秒。     |

## 前提条件

要调用环信即时通讯 RESTful API，请确保满足以下要求：

- 已在环信即时通讯云控制台 [开通配置环信即时通讯 IM 服务](enable_and_configure_IM.html)。
- 已从服务端获取 app token，详见 [使用 App Token 鉴权](easemob_app_token.html)。
- 了解环信 IM API 的调用频率限制，详见 [接口频率限制](limitationapi.html)。

## 认证方式

环信即时通讯 REST API 要求 Bearer HTTP 认证。每次发送 HTTP 请求时，都必须在请求头部填入如下 `Authorization` 字段：

`Authorization: Bearer YourAppToken`

为提高项目的安全性，环信使用 Token（动态密钥）对即将登录即时通讯系统的用户进行鉴权。本文介绍的即时通讯所有 REST API 均需使用 App Token 的鉴权方式，详见 [使用 App Token 鉴权](easemob_app_token.html)。

## 注册用户

### 开放注册单个用户

#### 功能说明

- 开放注册指用户可以在登录客户端 SDK 后自行通过账号密码注册账号。
- 一般在体验 Demo 和测试开发环境时使用。
- 使用前需先在[环信即时通讯云控制后台](https://console.easemob.com/user/login)打开相应应用的开放注册开关，即在控制台首页的 **应用列表** 下点击目标应用的 **操作** 一栏中的 **管理**，然后选择 **即时通讯** > **服务概览**，在页面的 **设置** 区域中将 **用户注册模式** 设置为 **开放注册**。
- 调用该 API 无需传入 token。
- 注册用户时，需满足用户 ID 和密码的设置要求。

**调用频率上限**：该 API、用户账户管理的其他接口、以及离线推送的相关接口的总调用频率上限为 100 次/秒/App Key，详见 [接口频率限制文档](limitationapi.html#用户体系管理)。

#### HTTP 请求

```http
POST https://{host}/{org_name}/{app_name}/users
```

##### 请求 Header

| 参数           | 类型   | 是否必需 | 描述                                |
| :------------- | :----- | :------- | :---------------------------------- |
| `Content-Type` | String | 是       | 内容类型。请填 `application/json`。 |

##### 请求 body

| 参数       | 类型   | 是否必需 | 描述          |
| :--------- | :----- | :------- | :-------------------------------------------- |
| `username` | String | 是       | 用户 ID，长度不可超过 64 个字节。不可设置为空。支持以下字符集：<br/>- 26 个小写英文字母 a-z；<br/>- 10 个数字 0-9；<br/>- “\_”, “-”, “.”。 <br/><Container type="notice" title="注意"><br/>- 请勿使用大写英文字母 A-Z。若你同时使用了大写字母和小写字母，响应中返回的用户 ID 只包含小写字母。<br/>- 请确保同一个 app 下，用户 ID 唯一；<br/>- 用户 ID 为公开信息，请勿使用 UUID、邮箱地址、手机号等敏感信息。</Container> |
| `password` | String | 是       | 用户的登录密码，长度不可超过 64 个字符。  |
| `nickname` | String | 否       | 离线推送时在接收方的客户端推送通知栏中显示的发送方的昵称。你可以自定义该昵称，长度不能超过 100 个字符。<br/>支持以下字符集：<br/> - 26 个小写英文字母 a-z；<br/> - 26 个大写英文字母 A-Z；<br/> - 10 个数字 0-9；<br/> - 中文；<br/> - 特殊字符。<Container type="tip" title="提示">1. 若不设置昵称，推送时会显示发送方的用户 ID，而非昵称。<br/>2. 该昵称可与用户属性中的昵称设置不同，不过我们建议这两种昵称的设置保持一致。因此，修改其中一个昵称时，也需调用相应方法对另一个进行更新，确保设置一致。更新用户属性中的昵称的方法，详见 [设置用户属性](userprofile.html#设置用户属性)。</Container> |

其他参数及说明详见 [公共参数](#公共参数)。

#### HTTP 响应

##### 响应 body

如果返回的 HTTP 状态码为 `200`，表示请求成功，响应包体中包含以下字段：

响应字段及说明详见 [公共参数](#公共参数)。

如果返回的 HTTP 状态码非 `200`，表示请求失败。你可以参考 [错误码](#错误码)了解可能的原因。

#### 示例

##### 请求示例

```shell
## 无需传入 token
curl -X POST -i "https://XXXX.com/XXXX-demo/XXXX/users" -d '{"username":"user1","password":"123","nickname":"testuser"}'
```

##### 响应示例

```json
{
  "action": "post",
  "application": "8be024f0-e978-XXXX-XXXX-5d598d5f8402",
  "path": "/users",
  "uri": "https://XXXX.com/XXXX-demo/XXXX/users",
  "entities": [
    {
      "uuid": "0ffe2d80-XXXX-XXXX-8d66-279e3e1c214b",
      "type": "user",
      "created": 1542795196504,
      "modified": 1542795196504,
      "username": "user1",
      "activated": true
    }
  ],
  "timestamp": 1542795196515,
  "duration": 0,
  "organization": "XXXX-demo",
  "applicationName": "XXXX"
}
```

#### 错误码

如果返回的 HTTP 状态码非 `200`，表示请求失败，可能提示以下错误码：

| HTTP 状态码        | 错误类型 | 错误提示          | 可能原因 | 处理建议 |
| :----------- | :--- | :------------- | :----------- | :----------- |
| 400         | illegal_argument  | username XXX is not legal   | 用户名不合法。  | 查看注册用户名[规范](#开放注册单个用户)。 |
| 400         | illegal_argument | USERNAME_TOO_LONG  | 用户长度超过限制。  | 查看注册用户名[规范](#开放注册单个用户)。 |
| 400         | illegal_argument  | password or pin must provided    | 注册用户请求 body 中没有提供 `password` 参数。 | 注册用户请求 body 中提供 `password`。   |
| 400         | illegal_argument | NICKNAME_TOO_LONG    | 注册用户的推送昵称长度超过限制。   | 查看注册用户名[规范](#开放注册单个用户)。 |
| 400         | duplicate_unique_property_exists   | Application XXX Entity user requires that property named username be unique, value of XXX exists | 注册用户名已经存在。 | 更换用户名重新注册。  |
| 401         | unauthorized  | Unable to authenticate (OAuth)   | token 不合法，可能过期或 token 错误。   | 使用新的 token 访问。       |
| 404         | organization_application_not_found | Could not find application for XXX/XXX from URI: XXX/XXX/users | App key  不存在。 | 检查 `orgName` 和 `appName` 是否正确或[创建应用](https://doc.easemob.com/product/enable_and_configure_IM.html#创建应用)。 |
| 429         | resource_limited    | You have exceeded the limit of the community edition,Please upgrade to the enterprise edition | 注册用户的数量超过当前产品套餐包的限制。 | 联系商务开通付费版。   |

关于其他错误，你可以参考 [错误码](#错误码) 了解可能的原因。

### 授权注册单个用户

#### 功能说明

- 授权注册模式指注册环信即时通讯 IM 账号时携带管理员身份认证信息，即 App Token。
- 要使用该注册方式，你需要在环信控制台进行如下配置：
在控制台首页的 **应用列表** 下点击目标应用的 **操作** 一栏中的 **管理**，然后选择 **即时通讯** > **服务概览**，在页面的 **设置** 区域中将**用户注册模式**设置**授权注册**，然后单击**保存**。
- 推荐使用该模式，因为该模式较为安全，可防止已获取了注册 URL 和了解注册流程的某些人恶意向服务器大量注册垃圾用户。
- 注册用户时，需满足用户 ID 和密码的设置要求。

**调用频率上限**：该 API、用户账户管理的其他接口、以及离线推送的相关接口的总调用频率上限为 100 次/秒/App Key，详见 [接口频率限制文档](limitationapi.html#用户体系管理)。

#### HTTP 请求

```http
POST https://{host}/{org_name}/{app_name}/users
```

##### 路径参数

参数及说明详见 [公共参数](#公共参数)。

##### 请求 header

| 参数            | 类型   | 是否必需 | 描述                 |
| :-------------- | :----- | :------- | --------------------------------- |
| `Content-Type`  | String | 是       | 内容类型。请填 `application/json`。                         |
| `Accept`        | String | 是       | 内容类型。请填 `application/json`。                      |
| `Authorization` | String | 是       | App 管理员的鉴权 token，格式为 `Bearer YourAppToken`，其中 `Bearer` 为固定字符，后面为英文空格和获取到的 app token。 |

##### 请求 body

| 参数       | 类型   | 是否必需 | 描述         |
| :--------- | :----- | :------- | :------------------------ |
| `username` | String | 是       | 用户 ID，长度不可超过 64 字节。不可设置为空。支持以下字符集：<br/>- 26 个小写英文字母 a-z；<br/>- 10 个数字 0-9；<br/>- “\_”, “-”, “.”。 <br/><Container type="notice" title="注意"><br/>- 请勿使用大写英文字母 A-Z。若你同时使用了大写字母和小写字母，响应中返回的用户 ID 只包含小写字母。<br/>- 请确保同一个 app 下，用户 ID 唯一；<br/>- 用户 ID 为公开信息，请勿使用 UUID、邮箱地址、手机号等敏感信息。</Container> |
| `password` | String | 是       | 用户的登录密码，长度不可超过 64 个字符。 |

#### HTTP 响应

##### 响应 body

如果返回的 HTTP 状态码为 `200`，表示请求成功，响应包体中包含以下字段：

响应字段及描述详见 [公共参数](#公共参数)。

如果返回的 HTTP 状态码非 `200`，表示请求失败。你可以参考 [错误码](#错误码)了解可能的原因。

#### 示例

##### 请求示例

```shell
# 将 <YourAppToken> 替换为你在服务端生成的 App Token

curl -X POST -H 'Content-Type: application/json' -H 'Accept: application/json' -H 'Authorization: Bearer <YourAppToken>' -d '[
   {
     "username": "user1",
     "password": "123"
   }
 ]' 'https://XXXX/XXXX/XXXX/users'
```

##### 响应示例

```json
{
  "action": "post",
  "application": "8be024f0-XXXX-XXXX-b697-5d598d5f8402",
  "path": "/users",
  "uri": "https://XXXX/XXXX/XXXX/users",
  "entities": [
    {
      "uuid": "0ffe2d80-XXXX-XXXX-8d66-279e3e1c214b",
      "type": "user",
      "created": 1542795196504,
      "modified": 1542795196504,
      "username": "user1",
      "activated": true
    }
  ],
  "timestamp": 1542795196515,
  "duration": 0,
  "organization": "XXXX",
  "applicationName": "XXXX"
}
```

#### 错误码

如果返回的 HTTP 状态码非 `200`，表示请求失败，可能提示以下错误码：

| HTTP 状态码 | 错误类型      | 错误提示       | 可能原因       | 处理建议       |
| :---- | :-------- | :------------ | :----------------- | :----------------- |
| 400         | illegal_argument                   | username XXX is not legal  | 用户名不合法。   | 查看注册用户名[规范](#开放注册单个用户)。 |
| 400         | illegal_argument                   | USERNAME_TOO_LONG   | 用户长度超过限制。 | 查看注册用户名[规范](#开放注册单个用户)。 |
| 400         | illegal_argument                   | password or pin must provided  | 注册用户请求 body 中没有提供 `password` 参数。| 注册用户请求 body 中提供 `password`。 |
| 400         | illegal_argument                   | NICKNAME_TOO_LONG    | 注册用户的推送昵称长度超过限制。 | 查看注册用户名[规范](#开放注册单个用户)。 |
| 400         | duplicate_unique_property_exists   | Application XXX Entity user requires that property named username be unique, value of XXX exists | 注册用户名已经存在。 | 更换用户名重新注册。   |
| 400         | illegal_argument                   | username [XXX] is not legal  | 注册用户的 `username` 不合法。| 请按照用户名的规范进行注册用户。 |
| 400         | illegal_argument                   | USERNAME_TOO_LONG    | 注册用户的 `username` 长度超限。 | 请按照用户名的规范进行注册用户。  |
| 400         | illegal_argument                   | password or pin must provided    | 注册用户时没有提供密码。   | 请为用户提供密码在进行注册。 |
| 400         | illegal_argument                   | NICKNAME_TOO_LONG   | 注册用户的 `nickname` 长度超限。   | 请按照用户推送昵称的规范进行注册用户。  |
| 401         | unauthorized                       | token is illegal.    | token 不合法，生成 token 使用信息与请求携带的信息不匹配。 | 使用新的 token 访问。   |
| 401         | unauthorized                       | Unable to authenticate (OAuth) | token 不合法，可能过期或 token 错误。  | 使用新的 token 访问。    |
| 401         | unauthorized                       | Open registration doesn't allow, so register user need token| 授权注册模式，注册用户时需要 token。 | 请求时携带 token。 |
| 404         | organization_application_not_found | Could not find application for XXX/XXX from URI: XXX/XXX/users | App key  不存在。 | 检查 `orgName` 和 `appName` 是否正确或[创建应用](https://doc.easemob.com/product/enable_and_configure_IM.html#创建应用) |
| 429         | resource_limited                   | You have exceeded the limit of the community edition,Please upgrade to the enterprise edition | 注册用户的数量超过当前产品套餐版本的限制。 | 联系商务开通付费版。 |

关于其他错误，你可以参考 [响应状态码](error.html) 了解可能的原因。

### 批量授权注册用户

- 批量注册为授权注册方式，服务端需要校验有效的 App Token 权限才能进行操作。
- 单次请求最多可注册 60 个用户 ID。
- 注册用户时，需满足用户 ID 和密码的设置要求。

**调用频率上限**：该 API、用户账户管理的其他接口、以及离线推送的相关接口的总调用频率上限为 100 次/秒/App Key，详见 [接口频率限制文档](limitationapi.html#用户体系管理)。

#### HTTP 请求

```http
POST https://{host}/{org_name}/{app_name}/users
```

##### 路径参数

参数及说明详见 [公共参数](#公共参数)。

##### 请求 header

| 参数            | 类型   | 是否必需 | 描述                  |
| :-------------- | :----- | :------- | :------------------ |
| `Content-Type`  | String | 是       | 内容类型。请填 `application/json`。     |
| `Authorization` | String | 是       | App 管理员的鉴权 token，格式为 `Bearer YourAppToken`，其中 `Bearer` 为固定字符，后面为英文空格和获取到的 app token。 |

##### 请求 body

| 参数       | 类型   | 是否必需 | 描述        |
| :--------- | :----- | :------- | :----------------------------- |
| `username` | String | 是       | 用户 ID，长度不可超过 64 个字节。不可设置为空。支持以下字符集：<br/>- 26 个小写英文字母 a-z；<br/>- 10 个数字 0-9；<br/>- “\_”, “-”, “.”。 <br/><Container type="notice" title="注意"><br/>- 请勿使用大写英文字母 A-Z。若你同时使用了大写字母和小写字母，响应中返回的用户 ID 只包含小写字母。<br/>- 请确保同一个 app 下，用户 ID 唯一；<br/>- 用户 ID 为公开信息，请勿使用 UUID、邮箱地址、手机号等敏感信息。</Container> |
| `password` | String | 是       | 用户的登录密码，长度不可超过 64 个字符。      |

#### HTTP 响应

##### 响应 body

如果返回的 HTTP 状态码为 `200`，表示请求成功，响应包体中包含以下字段：

响应字段及描述详见 [公共参数](#公共参数)。

如果返回的 HTTP 状态码非 `200`，表示请求失败。你可以参考 [错误码](#错误码) 了解可能的原因。

#### 示例

##### 请求示例一

注册 2 个用户：

```shell
# 将 <YourAppToken> 替换为你在服务端生成的 App Token

curl -X POST -H "Authorization: Bearer <YourAppToken>" -i  "https://XXXX/XXXX/XXXX/users" -d '[{"username":"user1", "password":"123"}, {"username":"user2", "password":"456"}]'
```

##### 响应示例一

```json
{
  "action": "post",
  "application": "22bcffa0-XXXX-XXXX-9df8-516f6df68c6d",
  "path": "/users",
  "uri": "https://XXXX/XXXX/XXXX/users",
  "entities": [
    {
      "uuid": "278b5e60-XXXX-XXXX-8f9b-d5d83ebec806",
      "type": "user",
      "created": 1541587920710,
      "modified": 1541587920710,
      "username": "user1",
      "activated": true
    },
    {
      "uuid": "278bac80-XXXX-XXXX-b192-73e4cd5078a5",
      "type": "user",
      "created": 1541587920712,
      "modified": 1541587920712,
      "username": "user2",
      "activated": true
    }
  ],
  "timestamp": 1541587920714,
  "data": [],
  "duration": 0,
  "organization": "XXXX",
  "applicationName": "XXXX"
}
```

##### 请求示例二

当请求 body 中存在已经注册过的用户 user 3 时，user 3 注册失败并在响应 body 中的 `data` 数组内返回，用户 user 1、user 2 仍然注册成功。

```shell
# 将 <YourAppToken> 替换为你在服务端生成的 App Token

curl -X POST -H "Authorization: Bearer <YourAppToken>" -i  "https://XXXX/XXXX/XXXX/users" -d '[{"username":"user1", "password":"123"}, {"username":"user2", "password":"456"}, {"username":"user3", "password":"789"}]'
```

##### 响应示例二

```json
{
  "action": "post",
  "application": "22bcffa0-XXXX-XXXX-9df8-516f6df68c6d",
  "path": "/users",
  "uri": "https://XXXX/XXXX/XXXX/testapp/users",
  "entities": [
    {
      "uuid": "278b5e60-XXXX-XXXX-8f9b-d5d83ebec806",
      "type": "user",
      "created": 1541587920710,
      "modified": 1541587920710,
      "username": "user1",
      "activated": true
    },
    {
      "uuid": "278bac80-XXXX-XXXX-b192-73e4cd5078a5",
      "type": "user",
      "created": 1541587920712,
      "modified": 1541587920712,
      "username": "user2",
      "activated": true
    }
  ],
  "timestamp": 1541587920714,
  "data": [
    {
      "username": "user3",
      "registerUserFailReason": "the user3 already exists"
    }
  ],
  "duration": 0,
  "organization": "XXXX",
  "applicationName": "XXXX"
}
```

#### 错误码

如果返回的 HTTP 状态码非 `200`，表示请求失败，可能提示以下错误码：

| HTTP 状态码 | 错误类型   | 错误提示      | 可能原因   | 处理建议       |
| :----- | :----------- | :----| :-------| :---------------|
| 400         | illegal_argument                   | username XXX is not legal  | 用户名不合法。| 查看注册用户名[规范](#开放注册单个用户)。 |
| 400         | illegal_argument                   | USERNAME_TOO_LONG    | 用户长度超过限制。 | 查看注册用户名[规范](#开放注册单个用户)。 |
| 400         | illegal_argument                   | password or pin must provided  | 注册用户请求 body 中没有提供 `password` 参数。  | 注册用户请求 body 中提供 `password`。  |
| 400         | illegal_argument                   | NICKNAME_TOO_LONG    | 注册用户的推送昵称长度超过限制。  | 查看注册用户名[规范](#开放注册单个用户)。 |
| 400         | duplicate_unique_property_exists   | Application XXX Entity user requires that property named username be unique, value of XXX exists | 注册用户名已经存在。  | 更换用户名重新注册。  |
| 400         | duplicate_unique_property_exists   | the same user XXX has a different password, the passwords are XXX | 注册用户时，请求 body 中存在 `username` 相同但密码不同的情况。 | 对相同的 `username` 进行修改重新注册。    |
| 400         | illegal_argument                   | username [XXX] is not legal    | 注册用户的 `username` 不合法。 | 请按照用户名的规范进行注册用户。 |
| 400         | illegal_argument                   | USERNAME_TOO_LONG      | 注册用户的 `username` 长度超限。| 请按照用户名的规范进行注册用户。 |
| 400         | illegal_argument                   | password or pin must provided       | 注册用户时没有提供密码。 | 请为用户提供密码在进行注册。|
| 400         | illegal_argument                   | NICKNAME_TOO_LONG       | 注册用户的 `nickname` 长度超限。 | 请按照用户推送昵称的规范进行注册用户。 |
| 400         | illegal_argument                   | Request body array size[XXX] had almost reached or been greater than the upper range value[XXX] | 可注册的用户数量超过限制。  | 请更改注册用户的数量。  |
| 401         | unauthorized                       | token is illegal.     | token 不合法，生成 token 使用信息与请求携带的信息不匹配。  | 使用新的 token 访问。 |
| 401         | unauthorized                       | Unable to authenticate (OAuth)     | token 不合法，可能过期或 token 错误。  | 使用新的 token 访问。  |
| 401         | unauthorized                       | Open registration doesn't allow, so register user need token, | 授权注册模式，注册用户时需要 token。  | 请求时携带 token。 |
| 404         | organization_application_not_found | Could not find application for XXX/XXX from URI: XXX/XXX/users | App key  不存在。 | 检查 `orgName` 和 `appName` 是否正确或[创建应用](/product/enable_and_configure_IM.html#创建应用)。 |
| 429         | resource_limited                   | You have exceeded the limit of the community edition,Please upgrade to the enterprise edition | 注册用户的数量超过当前产品套餐版本的限制。 | 联系商务开通付费版。 |

关于其他错误，你可以参考 [响应状态码](error.html) 了解可能的原因。

## 获取用户详情

### 获取单个用户的详情

#### 功能说明

获取单个应用用户的详细信息，包括用户 ID、用户的 UUID、用户注册时间、用户信息最近一次修改时间、用户的推送设置（例如，消息推送方式、是否开启免打扰、免打扰开始和结束时间、推送证书、是否屏蔽了群组消息的离线推送设置、推送证书、推送 token）等。

**调用频率上限**：该 API、用户账户管理的其他接口、以及离线推送的相关接口的总调用频率上限为 100 次/秒/App Key，详见 [接口频率限制文档](limitationapi.html#用户体系管理)。

#### HTTP 请求

```http
GET https://{host}/{org_name}/{app_name}/users/{username}
```

##### 路径参数

| 参数            | 类型   | 是否必需 | 描述       |
| :-------------- | :----- | :------- | :-------------------------- |
| `username`  | String  | 是 | 要获取哪个用户的详情。          |     

其他参数及说明详见 [公共参数](#公共参数)。

##### 请求 header

| 参数            | 类型   | 是否必需 | 描述       |
| :-------------- | :----- | :------- | :-------------------------- |
| `Accept`        | String | 是       | 内容类型。请填 `application/json`。                                                                                  |
| `Authorization` | String | 是       | App 管理员的鉴权 token，格式为 `Bearer YourAppToken`，其中 `Bearer` 为固定字符，后面为英文空格和获取到的 app token。 |

#### HTTP 响应

##### 响应 body

如果返回的 HTTP 状态码为 `200`，表示请求成功，响应包体中包含以下字段：

| 字段       | 类型   | 描述        |
| :------------ | :----- | :------------ |
| `entities` | JSON Array | 响应实体。 |
|  - `notification_display_style`         | Int    | 消息推送方式：<br/> - `0`：仅通知。推送标题为“您有一条新消息”，推送内容为“请点击查看”；<br/> - `1`：通知以及消息详情。推送标题为“您有一条新消息”，推送内容为发送人昵称和离线消息的内容。<br/>若用户未设置该参数，则响应中不返回。 |
|  - `notification_no_disturbing`         | Boolean   | 是否开启免打扰。<br/> - `true`：免打扰开启。若用户未设置该参数，则响应中不返回。<br/> - `false`：免打扰关闭。 |
|  - `notification_no_disturbing_start`   | String | 免打扰的开始时间。例如，“8” 代表每日 8:00 开启免打扰。若用户未设该参数，则响应中不返回。 |
|  - `notification_no_disturbing_end`     | String | 免打扰的结束时间。例如，“18” 代表每日 18:00 关闭免打扰。若用户未设该参数，则响应中不返回。     |
|  - `notification_ignore_63112447328257` | Bool   | 是否屏蔽了群组消息的离线推送的设置。参数中的数字，例如 `63112447328257` 表示群组 ID。 <br/> -`true`：已屏蔽。<br/> - `false`：未屏蔽。若用户未设该参数，则响应中不返回。   |
|  - `notifier_name`                      | String | 客户端推送证书名称。若用户未设置推送证书名称，则响应中不返回。  |
|  - `device_token`                       | String | 推送 token。若用户没有推送 token，则响应中不返回。   |
| `count`   | Int    | 用户数量。      |

其他字段及说明详见 [公共参数](#公共参数)。

如果返回的 HTTP 状态码非 `200`，表示请求失败。你可以参考 [错误码](#错误码) 了解可能的原因。

#### 示例

##### 请求示例

```shell
# 将 <YourAppToken> 替换为你在服务端生成的 App Token

curl -X GET -H 'Accept: application/json' -H 'Authorization: Bearer <YourAppToken>' 'https://XXXX/XXXX/XXXX/users/XXXX'
```

##### 响应示例

```json
{
  "action": "get",
  "path": "/users",
  "uri": "https://XXXX/XXXX/XXXX/users/XXXX",
  "entities": [
    {
      "uuid": "0ffe2d80-XXXX-XXXX-8d66-279e3e1c214b",
      "type": "user",
      "created": 1542795196504,
      "modified": 1542795196504,
      "username": "XXXX",
      "activated": true,
      "nickname": "testuser"
    }
  ],
  "timestamp": 1542798985011,
  "duration": 6,
  "count": 1
}
```

#### 错误码

如果返回的 HTTP 状态码非 `200`，表示请求失败，可能提示以下错误码：

| HTTP 状态码 | 错误类型    | 错误提示      | 可能原因      | 处理建议    |
| :---------- | :---------- | :--------- | :----------- | :---------- |
| 401         | unauthorized                       | Unable to authenticate (OAuth)    | token 不合法，可能过期或 token 错误。 | 使用新的 token 访问。    |
| 404         | organization_application_not_found | Could not find application for XXX/XXX from URI: XXX/XXX/users | App key  不存在。   | 检查 `orgName` 和 `appName` 是否正确或[创建应用](https://doc.easemob.com/product/enable_and_configure_IM.html#创建应用)。 |
| 404         | service_resource_not_found         | Service resource not found  | 用户不存在。  | 先注册用户或者检查用户名是否正确。  |

关于其他错误，你可以参考 [响应状态码](error.html) 了解可能的原因。

### 批量获取用户详情

#### 功能说明

- 该接口查询多个用户的信息列表，按照用户创建时间顺序返回。
- 你可以指定要查询的用户数量。
- 若数据库中的用户数量大于你要查询的用户数量（`limit`），返回的信息中会携带游标 `cursor` 标示下次数据获取的开始位置。你可以分页获取多个用户的详情，直到返回的信息中不再包含 `cursor`，即已经达到最后一页。

**调用频率上限**：该 API、用户账户管理的其他接口、以及离线推送的相关接口的总调用频率上限为 100 次/秒/App Key，详见 [接口频率限制文档](limitationapi.html#用户体系管理)。

#### HTTP 请求

```http
GET https://{host}/{org_name}/{app_name}/users?limit={N}&cursor={cursor}
```

##### 路径参数

参数及说明详见 [公共参数](#公共参数)。

##### 查询参数

| 参数     | 类型   | 是否必需 | 描述  |
| :------- | :----- | :------- | :--------------- |
| `limit`  | Int    | 否       | 请求查询用户的数量。取值范围为 [1,100]，默认值为 10。若实际用户数量超过 100，返回 100 个用户。   |
| `cursor` | String | 否       | 开始获取数据的游标位置，用于分页显示用户列表。第一次发起批量查询用户请求时若不设置 `cursor`，请求成功后会获得最早创建的用户。从响应 body 中获取 `cursor`，并在下一次请求的 URL 中传入该 `cursor`，直到响应 body 中不再有 `cursor` 字段，则表示已查询到 app 中所有用户。 | 

##### 请求 header

| 参数            | 类型   | 是否必需 | 描述        |
| :-------------- | :----- | :------- | :---------------------------- |
| `Accept`        | String | 是       | 内容类型。请填 `application/json`。       |
| `Authorization` | String | 是       | App 管理员的鉴权 token，格式为 `Bearer YourAppToken`，其中 `Bearer` 为固定字符，后面为英文空格和获取到的 app token。 |

#### HTTP 响应

##### 响应 body

如果返回的 HTTP 状态码为 `200`，表示请求成功，响应包体中包含以下字段：

| 字段   | 类型   | 描述    |
| :-------------------------------------------- | :----- | :------------------------------- |
| `entities`| JSON Array | 响应实体。 |
|  - `notification_display_style`         | Int    | 消息推送方式：<br/> - `0`：仅通知。推送标题为“您有一条新消息”，推送内容为“请点击查看”；<br/> - `1`：通知以及消息详情。推送标题为“您有一条新消息”，推送内容为发送人昵称和离线消息的内容。<br/>若用户未设置该参数，则响应中不会返回。   |
|  - `notification_no_disturbing`         | Bool   | 是否开启免打扰模式。<br/> - `true`：免打扰开启。若用户未设置改参数，则响应中不返回。<br/> - `false`：代表免打扰关闭。     |
|  - `notification_no_disturbing_start`   | String | 免打扰的开始时间。例如，`8` 代表每日 8:00 开启免打扰。若用户未设该参数，则响应中不返回。     |
|  - `notification_no_disturbing_end`     | String | 免打扰的结束时间。例如，`18` 代表每日 18:00 关闭免打扰。若用户未设该参数，则响应中不返回。  |
|  - `notification_ignore_63112447328257` | Bool   | 是否屏蔽了群组消息的离线推送的设置。数字表示群组 ID。 <br/> -`true`：已屏蔽。 <br/> - `false`：未屏蔽，没有设置则不会返回。   |
|  - `notifier_name`                      | String | 客户端推送证书名称。若用户未设置推送证书名称，则响应中不返回。   |
|  - `device_token`                       | String | 推送 token。若用户没有推送 token，则响应中不返回。   |
| `cursor`                                      | String | 游标，用于分页显示用户列表。<br>第一次发起批量查询用户请求时无需设置 `cursor`，请求成功后，从响应 body 中获取 `cursor`，并在下一次请求的 URL 中传入该 `cursor`，直到响应 body 中不再有 `cursor` 字段，则表示已查询到 app 中所有用户。 |
| `count`                                       | Number | 返回用户数量。      |

其他字段及说明详见 [公共参数](#公共参数)。

如果返回的 HTTP 状态码非 `200`，表示请求失败。你可以参考 [错误码](#错误码) 了解可能的原因。

#### 示例

##### 请求示例一

按照注册时间的顺序查询 2 个用户的信息列表：

```shell
# 将 <YourAppToken> 替换为你在服务端生成的 App Token

curl -X GET -H 'Accept: application/json' -H 'Authorization: Bearer <YourAppToken>' 'https://XXXX/XXXX/XXXX/users?limit=2'
```

使用返回的 cursor 获取下一页：

```shell
将 <YourAppToken> 替换为你在服务端生成的 App Token

curl -X GET -H 'Accept: application/json' -H 'Authorization: Bearer <YourAppToken>' 'https://XXXX/XXXX/XXXX/users?limit=2&cursor=LTgzXXXX2tB'
```

##### 响应示例一

返回注册时间较早的 2 个用户的信息列表：

```json
{
  "action": "get",
  "path": "/users",
  "uri": "https://XXXX/XXXX/XXXX/users",
  "entities": [
    {
      "uuid": "ab90eff0-XXXX-XXXX-9174-8f161649a182",
      "type": "user",
      "created": 1542356511855,
      "modified": 1542356511855,
      "username": "XXXX",
      "activated": true,
      "nickname": "user1"
    },
    {
      "uuid": "b2aade90-XXXX-XXXX-a974-f3368f82e4f1",
      "type": "user",
      "created": 1542356523769,
      "modified": 1542356523769,
      "username": "user2",
      "activated": true,
      "nickname": "user2"
    }
  ],
  "timestamp": 1542558467056,
  "duration": 11,
  "cursor": "LTgzXXXX2tB",
  "count": 2
}
```

##### 请求示例二

使用响应示例一中的 `cursor`，继续按照注册时间的顺序查询下一页用户列表，该页面用户数量为 2：

```shell
# 将 <YourAppToken> 替换为你在服务端生成的 App Token

curl -X GET -H 'Accept: application/json' -H 'Authorization: Bearer <YourAppToken>' 'https://XXXX/XXXX/XXXX/users?limit=2&cursor=LTgzXXXX  2tB'
```

##### 响应示例二

继续返回 2 个 用户的信息列表：

```json
{
  "action": "get",
  "path": "/users",
  "uri": "https://XXXX/XXXX/XXXX/users",
  "entities": [
    {
      "uuid": "fef7f250-XXXX-XXXX-ba39-0fed7dcc3cdd",
      "type": "user",
      "created": 1542361376245,
      "modified": 1542361376245,
      "username": "XXXX",
      "activated": true,
      "nickname": "testuser"
    }
  ],
  "timestamp": 1542559337702,
  "cursor": "LTgzXXXX2tB",
  "duration": 2,
  "count": 1
}
```

#### 错误码

如果返回的 HTTP 状态码非 `200`，表示请求失败，可能提示以下错误码：

| HTTP 状态码 | 错误类型  | 错误提示     | 可能原因     | 处理建议   |
| :---------- | :---------- | :-------------- | :------------- | :--------------- |
| 401         | unauthorized       | Unable to authenticate (OAuth)     | token 不合法，可能过期或 token 错误。 | 使用新的 token 访问。|
| 404         | organization_application_not_found | Could not find application for XXX/XXX from URI: XXX/XXX/users | App key 不存在。 | 检查 `orgName` 和 `appName` 是否正确或[创建应用](/product/enable_and_configure_IM.html#创建应用)。|

关于其他错误，你可以参考 [响应状态码](error.html) 了解可能的原因。

## 删除用户账号

### 删除单个用户

#### 功能说明

- 删除单个用户。
- 账号删除时，该用户的好友关系、用户属性、消息、会话等数据在服务端也会被删除。
- 账号删除后，该用户的数据将无法恢复，**请谨慎使用该接口**。
- 如果该用户是群主或者聊天室所有者，系统会同时删除对应的群组和聊天室。**请在操作前进行确认**。

**调用频率上限**：该 API、用户账户管理的其他接口、以及离线推送的相关接口的总调用频率上限为 100 次/秒/App Key，详见 [接口频率限制文档](limitationapi.html#用户体系管理)。

#### HTTP 请求

```http
DELETE https://{host}/{org_name}/{app_name}/users/{username}
```

##### 路径参数

参数及说明详见 [公共参数](#公共参数)。

##### 请求 header

| 参数            | 类型   | 是否必需 | 描述        |
| :-------------- | :----- | :------- | :------------------------- |
| `Accept`        | String | 是       | 内容类型。请填 `application/json`。                                                                                  |
| `Authorization` | String | 是       | App 管理员的鉴权 token，格式为 `Bearer YourAppToken`，其中 `Bearer` 为固定字符，后面为英文空格和获取到的 app token。 |

#### HTTP 响应

##### 响应 body

如果返回的 HTTP 状态码为 `200`，表示请求成功，响应包体中包含以下字段：

响应字段及描述详见 [公共参数](#公共参数)。

如果返回的 HTTP 状态码非 `200`，表示请求失败。你可以参考 [错误码](#错误码) 了解可能的原因。

#### 示例

##### 请求示例

```shell
# 将 <YourAppToken> 替换为你在服务端生成的 App Token

curl -X DELETE -H 'Accept: application/json' -H 'Authorization: Bearer <YourAppToken>' 'https://XXXX/XXXX/XXXX/users/user1'
```

##### 响应示例

```json
{
  "action": "delete",
  "application": "8be024f0-XXXX-XXXX-b697-5d598d5f8402",
  "path": "/users",
  "uri": "https://XXXX/XXXX/XXXX/users",
  "entities": [
    {
      "uuid": "ab90eff0-XXXX-XXXX-9174-8f161649a182",
      "type": "user",
      "created": 1542356511855,
      "modified": 1542356511855,
      "username": "XXXX",
      "activated": true,
      "nickname": "user1"
    }
  ],
  "timestamp": 1542559539776,
  "duration": 39,
  "organization": "XXXX",
  "applicationName": "XXXX"
}
```

#### 错误码

如果返回的 HTTP 状态码非 `200`，表示请求失败，可能提示以下错误码：

| HTTP 状态码 | 错误类型       | 错误提示         | 可能原因       | 处理建议           |
| :---------- | :---------- | :-------------- | :------------- | :--------------- |
| 400         | management     | User with id null does not exist in app XXX      | 用户不存在。  | 先注册用户或者检查用户名是否正确。  |
| 401         | unauthorized   | Unable to authenticate (OAuth)    | token 不合法，可能过期或 token 错误。 | 使用新的 token 访问。  |
| 404         | organization_application_not_found | Could not find application for XXX/XXX from URI: XXX/XXX/users | App key 不存在。  | 检查 `orgName` 和 `appName` 是否正确或[创建应用](/product/enable_and_configure_IM.html#创建应用)。 |
| 404         | service_resource_not_found         | Service resource not found   | 用户不存在。    | 先注册用户或者检查用户名是否正确。  |

关于其他错误，你可以参考 [响应状态码](error.html) 了解可能的原因。

### 批量删除用户

#### 功能说明

- 该 API 用于**删除你在集成了即时通讯 IM 后上线前的测试阶段创建的用户**。
- 建议一次删除的用户数量不要超过 100。
- 该 API 只指定了要删除的用户数量，**并未指定要删除的具体用户**，你可以在响应中查看删除的用户。
- 如果删除的多个用户中包含群主或聊天室所有者，**对应的群组或聊天室会解散**。

**调用频率上限**：该 API、用户账户管理的其他接口、以及离线推送的相关接口的总调用频率上限为 100 次/秒/App Key，详见 [接口频率限制文档](limitationapi.html#用户体系管理)。

#### HTTP 请求

```http
DELETE https://{host}/{org_name}/{app_name}/users?limit={N}&cursor={cursor}
```

##### 路径参数

参数及说明详见 [公共参数](#公共参数)。

##### 查询参数

| 参数     | 类型   | 是否必需 | 描述        |
| :------- | :----- | :------- | :----------------- |
| `limit`  | Int    | 否       | 要删除的用户的数量。取值范围为 [1,100]，默认值为 `10`。 |
| `cursor` | String | 否       | 开始删除用户的游标位置。第一次批量删除时若不设置 `cursor`，请求成功后会从最先创建的用户开始删除 `limit` 指定的用户数量。从响应 body 中获取 `cursor`，并在下一次请求的 URL 中传入该 `cursor`，直到响应 body 中不再有 `cursor` 字段，则表示已完全删除 app 中的所有用户。 |

##### 请求 header

| 参数            | 类型   | 是否必需 | 描述      |
| :-------------- | :----- | :------- | :-------------------- |
| `Accept`        | String | 是       | 内容类型。请填 `application/json`。                                                                                  |
| `Authorization` | String | 是       | App 管理员的鉴权 token，格式为 `Bearer YourAppToken`，其中 `Bearer` 为固定字符，后面为英文空格和获取到的 app token。 |

#### HTTP 响应

##### 响应 body

如果返回的 HTTP 状态码为 `200`，表示请求成功，响应包体中包含以下字段：

响应字段及说明详见 [公共参数](#公共参数)。

如果返回的 HTTP 状态码非 `200`，表示请求失败。你可以参考 [错误码](#错误码) 了解可能的原因。

#### 示例

##### 请求示例

```shell
# 将 <YourAppToken> 替换为你在服务端生成的 App Token

curl -X DELETE -H 'Accept: application/json' -H 'Authorization: Bearer <YourAppToken>' 'https://XXXX/XXXX/XXXX/users?limit=2'
```

##### 响应示例

```json
{
  "action": "delete",
  "application": "8be024f0-XXXX-XXXX-b697-5d598d5f8402",
  "path": "/users",
  "uri": "https://XXXX/XXXX/testapp/users",
  "entities": [
    {
      "uuid": "b2aade90-XXXX-XXXX-a974-f3368f82e4f1",
      "type": "user",
      "created": 1542356523769,
      "modified": 1542597334500,
      "username": "user2",
      "activated": true,
      "nickname": "testuser"
    },
    {
      "uuid": "b98ad170-XXXX-XXXX-XXXX-7f76daa76557",
      "type": "user",
      "created": 1542356535303,
      "modified": 1542356535303,
      "username": "user3",
      "activated": true,
      "nickname": "user3"
    }
  ],
  "timestamp": 1542867197779,
  "duration": 504,
  "organization": "XXXX",
  "applicationName": "testapp",
  "cursor": "LTgXXXXDNR"
}
```

#### 错误码

如果返回的 HTTP 状态码非 `200`，表示请求失败，可能提示以下错误码：

| HTTP 状态码 | 错误类型 | 错误提示     | 可能原因         | 处理建议   |
| :---------- | :----------- | :------------ | :---------- | :---------------- |
| 401         | unauthorized   | Unable to authenticate (OAuth)  | token 不合法，可能过期或 token 错误。 | 使用新的 token 访问。  |
| 404         | organization_application_not_found | Could not find application for XXX/XXX from URI: XXX/XXX/users | App key  不存在。  | 检查 `orgName` 和 `appName` 是否正确或[创建应用](/product/enable_and_configure_IM.html#创建应用)。 |

关于其他错误，你可以参考 [响应状态码](error.html) 了解可能的原因。

## 修改用户密码

#### 功能说明

- 修改用户的登录密码，不需要提供原密码。
- 设置的新密码的长度不可超过 64 个字符。
- 若用户在线，修改密码后会导致用户被踢下线。
- 修改密码后，用户原来的密码和用户 Token 失效，对客户端设备影响如下：
  - 对于在线设备，修改密码会导致这些设备被踢下线。需要使用新密码或重新获取 Token 登录。
  - 对于离线设备，用户上线时会提示鉴权失败，需要使用新密码或重新获取 Token 登录。

**调用频率上限**：该 API、用户账户管理的其他接口、以及离线推送的相关接口的总调用频率上限为 100 次/秒/App Key，详见 [接口频率限制文档](limitationapi.html#用户体系管理)。

#### HTTP 请求

```http
PUT https://{host}/{org_name}/{app_name}/users/{username}/password
```

##### 路径参数

| 参数            | 类型   | 是否必需 | 描述              |
| :-------------- | :----- | :------- | :---------------------------------------------- |
| `username`  | String | 是       | 修改该用户 ID 的登录密码。      |

参数及说明详见 [公共参数](#公共参数)。

##### 请求 header

| 参数            | 类型   | 是否必需 | 描述              |
| :-------------- | :----- | :------- | :---------------------------------------------- |
| `Content-Type`  | String | 是       | 内容类型。请填 `application/json`。      |
| `Accept`        | String | 是       | 内容类型。请填 `application/json`。      |
| `Authorization` | String | 是       | App 管理员的鉴权 token，格式为 `Bearer YourAppToken`，其中 `Bearer` 为固定字符，后面为英文空格和获取到的 app token。 |

##### 请求 body

请求包体为 JSON Object 类型，包含以下字段：

| 参数          | 类型   | 是否必需 | 描述                                       |
| :------------ | :----- | :------- | :----------------------------------------- |
| `newpassword` | String | 是       | 用户的新登录密码，长度不可超过 64 个字符。 |

其他参数及说明详见 [公共参数](#公共参数)。

#### HTTP 响应

##### 响应 body

如果返回的 HTTP 状态码为 `200`，表示请求成功，响应包体中包含以下字段：

| 参数     | 类型   | 描述                                                                         |
| :------- | :----- | :--------------------------------------------------------------------------- |
| `action` | String | 执行的操作。在该响应中，该参数的值为 `set user password`，表示设置用户密码。 |

其他字段及描述详见 [公共参数](#公共参数)。

如果返回的 HTTP 状态码非 `200`，表示请求失败。你可以参考 [错误码](#错误码) 了解可能的原因。

#### 示例

##### 请求示例

```shell
# 将 <YourAppToken> 替换为你在服务端生成的 App Token，<YourPassword> 替换为你设置的新密码

curl -X PUT -H 'Content-Type: application/json' -H 'Accept: application/json' -H 'Authorization: Bearer <YourAppToken>' -d '{ "newpassword": "<YourPassword>" }' 'https://XXXX/XXXX/XXXX/users/user1/password'
```

##### 响应示例

```json
{
  "action": "set user password",
  "timestamp": 1542595598924,
  "duration": 8
}
```

#### 错误码

如果返回的 HTTP 状态码非 `200`，表示请求失败，可能提示以下错误码：

| HTTP 状态码 | 错误类型     | 错误提示   | 可能原因    | 处理建议     |
| :---------- | :--------------- | :------------- | :------------ | :-----|
| 401         | unauthorized    | Unable to authenticate (OAuth)    | token 不合法，可能过期或 token 错误。 | 使用新的 token 访问。  |
| 404         | organization_application_not_found | Could not find application for XXX/XXX from URI: XXX/XXX/users | App key  不存在。   | 检查 `orgName` 和 `appName` 是否正确或[创建应用](/product/enable_and_configure_IM.html#创建应用)。 |
| 404         | entity_not_found  | User null not found    | 用户不存在。  | 先注册用户或者检查用户名是否正确。    |
| 400              | illegal_argument                   | "newpassword is required"   | 修改用户密码的请求体未提供 `newpassword` 属性。|

关于其他错误，你可以参考 [响应状态码](error.html) 了解可能的原因。

## 用户账号封禁、解禁和强制下线

### 账号封禁

#### 功能说明

- 封禁单个用户。封禁操作即刻生效。
- 用户被封禁后，不会在一段时间后自动解禁，只能调用 [解禁账号 API](#账号解禁) 解禁。
- 用户被封禁后，会立即下线并无法登录进入环信即时通讯 IM，直到被解禁后才能恢复登录。
- 被封禁期间，其他用户可向被封禁用户发送消息，但被封禁用户无法接收消息，无法收到推送通知。解禁后，用户可正常连接并使用即时通讯服务，再次上线可以收到被封禁期间的离线消息。请注意，离线消息默认最长存储 7 天，如果 7 天内客户端都没有上线，服务端将丢弃过期的消息。
- 该功能常用于对异常用户的即时处理场景。
- 若用户在线，封禁后会导致用户被踢下线。

**调用频率上限**：该 API、用户账户管理的其他接口、以及离线推送的相关接口的总调用频率上限为 100 次/秒/App Key，详见 [接口频率限制文档](limitationapi.html#用户体系管理)。

#### HTTP 请求

```http
POST https://{host}/{org_name}/{app_name}/users/{username}/deactivate
```

##### 路径参数

| 参数            | 类型   | 是否必需 | 描述      |
| :-------------- | :----- | :------- | :------------- |
| username            | String   | 是 | 要封禁的用户 ID。      |

参数及说明详见 [公共参数](#公共参数)。

##### 请求 header

| 参数            | 类型   | 是否必需 | 描述      |
| :-------------- | :----- | :------- | :------------- |
| `Accept`        | String | 是       | 内容类型。请填 `application/json`。                                                                                  |
| `Authorization` | String | 是       | App 管理员的鉴权 token，格式为 `Bearer YourAppToken`，其中 `Bearer` 为固定字符，后面为英文空格和获取到的 app token。 |

#### HTTP 响应

##### 响应 body

如果返回的 HTTP 状态码为 `200`，表示请求成功，响应包体中包含以下字段：

| 参数                | 类型   | 描述                                                                         |
| :------------------ | :----- | :--------------------------------------------------------------------------- |
| `action`            | String | 执行的操作。在该响应中，该参数的值为 `Deactivate user`，表示对账号进行封禁。 |

其他字段及说明详见[公共参数](#公共参数)。

如果返回的 HTTP 状态码非 `200`，表示请求失败。你可以参考[错误码](#错误码)了解可能的原因。

#### 示例

##### 请求示例

```shell
# 将 <YourAppToken> 替换为你在服务端生成的 App Token

curl -X POST -H 'Accept: application/json' -H 'Authorization: Bearer <YourAppToken>' 'https://XXXX/XXXX/XXXX/users/user1/deactivate'
```

##### 响应示例

```json
{
  "action": "Deactivate user",
  "entities": [
    {
      "uuid": "4759aa70-XXXX-XXXX-925f-6fa0510823ba",
      "type": "user",
      "created": 1542595573399,
      "modified": 1542597578147,
      "username": "user1",
      "activated": false,
      "nickname": "user"
    }
  ],
  "timestamp": 1542602157258,
  "duration": 12
}
```

#### 错误码

如果返回的 HTTP 状态码非 `200`，表示请求失败，可能提示以下错误码：

| HTTP 状态码 | 错误类型      | 错误提示     | 可能原因       | 处理建议      |
| :---------- | :------------------| :-------------------| :------------------| :-------------|
| 401         | unauthorized     | Unable to authenticate (OAuth)   | token 不合法，可能过期或 token 错误。 | 使用新的 token 访问。 |
| 404         | organization_application_not_found | Could not find application for XXX/XXX from URI: XXX/XXX/users | App key  不存在。    | 检查 `orgName` 和 `appName` 是否正确或[创建应用](/product/enable_and_configure_IM.html#创建应用)。 |
| 404         | service_resource_not_found         | Service resource not found   | 用户不存在。  | 先[注册用户](account_system.html#开放注册单个用户)或者检查用户名是否正确。 |

关于其他错误，你可以参考 [响应状态码](error.html) 了解可能的原因。

### 账号解禁

#### 功能说明

- 解禁单个用户。
- 用户被封后，不会在一段时间后自动解禁，需调用该 API 解禁。
- 解禁后，用户可正常连接并使用即时通讯服务，再次上线可以收到被封禁期间的离线消息。请注意，离线消息默认最长存储 7 天，如果 7 天内客户端都没有上线，服务端将丢弃过期的消息。

**调用频率上限**：该 API、用户账户管理的其他接口、以及离线推送的相关接口的总调用频率上限为 100 次/秒/App Key，详见 [接口频率限制文档](limitationapi.html#用户体系管理)

#### HTTP 请求

```http
POST https://{host}/{org_name}/{app_name}/users/{username}/activate
```

##### 路径参数

参数及说明详见 [公共参数](#公共参数)。

##### 请求 header

| 参数            | 类型   | 是否必需 | 描述         |
| :-------------- | :----- | :------- | :--------------- |
| `Accept`        | String | 是       | 内容类型。请填 `application/json`。                                                                                  |
| `Authorization` | String | 是       | App 管理员的鉴权 token，格式为 `Bearer YourAppToken`，其中 `Bearer` 为固定字符，后面为英文空格和获取到的 app token。 |

#### HTTP 响应

##### 响应 body

如果返回的 HTTP 状态码为 `200`，表示请求成功，响应包体中包含以下字段：

| 字段     | 类型   | 描述                 |
| :------- | :----- | :----------------------------- |
| `action` | String | 执行的操作。在该响应中，该参数的值为 `activate user`，表示对账号进行解禁。 |

其他字段及说明详见 [公共参数](#公共参数)。

如果返回的 HTTP 状态码非 `200`，表示请求失败。你可以参考 [错误码](#错误码) 了解可能的原因。

#### 示例

##### 请求示例

```shell
# 将 <YourAppToken> 替换为你在服务端生成的 App Token

curl -X POST -H 'Accept: application/json' -H 'Authorization: Bearer <YourAppToken>' 'https://XXXX/XXXX/XXXX/users/user1/activate'
```

##### 响应示例

```json
{
  "action": "activate user",
  "timestamp": 1542602404132,
  "duration": 9
}
```

#### 错误码

如果返回的 HTTP 状态码非 `200`，表示请求失败，可能提示以下错误码：

| HTTP 状态码 | 错误类型     | 错误提示      | 可能原因       | 处理建议    |
| :---------- | :---------| :---------------------| :----------| :--------|
| 401         | unauthorized                       | Unable to authenticate (OAuth)   | token 不合法，可能过期或 token 错误。 | 使用新的 token 访问。    |
| 404         | organization_application_not_found | Could not find application for XXX/XXX from URI: XXX/XXX/users | App key 不存在。    | 检查 `orgName` 和 `appName` 是否正确或[创建应用](/product/enable_and_configure_IM.html#创建应用)。 |
| 404         | service_resource_not_found         | Service resource not found   | 用户不存在。  | 先[注册用户](account_system.html#开放注册单个用户)或者检查用户名是否正确。 |

关于其他错误，你可以参考 [响应状态码](error.html) 了解可能的原因。

### 强制用户下线

#### 功能说明

- 强制用户即将用户状态改为离线，用户需要重新登录才能正常使用。
- 用户再次上线可以收到被封禁期间的离线消息。请注意，离线消息默认最长存储 7 天，如果 7 天内客户端都没有上线，服务端将丢弃过期的消息。
- 多设备登录情况下，调用该接口会强制将指定用户从所有登录的设备下线；若将用户从指定设备下线，你可以调用[强制指定账号从单设备下线](#强制指定账号从单设备下线)接口。

**调用频率上限**：该 API、用户账户管理的其他接口、以及离线推送的相关接口的总调用频率上限为 100 次/秒/App Key，详见 [接口频率限制文档](limitationapi.html#用户体系管理)。

#### HTTP 请求

```http
GET https://{host}/{org_name}/{app_name}/users/{username}/disconnect
```

##### 路径参数

参数及说明详见 [公共参数](#公共参数)。

##### 请求 header

| 参数            | 类型   | 是否必需 | 描述     |
| :-------------- | :----- | :------- | :---------------- |
| `Accept`        | String | 是       | 内容类型。请填 `application/json`。                                                                                  |
| `Authorization` | String | 是       | App 管理员的鉴权 token，格式为 `Bearer YourAppToken`，其中 `Bearer` 为固定字符，后面为英文空格和获取到的 app token。 |

#### HTTP 响应

##### 响应 body

如果返回的 HTTP 状态码为 `200`，表示请求成功，响应包体中包含以下字段：

| 字段          | 类型 | 描述                                                            |
| :------------ | :--- | :----------------------------------- |
| `data.result` | Bool | 用户是否已被强制下线：<br/> - `true`：是；<br/> - `false`：否。 |

其他字段及说明详见 [公共参数](#公共参数)。

如果返回的 HTTP 状态码非 `200`，表示请求失败。你可以参考 [错误码](#错误码) 了解可能的原因。

#### 示例

##### 请求示例

```shell
# 将 <YourAppToken> 替换为你在服务端生成的 App Token

curl -X GET -H 'Accept: application/json' -H 'Authorization: Bearer <YourAppToken>' 'https://XXXX/XXXX/XXXX/users/user1/disconnect'
```

##### 响应示例

```json
{
  "action": "get",
  "uri": "https://XXXX/XXXX/XXXX/users/user1/disconnect",
  "entities": [],
  "data": {
    "result": true
  },
  "timestamp": 1542602601332,
  "duration": 6,
  "count": 0
}
```

#### 错误码

如果返回的 HTTP 状态码非 `200`，表示请求失败，可能提示以下错误码：

| HTTP 状态码 | 错误类型    | 错误提示    | 可能原因    | 处理建议     |
| :---------- | :-------| :------| :---------| :------------------|
| 401   | unauthorized     | Unable to authenticate (OAuth)   | token 不合法，可能过期或 token 错误。 | 使用新的 token 访问。  |
| 404   | organization_application_not_found | Could not find application for XXX/XXX from URI: XXX/XXX/users | App key 不存在。    | 检查 `orgName` 和 `appName` 是否正确或[创建应用](/product/enable_and_configure_IM.html#创建应用)。 |

关于其他错误，你可以参考 [响应状态码](error.html) 了解可能的原因。

### 强制用户从单设备下线

#### 功能说明

- 如果用户在多个设备上登录，你可以调用该接口强制其在某一台设备上下线。
- 若强制用户从所有设备下线，可以调用[强制用户下线](#强制用户下线)接口。

**调用频率上限**：该 API、用户账户管理的其他接口、以及离线推送的相关接口的总调用频率上限为 100 次/秒/App Key，详见 [接口频率限制文档](limitationapi.html#用户体系管理)。

#### HTTP 请求

```http
DELETE https://{host}/{org_name}/{app_name}/users/{username}/disconnect/{resourceId}
```

##### 路径参数

| 参数       | 类型     | 描述               |
|:---------|:-------|:-----------------|
| `username` | String | 要将哪个用户从指定设备下线。|
| `resourceId` | String | 要将用户从哪个设备下线，即用户已登录设备的资源 ID，即服务器分配给每个设备资源的唯一标识符。资源 ID 的格式为 `{device type}_{resource ID}`，其中设备类型 `device type` 可以是 `android`、`ios` 或 `web`，`resource ID` 由 SDK 分配。例如，`android_123423453246`。|

其他参数及描述详见[公共参数](#公共参数)。

##### 请求 header

| 参数            | 类型   | 是否必需 | 描述                                                         |
| :-------------- | :----- | :------- | :----------------------------------------------------------- |
| `Accept`        | String | 是       | 内容类型。请填 `application/json`。                          |
| `Authorization` | String | 是       | App 管理员的鉴权 token，格式为 `Bearer YourAppToken`，其中 `Bearer` 为固定字符，后面为英文空格和获取到的 app token。 |

#### HTTP 响应

##### 响应 body

如果返回的 HTTP 状态码为 `200`，表示请求成功，响应包体中包含以下字段：

| 字段     | 类型 | 描述               |
| :------- | :--- | :----------------- |
| `result` | Bool  | 用户是否已被强制从该设备下线：<br/> - `true`：是；<br/> - `false`：否。|

如果返回的 HTTP 状态码非 `200`，表示请求失败。常见的错误为 404 错误，即用户不存在，如下所示：

```
{
    "error": "service_resource_not_found",
    "exception": "UserNotFoundException",
    "timestamp": 1709867821788,
    "duration": 0,
    "error_description": "Service resource not found"
}
```

关于其他异常，你可以参考 [错误码](#错误码) 了解可能的原因。

#### 示例

##### 请求示例

```shell
将 <YourAppToken> 替换为你在服务端生成的 App Token 
curl -X DELETE -H 'Accept: application/json'   \
-H 'Authorization: Bearer <YourAppToken>' 'https://XXX/XXX/XXX/users/{userName}/disconnect/{resourceId}'
```

##### 响应示例

```json
{
    "uri": "https://XXX/XXX/XXX",
    "timestamp": 1709865422596,
    "organization": "XXX",
    "application": "6b58d05d-XXX-1ff3e95a3dc0",
    "entities": [],
    "action": "delete",
    "data": {
        "result": true
    },
    "duration": 0,
    "applicationName": "90"
}
```

#### 错误码

如果返回的 HTTP 状态码非 `200`，表示请求失败，可能提示以下错误码：

| HTTP 状态码 | 错误类型  | 错误提示    | 可能原因     | 处理建议   |
| :---------- | :-------| :------| :---------| :------------------|
| 401  | unauthorized    | Unable to authenticate (OAuth)   | token 不合法，可能过期或 token 错误。 | 使用新的 token 访问。    |
| 404  | organization_application_not_found | Could not find application for XXX/XXX from URI: XXX/XXX/users | App key 不存在。 | 检查 `orgName` 和 `appName` 是否正确或[创建应用](/product/enable_and_configure_IM.html#创建应用)。 |

关于其他错误，你可以参考 [错误码](#错误码) 了解可能的原因。

## 获取用户在线状态

### 获取单个用户在线状态

#### 功能说明

- 查看单个用户是在线还是离线状态。
- 如果用户是多终端登录，则只要有一个终端的状态是 online ，用户就是 online。

**调用频率上限**：该 API、用户账户管理的其他接口、以及离线推送的相关接口的总调用频率上限为 100 次/秒/App Key，详见 [接口频率限制文档](limitationapi.html#用户体系管理)。

#### HTTP 请求

```http
GET https://{host}/{org_name}/{app_name}/users/{username}/status
```

##### 路径参数

参数及说明详见 [公共参数](#公共参数)。

##### 请求 header

| 参数            | 类型   | 是否必需 | 描述       |
| :-------------- | :----- | :------- | :--------------------------- |
| `Accept`        | String | 是       | 内容类型。请填 `application/json`。   |
| `Authorization` | String | 是       | App 管理员的鉴权 token，格式为 `Bearer YourAppToken`，其中 `Bearer` 为固定字符，后面为英文空格和获取到的 app token。 |

#### HTTP 响应

##### 响应 body

如果返回的 HTTP 状态码为 `200`，表示请求成功，响应包体中包含以下字段：

| 字段   | 类型 | 描述         |
| :----- | :--- | :---------------------- |
| `data` | JSON | 用户的在线状态数据。<br/> 格式为："用户 ID": "当前在线状态"，例如，user1 的在线和离线状态分别为 "user1": "online" 和 "user1": "offline"。 <br/> - `online`：客户端登录后和即时通讯 IM 服务器成功建立了长连接。<br/> - `offline`：iOS 和 Android 进程被杀或因网络问题断开连接，进入 `offline` 状态，此时可以接收消息的离线推送通知（前提是在环信控制台上传了推送证书，集成了离线推送服务）。 |

其他字段及说明详见 [公共参数](#公共参数)。

如果返回的 HTTP 状态码非 `200`，表示请求失败。你可以参考 [错误码](#错误码) 了解可能的原因。

#### 示例

##### 请求示例

```shell
将 <YourAppToken> 替换为你在服务端生成的 App Token

curl -X GET -H 'Accept: application/json' -H 'Authorization: Bearer <YourAppToken>' 'https://XXXX/XXXX/XXXX/users/user1/status'
```

##### 响应示例

```json
{
  "action": "get",
  "uri": "https://XXXX/XXXX/XXXX/users/user1/status",
  "entities": [],
  "data": {
    "user1": "offline"
  },
  "timestamp": 1542601284531,
  "duration": 4,
  "count": 0
}
```

#### 错误码

如果返回的 HTTP 状态码非 `200`，表示请求失败，可能提示以下错误码：

| HTTP 状态码 | 错误类型   | 错误提示         | 可能原因      | 处理建议    |
| :----- | :----------- | :--| :-------------- | :---|
| 401         | unauthorized     | Unable to authenticate (OAuth)       | token 不合法，可能过期或 token 错误。 | 使用新的 token 访问。   |
| 404         | organization_application_not_found | Could not find application for XXX/XXX from URI: XXX/XXX/users | App key  不存在  | 检查 `orgName` 和 `appName` 是否正确或[创建应用](/product/enable_and_configure_IM.html#创建应用)。 |
| 404         | service_resource_not_found | Service resource not found | App 用户不存在  | 提供已经创建的用户 |

关于其他错误，你可以参考 [错误码](#错误码) 了解可能的原因。

### 批量获取用户在线状态

#### 功能说明

- 批量查看用户是在线还是离线状态。
- 单次请求最多可查看 100 个用户的在线状态。
- 该接口不对用户 ID 进行校验。若查询不存在的用户 ID 的状态，则返回的状态为 `offline`。

**调用频率上限**：该 API、用户账户管理的其他接口、以及离线推送的相关接口的总调用频率上限为 100 次/秒/App Key，详见 [接口频率限制文档](limitationapi.html#用户体系管理)。

#### HTTP 请求

```http
POST https://{host}/{org_name}/{app_name}/users/batch/status
```

##### 路径参数

参数及说明详见 [公共参数](#公共参数)。

##### 请求 header

| 参数            | 类型   | 是否必需 | 描述        |
| :-------------- | :----- | :------- | :------------------ |
| `Content-Type`  | String | 是       | 内容类型。请填 `application/json`。                                                                                  |
| `Authorization` | String | 是       | App 管理员的鉴权 token，格式为 `Bearer YourAppToken`，其中 `Bearer` 为固定字符，后面为英文空格和获取到的 app token。 |

##### 请求 body

| 参数        | 类型  | 是否必需 | 描述                                           |
| :---------- | :---- | :------- | :--------------------------------- |
| `usernames` | Array | 是       | 要查询状态的用户 ID，**每次最多能传 100 个**。 |

#### HTTP 响应

##### 响应 body

如果返回的 HTTP 状态码为 `200`，表示请求成功，响应包体中包含以下字段：

| 字段     | 类型      | 描述       |
| :------- | :-------- | :-------------------------------------------------------------- |
| `action` | String    | 执行的操作。在该响应中，该参数的值为 `get batch user status`，表示批量获取用户在线状态。                                                  |
| `data`   | JSON Array | 查询的用户的在线状态。<br/> 数据格式为："用户 ID": "当前在线状态"，例如，user1 的在线和离线状态分别为 "user1": "online" 和 "user1": "offline"。<br/> - `online`：客户端登录后和即时通讯 IM 服务器成功建立了长连接。<br/> - `offline`：iOS 和 Android 进程被杀或因网络问题断开连接，进入 `offline` 状态，此时可以接收消息的离线推送通知。 |

如果返回的 HTTP 状态码非 `200`，表示请求失败。你可以参考 [错误码](#错误码) 了解可能的原因。

#### 示例

##### 请求示例

```shell
# 将 <YourAppToken> 替换为你在服务端生成的 App Token

curl -X POST https://XXXX/XXXX/chatdemoui/users/batch/status \
-H 'Accept: application/json'  \
-H 'Authorization: Bearer <YourAppToken>'  \
-H 'Content-Type: application/json'  \
-d '{"usernames":["user1","user2"]}'
```

##### 响应示例

该接口不对用户 ID 进行校验。若查询的用户 ID 不存在，则返回的状态为 `offline`。

```json
{
  "action": "get batch user status",
  "data": [
    {
      "user1": "offline"
    },
    {
      "user2": "offline"
    }
  ],
  "timestamp": 1552280231926,
  "duration": 4
}
```

#### 错误码

如果返回的 HTTP 状态码非 `200`，表示请求失败，可能提示以下错误码：

| HTTP 状态码 | 错误类型    | 错误提示    | 可能原因      | 处理建议     |
| :-- | :------------ | :--------- | :--------- | :---------- |
| 400   | illegal_argument      | request body exceeds maximum limit, maximum limit is 100     | 请求 body 中 `usernames` 的用户数量超过 100 个。 | 请调整`usernames` 中传入的用户 ID 数量。 |
| 401 | unauthorized  | Unable to authenticate (OAuth)   | token 不合法，可能过期或 token 错误。 | 使用新的 token 访问。    |
| 404  | organization_application_not_found | Could not find application for XXX/XXX from URI: XXX/XXX/users | App key 不存在。 |  检查 `orgName` 和 `appName` 是否正确或[创建应用](/product/enable_and_configure_IM.html#创建应用)。 |

关于其他错误，你可以参考 [错误码](#错误码) 了解可能的原因。

## 获取指定账号的在线登录设备列表

### 功能描述

多设备登录情况下，你可以调用该接口获取指定账号的在线登录设备列表。

**调用频率上限**：该 API、用户账户管理的其他接口、以及离线推送的相关接口的总调用频率上限为 100 次/秒/App Key，详见 [接口频率限制文档](limitationapi.html#用户体系管理)。

#### HTTP 请求

```http
GET https://{host}/{org_name}/{app_name}/users/{username}/resources
```

##### 路径参数

| 参数   | 类型   | 是否必需 | 描述         |
| :----- | :----- | :-----| :------------- |
| `username` | String | 是    | 用户 ID。 |

其他参数及描述详见 [公共参数](#公共参数)。

##### 请求 header

| 参数            | 类型   | 是否必需 | 描述       |
| :-------------- | :----- | :------- | :------------------ |
| `Accept`        | String | 是       | 内容类型，请填 `application/json`。       |
| `Authorization` | String | 是       | App 管理员的鉴权 token，格式为 `Bearer YourAppToken`，其中 `Bearer` 为固定字符，后面为英文空格和获取到的 app token。 |

#### HTTP 响应

##### 响应 body

如果返回的 HTTP 状态码为 `200`，表示请求成功，响应包体中包含以下字段：

| 参数       | 类型     | 描述               |
|:---------|:-------|:-----------------|
| `data`  | JSON Array  | 已登录设备的列表。          |
|  - `res` | String | 已登录设备的资源 ID，即服务器分配给每个设备资源的唯一标识符。资源 ID 的格式为 `{device type}_{resource ID}`，其中设备类型 `device type` 可以是 `android`、`ios` 或 `web`，`resource ID` 由 SDK 分配。例如，`android_123423453246`。|
|  - `device_uuid` | String | 已登录设备的 UUID。       |
|  - `device_name` | String | 已登录设备的名称。        |

其他参数及说明详见 [公共参数](#公共参数)。

如果返回的 HTTP 状态码非 `200`，表示请求失败。你可以参考 [错误码](#错误码) 了解可能的原因。

#### 示例

##### 请求示例

```shell
# 将 <YourAppToken> 替换为你在服务端生成的 App Token
curl -X GET 'http://XXXX/XXXX/XXXX/users/XXXX/resources' \
-H 'Accept: application/json' \
-H 'Authorization: Bearer <YourAppToken>'
```

##### 响应示例

```json
{
    "path": "/users/XXXX/resources",
    "uri": "https://XXXX/XXXX/XXXX/users/XXXX/resources",
    "timestamp": 1692325141777,
    "organization": "XXXX",
    "application": "0XXXX4",
    "entities": [],
    "action": "get",
    "data": [
        {
            "res": "android_XXXX",
            "device_uuid": "2a54-XXXX",
            "device_name": "HUAWEI-XXXX"
        }
    ],
    "duration": 0,
    "applicationName": "chatdemoui"
}
```

#### 错误码

如果返回的 HTTP 状态码非 `200`，表示请求失败，可能提示以下错误码：

| HTTP 状态码 | 错误类型     | 错误提示          | 可能原因      | 处理建议        |
| :----- | :--------- | :--------------- | :---------- | :------------- |
| 401         | unauthorized    | Unable to authenticate (OAuth)     | token 不合法，可能过期或 token 错误。 | 使用新的 token 访问。 |
| 404         | organization_application_not_found | Could not find application for XXX/XXX from URI: XXX/XXX/users | App key 不存在。    | 检查 `orgName` 和 `appName` 是否正确或[创建应用](/product/enable_and_configure_IM.html#创建应用)。 |

关于其他错误，你可以参考 [错误码](#错误码) 了解可能的原因。