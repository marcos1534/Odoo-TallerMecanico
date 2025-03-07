# -*- coding: utf-8 -*-

from xml.dom import ValidationErr
from odoo.exceptions import UserError # type: ignore
from odoo import models, fields, api

class Factura(models.Model):
    _name = 'mjiq_taller.factura'
    _description = 'Factura'
    
    name = fields.Char(string='Número de Factura', required=True)
    cliente_id = fields.Many2one('mjiq_taller.cliente', string='Cliente', required=True)
    cita_id = fields.Many2one('mjiq_taller.cita', string='Cita Relacionada')
    proveedor_ids = fields.Many2many('mjiq_taller.proveedor', 'proveedor_factura_rel', 'factura_id', 'proveedor_id', string='Proveedor')
    fecha_emision = fields.Date(string='Fecha de Emisión', required=True)
    total = fields.Monetary(string='Total', compute="_compute_total", inverse="_inverse_total", required=True, currency_field='currency_id', store=True)
    currency_id = fields.Many2one('res.currency', string='Moneda', required=True)
    repuestos_ids = fields.Many2many('mjiq_taller.repuestos', string='Repuestos Utilizados')
    estado = fields.Selection([
        ('0', 'Borrador'),
        ('1', 'Confirmada'),
        ('2', 'Pagada'),
        ('3', 'Cancelada')
    ], string='Estado')

    company_id = fields.Many2one('res.company', string="Compañía", default=lambda self: self.env.company, required=True)

    _sql_constraints = [
        ('check_total_positive', 'CHECK(total >= 0)', 'El total de la factura no puede ser negativo.')
    ]

    @api.constrains('total')
    def _check_total(self):
        for record in self:
            if record.total < 0:
                raise ValidationErr("No se permiten facturas con total negativo.")
    
    dias_desde_emision = fields.Integer(string="Dias desde emisión", compute="_compute_dias_desde_emision", store=True)

    @api.depends('fecha_emision')
    def _compute_dias_desde_emision(self):
        for factura in self:
            if factura.fecha_emision:
                delta = fields.Date.today() - factura.fecha_emision
                factura.dias_desde_emision = delta.days
            else:
                factura.dias_desde_emision = 0
    
    cantidad_proveedores = fields.Integer(string="Número de Proveedores", compute="_compute_cantidad_proveedores", store=True)

    @api.depends('proveedor_ids')
    def _compute_cantidad_proveedores(self):
        for factura in self:
            factura.cantidad_proveedores = len(factura.proveedor_ids)
    
    
    @api.depends('cita_id')
    def _compute_total(self):
        for factura in self:
            factura.total = factura.cita_id.precio_total if factura.cita_id else 0.0

    def _inverse_total(self):
        for factura in self:
            if factura.total and factura.cita_id:
                factura.cita_id.precio_total = factura.total

    def action_imprimir_informe(self):
        if self.estado not in ['1', '2']:
            raise UserError("Solo se puede imprimir el informe si la factura esta confirmada o pagada.")
        return self.env.ref('mjiq_taller.factura_report_action').report_action(self)