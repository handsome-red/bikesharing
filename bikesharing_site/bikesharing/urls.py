from django.urls import path
from .views import (
    BikeHome,
    AddPage,
    ShowPost,
    BikeCategory,
    TagPostList,
    about,
    contact,
    login, UpdatePage
)

urlpatterns = [
    path('', BikeHome.as_view(), name='home'),
    path('about/', about, name='about'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('contact/', contact, name='contact'),
    path('login/', login, name='login'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', BikeCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', TagPostList.as_view(), name='tag'),
    path('editpage/<slug:slug>/', UpdatePage.as_view(), name='edit_page'),
]