from django.urls import path
from db.views import views, ontology_views

urlpatterns = [
    # corpus
    path('api/corpus/get/', views.getCorpus),
    path('api/corpus/create/', views.createCorpus),
    path('api/corpus/update/', views.updateCorpus),
    path('api/corpus/delete/', views.deleteCorpus),

    # text
    path('api/text/get/', views.getText),
    path('api/text/create/', views.createText),
    path('api/text/update/', views.updateCorpus),
    path('api/text/delete/', views.deleteText),

    # Ontology
    path('api/ontology/get/', ontology_views.get_ontology),
    path('api/ontology/parents/', ontology_views.get_ontology_parent_classes),

    # Class
    path('api/class/get/', ontology_views.get_class),
    path('api/class/parents/', ontology_views.get_class_parents),
    path('api/class/children/', ontology_views.get_class_children),
    path('api/class/objects/', ontology_views.get_class_objects),
    path('api/class/create/', ontology_views.create_class),
    path('api/class/update/', ontology_views.update_class),
    path('api/class/delete/', ontology_views.delete_class),

    # Attributes
    path('api/class/attr/add/', ontology_views.add_class_attribute),
    path('api/class/attr/delete/', ontology_views.delete_class_attribute),
    path('api/class/obj_attr/add/', ontology_views.add_class_object_attribute),
    path('api/class/obj_attr/delete/', ontology_views.delete_class_object_attribute),
    path('api/class/parent/add/', ontology_views.add_class_parent),

    # Objects
    path('api/object/get/', ontology_views.get_object),
    path('api/object/create/', ontology_views.create_object),
    path('api/object/update/', ontology_views.update_object),
    path('api/object/delete/', ontology_views.delete_object),

    # Signatures
    path('api/class/signature/', ontology_views.collect_signature),
]
