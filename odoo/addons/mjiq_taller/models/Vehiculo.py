# -*- coding: utf-8 -*-

from datetime import date
from xml.dom import ValidationErr
from odoo import models, fields, api

class Vehiculo(models.Model):
    _name = 'mjiq_taller.vehiculo'
    _description = 'Vehiculo'

    name = fields.Char(string="Nombre del Vehículo", required=True)
    matricula = fields.Char('Matricula', required=True)
    marca = fields.Char('Marca', required=True)
    modelo = fields.Char('Modelo', required=True)
    descripcion = fields.Text('Descripción')
    anio = fields.Date('Año de fabricación del vehiculo')
    color = fields.Char('Color del vehiculo')
    kilometraje = fields.Integer('Kilometraje del vehiculo')
    cilindrada = fields.Integer('Cilindrada del vehiculo')
    foto_vehiculo = fields.Binary("Foto del Coche", attachment=True)
    propietario_id = fields.Many2one('mjiq_taller.cliente', string='Propietario')
    fecha_registro = fields.Datetime('Fecha de Registro')
    numeroPuertas = fields.Integer('Número de puertas')
    capacidad_pasajeros = fields.Integer('Capacidad de Pasajeros')
    test_vista_kanban_imagen = fields.Binary(string="Imagen de Kanban", widget="image")
    tipoCombustible = fields.Selection([
        ('0', 'Gasolina'),
        ('1', 'Diésel'),
        ('2', 'Eléctrico'),
        ('3', 'Híbrido')
    ], string='Tipo de Combustible')
    transmision = fields.Selection([
        ('0', 'Manual'),
        ('1', 'Automática')
    ], string='Transmisión')
    estado = fields.Selection([
        ('0', 'Nuevo'),
        ('1', 'Usado'),
        ('2', 'En Reparación')
    ], string='Estado', default='1')
    tipo_vehiculo = fields.Selection([
        ('Coche', 'Coche'),
        ('Motocicleta', 'Motocicleta'),
        ('Camión', 'Camión'),
        ('Furgoneta', 'Furgoneta'),
        ('Autobús', 'Autobús'),
        ('Grúa', 'Grúa'),
        ('Tractor', 'Tractor')
    ], string='Tipo de Vehículo')
    anio_formateado = fields.Char(string="Año Formateado", compute="_compute_anio_formateado")

    _sql_constraints = [
    ('unique_matricula', 'UNIQUE(matricula)', 'La matrícula debe ser única.'),
    ('check_kilometraje_positive', 'CHECK(kilometraje >= 0)', 'El kilometraje no puede ser negativo.'),
    ('check_numero_puertas', 'CHECK(numeroPuertas >= 0)', 'El número de puertas no puede ser negativo.'),
    ('check_capacidad_pasajeros', 'CHECK(capacidad_pasajeros >= 1)', 'El vehículo debe tener al menos un pasajero.')
    ]

    def _compute_anio_formateado(self):
        for record in self:
            if record.anio:
                record.anio_formateado = record.anio.strftime('%d/%m/%Y')
            else:
                record.anio_formateado = ''
    
    @api.constrains('matricula')
    def _check_matricula_unica(self):
        """Valida que la matrícula sea única"""
        for record in self:
            if self.search_count([('matricula', '=', record.matricula)]) > 1:
                raise ValidationErr("La matrícula debe ser única.")

    @api.constrains('kilometraje')
    def _check_kilometraje_no_negativo(self):
        """Valida que el kilometraje no sea negativo"""
        for record in self:
            if record.kilometraje < 0:
                raise ValidationErr("El kilometraje no puede ser negativo.")

    @api.constrains('numeroPuertas', 'capacidad_pasajeros')
    def _check_vehiculo_logico(self):
        """Valida que el número de puertas y pasajeros sea mayor a 0"""
        for record in self:
            if record.numeroPuertas is not None and record.numeroPuertas < 0:
                raise ValidationErr("El número de puertas no puede ser negativo.")
            if record.capacidad_pasajeros is not None and record.capacidad_pasajeros < 1:
                raise ValidationErr("El vehículo debe tener al menos 1 pasajero.")

    @api.constrains('anio')
    def _check_anio_fabricacion(self):
        """Valida que el año de fabricación no sea en el futuro"""
        for record in self:
            if record.anio and record.anio > date.today():
                raise ValidationErr("El año de fabricación no puede estar en el futuro.")