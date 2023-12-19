"""Zoom.us REST API Python Client -- Contact Center Component"""

from __future__ import absolute_import

from zoomus import util
from zoomus.components import base


class ContactCenterComponentV2(base.BaseComponent):
    
    def queues_list(self, **kwargs):
        return self.get_request("/contact_center/queues", params=kwargs)

    
    
    
    def queues_add(self, **kwargs):
        util.require_keys(kwargs, "queue_name", "queue_description")
        
        print("adding contact center")
        
        
        print(kwargs)
        
        return self.post_request("/contact_center/queues/", data=kwargs)
    
    
    
    
    
