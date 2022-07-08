# -*- coding: utf-8 -*-

from odoo import models, fields, api


class transportation_tracking(models.Model):
    _name = 'transportation.tracking'
    _description = 'transportation.tracking'

    name = fields.Char()
    # lot_number = fields.Char()