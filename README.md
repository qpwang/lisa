lisa
====
+ 一些说明: 
    * status参数判断请求是否正常
      - status返回状态码0为正常
      - 若出错, 返回的内容 status 不为 0.
    * 时间都以unix时间戳表示,为int,如 1332737012
    * 所有请求与用户相关的请求都为POST 带token参数

+ 登录:
    * URL : /profiles
    * 方法: POST
    * 参数:
    
    {   
        token: "0a00aeb93f14470e8a3ed3762ad11349",
        username: "wqq",
        email: "wqqqqq21@gmail.com",
        source: "sina" //sina|renren|...
    
    }
    
    * 返回: 
    
    {
        status: 0 // status 0为成功 其他为失败
    	data: {}
    }

+ 所有秘密：
    * URL : /all
    * 方法 : POST
    * 参数:
    
    {
    	token: "0a00aeb93f14470e8a3ed3762ad11349",
    	page: 3, //默认1
    	size: 4, //默认20
    }
    * 返回：
    
    {
    	status: 0,
    	data: {
    		secrets: [
            	{id: 177373776, content: "我是一条小秘密", time: 18737747},{id: 177373775, content: "我是一条小秘密", time: 18737746},{id: 177373774, content: "我是一条小秘密", time: 18737745},{id: 177373773, content: "我是一条小秘密", time: 18737744}
        	]
        }
    }

+ 在某学校发布新秘密:
    * URL : /<school-id>/secrets/add
    * 方法: POST
    * 参数: 
    
    {
    	token: "0a00aeb93f14470e8a3ed3762ad11349",
        content: "其实我...."
    }
    
    * 返回: 
    
    {
    	status: 0,
        data: {
        	id: 17263636, // 新秘密的id
        	time: 18738427
        }
    }

+ 获取某学校的秘密: 
    * URL : /<school-id>/secrets
    * 方法: POST
    * 参数: 
    
    {
    	token: "0a00aeb93f14470e8a3ed3762ad11349",
        page: 3, //默认1
        size: 3  //默认20
    } 
    
    * 返回: 
    
    {
    	status: 0,
    	data:     	{
        	secrets: [
            	{id: 177373774, content: "我是一条小秘密", time: 18737747, hot: 97},
            	{id: 177373773, content: "我是一条小秘密", time: 18737745, hot: 97},
            	{id: 177373772, content: "我是一条小秘密", time: 18737743, hot: 97}
            ]
        }
    }


+ 获取对一条秘密的评论:
    * URL:  /<secret-id>/comments
    * 方法: POST
    * 参数: 
    
    {
    	token: "0a00aeb93f14470e8a3ed3762ad11349",
        page: 1, // 默认1
        size: 2 //默认20
    } 
    
    * 返回: 
    
    {
    	status: 0,
    	data: {
        	comments: [
            	{id: 18287373, time: 17272733, content: "沙发", floor: 1}, 
            	{id: 28833838, time: 17288384, content: "二楼你好", floor: 2, replied_floor: <replied floor> or null},
            ]
        }
    }

+ 对一条秘密发表评论或回复它下面的某条评论:
    * URL : /<secret-id>/comments/add
    * 方法: POST
    * 参数: 
    
    {
    	token: "0a00aeb93f14470e8a3ed3762ad11349",
        reply_to: 1726337777 // 回复的那条评论的id
        content: "楼主我不知道你是谁"
    }
    
    * 返回: 
    
    {
    	status: 0,
    	data: {
        	id: 172837374 // 新评论的id
        	time: 1727338838 // 创建的时间
        	floor: 17
        }
    }

+ 我说过的秘密:
    * URL : /mine
    * 方法: POST 
    * 参数: 
    
    {
    	token: "0a00aeb93f14470e8a3ed3762ad11349",
        page: 2  // 默认1
        size: 1  // 默认20
    }
    
    * 返回: 
    
    {
    	status: 0,
    	data: {
        	secrets: [
            	{id: 177373774, content: "我是一条小秘密", time: 18737747, hot: 97}
        	]
        }
    }

+ 获取新消息:
    * URL : /notice
    * 方法: POST
    * 参数: 
    
    {
    	token: "0a00aeb93f14470e8a3ed3762ad11349",
    	since: 1727338838,  //若有，则只返回该时间戳之后的消
    	size: 3
    }
    
    * 返回: 
    
    {
    	status: 0,
    	data: {
        	notices: [
            	{
            		id: 188838383,
            		replied_content: "沙发!", 						reply_content: "沙发傻逼", 
            		reply_id: 71717, 
            		secret: { 
            			id:1772, 
            			content:"我是一条小秘密", time:17772}, time: 18883838
            		}
            	// 说明：如果有replied_content，则为回复一条评论，否则为回复一条秘密
            	.......
        	]
        }
    }

+ 把消息标为已读(从数据库里删除):
    * URL: /notice/<notice-id>
    * 方法: POST
    * 参数: {token: "0a00aeb93f14470e8a3ed3762ad11349"}
    * 返回: {status: 0, data: {}}

+ 检查更新：
    * URL: /update
    * 方法： GET
    * 参数： 无
    * 返回： 
    
    {
    	status: 0,
    	data: {
        	"version": 1,
        	"content": "版本1.1\n改了几个bug",
        	"url": "http://lisa.com/1.1.apk",
        	"flag": 0
        }
    }
