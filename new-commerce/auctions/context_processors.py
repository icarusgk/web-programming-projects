from .models import Category

global_categories_items = Category.objects.all()

global_categories = []

for category in global_categories_items:
    global_categories.append(category.name)

def add_variable_to_context(request):
    return {
       'global_categories': global_categories
    }