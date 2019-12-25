def get_attribute(cls):
    # 获取类中所有属性
    # import types
    # return [k for k, v in vars(cls).items()
    #         if not k.startswith("__") and
    #         not k.endswith("__") and
    #         not isinstance(v, types.FunctionType) and
    #         not isinstance(v, property) and
    #         not k.startswith("_")]
    from sqlalchemy.orm.attributes import InstrumentedAttribute
    return [k for k, v in vars(cls).items()
            if isinstance(v, InstrumentedAttribute)]


# 字典变对象
class DictObj(object):
    def __init__(self, map):
        self.map = map

    def __setattr__(self, name, value):
        if name == 'map':
            object.__setattr__(self, name, value)
            return
        # print('set attr called ', name, value)
        self.map[name] = value

    def __getattr__(self, name):
        try:  # 获取失败返回None
            v = self.map[name]
            if isinstance(v, dict):
                return DictObj(v)
            if isinstance(v, list):
                r = []
                for i in v:
                    r.append(DictObj(i))
                return r
            else:
                return self.map[name]
        except:
            return None

    def __getitem__(self, name):
        return self.map[name]
