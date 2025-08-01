# 常见错误码

<Toc />

本文介绍环信即时通讯 IM SDK 中接口调用或者回调中的错误码。可以根据具体错误码判断具体错误原因。

你可以在 `addEventHandler` 方法中通过 `options` 参数注册 `onError` 回调，然后通过该回调返回的参数，或其他 API 调用失败回调中返回的参数判断出错的原因。示例代码如下：

error.type === statusCode.WEBIM_CONNCTION_USER_NOT_ASSIGN_ERROR 其中 `error` 为回调返回的参数，`statusCode` 为 SDK 定义的错误信息。

| 错误码<div style="width: 80px;"></div> | 错误信息         | 描述和可能原因      | 解决办法 |
| :----- | :------------- | :--------------- | :--------------- |
| 0      | REQUEST_SUCCESS                                | 提示操作成功，没有错误。   | 操作成功。|
| -1     | REQUEST_TIMEOUT                             | 请求服务超时。 | 尝试重试，或者提示请求超时。 |
| -2     | REQUEST_UNKNOWN                                | 默认未区分类型的错误。| 提示请求失败。 |
| -3     | REQUEST_PARAMETER_ERROR               | 参数错误。     | 检查参数是否正确。 |
| -4     | REQUEST_ABORT               | 取消请求。|
| 1      | WEBIM_CONNCTION_OPEN_ERROR                    | 登录失败：获取 token 接口请求失败或 Token 无效。 | 根据 error message 判断是参数错误、已经登录、还是接⼝请求失败导致的登录失败，提示原因。 |
| 2      | WEBIM_CONNCTION_AUTH_ERROR                     | 登录鉴权失败。     | 检查是否没有使⽤正确 App Key 初始化，或者没有登录，或者登录的 Token ⽆效。|
| 16     | WEBIM_CONNCTION_DISCONNECTED                   | WebSocket 断开连接：由于断网等原因 WebSocket 已经断开。      | 提示连接已断开。 |
| 17     | WEBIM_CONNCTION_AJAX_ERROR                     | 服务请求的通用错误：请求服务器未成功时的默认错误。 | 根据 error message 判断当前操作的错误原因提示失败原因。|
| 27     | WEBIM_CONNCTION_APPKEY_NOT_ASSIGN_ERROR        | 未设置 App Key：设置的 App Key 错误，登录时会报此错误。 | 设置正确的 App Key。|
| 28     | WEBIM_CONNCTION_TOKEN_NOT_ASSIGN_ERROR         | 未传 token：调用 API 时没有携带 token，一般没登录时调用 API 会提示这个错误。 | 确保成功登录。 |
| 31     | WEBIM_CONNCTION_CALLBACK_INNER_ERROR           | 消息发送回调函数内部错误：在接收消息的回调及后续处理的函数中有错误。 | 检查回调函数⾥是否有报错，如 `onTextMessage` 的回调⾥处理消息时有报错。 |
| 39     | WEBIM_CONNECTION_CLOSED                        | 退出或未登录：未登录或掉线后发送消息。  | 重新登录。|
| 40     | WEBIM_CONNECTION_ERROR                         | 用户鉴权失败。  | 提示连接已断开。 |
| 50     | MAX_LIMIT                         | 达到上限，例如 Reaction 数量已达到限制、翻译用量达到上限、应用的日活跃用户数（DAU）超限、在线用户数量超限和月活跃用户数（MAU）。 | 根据 error message 确认哪项服务达到上限，限制相应数量。  |
| 51     | MESSAGE_NOT_FOUND                         | 没查到消息，如：没有查询到要举报的消息。   | 提示未找到原消息。 |
| 52     | NO_PERMISSION                          | 用户对当前操作没有权限。  | 提示没有权限进⾏相应的操作。 |
| 53     | OPERATION_UNSUPPORTED                         | 不支持的操作。    | 提示不⽀持这个操作。|
| 101    | WEBIM_UPLOADFILE_ERROR                         | 上传文件失败：如文件过大等。 | 发送附件消息上传时失败，显示发送失败。|
| 102    | WEBIM_UPLOADFILE_NO_LOGIN                      | 上传文件的请求中未携带用户 token：如未登录就上传文件。| 确保已经登录。 |
| 200    | WEBIM_DOWNLOADFILE_ERROR                       | 下载文件失败：如超时、网络错误。 | 提示重试。 |
| 204    | USER_NOT_FOUND                     | 用户不存在，如创建群拉人时不存在的用户报错。  | 检查 userId 是否正确。|
| 205    | MESSAGE_PARAMETER_ERROR                     | 消息参数错误。如撤回消息时未传消息 ID 或者发送消息时未传消息接收方的用户 ID。|确保消息⾥包含消息 ID 和接收方用户 ID，即 `id` 和 `to`。 |
| 206    | WEBIM_CONNCTION_USER_LOGIN_ANOTHER_DEVICE      | 用户在其他设备登录：如果没有开启多设备登录，则在其他设备登录会将当前登录的设备踢下线，用户会收到此错误。若开启了多设备登录并配置了支持的设备数量，设备间的互踢策略与 `ConnectionParameters#isFixedDeviceId` 参数有关，详见[多设备文档](multi_device.html)。  | 开启多设备功能，详见 [多设备⽂档](https://doc.easemob.com/document/web/multi_device.html)。 |
| 207    | WEBIM_CONNCTION_USER_REMOVED                   | 用户已经被注销：如果登录用户的 ID 被管理员从管理后台删除则会收到此错误。 | 提示⽤户被注销。|
| 208    | WEBIM_USER_ALREADY_LOGIN | 已经登录，又重复登录。 | 不能重复登录。 |
| 216    | WEBIM_CONNCTION_USER_KICKED_BY_CHANGE_PASSWORD | 用户密码更新：当前登录的用户密码被修改后，当前登录会断开并提示该错误。 |提示密码已经修改，请重新登录。|
| 217    | WEBIM_CONNCTION_USER_KICKED_BY_OTHER_DEVICE    | 用户被踢下线：开启多设备登录后，如果用户在其他设备上调用 API 或者通过管理后台踢出当前设备登录的 ID，SDK 会提示该错误。 | 提示被踢下线。|
| 219    | USER_MUTED_BY_ADMIN   | 用户被全局禁言：在管理后台禁言了此用户后，该用户发送消息时会提示该错误。   | 提示⽤户已被禁⾔。|
| 221    | USER_NOT_FRIEND                                | 非好友禁止发消息：开通非好友禁止发消息后，非好友间发消息提示此错误。该功能可在控制台开通。 | 提示⽤户⾮对⽅好友。|
| 500    | SERVER_BUSY                                    | 服务器忙碌。 | 提示服务忙，请重试。|
| 501    | MESSAGE_INCLUDE_ILLEGAL_CONTENT                | 消息含有非法内容：如果消息被过滤系统识别为非法消息时返回该错误。 | 提示消息发送失败，包含敏感词等⾮法内容。 |
| 502    | MESSAGE_EXTERNAL_LOGIC_BLOCKED                 | 消息被拦截：开通反垃圾服务后，消息被拦截报此错误。           | 提示消息发送失败。|
| 503    | SERVER_UNKNOWN_ERROR                           | 消息发送失败未知错误：服务端返回的错误信息超出 SDK 处理范围。 | 提示消息发送失败。|
| 504    | MESSAGE_RECALL_TIME_LIMIT                      | 撤回消息时超出限定时间。  | 提示已经超出可撤回的时间。 | 
| 505    | SERVICE_NOT_ENABLED                            | 服务未开启：要使用的某些功能未开通。   | 根据 error message 开通相应的功能。 |
| 506    | SERVICE_NOT_ALLOW_MESSAGING                    | 用户未在白名单中：群组或聊天室开启全员禁言时，若用户未在白名单中发送消息时提示该错误。 | 提示当前群组或聊天室已禁⾔。| 
| 507    | SERVICE_NOT_ALLOW_MESSAGING_MUTE               | 当前用户被禁言：在群组或者聊天室中被禁言后发消息报此错误。  | 提示⽤户已被禁⾔。|
| 508    | MESSAGE_MODERATION_BLOCKED                     | 第三方内容审核服务的消息审核结果为“拒绝”时提示该错误。  | 提示消息发送失败，消息内容不合规。|
| 509    | MESSAGE_CURRENT_LIMITING                       | 单个用户 ID 发送消息超出频率限制。默认情况下，SDK 对单个用户 ID 发送群消息未做频率限制。如果你联系了环信商务设置了该限制，一旦在在单聊、群聊或聊天室中单个用户的消息发送频率超过设定的上限，则会提示该错误。 | 提示⽤户发消息过于频繁。|
| 510    | MESSAGE_WEBSOCKET_DISCONNECTED                 | 消息发送失败，例如网络断开、重连失败等情况下导致发送失败。  | 提示消息发送失败。|
| 511    | MESSAGE_SIZE_LIMIT                 | 消息体大小超过限制。关于各端消息体大小的限制，详见[消息概述](message_overview.html#消息类型)。| 提示消息内容过⼤。| 
| 512    | MESSAGE_SEND_TIMEOUT                 | 发送消息超时。例如，发消息时连接断开，会提示该错误。| 提示发送超时。|
| 601    | GROUP_ALREADY_JOINED                           | 已在群组内：当前用户已在该群组中。 | 确保邀请的⽤户不在群组中，不要重复邀请。|
| 602    | GROUP_NOT_JOINED                               | 不在群组内：用户发送群消息或进行群操作时未加入该群组。 | 确保已经加⼊群组。|
| 603    | PERMISSION_DENIED                              | 用户无权限：例如，如果用户被添加到黑名单后，发送消息时会提示该错误。其他报错情况包括用户修改其他用户发出的消息、修改其他用户设置的群成员属性以及普通群成员试图解散子区（仅子区所在群组的群主和群管理员有权解散子区）。 | 提示⽤户没有权限。|
| 604    | WEBIM_LOAD_MSG_ERROR                           | 消息回调函数内部错误。 | 消息解析失败，确保消息格式正确。| 
| 605    | GROUP_NOT_EXIST                                | 群组不存在：发送消息时群组 ID 不正确。  | 检查群组或聊天室 ID 是否正确。| 
| 606    | GROUP_MEMBERS_FULL                             | 群组已满：群组成员数量已达到创建群组时设置的最大人数。  | 提示群组⼈数已达上限。| 
| 607    | GROUP_MEMBERS_LIMIT    | 创建群组时设置的群成员最大数量超过 IM 套餐包中的上限。各版本的即时通讯套餐包支持的群组成员最大数量，详见 [IM 套餐包功能详情](/product/product_package_feature.html)。 | 按照套餐限制⼈数上限。 |
| 609    | GROUP_MEMBER_ATTRIBUTES_SET_FAILED    | 群成员属性设置失败。 | 提示设置失败，请重试。|
| 700    | REST_PARAMS_STATUS                             | 用户 token 或 App Key 不存在或不正确导致 API 调用失败。 | 正确设置 App Key。 |
| 702    | CHATROOM_NOT_JOINED                             | 被操作的人员不在聊天室。  | 提示该⽤户不在当前聊天室。 |
| 704    | CHATROOM_MEMBERS_FULL                          | 聊天室已满：聊天室已经达到人数上限。  | 提示聊天室⼈数已满。|
| 705    | CHATROOM_NOT_EXIST                             | 聊天室不存在：尝试对不存在的聊天室进行操作时提示该错误。| 检查聊天室 ID 是否正确。 |
| 800    | LOCAL_DB_OPERATION_FAILED       | 本地数据库操作失败。| ⽤ miniCore 使⽤本地会话列表时，提示会话列表操作失败。|
| 999    | SDK_RUNTIME_ERROR                              | Websocket 发送消息错误。  | 提示登录失败，重新登录。|
| 1100   | PRESENCE_PARAM_EXCEED                          | 发布自定义在线状态时，参数长度超出限制。  | 设置⾃定义在线状态时不要超过1024 字节。|
| 1101   | REACTION_ALREADY_ADDED                         | Reaction 重复添加。   | 确保同⼀个⽤户不要添加重复的 Reaction。|
| 1102   | REACTION_CREATING                              | 创建 Reaction 时，其他人正在创建。| 提示其他⼈正在创建 Reaction。|
| 1103   | REACTION_OPERATION_IS_ILLEGAL                  | 用户对该 Reaction 没有操作权限：没有添加过该 Reaction 的用户进行删除操作，或者单聊消息非发送者和非接收者进行添加 Reaction 操作。 | 确保⽤户正确操作 Reaction。 |
| 1200   | TRANSLATION_NOT_VALID                          | 传入的语言 code 不合法。 | 使⽤翻译功能时，确保传⼊的 code 正确。|
| 1201   | TRANSLATION_TEXT_TOO_LONG                      | 翻译的文本过长。 | 提示消息⽂本过⻓，翻译失败。 |
| 1204   | TRANSLATION_FAILED                             | 获取翻译服务失败。 | 提示翻译失败。|
| 1300   | THREAD_NOT_EXIST                               | 子区不存在：未找到该子区。    | 确保⼦区 ID 正确。 |
| 1301   | THREAD_ALREADY_EXIST                           | 该消息 ID 下子区已存在，重复添加子区。 | 提示⼦区已存在，不能重复创建。|
| 1302   | MODIFY_MESSAGE_NOT_EXIST | 修改的消息不存在。  | 确保消息 ID 正确。 |
| 1304   | MODIFY_MESSAGE_FAILED | 消息修改失败。  | 提示修改消息失败。 |