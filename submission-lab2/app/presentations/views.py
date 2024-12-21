from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from functools import wraps
from urllib.parse import urljoin
from django.utils import translation
from django.conf import settings

def get_user_context(request, profile_index=None):
    context = {}
    if request.user.is_authenticated:
        profiles = request.user.profiles.all()
        profiles = sorted(profiles, key=lambda x: x.is_primary, reverse=True)
        context.update({
            'user': request.user,
            'profiles': profiles,
            'profile_index': profile_index,
            'current_profile': profiles[profile_index] if profile_index is not None else profiles[0]
        })
    
    # Add language context
    context.update({
        'LANGUAGE_CODE': translation.get_language(),
        'LANGUAGES': settings.LANGUAGES,
    })
    return context

def with_context(view_func):
    """Decorator to automatically add user context to view"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        profile_index = kwargs.get('profile_index')
        context = get_user_context(request, profile_index)
        # Check if view accepts profile_index parameter
        if 'profile_index' in view_func.__code__.co_varnames:
            template_name = view_func(request, **kwargs)
        else:
            # Remove profile_index if the view doesn't expect it
            kwargs.pop('profile_index', None)
            template_name = view_func(request, *args, **kwargs)
        return render(request, template_name, context)
    return wrapper

def profile_index_required(view_func):
    """Decorator to ensure profile_index is present in URL"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # If profile_index is not in kwargs, redirect to default profile (0)
        print(kwargs)
        if 'profile_index' not in kwargs:
            # Get the current path without leading/trailing slashes
            current_path = request.path.strip('/')
            # Redirect to the same path under profile index 0
            return redirect(f'/0/{current_path}')
        return view_func(request, *args, **kwargs)
    return wrapper

# Authentication Views
def auth_login(request, profile_index=None):
    if request.user.is_authenticated:
        return redirect('/')
    context = get_user_context(request, profile_index)
    return render(request, 'pages/auth-login.html', context)

def auth_register(request, profile_index=None):
    if request.user.is_authenticated:
        return redirect('/')
    context = get_user_context(request, profile_index)
    return render(request, 'pages/auth-register.html', context)

def auth_recoverpw(request, profile_index=None):
    if request.user.is_authenticated:
        return redirect('/')
    context = get_user_context(request, profile_index)
    return render(request, 'pages/auth-recoverpw.html', context)

@profile_index_required
@with_context
def auth_recoverypwd_mail(request, profile_index=None):
    return 'pages/auth-recoverypwd-mail.html'

@with_context
def reset_password(request, profile_index=None):
    return 'pages/reset-password.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def auth_lock_screen(request, profile_index=None):
    return 'pages/auth-lock-screen.html'

def auth_confirm_mail(request, profile_index=None):
    if request.user.is_authenticated:
        return redirect('/')
    context = get_user_context(request, profile_index)
    return render(request, 'pages/auth-confirm-mail.html', context)

def email_verification(request, profile_index=None):
    if request.user.is_authenticated:
        return redirect('/')
    context = get_user_context(request, profile_index)
    return render(request, 'pages/email-verification.html', context)

def auth_logout(request, profile_index=None):
    logout(request)
    context = get_user_context(request, profile_index)
    return render(request, 'pages/auth-logout.html', context)

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def change_password(request, profile_index=None):
    return 'pages/change-password.html'

# Error Pages
@with_context
def error_404(request, profile_index=None):
    return 'pages/error-404.html'

@with_context
def error_500(request, profile_index=None):
    return 'pages/error-500.html'

@with_context
def error_503(request, profile_index=None):
    return 'pages/error-503.html'

@with_context
def error_429(request, profile_index=None):
    return 'pages/error-429.html'

@with_context
def offline_page(request, profile_index=None):
    return 'pages/offline-page.html'

# Utility Pages
@login_required(login_url='auth-login')
@profile_index_required
@with_context
def pages_starter(request, profile_index=None):
    return 'pages/pages-starter.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def pages_profile(request, profile_index=None):
    return 'pages/pages-profile.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def pages_pricing(request, profile_index=None):
    return 'pages/pages-pricing.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def pages_timeline(request, profile_index=None):
    return 'pages/pages-timeline.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def pages_invoice(request, profile_index=None):
    return 'pages/pages-invoice.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def pages_faqs(request, profile_index=None):
    return 'pages/pages-faqs.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def pages_gallery(request, profile_index=None):
    return 'pages/pages-gallery.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def pages_maintenance(request, profile_index=None):
    return 'pages/pages-maintenance.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def pages_coming_soon(request, profile_index=None):
    return 'pages/pages-coming-soon.html'

# UI Component Views
@login_required(login_url='auth-login')
@profile_index_required
@with_context
def ui_accordions(request, profile_index=None):
    return 'pages/ui-accordions.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def ui_alerts(request, profile_index=None):
    return 'pages/ui-alerts.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def ui_badges(request, profile_index=None):
    return 'pages/ui-badges.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def ui_breadcrumb(request, profile_index=None):
    return 'pages/ui-breadcrumb.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def ui_buttons(request, profile_index=None):
    return 'pages/ui-buttons.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def ui_cards(request, profile_index=None):
    return 'pages/ui-cards.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def ui_collapse(request, profile_index=None):
    return 'pages/ui-collapse.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def ui_dropdowns(request, profile_index=None):
    return 'pages/ui-dropdowns.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def ui_video(request, profile_index=None):
    return 'pages/ui-video.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def ui_grid(request, profile_index=None):
    return 'pages/ui-grid.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def ui_images(request, profile_index=None):
    return 'pages/ui-images.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def ui_list(request, profile_index=None):
    return 'pages/ui-list.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def ui_modals(request, profile_index=None):
    return 'pages/ui-modals.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def ui_placeholders(request, profile_index=None):
    return 'pages/ui-placeholders.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def ui_pagination(request, profile_index=None):
    return 'pages/ui-pagination.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def ui_popovers(request, profile_index=None):
    return 'pages/ui-popovers.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def ui_progress(request, profile_index=None):
    return 'pages/ui-progress.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def ui_scrollspy(request, profile_index=None):
    return 'pages/ui-scrollspy.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def ui_spinners(request, profile_index=None):
    return 'pages/ui-spinners.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def ui_tabs(request, profile_index=None):
    return 'pages/ui-tabs.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def ui_tooltips(request, profile_index=None):
    return 'pages/ui-tooltips.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def ui_typography(request, profile_index=None):
    return 'pages/ui-typography.html'

# Extended UI Views
@login_required(login_url='auth-login')
@profile_index_required
@with_context
def extended_carousel(request, profile_index=None):
    return 'pages/extended-carousel.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def extended_notifications(request, profile_index=None):
    return 'pages/extended-notifications.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def extended_offcanvas(request, profile_index=None):
    return 'pages/extended-offcanvas.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def extended_range_slider(request, profile_index=None):
    return 'pages/extended-range-slider.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def extended_scrollbar(request, profile_index=None):
    return 'pages/extended-scrollbar.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def extended_scrollspy(request, profile_index=None):
    return 'pages/extended-scrollspy.html'

# Icons Views
@login_required(login_url='auth-login')
@profile_index_required
@with_context
def icons_feather(request, profile_index=None):
    return 'pages/icons-feather.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def icons_mdi(request, profile_index=None):
    return 'pages/icons-mdi.html'

# Forms Views
@login_required(login_url='auth-login')
@profile_index_required
@with_context
def forms_elements(request, profile_index=None):
    return 'pages/forms-elements.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def forms_validation(request, profile_index=None):
    return 'pages/forms-validation.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def forms_quilljs(request, profile_index=None):
    return 'pages/forms-quilljs.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def forms_pickers(request, profile_index=None):
    return 'pages/forms-pickers.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def forms_advanced(request, profile_index=None):
    return 'pages/forms-advanced.html'

# Tables Views
@login_required(login_url='auth-login')
@profile_index_required
@with_context
def tables_basic(request, profile_index=None):
    return 'pages/tables-basic.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def tables_datatables(request, profile_index=None):
    return 'pages/tables-datatables.html'

# Charts Views
@login_required(login_url='auth-login')
@profile_index_required
@with_context
def charts_line(request, profile_index=None):
    return 'pages/charts-line.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def charts_area(request, profile_index=None):
    return 'pages/charts-area.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def charts_column(request, profile_index=None):
    return 'pages/charts-column.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def charts_bar(request, profile_index=None):
    return 'pages/charts-bar.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def charts_mixed(request, profile_index=None):
    return 'pages/charts-mixed.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def charts_timeline(request, profile_index=None):
    return 'pages/charts-timeline.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def charts_flot(request, profile_index=None):
    return 'pages/charts-flot.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def charts_morris(request, profile_index=None):
    return 'pages/charts-morris.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def charts_sparklines(request, profile_index=None):
    return 'pages/charts-sparklines.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def charts_rangearea(request, profile_index=None):
    return 'pages/charts-rangearea.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def charts_funnel(request, profile_index=None):
    return 'pages/charts-funnel.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def charts_candlestick(request, profile_index=None):
    return 'pages/charts-candlestick.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def charts_boxplot(request, profile_index=None):
    return 'pages/charts-boxplot.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def charts_bubble(request, profile_index=None):
    return 'pages/charts-bubble.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def charts_scatter(request, profile_index=None):
    return 'pages/charts-scatter.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def charts_heatmap(request, profile_index=None):
    return 'pages/charts-heatmap.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def charts_treemap(request, profile_index=None):
    return 'pages/charts-treemap.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def charts_pie(request, profile_index=None):
    return 'pages/charts-pie.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def charts_radialbar(request, profile_index=None):
    return 'pages/charts-radialbar.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def charts_radar(request, profile_index=None):
    return 'pages/charts-radar.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def charts_polararea(request, profile_index=None):
    return 'pages/charts-polararea.html'

# Widgets
@login_required(login_url='auth-login')
@profile_index_required
@with_context
def widgets(request, profile_index=None):
    return 'pages/widgets.html'

# UI Component Views
@login_required(login_url='auth-login')
@profile_index_required
@with_context
def ui_carousel(request, profile_index=None):
    return 'pages/ui-carousel.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def ui_general(request, profile_index=None):
    return 'pages/ui-general.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def ui_offcanvas(request, profile_index=None):
    return 'pages/ui-offcanvas.html'

# Index Views
@login_required(login_url='auth-login')
@profile_index_required
@with_context
def index_sidebar_light_rtl(request, profile_index=None):
    return 'pages/index-sidebar-light-rtl.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def index_sidebar_light(request, profile_index=None):
    return 'pages/index-sidebar-light.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def index_sidebar_rtl(request, profile_index=None):
    return 'pages/index-sidebar-rtl.html'

@login_required(login_url='auth-login')
@profile_index_required
@with_context
def index(request, profile_index=None):
    return 'pages/index.html'

@with_context
def landing(request):
    return 'pages/landing.html'