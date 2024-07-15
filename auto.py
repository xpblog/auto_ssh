import os
import json
import paramiko
import requests

##
# 从环境变量中读取 ACCOUNTS_JSON
accounts_json = os.getenv('ACCOUNTS')
print(str(accounts_json))
accounts = json.loads(accounts_json)

# 尝试通过SSH连接的函数
def ssh_connect(host, username, password, domain):
    transport = None
    try:
        # 创建SSH客户端
        client = paramiko.SSHClient()
        # 自动添加未知的服务器密钥及策略
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 连接SSH服务端
        client.connect(host, port=22, username=username, password=password)
        print(f"SSH连接成功。")
        # 执行命令
        stdin, stdout, stderr = client.exec_command('cd domains/{domain}/public_html/data/')
        stdin, stdout, stderr = client.exec_command('ls -l')

        # 获取命令执行结果
        result = stdout.read()
        print(result.decode())

        client.exec_command('./test.sh')
    except Exception as e:
        ssh_status = f"SSH连接失败，错误信息: {e}"
        print(f"SSH连接失败: {e}")
    finally:
        if transport is not None:
            transport.close()

# 循环执行任务
for account in accounts:
    ssh_connect(account['host'], account['username'], account['password'], account['domian'])
