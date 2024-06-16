from .models import Category


def categories(request):
    """
    Context processor that adds the list of categories to the context.
    It filters the categories queryset to only include the top level categories.
    """
    
    return {
        'categories': Category.objects.filter(parent=None)
    }