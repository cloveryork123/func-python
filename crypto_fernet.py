from cryptography.fernet import Fernet

# txt_pwd = b"PWGce7JNpEJ8CeEy"
# txt_pwd = b"webx123"
# txt_pwd = b"vertu@123"
txt_pwd = b''

#生成密钥
key = Fernet.generate_key()
print(key)

#固定密钥
key = b'nIPqJtT_UOltTKJudnDjE57vYiUO_Q9w7x53R0fCJxE='
print(key)

fnet_obj = Fernet(key) #定义一个用于实现加密和解密方法的对象

#进行加密
encrypt_key = fnet_obj.encrypt(txt_pwd)
print(encrypt_key)

#进行解密
decrypt_key = fnet_obj.decrypt(encrypt_key)
print(decrypt_key)
