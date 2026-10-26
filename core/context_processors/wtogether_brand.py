from django.conf import settings


def wtogether_brand(request):
    return {
        "brand": {
            "platform_name": getattr(settings, "WTOGETHER_PLATFORM_NAME", "WTogether"),
            "platform_version": getattr(settings, "WTOGETHER_PLATFORM_VERSION", "2.0"),
            "product_name": getattr(settings, "WTOGETHER_PRODUCT_NAME", "Victoria"),
            "product_signature": getattr(settings, "WTOGETHER_PRODUCT_SIGNATURE", "Victoria by WTogether"),
            "product_slogan": getattr(settings, "WTOGETHER_PRODUCT_SLOGAN", "Connecting People, Building Communities"),
            "owner_name": getattr(settings, "WTOGETHER_OWNER_NAME", "WTogether"),
            "contact_email": getattr(settings, "WTOGETHER_CONTACT_EMAIL", "contacto@wtogether.org"),
        }
    }
