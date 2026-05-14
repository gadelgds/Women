from main.utils import menu  # Убедитесь, что список menu определен в utils.py

def get_fgm_context(request):
    return dict(mainmenu=menu)