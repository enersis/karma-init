
def to_selector(selector: dict):
    s = []
    for k, v in selector.items():
        s.append(f'{k}={v}')
    return ','.join(s)