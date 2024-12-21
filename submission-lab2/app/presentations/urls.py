from django.urls import path
from . import views

from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include
from django.urls import reverse


urlpatterns = [
    # Authentication Views
    path('auth-confirm-mail/', views.auth_confirm_mail, name='auth-confirm-mail'),
    path('auth-lock-screen/', views.auth_lock_screen, name='auth-lock-screen'),
    path('auth-login/', views.auth_login, name='auth-login'),
    path('auth-logout/', views.auth_logout, name='auth-logout'),
    path('auth-recoverpw/', views.auth_recoverpw, name='auth-recoverpw'),
    path('auth-register/', views.auth_register, name='auth-register'),
    path('email-verification/', views.email_verification, name='email-verification'),
    path('auth-recoverypwd-mail/', views.auth_recoverypwd_mail, name='auth-recoverypwd-mail'),
    path('reset-password/', views.reset_password, name='reset-password'),
    path('change-password/', views.change_password, name='change-password'),

    # Charts Views
    path('charts-area/', views.charts_area, name='charts-area'),
    path('charts-bar/', views.charts_bar, name='charts-bar'),
    path('charts-boxplot/', views.charts_boxplot, name='charts-boxplot'),
    path('charts-bubble/', views.charts_bubble, name='charts-bubble'),
    path('charts-candlestick/', views.charts_candlestick, name='charts-candlestick'),
    path('charts-column/', views.charts_column, name='charts-column'),
    path('charts-flot/', views.charts_flot, name='charts-flot'),
    path('charts-funnel/', views.charts_funnel, name='charts-funnel'),
    path('charts-heatmap/', views.charts_heatmap, name='charts-heatmap'),
    path('charts-line/', views.charts_line, name='charts-line'),
    path('charts-mixed/', views.charts_mixed, name='charts-mixed'),
    path('charts-morris/', views.charts_morris, name='charts-morris'),
    path('charts-pie/', views.charts_pie, name='charts-pie'),
    path('charts-polararea/', views.charts_polararea, name='charts-polararea'),
    path('charts-radar/', views.charts_radar, name='charts-radar'),
    path('charts-radialbar/', views.charts_radialbar, name='charts-radialbar'),
    path('charts-rangearea/', views.charts_rangearea, name='charts-rangearea'),
    path('charts-scatter/', views.charts_scatter, name='charts-scatter'),
    path('charts-sparklines/', views.charts_sparklines, name='charts-sparklines'),
    path('charts-timeline/', views.charts_timeline, name='charts-timeline'),
    path('charts-treemap/', views.charts_treemap, name='charts-treemap'),

    # Error Pages
    path('error-404/', views.error_404, name='error-404'),
    path('error-429/', views.error_429, name='error-429'),
    path('error-500/', views.error_500, name='error-500'),
    path('error-503/', views.error_503, name='error-503'),

    # Extended UI Views
    path('extended-carousel/', views.extended_carousel, name='extended-carousel'),
    path('extended-notifications/', views.extended_notifications, name='extended-notifications'),
    path('extended-offcanvas/', views.extended_offcanvas, name='extended-offcanvas'),
    path('extended-range-slider/', views.extended_range_slider, name='extended-range-slider'),
    path('extended-scrollbar/', views.extended_scrollbar, name='extended-scrollbar'),
    path('extended-scrollspy/', views.extended_scrollspy, name='extended-scrollspy'),

    # Forms Views
    path('forms-advanced/', views.forms_advanced, name='forms-advanced'),
    path('forms-elements/', views.forms_elements, name='forms-elements'),
    path('forms-pickers/', views.forms_pickers, name='forms-pickers'),
    path('forms-quilljs/', views.forms_quilljs, name='forms-quilljs'),
    path('forms-validation/', views.forms_validation, name='forms-validation'),

    # Icons Views
    path('icons-feather/', views.icons_feather, name='icons-feather'),
    path('icons-mdi/', views.icons_mdi, name='icons-mdi'),

    # Index Views
    path('index-sidebar-light-rtl/', views.index_sidebar_light_rtl, name='index-sidebar-light-rtl'),
    path('index-sidebar-light/', views.index_sidebar_light, name='index-sidebar-light'),
    path('index-sidebar-rtl/', views.index_sidebar_rtl, name='index-sidebar-rtl'),
    path('', views.index, name='index'),
    path('landing/', views.landing, name='landing'),
    path('offline-page/', views.offline_page, name='offline-page'),

    # Pages Views
    path('pages-coming-soon/', views.pages_coming_soon, name='pages-coming-soon'),
    path('pages-faqs/', views.pages_faqs, name='pages-faqs'),
    path('pages-gallery/', views.pages_gallery, name='pages-gallery'),
    path('pages-invoice/', views.pages_invoice, name='pages-invoice'),
    path('pages-maintenance/', views.pages_maintenance, name='pages-maintenance'),
    path('pages-pricing/', views.pages_pricing, name='pages-pricing'),
    path('pages-profile/', views.pages_profile, name='pages-profile'),
    path('pages-starter/', views.pages_starter, name='pages-starter'),
    path('pages-timeline/', views.pages_timeline, name='pages-timeline'),

    # Tables Views
    path('tables-basic/', views.tables_basic, name='tables-basic'),
    path('tables-datatables/', views.tables_datatables, name='tables-datatables'),

    # UI Component Views
    path('ui-accordions/', views.ui_accordions, name='ui-accordions'),
    path('ui-alerts/', views.ui_alerts, name='ui-alerts'),
    path('ui-badges/', views.ui_badges, name='ui-badges'),
    path('ui-breadcrumb/', views.ui_breadcrumb, name='ui-breadcrumb'),
    path('ui-buttons/', views.ui_buttons, name='ui-buttons'),
    path('ui-cards/', views.ui_cards, name='ui-cards'),
    path('ui-carousel/', views.ui_carousel, name='ui-carousel'),
    path('ui-collapse/', views.ui_collapse, name='ui-collapse'),
    path('ui-dropdowns/', views.ui_dropdowns, name='ui-dropdowns'),
    path('ui-general/', views.ui_general, name='ui-general'),
    path('ui-grid/', views.ui_grid, name='ui-grid'),
    path('ui-images/', views.ui_images, name='ui-images'),
    path('ui-list/', views.ui_list, name='ui-list'),
    path('ui-modals/', views.ui_modals, name='ui-modals'),
    path('ui-offcanvas/', views.ui_offcanvas, name='ui-offcanvas'),
    path('ui-pagination/', views.ui_pagination, name='ui-pagination'),
    path('ui-placeholders/', views.ui_placeholders, name='ui-placeholders'),
    path('ui-popovers/', views.ui_popovers, name='ui-popovers'),
    path('ui-progress/', views.ui_progress, name='ui-progress'),
    path('ui-scrollspy/', views.ui_scrollspy, name='ui-scrollspy'),
    path('ui-spinners/', views.ui_spinners, name='ui-spinners'),
    path('ui-tabs/', views.ui_tabs, name='ui-tabs'),
    path('ui-tooltips/', views.ui_tooltips, name='ui-tooltips'),
    path('ui-typography/', views.ui_typography, name='ui-typography'),
    path('ui-video/', views.ui_video, name='ui-video'),

    # Widgets
    path('widgets/', views.widgets, name='widgets'),
]