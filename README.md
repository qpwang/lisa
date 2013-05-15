lisa
====
+ 一些说明: 
    * 以http状态码判断是否出错:
      - 创建新用户,发表新秘密,发表新回复这三个创建操作返回状态码201为正常
      - 其它操作返回状态码200为正常
      - 若出错, 返回的内容为: { error_msg: "具体错误信息" },可直接把error_msg输出给用户.
    * 若遇到: sid表示secret id, uid表示user id, cid表示comment id, nid表示notice id
    * 时间都以unix时间戳表示,为int,如 1332737012
    * 认证采用http basic authentication(http://en.wikipedia.org/wiki/Basic_access_authentication)

+ 注册:
    * URL : /profiles
    * 方法: POST
    * 参数: {
    	token: "0a00aeb93f14470e8a3ed3762ad11349",
        username: "wqq",
        email:"wqqqqq21@gmail.com",
        
    }
    * 返回: {
        id: 1726 // 创建好的用户的id
    }

+ 登录认证：
    * URL : /profiles/me
    * 方法 ：GET
    * http basic auth
    * 返回: {
        id: 1726 // 如果登录成功，则返回用户id
    }

+ 不分学校的所有秘密：
    * URL : /all
    * 方法 : GET
    * 返回： {
        secrets: [
            {id: 177373774, content: "我是一条小秘密", time: 18737747}
        ]
    }

+ 在某学校发布新秘密:
    * URL : /<school-id>/secrets
    * 方法: POST
    * 参数: {
        content: "其实我...."
    }
    * 返回: {
        id: 17263636 // 新秘密的id
    }

+ 获取某学校的秘密: 
    * URL : /<school-id>/secrets
    * 方法: GET
    * 参数: {
        page: 2 // 返回第几页(默认第1页), page szie需确定
    } 
    * 返回: {
        secrets: [
            {id: 177373774, content: "我是一条小秘密", time: 18737747, hot: 97}
        ]
    }


+ 获取对一条秘密的评论:
    * URL:  /<secret-id>/comments
    * 方法: GET
    * 参数: {
        page: 2 // 返回第几页(默认第1页), page szie需确定
    } 
    * 返回: {
        comments: [
            {id: 18287373, time: 17272733, content: "沙发", floor: 1}, 
            {id: 28833838, time: 17288384, content: "二楼你好", floor: 2, replied_floor: <replied floor> or null}, 
            ........
        ]
    }

+ 对一条秘密发表评论或回复它下面的某条评论:
    * URL : /<secret-id>/comments
    * 方法: POST
    * 参数: {
        reply_to: 1726337777 // 回复的那条评论的id
        content: "楼主我不知道你是谁"
    }
    * 返回: {
        id: 172837374 // 新评论的id
        time: 1727338838 // 创建的时间
        floor: 17
    }

+ 今日热门: 
    * URL : /<school-id>/hot/today
    * 方法: GET 
    * 参数: 无
    * 返回: {
        secrets: [
            {id: 177373774, content: "我是一条小秘密", time: 18737747, hot: 97}
        ]
    }

+ 本周热门:
    * URL : /<school-id>/hot/week
    其它同上

+ 我说过的秘密:
    * URL : /mine
    * 方法: GET 
    * 参数: {
        page: 2  // 分页
    }
    * 返回: {
        secrets: [
            {id: 177373774, content: "我是一条小秘密", time: 18737747, hot: 97}
        ]
    }

+ 获取新消息:
    * URL : /notice
    * 方法: GET
    * 可选参数: since： 若有，则只返回该时间戳之后的消息
    * 可选参数： page：分页，默认为1
    * 返回: {
        notices: [
            {id: 188838383, replied_content: "沙发!", reply_content: "沙发傻逼", reply_id: 71717, secret: { id:1772, content:"我是一条小秘密", time:17772}, time: 18883838}
            // 说明：如果有replied_content，则为回复一条评论，否则为回复一条秘密
            .......
        ]
    }

+ 把消息标为已读(从数据库里删除):
    * URL: /notice/<notice-id>
    * 方法: DELETE
    * 参数: 无
    * 返回: 正常则无

+ 检查更新：
    * URL: /update
    * 方法： GET
    * 参数： 无
    * 返回： {
        "version": 1,
        "content": "版本1.1\n改了几个bug",
        "url": "http://lisa.com/1.1.apk",
        "flag": 0
    }
