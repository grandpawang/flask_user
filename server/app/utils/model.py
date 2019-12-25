import sys
from datetime import datetime
from flask import jsonify, request

from . import common
from app import get_config
from database import db
from database.utils import get_attribute
from collections import Counter

cfg = get_config()


# dict表单转模型
def form_to_model(form, model):
    for name, data in form.items():
        try:  # 数据大小大于256 则不变model
            if sys.getsizeof(data) < 256 and not isinstance(data, list):
                model.__setattr__(name, data)
        except:
            pass
    return model


def quert2dict(obj, parant_cls=type(None)):
    """
        obj: DynamicModel.query.paginate.items []
        parant_cls: use it to break the callback
    """
    items = []
    for item in obj:
        result = {}
        for key in get_attribute(item.__class__):  # 要小心回环 一对多 多对一 父亲的类和子类相等则不遍历
            result[key] = eval(f'item.{key}')
            if isinstance(result[key], datetime):
                result[key] = result[key].strftime("%Y-%m-%d %H:%M:%S")
            elif isinstance(result[key], list) and result[key]:
                if not isinstance(result[key][0], parant_cls):  # 判断是否回环
                    result[key] = quert2dict(result[key], item.__class__)
                else:  # 删除回环的数据
                    del result[key]
            elif isinstance(result[key], db.Model):  # 多对一 一的数据
                if not isinstance(result[key], parant_cls):  # 一对一
                    result[key] = quert2dict([result[key]], item.__class__)[0]
                else:
                    del result[key]
            elif isinstance(result[key], bytes):
                result[key] = result[key].decode()

        items.append(result)
    return items


# 获取多表连接项的选项
def select_table(db_table):
    table_columns = list(db_table.columns)
    table_query = db.session.query(db_table).all()
    return [{table_columns[i].name: res[i] for i in range(len(res))} for res in table_query]


def get_table(column):
    result = []
    try:
        result.append(column.left.table)
        result.append(column.right.table)
    except:
        for column in column.clauses:
            result += get_table(column)
    return result


def get_options(dynamic_model):
    attr = get_attribute(dynamic_model)
    columns = [column.name for column in dynamic_model.__table__.columns]
    # 获取多表连接项即relationship项
    relationships = list(set(attr) - set(columns))
    tables = []
    for relationship in relationships:
        tables += get_table(eval(f'dynamic_model.{relationship}').expression)
    # 获取自己的外键连接表
    tables += [foreign.column.table for foreign in dynamic_model.__table__.foreign_keys
               if foreign.column.table not in tables]
    query = {}
    for table, count in Counter(tables).items():
        if count == 1 and table.name != dynamic_model.__tablename__:
            if table.foreign_keys:
                for foreignkey in table.foreign_keys:
                    query[foreignkey.column.table.name] = select_table(
                        foreignkey.column.table)
            query[table.name] = select_table(table)

    return query


def paginate_to_dict(obj):
    return {
        "content": quert2dict(obj.query.all()),
        "pageRequest": {
            "total": obj.total,  # 数据总长度
            'page': obj.page,  # 当前页数
            'size': obj.per_page,
            'page_count': obj.pages,  # 总页数
        },
    }


def common_list(dynamic_model, query=None, filter_select=None):
    """
    select method
    :param dynamic_model: database model
    :param query: maybe use sql to query
    :param filter_select: use this method before filter column
    :return: {content: [], pageRequest: {total: total, page: page, size: size, page_count:page_count}, labels: []}
    """
    search = request.json
    page = int(request.args.get('page')) if request.args.get('page') else 1
    sizes = int(request.args.get('size')) if request.args.get(
        'size') else cfg.ITEMS_PER_PAGE
    # 查询列表
    if query is None:
        query = dynamic_model.query.filter(
            filter_select) if filter_select else dynamic_model.query
        if search:
            if isinstance(search['word'], list):
                column = eval(f"dynamic_model.{search['column']}")
                # 查找table
                table = [table for table, count in Counter(get_table(column.expression)).items(
                ) if count == 1 and table.name != dynamic_model.__tablename__][0]

                query = query.filter(column.any(
                    table.c.id.in_(search['word'])))
            else:
                query = query.filter(
                    eval(f"dynamic_model.{search['column']}.like('%%{search['word']}%%')"))

    # 处理分页
    query = query.paginate(page, sizes)
    query = paginate_to_dict(query)
    query["options"] = get_options(dynamic_model)
    return query


# 删
def common_delete(dynamic_model, filter_del=(False, None)):
    """
    delete method
    :param dynamic_model: database model
    :param filter_del: use this method before filter delete
    :return: {status: True/False, data: '', msg: 'success/fail'}
    """
    ids = request.args.get('id')
    ids = ids.split(",")
    if filter_del[0]:  # 过滤删除内容
        return jsonify(common.false_return('', filter_del[1]))
    else:
        try:
            for item_id in ids:
                dynamic_model.query.filter(
                    dynamic_model.id == item_id).first().delete()
            return True
        except:
            return False


# 增/修model数据 只能修改一个
def common_edit(dynamic_model, edit_model=lambda x, y: y):
    form = request.json
    try:
        model = dynamic_model.query.filter(dynamic_model.id == form['id']).first()
    except:
        model = dynamic_model()
    form_to_model(form, model)
    edit_model(form, model)
    return model.save()
