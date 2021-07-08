from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from Mall import models
from Mall.models import User, Admin, Goods, ShoppingCart, Order, OrderInfo
import datetime


def sign(request):
    if request.method == "GET":
        return render(request, "sign.html")
    if_exit_id = User.objects.filter(id=request.POST.get('user_id')).first()
    if if_exit_id:
        return HttpResponse("<script>alert('该用户名已存在，无法重复注册!!!')</script>")
    else:
        User.objects.create(id=request.POST.get('user_id'), password=request.POST.get('user_password'),
                            name=request.POST.get('user_name'), sex=request.POST.get('user_sex'),
                            number=request.POST.get('user_number'), address=request.POST.get('user_address'),
                            birthday=request.POST.get('user_birthday'))
        return HttpResponse("<script>alert('注册成功!!!请返回登陆界面进行登陆。')</script>")


def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    if request.POST.get('user_identity') == 'user':  # 用户登录
        if_true = User.objects.filter(id=request.POST.get('user_id'), password=request.POST.get('user_password'))
        if not if_true:
            return HttpResponse("<script>alert('账号或密码错误')</script>")
        else:
            request.session['is_login'] = True
            request.session['identity'] = 'user'
            request.session['log_id'] = request.POST.get('user_id')
            return redirect('/homepage/')
    else:  # 管理员登录
        if_true_admin = Admin.objects.filter(id=request.POST.get('user_id'), password=request.POST.get('user_password'))
        if not if_true_admin:
            return HttpResponse("<script>alert('账号或密码错误')</script>")
        else:
            request.session['is_login'] = True
            request.session['log_id'] = request.POST.get('user_id')
            request.session['identity'] = 'admin'
            return redirect('/homepage/')


def homepage(request):
    status = request.session.get('is_login')
    if not status:
        return redirect('/login/')
    user_id = request.session.get('log_id')
    if request.session.get('identity') == 'user':
        user_name = User.objects.filter(id=user_id).first().name
    else:
        user_name = Admin.objects.filter(id=user_id).first().name
    goods = models.Goods.objects.all()  # 所有商品
    context = {'id': user_id, 'name': user_name, 'identity': request.session.get('identity'), 'goods_list': goods}
    return render(request, "Index.htm", context)


def admin(request):
    if not request.session.get('is_login'):
        return redirect('/login/')
    if not (request.session.get('identity') == 'admin'):
        return redirect('/login/')
    user_id = request.session.get('log_id')
    user_name = Admin.objects.filter(id=user_id).first().name
    goods = models.Goods.objects.all()  # 所有商品
    users = models.User.objects.all()  # 所有用户
    admin = models.Admin.objects.all()  # 所有用户
    order_list = Order.objects.all()
    context = {'order_list': order_list}
    context = {'id': user_id, 'name': user_name, 'goods_list': goods, 'user_list': users, 'admin_list': admin, 'order_list': order_list}
    return render(request, "admin.html", context)


def add_admin(request):
    if not request.session.get('is_login'):
        return redirect('/login/')
    if not (request.session.get('identity') == 'admin'):
        return redirect('/login/')
    if_exit_id = Admin.objects.filter(id=request.POST.get('add_admin_id')).first()
    if if_exit_id:
        return HttpResponse("<script>alert('该管理员账号已存在，无法重复添加!!!')</script>")
    else:
        Admin.objects.create(id=request.POST.get('add_admin_id'), password=request.POST.get('add_admin_password'),
                             name=request.POST.get('add_admin_name'))
        return HttpResponse("<script>alert('管理员添加成功!!!请返回查看。')</script>")


def add_goods(request):
    if not request.session.get('is_login'):
        return redirect('/login/')
    if not (request.session.get('identity') == 'admin'):
        return redirect('/login/')
    if_exit_id = Goods.objects.filter(id=request.POST.get('add_goods_id')).first()
    if if_exit_id:
        return HttpResponse("<script>alert('该商品id已存在，无法重复添加!!!')</script>")
    else:
        Goods.objects.create(id=request.POST.get('add_goods_id'), name=request.POST.get('add_goods_name'),
                             image=request.POST.get('add_goods_image'),
                             price=float(request.POST.get('add_goods_price')),
                             sort=request.POST.get('add_goods_sort'), num=int(request.POST.get('add_goods_num')))
        return HttpResponse("<script>alert('商品添加成功!!!请返回查看。')</script>")


def delete_goods(request):
    if not request.session.get('is_login'):
        return redirect('/login/')
    if not (request.session.get('identity') == 'admin'):
        return redirect('/login/')
    if_exit_id = Goods.objects.filter(id=request.POST.get('delete_goods_id')).first()
    if not if_exit_id:
        return HttpResponse("<script>alert('该商品id不存在，无法操作!!!')</script>")
    else:
        Goods.objects.filter(id=request.POST.get('delete_goods_id')).delete()
        return HttpResponse("<script>alert('商品删除成功!!!请返回查看。')</script>")


def update_goods_info(request):
    if not request.session.get('is_login'):
        return redirect('/login/')
    if not (request.session.get('identity') == 'admin'):
        return redirect('/login/')
    Goods.objects.filter(id=request.POST.get('update_goods_id')).update(name=request.POST.get('update_goods_name'),
                                                                        image=request.POST.get('update_goods_image'),
                                                                        price=float(
                                                                            request.POST.get('update_goods_price')),
                                                                        sort=request.POST.get('update_goods_sort'),
                                                                        num=int(request.POST.get('update_goods_num')))
    return HttpResponse("<script>alert('商品信息修改成功!!!请返回查看。')</script>")


def delete_user(request):
    if not request.session.get('is_login'):
        return redirect('/login/')
    if not (request.session.get('identity') == 'admin'):
        return redirect('/login/')
    if_exit_id = User.objects.filter(id=request.POST.get('delete_user_id')).first()
    if not if_exit_id:
        return HttpResponse("<script>alert('该用户id不存在，无法操作!!!')</script>")
    User.objects.filter(id=request.POST.get('delete_user_id')).delete()
    return HttpResponse("<script>alert('用户删除成功!!!请返回查看。')</script>")


def logout(request):
    request.session.flush()
    return redirect('/login/')


def personal_info(request):
    if not request.session.get('is_login'):
        return redirect('/login/')
    if request.session.get('identity') == 'user':  # 用户登录
        user_info = User.objects.filter(id=request.session.get('log_id')).first()
        context = {'id': request.session.get('log_id'), 'identity': request.session.get('identity'),
                   'personal_info': user_info}
        return render(request, "personal_info.html", context)
    else:  # 管理员登录
        admin_info = Admin.objects.filter(id=request.session.get('log_id')).first()
        context = {'id': request.session.get('log_id'), 'identity': request.session.get('identity'),
                   'personal_info': admin_info}
        return render(request, "personal_info.html", context)


def update_personal_info(request):
    if not request.session.get('is_login'):
        return redirect('/login/')
    if request.session.get('identity') == 'user':
        user_id = request.session.get('log_id')
        new_password = request.POST.get('update_user_password')
        new_name = request.POST.get('update_user_name')
        new_sex = request.POST.get('update_user_sex')
        new_number = request.POST.get('update_user_number')
        new_address = request.POST.get('update_user_address')
        User.objects.filter(id=user_id).update(password=new_password, name=new_name, sex=new_sex, number=new_number,
                                               address=new_address)
        return redirect('/personal_info/')
    else:
        admin_id = request.session.get('log_id')
        new_password = request.POST.get('update_user_password')
        new_name = request.POST.get('update_user_name')
        Admin.objects.filter(id=admin_id).update(password=new_password, name=new_name)
        return redirect('/personal_info/')


def search(request):
    key_words = request.POST.get('search_key_words')
    result = Goods.objects.filter(name__icontains=key_words)
    if request.session.get('identity') == 'user':
        _id = request.session.get('log_id')
        _name = User.objects.filter(id=_id).first().name
    else:
        _id = request.session.get('log_id')
        _name = Admin.objects.filter(id=_id).first().name
    context = {'id': _id, 'name': _name, 'identity': request.session.get('identity'), 'goods_list': result}
    return render(request, "Index.htm", context)


def filtrate(request):
    sort_filter = request.POST.get('filter_sort')
    price_min = request.POST.get('min_price')
    price_max = request.POST.get('max_price')
    if sort_filter == 'All':
        result = Goods.objects.filter(price__range=(int(price_min), int(price_max)))
    else:
        result = Goods.objects.filter(sort=sort_filter, price__range=(int(price_min), int(price_max)))
    if request.session.get('identity') == 'user':
        _id = request.session.get('log_id')
        _name = User.objects.filter(id=_id).first().name
    else:
        _id = request.session.get('log_id')
        _name = Admin.objects.filter(id=_id).first().name

    context = {'id': _id, 'name': _name, 'identity': request.session.get('identity'), 'goods_list': result}
    return render(request, "Index.htm", context)


def add_cart(request):
    if not request.session.get('is_login'):
        return redirect('/login/')
    if not (request.session.get('identity') == 'user'):
        return redirect('/login/')
    user_id = request.session.get('log_id')
    goods_id = request.POST.get('add_goods_id')
    goods_price = Goods.objects.filter(id=goods_id).first().price
    goods_num = request.POST.get('add_num')
    if int(goods_num) == 0:
        return redirect('/homepage/')
    if_exit = ShoppingCart.objects.filter(user=user_id, goods=goods_id).first()
    if if_exit:  # 判断该用户购物车中是否存在该商品
        new_num = ShoppingCart.objects.filter(user=user_id, goods=goods_id).first().num + int(goods_num)
        ShoppingCart.objects.filter(user=user_id, goods=goods_id).update(num=new_num)
    else:
        ShoppingCart.objects.create(user=User.objects.filter(id=user_id).first(),
                                    goods=Goods.objects.filter(id=goods_id).first(), price=goods_price, num=goods_num)
    return redirect('/homepage/')


def cart(request):
    if not request.session.get('is_login'):
        return redirect('/login/')
    if not (request.session.get('identity') == 'user'):
        return redirect('/login/')
    cart_list = ShoppingCart.objects.filter(user=request.session.get('log_id'))
    return render(request, "cart.html", context={'cartList': cart_list, 'id': request.session.get('log_id'),
                                                 'identity': request.session.get('identity')})


def delete_cart(request):
    if not request.session.get('is_login'):
        return redirect('/login/')
    if not (request.session.get('identity') == 'user'):
        return redirect('/login/')
    user_id = request.session.get('log_id')
    goods_id = request.POST.get('delete_cart_goods_id')
    ShoppingCart.objects.filter(user=user_id, goods=goods_id).delete()
    # return HttpResponse("<script>alert('删除成功!!!请返回查看。')</script>")
    return redirect('/cart/')


def buy_cart(request):
    if not request.session.get('is_login'):
        return redirect('/login/')
    if not (request.session.get('identity') == 'user'):
        return redirect('/login/')
    user_id = request.session.get('log_id')
    goods_id = request.POST.get('delete_cart_goods_id')
    goods_name= Goods.objects.filter(id=goods_id).first().name
    buy_time = datetime.datetime.now()
    order_id = 'order' + buy_time.strftime('%Y%m%d%H%M%S')
    buyer = User.objects.filter(id=user_id).first()
    buyer_name = User.objects.filter(id=user_id).first().name
    buyer_number = User.objects.filter(id=user_id).first().number
    buyer_address = User.objects.filter(id=user_id).first().address
    order_total_price = int(request.POST.get('order_num')) * Goods.objects.filter(id=goods_id).first().price
    Order.objects.create(orderId=order_id, user=buyer, name=buyer_name, number=buyer_number, address=buyer_address,
                         totalPrice=order_total_price, time=buy_time)
    OrderInfo.objects.create(orderId=Order.objects.filter(orderId=order_id).first(), goods=goods_id, name=goods_name,
                             num=int(request.POST.get('order_num')))

    ShoppingCart.objects.filter(user=user_id, goods=goods_id).delete()
    # 更新库存
    old_num = Goods.objects.filter(id=goods_id).first().num
    Goods.objects.filter(id=goods_id).update(num=old_num - int(request.POST.get('order_num')))
    return redirect('/cart/')


def order(request):
    if not request.session.get('is_login'):
        return redirect('/login/')
    if request.session.get('identity') == 'user':
        user_id = request.session.get('log_id')
        order_list = Order.objects.filter(user=user_id)
        context = {'order_list': order_list}
        return render(request, 'order.html', context)


def order_detail(request):
    if not request.session.get('is_login'):
        return redirect('/login/')
    order_id = request.POST.get('order_id')
    detail_list = OrderInfo.objects.filter(orderId=order_id)
    context = {'detail': detail_list}
    return render(request, 'order_detail.html', context)


def delete_order(request):
    if not request.session.get('is_login'):
        return redirect('/login/')
    if not (request.session.get('identity') == 'admin'):
        return redirect('/login/')
    if_exit_id = Order.objects.filter(orderId=request.POST.get('delete_order_id')).first()
    if not if_exit_id:
        return HttpResponse("<script>alert('该订单编号不存在，无法操作!!!')</script>")
    Order.objects.filter(orderId=request.POST.get('delete_order_id')).delete()
    return HttpResponse("<script>alert('订单删除成功!!!请返回查看。')</script>")
