from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    # Core app
    # path('', include('core.urls')),

    # Users
    path('users/', include('users.urls')),

    # Shop app (ROOT URL)
    path('', include('shop.urls')),
    path('seller/', include('seller.urls')),

    path('account/', include('accounts.urls')),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)