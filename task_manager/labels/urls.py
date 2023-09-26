from django.urls import path

from .views import LabelsCreateView, LabelsDeleteView, LabelsListView, LabelsUpdateView

urlpatterns = [
    path('', LabelsListView.as_view(), name="labels_list"),
    path('create/', LabelsCreateView.as_view(), name="create_label"),
    path('update/<int:pk>', LabelsUpdateView.as_view(), name="update_label"),
    path('delete/<int:pk>', LabelsDeleteView.as_view(), name="delete_label"),
]
