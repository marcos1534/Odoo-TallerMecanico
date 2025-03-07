# -*- coding: utf-8 -*-

from xml.dom import ValidationErr
from odoo import models, fields, api

class Mecanico(models.Model):
    _name = 'mjiq_taller.mecanico'
    _description = 'Mecánico'
    
    name = fields.Char('Nombre del mecánico', required=True)
    edad = fields.Integer('Edad del mecánico')
    salario = fields.Float('Salario del mecánico')
    telefono = fields.Char('Teléfono')
    email = fields.Char('Correo Electrónico')
    fecha_contratacion = fields.Date('Fecha de contratación')
    experiencia = fields.Integer('Años de experiencia')
    activo = fields.Boolean('Activo', default=True)
    foto_mecanico = fields.Binary('Foto del mecánico', attachment=True)
    preview_image = fields.Binary(string="Imagen de Vista Previa")
    especialidad = fields.Selection([
        ('Becario', 'Becario'),
        ('Mecánica general', 'Mecánica general'),
        ('Electricidad automotriz', 'Electricidad automotriz'),
        ('Chapa y pintura', 'Chapa y pintura'),
        ('Transmisión y embrague', 'Transmisión y embrague'),
        ('Motores y sistemas de inyección', 'Motores y sistemas de inyección'),
        ('Aire acondicionado y climatización', 'Aire acondicionado y climatización')
    ], string='Especialidad')
    
    cargo = fields.Selection([
        ('Aprendiz', 'Aprendiz'),
        ('Mecánico Junior', 'Mecánico Junior'),
        ('Mecánico Senior', 'Mecánico Senior'),
        ('Jefe de Taller', 'Jefe de Taller'),
        ('Supervisor Técnico', 'Supervisor Técnico')
    ], string='Cargo')

    _sql_constraints = [
    ('check_salario_positive', 'CHECK(salario >= 0)', 'El salario no puede ser negativo.'),
    ('unique_email', 'UNIQUE(email)', 'El correo electrónico ya está registrado en otro mecánico.')
    ]

    @api.constrains('edad')
    def _check_edad(self):
        """Valida que el mecánico tenga al menos 18 años"""
        for record in self:
            if record.edad and record.edad < 18:
                raise ValidationErr("El mecánico debe tener al menos 18 años.")

    @api.constrains('experiencia')
    def _check_experiencia(self):
        """Valida que la experiencia no sea negativa"""
        for record in self:
            if record.experiencia is not None and record.experiencia < 0:
                raise ValidationErr("Los años de experiencia no pueden ser negativos.")
