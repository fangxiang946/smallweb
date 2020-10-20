from Common.models.mongohelper import MongoDB

class Handler(object):
    
    def insert( objectname, data):
        """插入数据
        :param data: 可以是kv、{}、[{}]、({})
        :return:
        """
        mongodb = MongoDB(collection=objectname)
        mongodb.insert(data)
        return

    def update(objectname, dic):
        mongodb = MongoDB(collection=objectname)
        mongodb.update(dic)
        return

    def delete(objectname, dic):
        mongodb = MongoDB(collection=objectname)
        return mongodb.delete(dic)
    
    def query( objectname, showcol, condition=None, orderby=None):
        mongodb = MongoDB(collection=objectname)
        return mongodb.find_list(showcol, condition, orderby)
    
    
    def query_page(objectname, showcol, condition=None, orderby=None, page_size=None, page_no=None):
        mongodb = MongoDB(collection=objectname)
        return mongodb.find_list_page(showcol, condition, orderby, page_size, page_no)
