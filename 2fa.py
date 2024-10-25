import pyotp
import time
 
# 生成2FA密钥
secret_key = pyotp.random_base32()
print("2FA密钥:", secret_key)

# 创建TOTP对象
totp = pyotp.TOTP(secret_key)

# 生成当前的2FA密码
for i in range(60):
    # 生成当前的2FA密码
    current_password = totp.now()
    print("当前2FA密码:", current_password)
    time.sleep(5)

# 验证2FA密码
expected_password = input("请输入您的2FA密码: ")
if totp.verify(expected_password):
    print("2FA验证成功")
else:
    print("2FA验证失败")
