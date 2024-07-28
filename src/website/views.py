import stripe
from django.contrib import messages
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, ListView, DetailView

from cocognite import settings
from src.portals.admins.forms import FilingForm, CallRequestForm, SubscriberForm
from src.portals.admins.models import Blog, BlogTag, BlogCategory, Subscriber, Filing


def handler404(request, exception, template_name='404.html'):
    return render(request, template_name)


class HomeView(TemplateView):
    template_name = 'website/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['filing_form'] = FilingForm()
        context['call_request_form'] = CallRequestForm()
        return context


class BlogListView(ListView):
    queryset = Blog.objects.filter(is_active=True)
    template_name = 'website/blog.html'
    paginate_by = 15

    def get_queryset(self):
        search = self.request.GET.get('search')
        category = self.request.GET.get('category')
        tag = self.request.GET.get('tag')

        if search:
            return self.queryset.filter(title__contains=search)
        elif category:
            return self.queryset.filter(blog_category__name=category)
        elif tag:
            return self.queryset.filter(tags__name=tag)
        else:
            return self.queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BlogListView, self).get_context_data(**kwargs)
        context['blog_categories'] = BlogCategory.objects.all()
        context['blog_tags'] = BlogTag.objects.all()
        context['blog_recents'] = Blog.objects.filter(is_active=True).order_by('created_on')[:5]
        return context


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'website/blog_detail.html'

    def get_context_data(self, **kwargs):
        context = super(BlogDetailView, self).get_context_data(**kwargs)
        context['blog_categories'] = BlogCategory.objects.all()
        context['blog_tags'] = BlogTag.objects.all()
        context['blog_recents'] = Blog.objects.filter(is_active=True).exclude(slug=self.object.slug).order_by(
            'created_on')[:5]
        return context


class AboutView(TemplateView):
    template_name = 'website/about.html'

    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        context['call_request_form'] = CallRequestForm()
        return context


class PricingView(TemplateView):
    template_name = 'website/pricing.html'

    def get_context_data(self, **kwargs):
        context = super(PricingView, self).get_context_data(**kwargs)
        context['filing_form'] = FilingForm()
        return context


class TermsView(TemplateView):
    template_name = 'website/terms.html'


class PrivacyView(TemplateView):
    template_name = 'website/privacy.html'


class FilingAddView(View):

    def post(self, request):

        form = FilingForm(data=request.POST)
        if form.is_valid():
            filing = form.save()
            return redirect('website:create_checkout_session', filing.pk)
        return redirect('website:home')


class FilingAddView280(View):

    def post(self, request):

        form = FilingForm(data=request.POST)
        if form.is_valid():
            filing = form.save()
            return redirect('website:create_checkout_session_280', filing.pk)
        return redirect('website:home')


class FilingAddView40(View):

    def post(self, request):

        form = FilingForm(data=request.POST)
        if form.is_valid():
            filing = form.save()
            return redirect('website:create_checkout_session_40', filing.pk)
        return redirect('website:home')


class CallRequestAddView(View):

    def post(self, request):
        form = CallRequestForm(data=request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'website/callback_success.html')
        return redirect('website:home')


@method_decorator(csrf_exempt, name='dispatch')
class SubscriberAddView(View):

    def post(self, request):
        form = SubscriberForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Requested successfully, we will contact within 24 hours")
        return redirect('website:home')


""" STRIPE REQUESTS"""


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request, pk):
    filing = get_object_or_404(Filing, pk=pk)
    domain_url = settings.DOMAIN_URL
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.create(
        line_items=[{
            'name': 'Sole Traders',
            'quantity': 1,
            'currency': 'gbp',
            'amount': 9000,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(
            reverse('website:success')
        ) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse('website:cancel')),
    )
    filing.stripe_payment_intent = session.id
    filing.save()

    return redirect(session.url, code=303)


@csrf_exempt
def create_checkout_session_280(request, pk):
    filing = get_object_or_404(Filing, pk=pk)
    domain_url = settings.DOMAIN_URL
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.create(
        line_items=[{
            'name': 'Limited Companies',
            'quantity': 1,
            'currency': 'gbp',
            'amount': 28000,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(
            reverse('website:success')
        ) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse('website:cancel')),
    )
    filing.stripe_payment_intent = session.id
    filing.save()

    return redirect(session.url, code=303)


@csrf_exempt
def create_checkout_session_40(request, pk):
    domain_url = settings.DOMAIN_URL
    filing = get_object_or_404(Filing, pk=pk)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.create(
        line_items=[{
            'name': 'Dormant Accounts',
            'quantity': 1,
            'currency': 'gbp',
            'amount': 3500,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(
            reverse('website:success')
        ) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse('website:cancel')),
    )
    filing.stripe_payment_intent = session.id
    filing.save()

    return redirect(session.url, code=303)


@csrf_exempt
def create_checkout_session2(request):
    if request.method == 'GET':
        domain_url = settings.DOMAIN_URL
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - lets capture the payment later
            # [customer_email] - lets you prefill the email input in the form
            # For full details see https:#stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param

            # If we want to identify the user when using webhooks we can pass client_reference_id  to checkout
            # session constructor. We will then be able to fetch it and make changes to our Django models.
            #
            # If we offer a SaaS service it would also be good to allow only authenticated users to purchase
            # anything on our site.

            checkout_session = stripe.checkout.Session.create(
                # client_reference_id=request.user.id if request.user.is_authenticated else None,
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'name': 'Vat - 176+',
                        'quantity': 1,
                        'currency': 'eur',
                        'amount': 17600,
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


class SuccessView(TemplateView):
    template_name = 'website/success.html'

    def get(self, request, *args, **kwargs):
        session_id = request.GET.get('session_id')
        if session_id is None:
            return HttpResponseNotFound()

        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.retrieve(session_id)

        filing = get_object_or_404(Filing, stripe_payment_intent=session_id)
        filing.is_paid = True
        filing.is_active = False
        filing.save()

        return render(request, self.template_name)


class CancelledView(TemplateView):
    template_name = 'website/cancelled.html'
