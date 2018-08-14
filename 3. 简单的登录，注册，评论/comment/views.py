from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from .models import Comment


def update_comment(request):
    referer = request.META.get('HTTP_REFERER', reverse('index'))

    # 数据检查
    if not request.user.is_authenticated:
        return render(request, 'login/error.html', {'message': '用户未登录', 'redirect_to': referer})
    text = request.POST.get('text', '').strip()
    if text == '':
        return render(request, 'login/error.html', {'message': '评论内容为空', 'redirect_to': referer})
    try:
        content_type = request.POST.get('content_type', '')  # 使用POST方式获取提交的信息，没有就给content_type赋值为空字符串
        object_id = int(request.POST.get('object_id', ''))  # 获取提交信息的中id值， 这里面是获取博客列表对应的ID
        model_class = ContentType.objects.get(model=content_type).model_class()  # 获取提交信息中的类型，这里即获取到博客这个类，方面下面使用
        model_obj = model_class.objects.get(pk=object_id)
    except Exception as e:
        return render(request, 'login/error.html', {'message': '评论对象不存在', 'redirect_to': referer})

    # 检查通过，保存数据
    comment = Comment()
    comment.user = request.user
    comment.text = text
    comment.content_object = model_obj
    comment.save()
    return redirect(referer)
