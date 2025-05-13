import requests
from typing import Optional, Dict, Union
from fake_useragent import UserAgent


class RequestClient:
    """Requests库封装类，支持智能协议头管理、异常处理和代理配置"""
    ua = UserAgent()
    _default_headers = {
        'User-Agent': ua.random,
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
    }

    def __init__(self,
                 base_headers: Optional[Dict] = None,
                 timeout: int = 10,
                 verify_ssl: bool = True,
                 proxy: Optional[Dict[str, str]] = None):  # 新增默认代理参数
        """
        初始化HTTP客户端
        :param base_headers: 基础协议头（会被后续请求继承）
        :param timeout: 默认超时时间(秒)
        :param verify_ssl: 是否验证SSL证书
        :param proxy: 默认代理配置（格式：{'http': 'http://user:pass@proxy', 'https': 'https://proxy'}）
        """
        self.headers = self._default_headers.copy()
        if base_headers:
            self.headers.update(base_headers)

        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.proxy = proxy  # 保存默认代理配置

    def _merge_headers(self,
                       extra_headers: Optional[Dict] = None) -> Dict:
        """合并基础协议头和临时协议头"""
        merged = self.headers.copy()
        if extra_headers:
            merged.update(extra_headers)
        return merged

    def _merge_proxies(self,
                       request_proxies: Optional[Dict[str, str]] = None) -> Optional[Dict[str, str]]:
        """合并默认代理和请求代理（请求代理优先级更高）"""
        if not self.proxy and not request_proxies:
            return None
        if self.proxy and not request_proxies:
            return self.proxy.copy()
        if not self.proxy and request_proxies:
            return request_proxies.copy()
        # 合并并让请求代理覆盖默认代理的相同协议
        return {**self.proxy, **request_proxies}

    def get(self,
            url: str,
            params: Optional[Dict] = None,
            headers: Optional[Dict] = None,
            timeout: Optional[int] = None,
            proxies: Optional[Dict[str, str]] = None) -> Dict:  # 新增单次请求代理参数
        """
        GET请求
        :param proxies: 本次请求使用的代理（格式：{'http': 'http://proxy', 'https': 'https://proxy'}）
        :return: 包含请求结果的字典
        """
        return self._request(
            method='GET',
            url=url,
            params=params,
            headers=headers,
            timeout=timeout,
            proxies=proxies  # 传递代理参数
        )

    def post(self,
             url: str,
             data: Optional[Union[Dict, str, bytes]] = None,
             json: Optional[Dict] = None,
             headers: Optional[Dict] = None,
             timeout: Optional[int] = None,
             proxies: Optional[Dict[str, str]] = None) -> Dict:  # 新增单次请求代理参数
        """
        POST请求
        :param data: 表单格式数据
        :param json: JSON格式数据
        :param proxies: 本次请求使用的代理（格式：{'http': 'http://proxy', 'https': 'https://proxy'}）
        """
        return self._request(
            method='POST',
            url=url,
            data=data,
            json=json,
            headers=headers,
            timeout=timeout,
            proxies=proxies  # 传递代理参数
        )

    def _request(self,
                 method: str,
                 url: str,
                 headers: Optional[Dict] = None,
                 timeout: Optional[int] = None,
                 proxies: Optional[Dict[str, str]] = None,  # 新增代理参数
                 **kwargs) -> Dict:
        """统一请求处理方法"""
        final_headers = self._merge_headers(headers)
        final_timeout = timeout or self.timeout
        final_proxies = self._merge_proxies(proxies)  # 合并代理配置

        try:
            response = requests.request(
                method=method,
                url=url,
                headers=final_headers,
                timeout=final_timeout,
                verify=self.verify_ssl,
                proxies=final_proxies,  # 使用合并后的代理
                **kwargs
            )
            response.raise_for_status()

            return {
                'success': True,
                'status_code': response.status_code,
                'content': response.text,
                'response': response,  # 保留原始响应对象引用
                'proxies':proxies
            }

        except requests.exceptions.HTTPError as e:
            return self._handle_error(e, 'HTTP错误')
        except requests.exceptions.ConnectionError as e:
            return self._handle_error(e, '连接错误（可能由代理问题引起）')
        except requests.exceptions.Timeout as e:
            return self._handle_error(e, '请求超时')
        except requests.exceptions.RequestException as e:
            return self._handle_error(e, '请求异常')

    @staticmethod
    def _handle_error(exception: Exception, error_type: str) -> Dict:
        """统一错误处理"""
        return {
            'success': False,
            'error_type': error_type,
            'exception': str(exception),
            'status_code': getattr(exception.response, 'status_code', None)
        }


# 使用示例
if __name__ == '__main__':
    # 初始化客户端（设置全局代理）
    client = RequestClient(
        base_headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        },
        # 配置全局HTTP/HTTPS代理（示例代理，请替换为真实可用代理）
        proxy={
            'http': 'http://user:password@127.0.0.1:8080',
            'https': 'https://user:password@127.0.0.1:8080'
        }
    )

    # 发送GET请求（使用全局代理）
    get_result = client.get(url='http://www.baidu.com')

    # 发送POST请求（覆盖使用临时代理）
    post_result = client.post(
        url='https://httpbin.org/post',
        json={'key': 'value'},
        # 临时代理会覆盖全局代理的https配置
        proxies={'https': 'https://user:password@192.168.1.1:8888'}
    )

    print(f"GET结果: {get_result}, 状态码: {get_result['status_code']}")
    print(f"POST结果: {post_result}, 状态码: {post_result['status_code']}")
