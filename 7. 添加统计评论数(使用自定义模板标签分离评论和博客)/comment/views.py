from django.http import JsonResponse
from django.urls import reverse
from .models import Comment
from .forms import CommentForm


def update_comment(request):
	referer = request.META.get('HTTP_REFERER', reverse('index'))
	comment_form = CommentForm(request.POST, user=request.user)
	data = dict()
	
	if comment_form.is_valid():
		# 检查通过，保存数据
		comment = Comment()
		comment.user = comment_form.cleaned_data['user']
		comment.text = comment_form.cleaned_data['text']
		comment.content_object = comment_form.cleaned_data['content_object']
		
		parent = comment_form.cleaned_data['parent']
		if not parent is None:
			comment.root = parent.root if not parent.root is None else parent
			comment.parent = parent
			comment.reply_to = parent.user
		
		comment.save()
		
		# 返回数据
		data['status'] = 'SUCCESS'
		data['username'] = comment.user.username
		data['comment_time'] = comment.comment_time.timestamp()
		data['text'] = comment.text
		
		if not parent is None:
			data['reply_to'] = comment.reply_to.username
		else:
			data['reply_to'] = ''
		data['id'] = comment.id
		data['root_pk'] = comment.root.pk if not comment.root is None else ''
	else:
		# return render(request, 'error.html', {'message': comment_form.errors, 'redirect_to': referer})
		data['status'] = 'ERROR'
		data['message'] = list(comment_form.errors.values())[0][0]
	return JsonResponse(data)
