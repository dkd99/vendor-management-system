from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from User.api.views import vendor_registration_view,logout_view

urlpatterns = [
    path('register/', vendor_registration_view, name='register'),
    path('login/', obtain_auth_token, name='login'),
    path('logout/', logout_view, name='logout'),



    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]