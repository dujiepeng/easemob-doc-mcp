# 环信即时通讯 IM Web 快速开始

<Toc />

本页面介绍如何快速集成环信即时通讯 IM Web SDK 实现单聊。

## 实现原理

下图展示在客户端发送和接收一对一文本消息的工作流程。

![](/images/web/sendandreceivemsg.png)

## 前提条件

- 有效的环信即时通讯 IM 开发者账号；
- [创建环信即时通讯 IM 项目并获取 App Key](/product/enable_and_configure_IM.html)；
- [npm](https://www.npmjs.com/get-npm)；
- SDK 支持 IE 9+、Firefox 10+、Chrome 54+ 和 Safari 6+。

## 操作步骤

### 1. 准备开发环境

本节介绍如何创建项目，将环信即时通讯 IM Web SDK 集成到你的项目中。

#### 新建 Web 项目

新建 `Easemob_quickstart` 目录。在该目录下运行 `npm init` 命令创建 `package.json` 文件，然后创建以下文件:

- `index.html`：设置 Web 应用的用户界面；
- `index.js`：包含消息发送和接收逻辑的实现代码。
此时你的目录中包含以下文件：

Easemob_quickstart<br>
├─ index.html<br>
├─ index.js<br>
└─ package.json

### 2. 集成 SDK

- 在 `package.json` 中的 `dependencies` 字段中加入 `easemob-websdk` 及对应版本：

```json
{
    "name": "web",
    "version": "1.0.0",
    "description": "",
    "main": "index.js",
    "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
    },
    "dependencies": {
    "easemob-websdk": "latest"
    },
    "author": "",
    "license": "ISC"
}
```

### 3. 创建用户

在 [环信控制台](https://console.easemob.com/user/login) 创建用户，获取用户 ID 和用户 token。详见 [创建用户文档](/product/enable_and_configure_IM.html#创建-im-用户)。

在生产环境中，为了安全考虑，你需要在你的应用服务器集成 [获取 App Token API](/document/server-side/easemob_app_token.html) 和 [获取用户 Token API](/document/server-side/easemob_user_token.html) 实现获取 Token 的业务逻辑，使你的用户从你的应用服务器获取 Token。

### 3. 实现用户界面

`index.html` 的内容如下。

`<script src="./dist/bundle.js"></script>` 用于引用 webpack 打包之后的 `bundle.js` 文件。webpack 的配置在后续步骤中介绍。

```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>Easemob Chat Examples</title>
</head>

<body>
    <h2 class="left-align">Easemob Chat Examples</h2>
    <form id="loginForm">
        <div class="col" style="min-width: 433px; max-width: 443px">
            <div class="card" style="margin-top: 0px; margin-bottom: 0px;">
                <div class="row card-content" style="margin-bottom: 0px; margin-top: 10px;">
                    <div class="input-field">
                        <label>Username</label>
                        <input type="text" placeholder="Username" id="userID">
                    </div>
                    <div class="input-field">
                        <label>Token</label>
                        <input type="text" placeholder="Token" id="token">
                    </div>
                    <div class="row">
                        <div>
                            <button type="button" id="login">login</button>
                            <button type="button" id="logout">logout</button>
                        </div>
                    </div>
                    <div class="input-field">
                        <label>Peer username</label>
                        <input type="text" placeholder="Peer username" id="peerId">
                    </div>
                    <div class="input-field">
                        <label>Peer Message</label>
                        <input type="text" placeholder="Peer message" id="peerMessage">
                        <button type="button" id="send_peer_message">send</button>
                    </div>
                </div>
            </div>
        </div>
    </form>
    <hr>
    <div id="log"></div>
</body>
<script src="./dist/bundle.js"></script>
</html>
```

### 4. 实现消息发送与接收

`index.js` 的内容如下。本文使用 import 方法导入 SDK，并使用 webpack 对 JavaScript 文件进行打包，以避免浏览器兼容性问题。你需要分别将代码中的 `<Your app key>` 替换为你之前获取的 App Key。

```javascript
import WebIM from 'easemob-websdk'
const appKey = "<Your app key>"

let username, accessToken

// 初始化客户端。相关的参数配置，详见 API 参考中的 `Connection` 类。
WebIM.conn = new WebIM.connection({
    //注意这里的 "K" 需大写。
    appKey: appKey,
})

// 添加回调函数。
WebIM.conn.addEventHandler('connection&message', {
    onConnected: () => {
        document.getElementById("log").appendChild(document.createElement('div')).append("Connect success !")
    },
    onDisconnected: () => {
        document.getElementById("log").appendChild(document.createElement('div')).append("Logout success !")
    },
    onTextMessage: (message) => {
        console.log(message)
        document.getElementById("log").appendChild(document.createElement('div')).append("Message from: " + message.from + " Message: " + message.msg)
    },
    onError: (error) => {
        console.log('on error', error)
    }
})


// 按钮行为定义。
window.onload = function () {
    // 登录。
    document.getElementById("login").onclick = function () {
        username = document.getElementById("userID").value.toString()
        accessToken = document.getElementById("token").value.toString()
        WebIM.conn
            .open({ user: username, accessToken })
            .then((res) => {
                document
                .getElementById("log")
                .appendChild(document.createElement("div"))
                .append(`Login Success`);
            })
            .catch((e) => {
                document
                .getElementById("log")
                .appendChild(document.createElement("div"))
                .append(`Login failed`);
            });
    }

    // 登出。
    document.getElementById("logout").onclick = function () {
        WebIM.conn.close();
    }

    // 发送一条单聊消息。
    document.getElementById("send_peer_message").onclick = function () {
        let peerId = document.getElementById("peerId").value.toString()
        let peerMessage = document.getElementById("peerMessage").value.toString()
        let option = {
            chatType: 'singleChat',    // 会话类型，设置为单聊。
            type: 'txt',               // 消息类型。
            to: peerId,                // 消息接收方（用户 ID)。
            msg: peerMessage           // 消息内容。
        }
        let msg = WebIM.message.create(option);
        WebIM.conn.send(msg).then((res) => {
            console.log('send private text success');
            document.getElementById("log").appendChild(document.createElement('div')).append("Message send to: " + peerId + " Message: " + peerMessage)
        }).catch(() => {
            console.log('send private text fail');
        })
    }
}
```
:::tip
对于 Typescript，通过以下代码引入类型声明：
```javascript
import WebIM, { EasemobChat } from 'easemob-websdk'
```
:::

### 5. 运行项目

本文使用 webpack 对项目进行打包，并使用 `webpack-dev-server` 运行项目。

1. 在 `package.json` 的 `dependencies` 字段中添加 `webpack`、`webpack-cli` 和 `webpack-dev-server`，并且在 `scripts` 字段中添加 `build` 和 `start:dev` 命令。

```json
{
    "name": "web",
    "version": "1.0.0",
    "description": "",
    "main": "index.js",
    "scripts": {
        "build": "webpack --config webpack.config.js",
        "start:dev": "webpack serve --open --config webpack.config.js"
    },
    "dependencies": {
        "easemob-websdk": "latest",
        "webpack": "^5.50.0",
        "webpack-dev-server": "^3.11.2",
        "webpack-cli": "^4.8.0"
    },
    "author": "",
    "license": "ISC"
}
```

2. 在项目根目录中添加 `webpack.config.js` 文件，用于配置 webpack。文件内容如下：

```javascript
const path = require('path');

module.exports = {
    entry: './index.js',
    mode: 'production',
    output: {
        filename: 'bundle.js',
        path: path.resolve(__dirname, './dist'),
    },
    devServer: {
        compress: true,
        port: 9000,
        https: true
    }
};
```

此时你的目录中包含以下文件：

Easemob_quickstart<br>
├─ index.html<br>
├─ index.js<br>
├─ package.json<br>
└─webpack.config.js

3. 在项目根目录运行以下命令，安装依赖项。

```bash
$ npm install
```

4. 运行以下命令使用 `webpack` 构建并运行项目。

```bash
# 使用 webpack 打包。
$ npm run build

# 使用 webpack-dev-server 运行项目。
$ npm run start:dev
```

项目启动后，在页面输入用户名和密码进行注册，然后利用该用户名和密码登录。登录成功后，输入对方的用户名和要发送的消息，点击 **发送** 按钮发送消息，可同时打开另一页面相互收发消息。