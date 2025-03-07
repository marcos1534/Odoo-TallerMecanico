# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Cita(models.Model):
    _name = 'mjiq_taller.cita'
    _description = 'Cita'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # Agregar chatter

    name = fields.Char(string='Referencia', required=True, tracking=True)
    cliente_id = fields.Many2one('mjiq_taller.cliente', string='Cliente', required=True, tracking=True)
    fecha_cita = fields.Datetime(string='Fecha de la Cita', required=True, tracking=True)
    servicio = fields.Char('Servicio', tracking=True)
    precio_total = fields.Float('Precio total', tracking=True)
    estado = fields.Selection([
        ('0', 'Pendiente'),
        ('1', 'Confirmada'),
        ('2', 'Cancelada'),
        ('3', 'Completada')
    ], string='Estado', tracking=True)
    descripcion = fields.Text(string='Descripción', tracking=True)

    @api.model
    # Obtener todos los registros
    def obtener_registros(self):
        registros = self.env['mjiq_taller.cita'].search([])
        return registros

    # Obtener un registro especifico por ID
    def registro_por_id(self):
        registro = self.env['mjiq_taller.cita'].browse(1)
        return registro

    # Obtener registros con condiciones
    def registros_filtro(self):
        registros_filtrados = self.env['mjiq_taller.cita'].search([('estado', '=', '1')])
        return registros_filtrados

    def actualizar_nombre(self, nuevo_nombre):
        self.write({'name': nuevo_nombre})

    # Cambiar la descripción según el estado
    def actualizar_descripcion(self, new_description):
        self.env['mjiq_taller.cita'].search([('estado', '=', '1')]).write({'descripcion': new_description})

    # Eliminar un registro por ID
    def eliminar_registro(self, id):
        registro2 = self.env['mjiq_taller.cita'].browse(id)
        if registro2:
            registro2.unlink()