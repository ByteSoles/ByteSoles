from django.urls import path
from review.views import show_reviews, add_review_ajax, show_json, show_xml, show_json_by_id, show_xml_by_id

app_name = 'review'

urlpatterns = [
    path('reviews/<str:sneaker_name>/', show_reviews, name='show_reviews'),
    path('add-review-ajax/<str:sneaker_name>', add_review_ajax, name='add_review_ajax'),
    path('xml/<str:sneaker_name>/', show_xml, name='show_xml'),
    path('json/<str:sneaker_name>/', show_json, name='show_json'),
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
]