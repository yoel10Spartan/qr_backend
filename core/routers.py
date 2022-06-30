from rest_framework.routers import SimpleRouter
from core.authentication.viewsets import (
    LoginViewSet, 
    RegistrationViewSet, 
    RefreshViewSet,
    RefreshDataViewSet
)
from core.events.viewsets import (
    EventViewSet
)
from .attendees.viewsets import (
    AttendeeGroupViewSet,
    LoungeViewSet,
    AttendeeViewSet,
)
from .operators.viewsets import (
    OperatorsViewSet
)

routes = SimpleRouter()

# AUTHENTICATION
routes.register(r'auth/login', LoginViewSet, basename='auth-login')
routes.register(r'auth/register', RegistrationViewSet, basename='auth-register')
routes.register(r'auth/refresh', RefreshViewSet, basename='auth-refresh')
routes.register(r'auth/refresh_data', RefreshDataViewSet, basename='auth-refresh-data')

# EVENTS
routes.register(r'events', EventViewSet, basename='events-controller')

# ATTENDEES
routes.register(r'attendees_group', AttendeeGroupViewSet, basename='attendee-group-controller')
routes.register(r'attendees', AttendeeViewSet, basename='attendee-controller')

# LOUNGE
routes.register(r'lounge', LoungeViewSet, basename='lounge-controller')

# OPERATORS
routes.register(r'operators', OperatorsViewSet, basename='operator-controller')

urlpatterns = [
    *routes.urls,
]