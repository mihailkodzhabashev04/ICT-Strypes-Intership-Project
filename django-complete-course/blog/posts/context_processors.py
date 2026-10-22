def categories(request):
    categories = [
    "Technology",
    "Programming",
    "Web Development"
    ]
    return {'categories': categories}