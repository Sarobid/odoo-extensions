from odoo import models, api, fields
from datetime import datetime
class picking_product_line(models.Model):
    _inherit = 'picking.product.line'
    
    @api.model
    def update_picking_return_mg_to_product_return(self,picking_product_line_id, picking_id):
        pProduct = self.env['picking.product.line'].search([
            ('id', '=', picking_product_line_id)
          ])
        if pProduct:
            pProduct.write({
                'picking_return_mg': picking_id
            })
            return {"status": "200", "message": "Picking product line updated successfully."}
        else:
            return {"status": "404", "message": "Picking product line not found."}