from django.urls import path

from . import views, views2
urlpatterns = [
    path('xwordelgame/', views.xwordelGame, name='gameUI'),
    path('xwordelgame/genGame/', views.genGame, name='gengame'),
    path('xwordelgame/getpercentage/', views.get_completed_percentage, name='getpercentage'),

    path('options/', views.options, name='options'),
    path('options/fileupload/', views.file_upload, name='fileupload'),

    path('endgame/', views2.end_game, name='empty_wordlist'),

    path('API/OCR/', views2.OCR_API, name='OCR_API'),
    path('API/Spacy/', views2.Spacy_API, name='Spacy_API'),
    

]
