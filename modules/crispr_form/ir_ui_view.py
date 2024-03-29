from odoo import models, api
from lxml import etree


class IrUiView(models.Model):

    _inherit = "ir.ui.view"

    def apply_view_form_arch_insert(self, arch):

        for insert_arch_tag in arch.xpath("//form-arch-insert"):
            view = self.env.ref(insert_arch_tag.get("view_ref"))
            view_arch = view.read_combined(["arch", "type"])["arch"]
            view_arch_tree = etree.fromstring(view_arch)

            parent_tag = insert_arch_tag.getparent()
            parent_tag.replace(insert_arch_tag, view_arch_tree)

        return arch

    @api.model
    def apply_view_inheritance(self, source, source_id, model, root_id=None):
        source = self.apply_view_form_arch_insert(source)
        return super(IrUiView, self).apply_view_inheritance(
            source, source_id, model, root_id
        )
