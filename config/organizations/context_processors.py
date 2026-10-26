from .models import Membership



def organization_context(request):
    if not request.user.is_authenticated:
        return {}

    membership = (
        Membership.objects
        .select_related("organization")
        .filter(user=request.user)
        .first()
    )

    if membership is None:
        return {}

    return {
        "current_organization": membership.organization,
        "current_membership": membership,
    }