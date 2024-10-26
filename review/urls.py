from django.urls import path
from review.views import show_reviews, add_review_ajax, edit_review_ajax, delete_review, get_rating, show_json, show_xml, show_json_by_id, show_xml_by_id

app_name = 'review'

urlpatterns = [
    path('reviews/<slug:slug>/', show_reviews, name='show_reviews'),
    path('add-review-ajax/<slug:slug>/', add_review_ajax, name='add_review_ajax'),
    path('edit-review-ajax/<slug:slug>/', edit_review_ajax, name='edit_review_ajax'),
    path('delete/<slug:slug>/', delete_review, name='delete_review'),
    path('rating/<slug:slug>/', get_rating, name='get_rating'),
    path('xml/<slug:slug>/', show_xml, name='show_xml'),
    path('json/<slug:slug>/', show_json, name='show_json'),
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
]