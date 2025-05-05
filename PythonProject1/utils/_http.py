import requests
from typing import Optional, Dict, Union


class RequestClient:
    """Requests库封装类，支持智能协议头管理和异常处理"""

    _default_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
    }

    def __init__(self,
                 base_headers: Optional[Dict] = None,
                 timeout: int = 10,
                 verify_ssl: bool = False):
        """
        初始化HTTP客户端
        :param base_headers: 基础协议头（会被后续请求继承）
        :param timeout: 默认超时时间(秒)
        :param verify_ssl: 是否验证SSL证书
        """
        self.headers = self._default_headers.copy()
        if base_headers:
            self.headers.update(base_headers)

        self.timeout = timeout
        self.verify_ssl = verify_ssl

    def _merge_headers(self,
                       extra_headers: Optional[Dict] = None) -> Dict:
        """合并基础协议头和临时协议头"""
        merged = self.headers.copy()
        if extra_headers:
            merged.update(extra_headers)
        return merged

    def get(self,
            url: str,
            params: Optional[Dict] = None,
            headers: Optional[Dict] = None,
            timeout: Optional[int] = None) -> Dict:
        """
        GET请求
        :return: 包含请求结果的字典
        """
        return self._request(
            method='GET',
            url=url,
            params=params,
            headers=headers,
            timeout=timeout
        )

    def post(self,
             url: str,
             data: Optional[Union[Dict, str, bytes]] = None,
             json: Optional[Dict] = None,
             headers: Optional[Dict] = None,
             timeout: Optional[int] = None) -> Dict:
        """
        POST请求
        :param data: 表单格式数据
        :param json: JSON格式数据
        """
        return self._request(
            method='POST',
            url=url,
            data=data,
            json=json,
            headers=headers,
            timeout=timeout
        )

    def _request(self,
                 method: str,
                 url: str,
                 headers: Optional[Dict] = None,
                 timeout: Optional[int] = None,
                 **kwargs) -> Dict:
        """统一请求处理方法"""
        # 协议头合并策略：实例头 < 初始化头 < 请求头
        final_headers = self._merge_headers(headers)
        final_timeout = timeout or self.timeout

        try:
            response = requests.request(
                method=method,
                url=url,
                headers=final_headers,
                timeout=final_timeout,
                verify=self.verify_ssl,
                **kwargs
            )
            response.raise_for_status()

            return {
                'success': True,
                'status_code': response.status_code,
                'content': response.text,
                'response': response  # 保留原始响应对象引用
            }

        except requests.exceptions.HTTPError as e:
            return self._handle_error(e, 'HTTP错误')
        except requests.exceptions.ConnectionError as e:
            return self._handle_error(e, '连接错误')
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
    # 初始化客户端（设置全局协议头）
    # client = RequestClient(
    #     base_headers={'X-Client': 'MyAPI'},
    #     verify_ssl=False
    # )
    client = RequestClient(base_headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
    })

    # GET请求示例
    get_result = client.get(
        url='http://www.baidu.com',
        # params={'test': 'value'},
        # headers={'X-Request-ID': '123'}  # 本次请求特有协议头
    )

    # # POST请求示例（JSON数据）
    # post_result = client.post(
    #     url='https://httpbin.org/post',
    #     json={'key': 'value'},
    #     headers={'Content-Type': 'application/json'}  # 显式指定内容类型
    # )

    # 处理结果
    print(f"GET结果: {get_result}, 状态码: {get_result['status_code']}")
    # print(f"POST结果: {post_result}, 状态码: {post_result['status_code']}")