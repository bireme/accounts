from django.db.models import signals
from main.models import Network, CooperativeCenter, NetworkMembership

def append_memberships(sender, instance, created, **kwargs):
    if created:
        
        if instance.type == 'national' and instance.country:
            for cc in CooperativeCenter.objects.filter(country=instance.country):
                nm = NetworkMembership(network=instance, cooperative_center=cc)
                nm.save()
    
signals.post_save.connect(append_memberships, sender=Network, dispatch_uid="some.unique.string.id")