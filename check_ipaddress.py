import ipaddress
import urllib.parse

# 局域网地址
# 10.0.0.0~10.255.255.255 a类
# 172.16.0.0~172.31.255.255 b类
# 192.168.0.0~192.168.255.255 c类

def is_url_in_local_network(url):
    try:
        parsed_url = urllib.parse.urlparse(url)
        hostname = parsed_url.hostname
        ip_address = ipaddress.ip_address(hostname)

        print("url:", url, "parsed_url:", parsed_url)
        print("hostname:", hostname, "ip_address:", ip_address)

        # 检查IP地址是否在局域网范围内
        private_networks = ['10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16']
        for network in private_networks:
            if ip_address in ipaddress.IPv4Network(network):
                return True
        return False
    except ValueError:
        # 无法解析主机名或者IP地址，可能是一个无效的URL
        return False

if __name__ == '__main__':
    # 使用示例
    url1 = 'http://192.168.1.1:8000/docs'
    url2 = 'http://10.1.1.1'
    url3 = 'http://172.16.10.1'
    url4 = 'http://example.com'
    
    print(is_url_in_local_network(url1))  # 输出: True
    print(is_url_in_local_network(url2))  # 输出: True
    print(is_url_in_local_network(url3))  # 输出: True
    print(is_url_in_local_network(url4))  # 输出: False
