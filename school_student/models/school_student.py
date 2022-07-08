# -*- coding: utf-8 -*-
import random

from odoo import models, fields, api, _, registry, tools
from odoo.exceptions import UserError

import datetime
from lxml import etree


class Address(models.Model):
    _name = 'address'
    _rec_name = 'street'

    street = fields.Char("Street")
    addr_number = fields.Char("No.")
    city = fields.Char("City")
    state = fields.Char("State")
    country = fields.Char("Country")
    zip_code = fields.Char("ZIP Code")


class school_student(models.Model):
    _name = 'school.student'
    _inherit = 'address'
    _description = 'school_student.school_student'
    _order = 'student_seq'
    _sql_constraints = [('unique_name', 'unique(name)', 'Please previde other student name')]

    roll_number = fields.Char("Roll Number")
    student_seq = fields.Integer("Student Seq")
    name = fields.Char(string="Student Name", required=True)
    school_id = fields.Many2one("school.profile", string="School",
                                # Single Multi domain working
                                # domain="[('school_type','=','public'),"
                                #        "('is_virtual_class','=','true')]"

                                # It won't be work due to wrong value.
                                # domain="[('school_type','=','public school')]"

                                # Left side sub fields you can access like this way.
                                # domain="[('currency_id.name', '=', 'EUR')]"
                                )
    hobby_list = fields.Many2many('hobby', 'school_hobby_rel',
                                  'student_id', 'hobby_id',
                                  string="Hobbies")  # 4 parameters are required.

    is_virtual_school = fields.Boolean(string="Is Virtual Class.",
                                       related="school_id.is_virtual_class",
                                       store=True)

    school_addr = fields.Text(string="School Address",
                              related="school_id.school_addr")

    currency_id = fields.Many2one("res.currency", string="Currency")
    student_fees = fields.Monetary(string="Student Fees")
    total_fees = fields.Float(string="Total Fees")

    ref_id = fields.Reference([('school.profile', 'School'),
                               ('account.move', 'Invoice')],
                              string="Reference Field")

    bdate = fields.Datetime("Birthday Date")
    student_age = fields.Integer("Student Age")

    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection([('draft', 'Draft'),
                              ('progress', 'Progress'),
                              ('paid', 'Paid'),
                              ('done', 'Done')], string="State")

    student_img = fields.Image("Student Image")

    @api.onchange("school_id")
    def _onchange_school_profile(self):
        currency_id = 0
        if self.school_id:
            currency_id = self.school_id.currency_id.id
        return {'domain': {'currency_id': [('id','=', currency_id)]}}


    # Open Wizard Function
    def open_wizard(self):
        # return {'type': 'ir.actions.act_window',
        #         'res_model': 'student.fees.update.wizard',
        #         'view_mode': 'form',
        #         'target': 'new'}

        return self.env['ir.actions.act_window']._for_xml_id("school_student.student_fees_update_wizard_action")

    # ORM Override field_view_get method
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):

        rtn = super(school_student, self).fields_view_get(view_id=view_id,
                                                          view_type=view_type,
                                                          toolbar=toolbar,
                                                          submenu=submenu)

        # if view_type == 'form':
        #     doc = etree.XML(rtn['arch'])
        #     new_field = doc.xpath('//field[@name="name"]')
        #     if new_field:
        #         new_field[0].addnext(etree.Element('label',
        #                                            {'string': 'view field get'}))
        #         rtn['arch'] = etree.tostring(doc, encoding='unicode')
        #
        # if view_type == 'tree':
        #     doc = etree.XML(rtn['arch'])
        #     new_column = doc.xpath('//field[@name="school_id"]')
        #     if new_column:
        #         new_column[0].addnext(etree.Element('field', {'string': 'Total Fees',
        #                                                       'name': 'total_fees'}))
        #         rtn['arch'] = etree.tostring(doc, encoding='unicode')

        return rtn

    def specialCommand7(self):
        ids = [12, 15, 26]
        self.write({'hobby_list': [(6, 0, ids)]})

    # Add New Custom Button
    def custom_button_method(self):

        cli = tools.config.options
        [print(i) for i in cli]
        print("DB Name :", cli.get('db_name'))
        print("DB Pass :", cli.get('db_password'))


    @api.model
    def _change_roll_number(self, add_str):
        """This action is used to add roll number to the student profile."""

        for stud in self.search([('roll_number','=',False)]):
            stud.roll_number = f'{add_str.upper()}{stud.id}'

        return True

    def buttonClickEvent(self):
        raise UserError(_("You click this button."))


        # print("Hello this is Custom Button called by you...")
        #
        # print("Env....", self.env)
        # print("UID....", self.env.uid)
        # print("User....", self.env.user.name)
        # print("Admin....", "YES" if self.env.su else "NO")
        # print("Company....", self.env.company.name)
        # print("Companies....", self.env.companies)
        # print("Lang....", self.env.lang)
        # print("Cr....", self.env.cr)
        #
        # new_cr = registry(self.env.cr.dbname).cursor()
        # print('New CR :', new_cr)
        #
        # partner_id = self.env['res.partner'].with_env(self.env(new_cr)).create({'name': 'Partner with_env new cr.2'})
        # partner_id.env.cr.commit()

        # self.total_fees = random.randint(1, 1000)

    # ORM Override default_get() method
    # @api.model
    # def default_get(self, field_list=[]):
    #     print("field list :", field_list)
    #     rtn = super(school_student, self).default_get(field_list)
    #     rtn['active'] = True
    #     rtn['name'] = 'Stu '
    #     print("return statement :", rtn)
    #
    #     return rtn

    # ORM Override unlink() method
    # def unlink(self):
    #     for s in self:
    #         if s.total_fees > 0:
    #             raise UserError(_(f"Can't delete this {s.name} statement profile."))
    #
    #     rtn = super(school_student, self).unlink()
    #     return rtn

    # ORM Override create() method
    # @api.model
    # def create(self, vals):
    #     rtn = super(school_student, self).create(vals)
    #     # rtn.active = True
    #
    #     return rtn

    # ORM Override write() method
    # def write(self, vals):
    #     rtn = super(school_student, self).write(vals)
    #
    #     if not self.hobby_list:
    #         raise UserError(_("Please select at least one hobby."))
    #
    #     return rtn

    # ORM Override copy() method
    # @api.returns('self', lambda value: value.id)
    # def copy(self, default={}):
    #     default['name'] = self.name + " (Copy)"
    #     rtn = super(school_student, self).copy(default=default)
    #     rtn.total_fees = 20000
    #     return rtn


class SchoolProfile(models.Model):
    _inherit = 'school.profile'

    student_list = fields.One2many('school.student', 'school_id',
                                   string="Student List")
    school_number = fields.Char("School Code")

    @api.model
    def create(self, vals):
        rtn = super(SchoolProfile, self).create(vals)
        # if not rtn.student_list:
        #     raise UserError(_("Student list is empty! "))

        return rtn


class StudentHobbies(models.Model):
    _name = 'hobby'

    name = fields.Char("Hobby")


class Partner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def create(self, vals):

        print("Env....", self.env)
        print("UID....", self.env.uid)
        print("User....", self.env.user.name)
        print("Admin....", "YES" if self.env.su else "NO")
        print("Company....", self.env.company.name)
        print("Companies....", self.env.companies)
        print("Context....", self.env.context)
        print("Cr....", self.env.cr)

        print("Partner values :", vals)

        if 'company_id' not in vals:
            vals['company_id'] = self.env.company.id

        return super(Partner, self).create(vals)


class Car(models.Model):
    _name = "car"

    name = fields.Char("Car")
    price = fields.Float("Cost")


class CarEngine(models.Model):
    _name = "car.engine"
    _inherits = {"car": "car_id"}    #{"<key_is_modelname>": "<values_is_filesnameofmany2one>"}

    name = fields.Char("Car Engine")
    car_id = fields.Many2one("car", string="Car")




