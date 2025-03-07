# -*- coding: utf-8 -*-
import re
from xml.dom import ValidationErr
from odoo import models, fields, api

class Proveedor(models.Model):
    _name = 'mjiq_taller.proveedor'
    _description = 'Proveedor'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # Agregar chatter

    name = fields.Char(string='Nombre del Proveedor', required=True, tracking=True)
    identificacion = fields.Char(string='Identificación', required=True, tracking=True)
    telefono = fields.Char(string='Teléfono', tracking=True)
    email = fields.Char(string='Correo Electrónico', tracking=True)
    direccion = fields.Text(string='Dirección', tracking=True)
    productos_ids = fields.One2many('mjiq_taller.repuestos', 'proveedor_id', string='Productos Suministrados', tracking=True)
    estado = fields.Selection([
        ('0', 'Activo'),
        ('1', 'Inactivo')
    ], string='Estado', tracking=True)
    factura_ids = fields.Many2many('mjiq_taller.factura', 'proveedor_factura_rel', 'proveedor_id', 'factura_id', string='Facturas', tracking=True)

    _sql_constraints = [
    ('unique_identificacion', 'UNIQUE(identificacion)', 'La identificación del proveedor debe ser única.'),
    ('unique_email', 'UNIQUE(email)', 'El correo electrónico ya está registrado en otro proveedor.')
    ]
    
    @api.constrains('telefono')
    def _check_telefono(self):
        """Valida que el teléfono contenga solo números y tenga al menos 8 dígitos"""
        phone_regex = r'^\d{8,}$'
        for record in self:
            if record.telefono and not re.match(phone_regex, record.telefono):
                raise ValidationErr("El teléfono debe contener solo números y tener al menos 8 dígitos.")