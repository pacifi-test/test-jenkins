from uuid import UUID

import simplejson as json

ADMIN = "ADMIN"
SUPERADMIN = "SUPERADMIN"
ALMACEN = "ALMACEN"
COMPRA = "COMPRA"
VENTA = "VENTA"
DISTRIBUIDOR = "DISTRIBUIDOR"


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)
