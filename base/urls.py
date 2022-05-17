from django.urls import path
from .views import EventList, EventDetail, EventCreate, EventUpdate, DeleteView, CustomLoginView, RegisterPage, EventReorder
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),

    path('', EventList.as_view(), name='events'),
    path('event/<int:pk>/', EventDetail.as_view(), name='event'),
    path('event-create/', EventCreate.as_view(), name='event-create'),
    path('event-update/<int:pk>/', EventUpdate.as_view(), name='event-update'),
    path('event-delete/<int:pk>/', DeleteView.as_view(), name='event-delete'),
    path('event-reorder/', EventReorder.as_view(), name='event-reorder'),
]
