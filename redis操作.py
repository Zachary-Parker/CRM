import redis

"""
{
    "k1":"v1",
    'names': ['把几个','鲁宁','把几个','鲁宁','把几个','把几个','把几个','把几个',]
}

"""

conn = redis.Redis(host='47.93.4.198',port=6379,password='123123')
# conn.set('k1','v1') # 向远程redis中写入了一个键值对
# val = conn.get('k1') # 获取键值对
# print(val)
# conn.lpush('names_list',*['把几个','鲁宁']) #
# v = conn.llen('names_list')
#
# for i in range(v):
#     val = conn.rpop('names_list')
#     val = conn.lpop('names_list')
#     print(val.decode('utf-8'))
# v = conn.llen('namessssss_list')
# print(v)

# ['把几个','鲁宁','把几个','鲁宁','把几个','把几个','把几个','把几个',]

# conn.lpush('sale_id_list',*[1,2,3,1,2,1,1,1])

# 自动分配时，获取销售ID
# sale_id = conn.rpop('sale_id_list')

# 获取之后，未使用。再重新加入到原来的列表中
# conn.rpush('sale_id_list',3)

# conn.delete('sale_id_list_origin')
# conn.rpush('sale_id_list_origin',*[1,2,3,1,2,1,1,1])

# ct = conn.llen('sale_id_list_origin')
# for i in range(ct):
#     v = conn.lindex('sale_id_list_origin',i)
#     conn.rpush('sale_id_list',v)
#
# v = conn.lpop('sale_id_list')
# print(v)
#
# conn.delete('sale_id_list_origin')
# conn.delete('sale_id_list')

# 第一次运行，只有数据库有数据

# 如果数据库中没有取到数据，那么直接返回None
# 否则
# conn.rpush('sale_id_list',*[1,2,3,1,2,1,1,1])
# conn.rpush('sale_id_list_origin',*[1,2,3,1,2,1,1,1])

# 接下类一个一个获取,如果取到None，表示已经取完
# sale_id = conn.lpop('sale_id_list')
# if not sale_id:
#     # 先判断，是否需要重置
#     if reset:
#         conn.delete('sale_id_list_origin')
#         conn.delete('sale_id_list')
#         # 重新从数据库获取，并给两个进行复制
#         reset = False
#     else:
#         ct = conn.llen('sale_id_list_origin')
#         for i in range(ct):
#             v = conn.lindex('sale_id_list_origin', i)
#             conn.rpush('sale_id_list', v)
#     sale_id = conn.lpop('sale_id_list')
#
# print(sale_id)


v = conn.get('xxfasdf9dfsd')
print(v)




