from . import  MongoDB

class Handler:
    
    def insert(objectname, data):
         """插入数据
        :param data: 可以是kv、{}、[{}]、({})
        :return:
        """
        mongodb = MongoDB(collection = objectname)  
        mongodb.insert(data)
        return
    
    
    def update(objectname, ids, dic):
        mongodb = MongoDB(collection = objectname)      
        mongodb.update(ids, dic)
        return
    
    
    def query(objectname, showcol, condition, orderby=None):
        mongodb = MongoDB(collection = objectname)
        return mongodb.find_list(showcol, condition, orderby)
    
    
    def query_page(objectname, showcol, condition, orderby=None, page_size=10, page_no=1):
        mongodb = MongoDB(collection = objectname)
        return mongodb.find_list_page(showcol, condition, orderby, page_size, page_no)
        
    