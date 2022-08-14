from odoo import api,models, fields

# class ProductTemlate(models.Model):
#     _inherit = 'product.template'
#
#     case_barcode = fields.Char('Case Barcode')


class Product(models.Model):
    _inherit = 'product.product'

    website_image_url = fields.Char(
        string='Image URL',
        compute='_compute_website_image_url', compute_sudo=True,store=False)

    @api.model
    def get_all_products_by_barcode(self):
        products = self.env['product.product'].search_read(
            [('barcode', '!=', None), ('type', '!=', 'service')],
            ['barcode', 'display_name', 'uom_id', 'tracking']
        )
        packagings = self.env['product.packaging'].search_read(
            [('barcode', '!=', None), ('product_id', '!=', None)],
            ['barcode', 'product_id', 'qty']
        )
        # for each packaging, grab the corresponding product data
        to_add = []
        to_read = []
        products_by_id = {product['id']: product for product in products}
        for packaging in packagings:
            if products_by_id.get(packaging['product_id']):
                product = products_by_id[packaging['product_id']]
                to_add.append(dict(product, **{'qty': packaging['qty']}))
            # if the product doesn't have a barcode, you need to read it directly in the DB
            to_read.append((packaging, packaging['product_id'][0]))
        products_to_read = self.env['product.product'].browse(list(set(t[1] for t in to_read))).sudo().read(
            ['display_name', 'uom_id', 'tracking'])
        products_to_read = {product['id']: product for product in products_to_read}
        to_add.extend([dict(t[0], **products_to_read[t[1]]) for t in to_read])
        return {product.pop('barcode'): product for product in products + to_add}

    @api.depends('image_1920','image_512', 'image_256')
    def _compute_website_image_url(self):
        for prod in self:
            if prod.image_512:
                # image_512 is stored, image_256 is derived from it dynamically
                prod.website_image_url = self.env['website'].image_url(prod, 'image_512', size=256)
            elif prod.image_256:
                prod.website_image_url = self.env['website'].image_url(prod, 'image_256', size=256)
            elif prod.image_1920:
                prod.website_image_url = self.env['website'].image_url(prod, 'image_1920', size=256)
            else:
                prod.website_image_url = False

            print("image_url",prod.website_image_url)


