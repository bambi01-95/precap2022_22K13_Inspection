from django.apps import AppConfig

# .admin/上の名前を変えるだけ
class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dashboard'

