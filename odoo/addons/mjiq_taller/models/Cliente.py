# -*- coding: utf-8 -*-
import re
from xml.dom import ValidationErr
from odoo import models, fields, api

class Cliente(models.Model):
    _name = 'mjiq_taller.cliente'
    _description = 'Cliente'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # Agregar chatter

    name = fields.Char('Nombre del cliente', required=True, tracking=True)
    dni = fields.Char('DNI', required=True, tracking=True)
    telefono = fields.Char('Teléfono', tracking=True)
    correo = fields.Char('Correo Electrónico', tracking=True)
    direccion = fields.Text('Dirección', tracking=True)
    vehiculo_ids = fields.One2many('mjiq_taller.vehiculo', 'propietario_id', string='Vehículos', tracking=True)
    cita_ids = fields.One2many('mjiq_taller.cita', 'cliente_id', string='Citas', tracking=True)

    _sql_constraints = [
        ('unique_dni', 'UNIQUE(dni)', 'El DNI ya está registrado en el sistema.')
    ]

    @api.constrains('dni')
    def _check_dni_format(self):
        """Valida que el DNI tenga un formato correcto (Ejemplo: 12345678X en España)"""
        dni_regex = r'^\d{8}[A-Za-z]$'
        for record in self:
            if record.dni and not re.match(dni_regex, record.dni):
                raise ValidationErr("El DNI debe tener el formato correcto (8 números seguidos de una letra).")

    @api.constrains('correo')
    def _check_email_format(self):
        """Valida que el correo tenga un formato correcto"""
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        for record in self:
            if record.correo and not re.match(email_regex, record.correo):
                raise ValidationErr("El correo electrónico no tiene un formato válido.")