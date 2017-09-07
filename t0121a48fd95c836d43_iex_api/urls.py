from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from t0121a48fd95c836d43_iex_api import views


urlpatterns = [
                  url(r'^admin/', admin.site.urls),
                  url(r'^$', view=views.index),
                  url(r'^add-algo/$', view=views.add_algo),
                  url(r'^algo-table/$', view=views.algo_table),
                  url(r'^algo-table/(?P<algo_name>.*)$', view=views.algo)
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
