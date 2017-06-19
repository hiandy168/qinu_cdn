from mongoengine import connect

from octopus.vendor_conf import VendorConfig

connect(host=VendorConfig.get_config('mongodb', 'host'),
        port=int(VendorConfig.get_config('mongodb', 'port')),
        db=VendorConfig.get_config('mongodb', 'db'))
