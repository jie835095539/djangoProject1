from django.utils.safestring import mark_safe
import copy
class Pagination(object):
    """页面分页展示组件request"""

    def __init__(self,request,queryset,page_size=10,page_param="page",page_max=11):
        """页面分页展示组件
        request：请求的对象
        queryset：请求查询的查询结果
        page_size：每页展示的条数
        page_param：页码参数
        page_max:页码展示的页码个数
        """

        # 拼接查询原有的查询条件(分页的情况下，获取原有的查询条件)
        query_dict = copy.deepcopy(request.GET)  # 通过copy功能，进行深度复制一份get请求参数
        query_dict.mutable = True
        self.page_param=page_param
        self.query_dict=query_dict
        self.query_dict.setlist(self.page_param, [1])#拼接查询条件
       # print(self.query_dict.urlencode())


        #获取数据展示页码，默认页码为：1
        page = request.GET.get(page_param,"1")
        print(page)
        if page.isdecimal():
            page=int(page)
        else:
            page=1
        self.page=page
        self.page_size=page_size
        self.start_row = (self.page - 1) * self.page_size
        self.end_row = self.page * self.page_size
        self.page_queryset=queryset[self.start_row:self.end_row]
        #获取数据的总条数，根据总条数，返回要显示的页码
        data_count = queryset.count()
        page_count, div = divmod(data_count, self.page_size)
        if div:
            page_count = page_count + 1
        self.page_count = page_count
        self.page_max = page_max
        """分页组件处理<li><a href="?page=1">1</a></li>"""
        # 为了显示前后几个页面，则将显示的页码，根据数据进行拆分

    def html(self):

        if self.page_count <= 2 * self.page_max + 1:
            start_page = 1
            end_page = self.page_count
        else:
            if self.page <= self.page_max:
                start_page = 1
                end_page = self.page + self.page_max
            else:
                start_page = self.page - self.page_max
                if self.page >= self.page_count - self.page_max:
                    end_page = self.page_count
                else:
                    end_page = self.page + self.page_max
        # 通过循环，构造页码显示页签
        page_list_string = []
        # 根据判断数据条件，增加首页功能
        self.query_dict.setlist(self.page_param, [1])
        # print(self.query_dict.urlencode())
        page_list_string.append('<li><a href="?{}">首页</a></li>'.format(self.query_dict.urlencode()))
        # 根据判断数据条件，增加上一页功能
        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page - 1])
            pre_page = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [1])
            pre_page = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        page_list_string.append(pre_page)
        for i in range(start_page, end_page + 1):
            # 根据判断，当前页是否等于，如果是则给当前页码加样式，凸显当前页
            if i == self.page:
                self.query_dict.setlist(self.page_param, [i])
                page_ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                self.query_dict.setlist(self.page_param, [i])
                page_ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_list_string.append(page_ele)
        # 根据判断数据条件，增加下一个功能
        if self.page < self.page_count:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            prev_page = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [self.page_count])
            prev_page = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        page_list_string.append(prev_page)
        # 根据判断数据条件，增加尾页功能
        self.query_dict.setlist(self.page_param, [self.page_count])
        page_list_string.append('<li><a href="?{}">尾页</a></li>'.format(self.query_dict.urlencode()))
        #print("处理前", page_list_string)
        jump = """
                <li>
                <form method="get" style="float:left;margin-left: -1px">
                <input  class="input-sm" style="position:relative;float: left;display: inline-block;width: 80px;border-radius:0" type="text" name="page" placeholder="页码">
                <button type="submit" class="btn-default" style="border-radius: 0;margin-right:10px">跳转</button>
                </form>
                </li>
                """
        page_list_string.append(jump)
        page_data = mark_safe("".join(page_list_string))  # 通过mark_safe,函数处理页面标签，将页面标签数据返回
        return page_data
        #print("处理后", page_data)