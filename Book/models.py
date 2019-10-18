from django.db import models

# Create your models here.
# Create your models here.
# orm模型一个类对应一张数据库中的表
# class BookInfo(models.Model):
#
#     name = models.CharField(max_length=20)
#     author = models.CharField(max_length=20)
#     read_count = models.IntegerField()
#     isdelete = models.BooleanField(default=False)
#
#
#     def __str__(self):
#         return self.name
#
# class PeopleInfo(models.Model):
#
#     name = models.CharField(max_length=10)
#     gender = models.BooleanField(default=True)
#     method = models.CharField(max_length=20)
#     isdelete = models.BooleanField(default=False)
#     # book = models.ForeignKey(BookInfo,on_delete=models.CASCADE)
#     book = models.ForeignKey(BookInfo,on_delete=models.CASCADE)
#
#     # 重写str方法否则显示的为对象类型
#     def __str__(self):
#         return self.name

# 书籍信息模型
class BookInfo(models.Model):
    name = models.CharField(max_length=20)  # 图书名称
    pub_date = models.DateField(null=True)  # 发布日期
    readcount = models.IntegerField(default=0)  # 阅读量
    commentcount = models.IntegerField(default=0)  # 评论量
    isDelete = models.BooleanField(default=False)  # 逻辑删除

    # 元类信息 : 修改表名
    class Meta:
        db_table = 'bookinfo'

# 人物信息模型
class PeopleInfo(models.Model):
    name = models.CharField(max_length=20)  # 人物姓名
    gender = models.BooleanField(default=True)  # 人物性别
    description = models.CharField(max_length=20)  # 人物描述
    isDelete = models.BooleanField(default=False)  # 逻辑删除
    book = models.ForeignKey(BookInfo,on_delete=models.CASCADE)  # 外键约束，人物属于哪本书

    # 元类信息 : 修改表名
    class Meta:
        db_table = 'peopleinfo'

    # 上传图片的模型
class PictureInfo(models.Model):
    # upload_to：表示图片上传到哪儿相对于meidia
    path = models.ImageField(upload_to='Book/')

    # 元类信息 ：修改表名
    class Meta:
        db_table = 'pictureinfo'