from redis import *


if __name__ == '__main__':

    try:
        src = StrictRedis()
        # 添加key
        res = src.set('name','yc')
        print(res)

    #     获取值
        print(src.get('name'))

        src.set('name','zxy')
        print(src.get('name'))

        src.delete('name')

        print(src.get('name'))

        src1 = StrictRedis(db=10)

        print(src1.keys())
    except Exception as ex:
        print(ex)