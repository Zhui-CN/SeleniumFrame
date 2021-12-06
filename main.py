# coding=utf-8

from chrome.base import Chrome
from operate import operate_ls
from chrome.component import component_function


def run(server=None, components=None):
    component_idx = 0
    chrome = Chrome(server)
    init_retry = 1
    retry_numb = init_retry + 2
    while component_idx < len(components):
        retry = init_retry if components[component_idx].get("retry") is None else components[component_idx]["retry"]
        operate = components[component_idx]["operate"]
        arguments = components[component_idx]["arguments"]
        callback = components[component_idx].get("callback")
        func = component_function[operate]
        result = func(chrome, **arguments)
        if result:
            if callback:
                callback(chrome, result)
            component_idx += 1
        elif retry:
            print(f"执行第{component_idx + 1}个环节的{operate}失败,正在重试第{retry_numb - retry}次")
            components[component_idx]["retry"] = retry - 1
        else:
            print(f"执行第{component_idx + 1}个环节的{operate}失败,尝试跳过")
            component_idx += 1
        for layer in range(chrome.frame_layers):
            chrome.driver.switch_to.parent_frame()
            chrome.frame_layers -= 1
    chrome.close()


if __name__ == '__main__':
    # run(server="127.0.0.1:9527", components=operate_ls)
    run(server=None, components=operate_ls)
