from chrome.base import Chrome
from chrome.base import ElementConfig


def print_title(chrome: Chrome, result):
    print(chrome.driver.title)


def find_element(chrome: Chrome):
    data = chrome.get_element(ElementConfig("//title[text()='一个教程']", is_frame=False))
    print(data)
    return True if data else False


def find_element_frame1(chrome: Chrome):
    data = chrome.get_element(ElementConfig("//title[text()='一个教程']", is_frame=True))
    print(data)
    return True if data else False


def find_element_frame2(chrome: Chrome):
    dom = chrome.get_element(ElementConfig("//p[text()='结果:']", is_frame=False))
    return dom


def find_element_frame2_callback(chrome: Chrome, result):
    print(result)


def print_node(chrome: Chrome, result):
    print(result)



operate_ls = [
    {
        "operate": "open_link",
        "arguments": {"url": "http://yige.org/html/yige.php?filename=iframe"},
        "callback": print_title
    },
    {
        "operate": "my_func",
        "arguments": {"func": find_element},
    },
    {
        "operate": "my_func",
        "arguments": {"func": find_element_frame1},
    },
    {
        "operate": "my_func",
        "arguments": {"func": find_element_frame2},
        "callback": find_element_frame2_callback
    },
    {
        "operate": "node_html",
        "arguments": {"ele": ElementConfig("/html")},
        "callback": print_node
    },
    {
        "operate": "input",
        "arguments": {"ele": ElementConfig("//input[@name='q']", is_frame=True), "text": "hello"},
    },
    {
        "operate": "click",
        "arguments": {"ele": ElementConfig("//input[@type='submit']", is_frame=True)},
    }
]