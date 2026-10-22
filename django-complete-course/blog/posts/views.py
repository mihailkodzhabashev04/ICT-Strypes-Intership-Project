from django.shortcuts import render
from django.http import HttpResponseNotFound, Http404


posts = [
    {
        "id": 1,
        "title": "Exploring Django Basics",
        "content": "A quick guide to setting up your first Django project."
    },
    {
        "id": 2,
        "title": "Understanding Models",
        "content": "Learn how to define and use models in Django."
    },
    {
        "id": 3,
        "title": "Views and Templates",
        "content": "Connecting views to templates for dynamic content rendering."
    },
]





def home(request):
    html = ''
    for post in posts:
        html += f"""
        <div>
        <a href='/post/{post['id']}/'>
            <h1>{post['id']} - {post['title']}</h1></a>
            <p>{post['content']}</p>
        </div>"""
    return render(request, 'posts/index.html', {'posts': posts})

def post(request, id):
    valid_id = False
    for post in posts:
        if post['id'] == id:
            post_dict = post
            valid_id = True
            break
    if valid_id:
        return render(request, 'posts/post.html', {'post': post_dict})
    else:
        raise Http404(f"Post with id {id} not found.")


