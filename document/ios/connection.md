# 连接

应用客户端成功连接到环信服务器后，才能使用环信即时通讯 SDK 的收发消息等功能。

你调用 `login` 方法登录后，客户端 SDK 会自动连接环信服务器。关于登录详情，请参见[登录文档](login.html)。

## 监听连接状态

你可以通过注册连接监听确认连接状态。

```swift
override func viewDidLoad() {
    ...
    // 注册连接状态监听，在 SDK 初始化之后调用。
    EMClient.shared().add(self, delegateQueue: nil)
    ...
}

extension ViewController: EMClientDelegate {
    // 连接成功，开始从服务器拉取离线消息时触发。
    // 注意：如果本次登录服务器没有离线消息，不会触发该回调。
    func onOfflineMessageSyncStart() {
    }
    // 离线用户上线后从服务器拉取离线消息结束时触发。
    // 注意：如果再拉取离线过程中因网络或其他原因导致连接断开，不会触发该回调。
    func onOfflineMessageSyncFinish() {
    }
    
    // 连接状态变更时触发该回调
    func connectionStateDidChange(_ aConnectionState: EMConnectionState) {
        
    }
    // 自 4.15.0 版本，SDK 会在 Token 有效期达到 80% 时回调即将过期通知。
    func tokenWillExpire(_ aErrorCode: EMErrorCode) {
        // 通过 App Server 获取新的 token,然后调用 sdk 的 renewToken 方法更新 token
        EMClient.shared().renewToken("newToken") { e in
            
        }
    }
    
    // token 已过期
    func tokenDidExpire(_ aErrorCode: EMErrorCode) {
        
        
    }
    
}

```

## 自动重连

登录后，如果由于网络信号弱、切换网络等引起的连接中断，SDK 会自动尝试重连。重连成功或者失败时会收到 `connectionStateDidChange` 通知。

不过，SDK 在以下情况下会停止自动重连。你需要调用 `login` 方法登录。

- 用户调用了 SDK 的登出方法 `logout` 主动退出登录。
- 登录时鉴权错误，例如， token 无效（错误码 104）或已过期（错误码 108）。
- 用户在其他的设备上更改了密码，导致此设备上自动登录失败，提示错误码 216。
- 用户的账号被从服务器端删除，提示错误码 207。
- 用户在另一设备登录，将当前设备上登录的用户踢出，提示错误码 206。 
- 用户登录设备数量超过限制，提示错误码 214。
- 应用程序的日活跃用户数量（DAU）或月活跃用户数量（MAU）达到上限，提示错误码 8。
- 开启多设备服务后，用户在其他设备上通过调用 API 或者管理后台将当前设备登录的 ID 强制退出登录（错误码 217）。