# -*- coding: utf-8 -*-

from xml.dom import ValidationErr
from odoo import models, fields, api

class Repuestos(models.Model):
    _name = 'mjiq_taller.repuestos'
    _description = 'Repuestos'
    
    name = fields.Char(string='Nombre del Repuesto', required=True)
    codigo = fields.Char(string='Código del Repuesto', required=True, unique=True)
    proveedor_id = fields.Many2one('mjiq_taller.proveedor', string='Proveedor')
    precio = fields.Float(string='Precio', required=True)
    cantidad_disponible = fields.Integer(string='Cantidad Disponible', default=0)
    descripcion = fields.Text(string='Descripción')
    importe_total = fields.Float(string="Importe total", compute="_importetotal", store=True)
    imagen_repuesto = fields.Binary(string="Foto Repuesto")
    factura_ids = fields.Many2many('mjiq_taller.factura', string='Facturas Asociadas')
    preview_image = fields.Binary(string="Imagen del mecanico que usa el repuesto")

    _sql_constraints = [
    ('unique_codigo', 'UNIQUE(codigo)', 'El código del repuesto debe ser único.'),
    ('check_precio_positive', 'CHECK(precio > 0)', 'El precio debe ser mayor a 0.')
    ]

    @api.constrains('cantidad_disponible')
    def _check_cantidad_no_negativa(self):
        """Valida que la cantidad disponible no sea negativa"""
        for record in self:
            if record.cantidad_disponible < 0:
                raise ValidationErr("La cantidad disponible no puede ser negativa.")
    
    @api.depends('precio', 'cantidad_disponible')
    def _importetotal(self):
        for r in self:
            r.importe_total = r.cantidad_disponible*r.precio

    def get_imagen_base64(self):
        return "data:image/jpeg;base64," + (self.imagen_repuesto.decode("utf-8") if self.imagen_repuesto else "")