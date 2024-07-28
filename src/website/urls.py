from django.urls import path
from .views import (
    HomeView, BlogDetailView, BlogListView, PrivacyView, TermsView,
    AboutView, PricingView,
    CallRequestAddView, FilingAddView, SubscriberAddView,

    # STRIPE
    stripe_config,
    create_checkout_session, CancelledView, SuccessView, FilingAddView40,
    FilingAddView280, create_checkout_session_280, create_checkout_session_40
)

app_name = 'website'
urlpatterns = [

    # WEBSITE AND BLOG INFORMATION ------------------------------------------------------------------------------------
    path('', HomeView.as_view(), name='home'),
    path('terms/', TermsView.as_view(), name='terms'),
    path('about/', AboutView.as_view(), name='about'),
    path('pricing/', PricingView.as_view(), name='pricing'),
    path('privacy/', PrivacyView.as_view(), name='privacy'),

    path('blog/', BlogListView.as_view(), name='blog'),
    path('blog/<slug:slug>/', BlogDetailView.as_view(), name='blog-detail'),

    # STRIPE LINKED FORMS ---------------------------------------------------------------------------------------------
    path('filing/add/', FilingAddView.as_view(), name='filing-add'),
    path('filing/add/40/', FilingAddView40.as_view(), name='filing-add-40'),
    path('filing/add/280/', FilingAddView280.as_view(), name='filing-add-280'),

    # SUBSCRIBER AND CALL BACKS ---------------------------------------------------------------------------------------
    path('subscriber/add/', SubscriberAddView.as_view(), name='subscriber-add'),
    path('call-request/add/', CallRequestAddView.as_view(), name='call-request-add'),

    # """ STRIPE VIEWS ------------------------------------------------------------------------------------------------
    path('config/', stripe_config, name='stripe-config'),

    path('create-checkout-session/<int:pk>/', create_checkout_session, name='create_checkout_session'),
    path('create-checkout-session-40/<int:pk>/', create_checkout_session_40, name='create_checkout_session_40'),
    path('create-checkout-session-280/<int:pk>/', create_checkout_session_280, name='create_checkout_session_280'),

    path('success/', SuccessView.as_view(), name='success'),
    path('cancelled/', CancelledView.as_view(), name='cancel'),
]
