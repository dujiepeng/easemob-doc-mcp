# 常见错误码

<Toc />

本文主要介绍在调用环信即时通讯的接口过程中，SDK 返回的错误码和错误信息。

你可以根据如下错误码及错误信息了解出错的可能原因，并采取响应措施。

环信即时通讯 SDK 在运行过程中，可能通过如下方式返回错误码和错误信息：

- 调用方法失败时的返回值。
- 通过 `onError` 回调报告错误码。

例如，注册时用户返回已存在的错误可以这样检测：

```csharp
SDKClient.Instance.Login(username, passwd,
    callback: new CallBack(
        onSuccess: () =>
        {
        },
        onError: (code, desc) =>
        {
            //注册失败，回调函数会返回错误码和错误描述
            //如：code为：USER_ALREADY_EXIST(203)
            //desc : User already exist.
        }
    )
);
```

错误码定义如下：

| 错误码 | 错误信息        | 描述和可能原因       | 解决方法 |
| :----- | :------------------| :------------------ | :--------------------------- |
| 0      | EM_NO_ERROR                           | 操作成功。      |  |
| 1      | GENERAL_ERROR                         | SDK 或请求相关的默认错误，未区分具体错误类型：例如，SDK 内部未正确初始化，或者请求服务器时未识别出具体原因的错误。 | 需要结合日志和调用的 API 进行分析。 |
| 2      | NETWORK_ERROR                         | 网络错误：无网络服务时会回调此错误，表示 SDK 与服务器的连接已断开。 | 群组/聊天室操作时，如果无网络，可能返回该错误，可以在网络恢复后，重复操作。 |
| 3      | DATABASE_ERROR                        | 数据库操作失败：打开本地数据库失败。 | 需要根据调用的 API 结合日志分析，如果使用 `Conversation#UpdateMessage` 方法更新一条本地不存在的消息，可能返回该错误；在数据库未打开时，调用其他本地数据库操作，也可能返回该错误。 |
| 4      | EXCEED_SERVICE_LIMIT                  | 超过服务限制：超过当前服务版本的数量限制，例如，创建的用户 ID 数量超过购买服务的限制时提示该错误；设置和获取用户属性的接口，包括[设置当前用户的属性](userprofile.html#设置当前用户的属性)和[获取单个或多个用户的用户属性](userprofile.html#获取用户属性)，超过调用频率限制时，会上报该错误。 | 检查调用的 API，若传入 `limit` 参数，可将该参数控制在上限内，若是限流导致，可以在延后一段时间重新调用。 |
| 8      | APP_ACTIVE_NUMBER_REACH_LIMITATION    | 应用程序的日活跃用户数量（DAU）或月活跃用户数量（MAU）达到上限。 | 需在[环信控制台](https://console.easemob.com/user/login)对 IM 服务进行升级。 |
| 100    | INVALID_APP_KEY                       | App Key 不合法：用户的 App Key 格式不正确。可在[环信控制台](https://console.easemob.com/user/login)的 **应用详情** 页面查看 App Key。 | 使用正确的 App Key 进行初始化。 |
| 101    | INVALID_USER_NAME                     | 用户 ID 不正确：一般情况下，用户 ID 为空时提示该错误，例如，邀请好友时 username 参数为空字符。 | 检查报错API 中传入的用户 ID 参数是否为空。 |
| 102    | INVALID_PASSWORD                      | 用户密码不正确：登录时提供的密码为空或不正确。 | 检查调用的 API 中传的密码参数是否正确。 |
| 103    | INVALID_URL                           | URL 不正确。 | 检查调用 API 时传入的参数是否正确。 |
| 104    | INVALID_TOKEN                         | 用户 token 不正确：登录时提供的 token 为空或不正确。 | 检查调用的 API 中传入的 token 参数是否正确。 |
| 105    | USER_NAME_TOO_LONG                    | 用户 ID 过长：用户 ID 长度不能超过 64 字节。 | 检查 API 中传入的用户 ID 长度是否超过限制。 |
| 108    | TOKEN_EXPIRED                         | 用户 token 已过期：超出 token 有效期。 | 收到 token 已过期的回调后，需要开发者重新生成 token，并调用 `login` 方法重新登录。 |
| 109    | TOKEN_WILL_EXPIRE                     | 用户 token 即将过期：超出 token 的一半有效期时会开始回调此错误码。 | 收到 token 即将过期的回调后，需重新生成 token，并调用 `SDKClient#RenewToken` 方法更新 token。 |
| 110    | INVALID_PARAM                         | 参数无效。 | 检查调用的 API 中传入的参数是否有效。 |
| 200    | USER_ALREADY_LOGIN                    | 用户已登录：该用户 ID 已经登录。 | 检查 SDK 是否开启了自动登录或已调用了登录方法。如果已开启，在 IM 登录成功后，下次打开时，不需要再重新调用登录方法。 |
| 201    | USER_NOT_LOGIN                        | 用户未登录：例如，如果未登录成功时发送消息或者使用群组操作的 API，SDK 会提示该错误。 | 检查调用 API 时，是否已完成 IM 登录。 |
| 202    | USER_AUTHENTICATION_FAILED            | 用户鉴权失败：<br/> - 若使用用户 ID 和密码登录，用户 ID 或密码不正确时会上报改错误；<br/> - 若使用用户 ID 和用户 token 登录，一般为用户 token 无效或已过期。 | 如果用户已退出登录，需要重新登录，未退出登录，则重新生成 token，调用 `SDKClient#RenewToken`。 |
| 203    | USER_ALREADY_EXIST                    | 用户已经存在：注册用户时，传入的的用户 ID 已经存在会提示该错误。 | 需要使用其他的用户 ID 注册，或者可认为已成功注册。 |
| 204    | USER_NOT_FOUND                        | 用户不存在：例如，登录或获取用户会话列表时，用户 ID 不存在。 | 检查调用的 API，传入的用户 ID 参数是否正确。 |
| 205    | USER_ILLEGAL_ARGUMENT                 | 用户参数不正确：例如，创建用户或更新用户属性时，用户 ID 为空或无效。 | 检查调用的 API 传入的参数是否正确。 |
| 206    | USER_LOGIN_ANOTHER_DEVICE             | 用户在其他设备登录：如果未开启多设备登录，则在其他设备登录会将当前登录设备踢下线，用户会在当前设备收到该错误。 | 设备被踢时，会触发回调 `IConnectionDelegate#OnLoggedOtherDevice`。收到该回调时，需重新登录。 |
| 207    | USER_REMOVED                          | 用户已被注销：当前的登录用户 ID 从[环信控制台](https://console.easemob.com/user/login)删除会收到该错误。 | 账号被注销时，会触发 `IConnectionDelegate#OnRemovedFromServer` 事件。收到该事件时，该账号已不可用，需要回到登录页面。 |
| 208    | USER_REG_FAILED                       | 用户注册失败：例如，注册用户之前未开启[开放注册功能](/document/server-side/account_system.html#开放注册单个用户)等原因。 | 不推荐使用 SDK 注册账号，建议开发者在业务服务器注册账号。 |
| 210    | USER_PERMISSION_DENIED                | 用户无权限：例如，如果用户被添加到黑名单后，发送消息时会提示该错误。其他报错情况包括用户修改其他用户发出的消息、修改其他用户设置的群成员属性以及普通群成员试图解散子区（仅子区所在群组的群主和群管理员有权解散子区）。 | 检查用户是否有操作权限。 |
| 213    | USER_BIND_ANOTHER_DEVICE              | 用户已在其他设备登录：在单设备登录场景中，默认情况下，后登录的设备会踢掉当前设备的登录。若设置为先登录的设备优先，则后登录设备登录失败并提示该错误。 | 可修改为多设备登录，或先使用 `SDKClient#KickDevice` 踢掉其他设备再登录。 |
| 214    | USER_LOGIN_TOO_MANY_DEVICES           | 用户登录设备数超过限制：该错误在多设备自动登录场景中且打开不踢掉其他设备上的登录的开关时超过登录设备数量的限制才会出现。例如，用户最多可同时登录 4 台设备， A（开启了自动登录）、B、C 和 D。最初，用户在这四个设备上均为登录状态，但由于网络连接原因登出了设备 A，然后手动登录了设备 E。这种情况下，设备 A 的网络恢复正常时会自动登录，这时登录失败且提示该错误。 | 可增加同时在线的设备数量，或先使用 `SDKClient#KickDevice` 踢掉其他设备再登录。 |
| 215    | USER_MUTED                            | 用户在群组或聊天室中被禁言：用户被禁言后发送消息时提示该错误。 | 用户在群组/聊天室内被禁言情况下，不能发送消息，可在 UI 上限制。 |
| 216    | USER_KICKED_BY_CHANGE_PASSWORD        | 用户密码更新：当前登录的用户密码被修改后，当前登录会断开并提示该错误。 | 密码更新会收到回调`IConnectionDelegate#OnChangedIMPwd`，需要在收到该回调时，调用 `SDKClient#Logout` 方法，并回到登录页面。 |
| 217    | USER_KICKED_BY_OTHER_DEVICE           | 用户被踢下线：开启多设备服务后，如果用户在其他设备上通过调用 API 或者管理后台将当前设备登录的 ID 强制退出登录，SDK 会提示该错误。 | 被踢设备会收到回调`IConnectionDelegate#OnKickedByOtherDevice`。收到该回调时，需调用`SDKClient#Logout` 方法，并回到登录页面。 |
| 218    | USER_ALREADY_LOGIN_ANOTHER            | 其他用户已登录：用户在同一台设备上退出登录前又使用另一账户登录。 | 如果在已登录情况下，要登录另一个账号，需要先调用`SDKClient#Logout` 退出账号。 |
| 219    | USER_MUTED_BY_ADMIN                   | 用户被禁言：用户被全局禁言后发送消息时提示该错误。 | 在群组/聊天室开启全员禁言的情况下，不能发送消息，可在 UI 上限制。 |
| 220    | USER_DEVICE_CHANGED                   | 用户的登录设备与上次不一致。该错误在单设备自动登录场景中且打开不踢掉其他设备上的登录的开关时才会出现。例如，用户自动登录设备 A，之后手动登录设备 B。用户再次自动登录设备 A 时登录失败且提示该错误。 | 登录失败的设备会收到 `IConnectionDelegate#OnLoggedOtherDevice` 事件。收到该事件时，需调用 `Client#Logout` 方法，并回到登录页面。 |
| 221    | USER_NOT_FRIEND                       | 非好友禁止发消息：开通非好友禁止发消息后，非好友间发消息提示此错误。你可以在[环信控制台](https://console.easemob.com/user/login)的**即时通讯 > 服务概览**页面的**设置**区域开启好友关系检查功能。 | 需要先调用 `ContactManager#AddContact` 方法添加好友。对方同意好友请求后，才能发送消息。 |
| 300    | SERVER_NOT_REACHABLE                  | 服务器不可达：例如，发送或撤回消息时，如果 SDK 与消息服务器未保持连接，会返回该错误；操作群组、好友等请求时因网络不稳定导致失败，也会返回该错误。 | 调用登录 API 返回该错误码，可能是由于网络受限，或域名被封禁，可尝试切换设备网络。如果用户在沙特/菲律宾等地区，需要联系商务，开启 dnsconfig中 TLS 加密。其他操作返回该错误码，一般是网络问题，可在切换网络或延迟一段时间后重新调用。 |
| 301    | SERVER_TIMEOUT                        | 请求服务超时：如果调用 API 在特定时间内服务器未响应则返回该错误，一般为 30 秒或 60 秒。 | 一般是网络问题，可在切换网络或延迟一段时间后重新调用 API。 |
| 302    | SERVER_BUSY                           | 服务器忙碌：服务器当前忙碌会返回该错误，建议稍后再尝试请求。 | 检查调用的 API 是否重复调用。如果在上次调用后，结果未返回时重复调用 API，可能返回该错误码。 |
| 303    | SERVER_UNKNOWN_ERROR                  | 服务请求的通用错误：请求服务器未成功时的默认错误。 | 提供日志以及调用的 API，进一步排查。 |
| 304    | SERVER_GET_DNSLIST_FAILED             | 获取服务器配置信息失败：SDK 获取当前应用的服务器配置时失败。 | 如果设置了 `Options#EnableDNSConfig` 为`No`，可能是没设置访问的 IM/REST 服务器导致，否则一般为登录时的网络问题，导致请求 dnsConfig 失败。 |
| 305    | SERVER_SERVICE_RESTRICTED             | 当前 app 被禁用：若在 app 被禁用时调用 API 会返回该错误。 | app 或账号的 IM 功能被禁用，需要到环信控制台开启或联系商务。 |
| 400    | FILE_NOT_FOUND                        | 文件未找到：例如，用户获取不到日志文件，或者下载附件失败时提示该错误。 | 如果是获取日志文件的接口，可尝试重新获取；如果是下载附件接口，表示消息的附件已不存在，不能再下载。 |
| 401    | FILE_INVALID                          | 文件异常：例如，当上传消息附件或者群组共享文件时可能会提示该错误。 | 需要用户重新选择附件文件，并调用相关 API 上传文件。 |
| 402    | FILE_UPLOAD_FAILED                    | 上传文件错误：例如，上传消息附件失败时提示该错误。 | 需要结合调用的 API 和日志进一步分析。 |
| 403    | FILE_DOWNLOAD_FAILED                  | 下载文件错误：例如，下载消息附件失败时提示该错误。 | 可能是网络原因，或消息已过期，需要结合日志进一步查看。 |
| 404    | FILE_DELETE_FAILED                    | 删除日志文件错误：通过 API 获取日志文件时会将旧的日志文件删除，然后生成新的日志文件。如果删除旧日志文件失败会提示该错误。 | 检查是否有权限删除 app 的日志文件。 |
| 405    | FILE_TOO_LARGE                        | 文件太大：例如，消息附件或群共享文件超过文件大小限制时提示该错误。 | 消息附件或群组共享文件等默认不能超过 10 MB。重新选择符合要求的文件，或者联系商务提升支持的文件大小。 |
| 406    | FILE_CONTENT_IMPROPER                 | 文件内容不合规：例如，消息附件或群共享文件内容不合规时提示该错误。 | 重新选择符合要求的文件，发送或上传。 |
| 407    | FILE_IS_EXPIRED                       | 文件已过期：例如，用户下载过期的消息附件或群共享文件时提示该错误。消息附件和群共享文件默认可存储 7 天。 | 要提升文件存储时间上限，请联系商务。 |
| 500    | MESSAGE_INVALID                       | 消息异常：例如，发送消息时，若消息对象或消息 ID 为空或者消息的发送方 ID 与当前登录 ID 不同则会提示该错误。 | 需要开发者检查消息的构造过程，消息 ID、发送方和消息 body 的设置是否符合要求。 |
| 501    | MESSAGE_INCLUDE_ILLEGAL_CONTENT       | 消息含有非法内容：如果消息被过滤系统识别为非法消息时返回该错误。| 发送消息被敏感词拦截系统或反垃圾系统拦截，可在环信控制台上查看拦截记录。 |
| 504    | MESSAGE_RECALL_TIME_LIMIT             | 消息撤回超时错误：消息撤回超过时间限制时会提示该错误。   | 可在 UI 上进行错误提示，或者联系商务延长消息可撤回时间。 |
| 505    | SERVICE_NOT_ENABLED                   | 服务未开启：尝试使用某些未开通的功能时提示该错误。  | 需要结合使用的 API 和日志分析，在环信控制台开通相应功能。|
| 506    | MESSAGE_EXPIRED                       | 消息已过期：发送群组消息的已读回执时若超过时间限制 (默认 3 天) 会提示该错误。  | 可在 UI 上进行错误提示，或者联系商务延长发送群组回执的有效时间。 |
| 507    | MESSAGE_ILLEGAL_WHITELIST             | 用户未在白名单中：如果群组聊天室开启全员禁言，且用户未在白名单中发送消息时提示该错误。 | 可在 UI 上进行错误提示，或者检查是否已开启群组全员禁言。 |
| 508    | MESSAGE_EXTERNAL_LOGIC_BLOCKED        | 发送前回调拦截：发送的消息被用户自己的服务器定义的规则拦截掉时提示该错误。 | 可在 UI 上做提示，或检查发送前回调记录。 |
| 509    | MESSAGE_CURRENT_LIMITING              | 单个用户 ID 发送消息超出频率限制。默认情况下，SDK 对单个用户 ID 发送群消息未做频率限制。如果你联系了环信商务设置了该限制，一旦在在单聊、群聊或聊天室中单个用户的消息发送频率超过设定的上限，则会提示该错误。 | 可在 UI 上进行提示，或检查消息发送频率设置。 |
| 510    | MESSAGE_SIZE_LIMIT                    | 发送消息时消息体大小超过上限。      | 可在 UI 上进行提示，或减小消息体长度（默认不超过 5 KB）。|
| 511    | MESSAGE_EDIT_FAILED                   | 消息修改失败。 | 需结合日志进一步分析。 |
| 600    | GROUP_INVALID_ID                      | 群组 ID 异常：使用群组相关 API，提供的群组 ID 为空或无效。| 检查调用的 API，传入的群组 ID 参数是否为空或传入了不存在（已解散）的群组 ID。 |
| 601    | GROUP_ALREADY_JOINED                  | 已在该群组中：例如，调用加入群组的 API 时如果已经在该群组中则提示该错误。   | 可以将该错误按照加入群组成功处理。 |
| 602    | GROUP_NOT_JOINED                      | 未加入该群组：尝试在未加入的群组中发送消息或进行群组操作时提示该错误。     | 结合日志，检查调用 API 中传入的群组 ID 是否是已加入的群组的 ID，或者该群组是否已解散或之前加入。 |
| 603    | GROUP_PERMISSION_DENIED               | 无权限的群组操作：例如，群组普通成员没有权限设置群组管理员。  | 检查是否有权限调用该 API。 |
| 604    | GROUP_MEMBERS_FULL                    | 群组已满：群组成员数量已达到创建群组时设置的最大人数。  | 可在 UI 上进行提示，或者检查创建群组时指定的最大人数是否超过了上限（默认为 200）。 |
| 605    | GROUP_SHARED_FILE_INVALIDID           | 群组共享文件 ID 不合法。 | 检查调用的下载和删除共享文件 API，确认传入的共享文件 ID 参数 `sharedFileId` 是否为空。|
| 606    | GROUP_NOT_EXIST                       | 群组不存在：尝试对不存在的群组进行操作时提示该错误。  | 结合日志，检查调用的 API 中传入的群组 ID 是否正确，或为已解散的群组的 ID。 |
| 607    | GROUP_DISABLED                        | 群组被禁用。 | 可在 UI 上进行提示，向管理员申请解禁群组。 |
| 608    | GROUP_NAME_VIOLATION                  | 群组名称无效。| 检查调用的 API 中传入的群组名称参数是否包含敏感信息。 |
| 609    | GROUP_MEMBER_ATTRIBUTES_REACH_LIMIT   | 群组成员自定义属性个数达到上限。| 单个群组成员的自定义属性总长度不能超过 4 KB。 |
| 610    | GROUP_MEMBER_ATTRIBUTES_UPDATE_FAILED | 设置群成员自定义属性失败。  | 需要结合调用的 API 以及日志进一步分析。 |
| 611    | GROUP_MEMBER_ATTRIBUTES_KEY_REACH_LIMIT   | 设置的群成员自定义属性 key 长度（不能超过 16 字节）超限。                        | 检查调用的 API 查看设置的群成员属性的 key 是否超过限制。 |
| 612    | GROUP_MEMBER_ATTRIBUTES_VALUE_REACH_LIMIT   | 设置的群成员自定义属性 value 长度（不能超过 512 字节）超限。  | 检查调用的 API 查看设置的群成员属性的 value 是否超过限制。 |
| 613    | GROUP_USER_IN_BLOCKLIST   | 该用户在群组黑名单中。例如，群组黑名单中的用户进行某些操作时，例如，加入群组，会提示该错误。  | 可在 UI 上进行提示，或检查用户是否在群组黑名单中。 |
| 700    | CHATROOM_INVALID_ID                   | 聊天室 ID 无效：调用聊天室相关 API，传入的聊天室 ID 为空时提示该错误。 | 检查调用的 API 中传入的聊天室 ID 是否为空。 |
| 701    | CHATROOM_ALREADY_JOINED               | 已在该聊天室中：调用加入聊天室的 API 时如果已经在该聊天室中则提示该错误。   | 可以按照加入聊天室成功的情况处理。 |
| 702    | CHATROOM_NOT_JOINED                   | 未加入该聊天室：用户在未加入的聊天室中发送消息或进行聊天室操作时提示该错误。 | 结合日志，检查调用 API 时传入的聊天室 ID 是否正确，或传入了已解散或之前加入失败的聊天室 ID。 |
| 703    | CHATROOM_PERMISSION_DENIED            | 无权限的聊天室操作：例如，聊天室普通成员没有权限设置聊天室管理员。  | 检查是否有权限调用该 API。 |
| 704    | CHATROOM_MEMBERS_FULL                 | 聊天室已满：聊天室成员数量已达到创建聊天室时设置的最大人数。   | 检查创建聊天室时指定的最大人数。 |
| 705    | CHATROOM_NOT_EXIST                    | 聊天室不存在：尝试对不存在的聊天室进行操作时提示该错误。  | 检查调用的 API 中传入的聊天室 ID 是否正确，或传入了已解散或之前加入失败的聊天室 ID。 |
| 706    | CHATROOM_OWNER_NOT_ALLOW_LEAVE        | 聊天室所有者不允许离开聊天室。若初始化时，`Options#IsRoomOwnerLeaveAllowed` 参数设置为 `false`，聊天室所有者调用 `LeaveRoom` 方法离开聊天室时会提示该错误。| 检查 SDK 初始化时 `Options#IsRoomOwnerLeaveAllowed` 设置的值。 |
| 707    | CHATROOM_USER_IN_BLOCKLIST            | 该用户在聊天室黑名单中。聊天室黑名单中的用户进行某些操作时，例如，加入聊天室，会提示该错误。| 在环信控制台上检查用户是否在聊天室的黑名单中。|
| 900    | USERINFO_USERCOUNT_EXCEED             | 获取用户属性的用户个数超过 100。 | 调用 API 获取用户属性时一次最多可获取 100个用户的属性，可分批获取。 |
| 901    | USERINFO_DATALENGTH_EXCEED            | 设置的用户属性太长。单个用户的所有属性数据不能超过 2 KB，单个 app 所有用户属性数据不能超过 10 GB。  | 检查调用 API 设置的用户属性是否超过限制。 |
| 1000   | CONTACT_ADD_FAILED                    | 添加联系人失败。   | 结合调用的 API 和 `Error#Desc` 分析联系人添加失败的原因。 |
| 1001   | CONTACT_REACH_LIMIT                   | 邀请者的联系人数量已达到上限。 | 可以在 UI 上提示该错误，或联系商务提升最大联系人数量。 |
| 1002   | CONTACT_REACH_LIMIT_PEER              | 受邀者的联系人数量已达到上限。   | 可以在 UI 上提示该错误，或联系商提升最大联系人数量。 |
| 1100   | PRESENCE_PARAM_LENGTH_EXCEED          | 调用 Presence 相关方法时参数长度超出限制。  | 调用[发布自定义在线状态 API](presence.html#发布自定义在线状态) 时设置的在线状态详细信息的长度不能超过 64 字节。 |
| 1101   | PRESENCE_CANNOT_SUBSCRIBE_YOURSELF    | 不能订阅你自己的状态。 | 检查调用 API 时传入的订阅用户 ID 是否是自己的用户 ID。 |
| 1110   | TRANSLATE_PARAM_INVALID               | 翻译参数错误。 | 需结合 Debug 日志，分析翻译方法传入的参数错误原因。 |
| 1111   | TRANSLATE_SERVICE_NOT_ENABLE          | 翻译服务未启用。使用翻译服务前，应在[环信控制台](https://console.easemob.com/user/login)开启该服务。 | 在[环信控制台](https://console.easemob.com/user/login)开启翻译服务。 |
| 1112   | TRANSLATE_USAGE_LIMIT                 | 翻译用量达到上限。 | 联系商务，进行翻译用量续费。 |
| 1113   | TRANSLATE_MESSAGE_FAIL                | 消息翻译失败。  | 需结合 Debug 日志分析翻译失败的原因。 |
| 1200   | THIRD_MODERATION_FAILED               | 第三方内容审核服务的消息审核结果为“拒绝”。  | 可以从[环信控制台](https://console.easemob.com/user/login)上查看内容审核配置及记录，进行分析。 |
| 1299   | THIRD_DEFAULT_FAILED                  | 除第三方内容审核服务的其他服务的消息审核结果为“拒绝”。  | 可以从[环信控制台](https://console.easemob.com/user/login)上查看内容审核配置及记录，进行分析。 |
| 1300   | REACTION_REACH_LIMIT                  | 该消息的 Reaction 数量已达到限制。 | 可以在 UI 上进行提示，或联系商务增加消息支持的 Reaction 数量上线。 |
| 1301   | REACTION_HAS_BEEN_OPERATED            | 用户已添加该 Reaction，不能重复添加。   | 可以按照添加 Reaction 成功的情况处理。 |
| 1302   | REACTION_OPERATION_IS_ILLEGAL         | 用户对该 Reaction 没有操作权限。例如，未添加过该 Reaction 的用户进行删除操作，或者既非单聊消息的发送方也不是非接收方的用户对消息添加 Reaction。 | 结合日志分析，检查调用的 API 中传入的参数是否正确。 |
| 1400   | THREAD_NOT_EXIST                      | 该子区不存在。   | 结合日志，检查调用的 API 中传入的子区 ID 是否正确。 |
| 1401   | THREAD_ALREADY_EXIST                  | 该消息 ID 下子区已存在，不能重复添加。| 检查调用 API 传入的消息下是否已经创建了子区。 |