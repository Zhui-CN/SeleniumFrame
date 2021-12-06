from chrome.base import Chrome

component_function = {
    "my_func": Chrome.my_func,
    'set_cookie': Chrome.set_cookies,
    'open_link': Chrome.get,
    'input': Chrome.input,
    'click': Chrome.click,
    'select': Chrome.select,
    'node_html': Chrome.node_html,
    'switch_window': Chrome.switch_window
}
