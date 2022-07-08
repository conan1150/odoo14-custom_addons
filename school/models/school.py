from odoo import fields, models, api


class SchoolProfile(models.Model):
    _name = 'school.profile'

    name = fields.Char(string="School Name", copy=False)
    email = fields.Char(string="Email", copy=False)
    phone = fields.Char(string="Phone", copy=False)
    currency_id = fields.Many2one("res.currency", string="Currency")
    is_virtual_class = fields.Boolean(string="Virtual Class Support?")
    school_rank = fields.Integer(string="Rank")
    result = fields.Float(string="Result")
    school_addr = fields.Text(string="Address", copy=False)
    open_date = fields.Datetime("Open Date")
    estalish_date = fields.Date(string="Establish Date")
    school_type = fields.Selection([('public', 'Public School'),
                                    ('private', 'Private School')],
                                   string="Type of School")
    documents = fields.Binary(string="Document")
    document_name = fields.Char(string="File Name")
    school_image = fields.Image(string="Upload School Image",
                                max_width=100, max_height=100)
    school_description = fields.Html(string="Description")

    auto_rank = fields.Integer(compute="_auto_rank_populate",
                               string="Auto Rank", store=True)

    # functions
    @api.depends("school_type")
    def _auto_rank_populate(self):
        for rec in self:
            if rec.school_type == "private":
                rec.auto_rank = 50
            elif rec.school_type == "public":
                rec.auto_rank = 100
            else:
                rec.auto_rank = 0

    @api.model
    def create(self, vals):
        print("School Profile create vals", vals)

        return super(SchoolProfile, self).create(vals)

    def write(self, vals):
        print("School Profile write vals", vals)

        return super(SchoolProfile, self).write(vals)

    def specialCommand(self):

        student_obj = self.env['school.student']

        # First Way to create child model for existing model
        # stu_id = student_obj.create({"name": "Stu N2", "school_id": self.id})


        # Parent Model and Child Model
        # school_id = self.create({"name": "School S"})
        # student_obj.create({"name": "Stu S1", "school_id": school_id.id})
        # student_obj.create({"name": "Stu S2", "school_id": school_id.id})
        # student_obj.create({"name": "Stu S3", "school_id": school_id.id})
        # student_obj.create({"name": "Stu S4", "school_id": school_id.id})
        # student_obj.create({"name": "Stu S5", "school_id": school_id.id})


        # Using Special Command (0, 0, vals)
        self.create({"name": "School Special SS", "student_list": [(0, 0, {"name": "Stu Special SS One", "total_fees": 0}),
                                                                  (0, 0, {"name": "Stu Special SS Two", "total_fees": 0}),
                                                                  (0, 0, {"name": "Stu Special SS Three", "total_fees": 0})]})


    def specialCommand2(self):

        # for stud in self.student_list:
        #     stud.name = f"{stud.name} = {stud.id}"
        #     stud.total_fees = 3600
        #     stud.student_fees = 12000

        # vals = {'student_list': []}
        # for stud in self.student_list:
        #     vals['student_list'].append([1, stud.id, {'name': f'{stud.name} = {stud.id}',
        #                                               'student_fees': 18000,
        #                                               'total_fees': 4200}])
        # self.write(vals)

        for stud in self.student_list:
            stud.write({'name': f'{stud.name} = {stud.id}',
                        'student_fees': 32000,
                        'total_fees': 5000})

    def specialCommand3(self):
        self.write({'student_list': [(2, 71, 0), (2, 73, 0)]})

    def specialCommand4(self):
        self.write({'student_list': [(3, 63, 0), (3, 65, 0), (3, 67, 0)]})

    def specialCommand5(self):
        self.write({'student_list': [(4, 63, 0)]})

    def specialCommand6(self):
        self.write({'student_list': [(5, False, 0)]})





    #
    # @api.model
    # def name_search(self, name, args=None, operator='like', limit=100):
    #     args = args or []
    #
    #     if name:
    #         records = self.search(['|', '|', '|', ('name', operator, name),
    #                                ('email', operator, name),
    #                                ('phone', operator, name),
    #                                ('school_type', operator, name)])
    #
    #         return records.name_get()
    #     return super(SchoolProfile, self).name_search(name=name, args=args, operator=operator, limit=limit)

    # @api.model
    # def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
    #     args = args or []
    #     domain = []
    #     if name:
    #         domain = ['|', '|', '|', ('name', operator, name),
    #                   ('email', operator, name)]
    #
    #     school_ids = self.search(domain+args, limit=limit)
    #     return school_ids.name_get()

    # ORM Override name_get() method
    def name_get(self):
        student_list = []
        for school in self:
            name = school.name

            if school.school_type:
                name += f' ({school.school_type})'

            student_list.append((school.id, name))
        return student_list

    # ORM Override name_create() method
    # @api.model
    # def name_create(self, name):
    #     print('self :', self)
    #     print('School name :', name)
    #     rtn = self.create({'name': name})
    #     print('rtn :', rtn)
    #     print('rtn.name_get()[0] :', rtn.name_get()[0])
    #
    #     return rtn.name_get()[0]
