# -*- coding: utf-8 -*-

from odoo import models, fields, api


class configurations_states(models.Model):
    _name = 'transportation.states'
    _description = 'transportation.states'

    name = fields.Char(string="State Name")
    active = fields.Boolean(string="Active", default=True)
    create_button = fields.Boolean(string='Button', default=False)
