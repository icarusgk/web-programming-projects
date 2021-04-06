from .models import Category
from .models import *

global_categories_items = Category.objects.all()
all_categories_items = Category.objects.all()

global_categories = []
all_categories_list = []


for category in global_categories_items:
    global_categories.append(category.name)

for c in all_categories_items:
    all_categories_list.append(c)

def add_variable_to_context(request):
    return {
        'all_categories': all_categories_list
    }