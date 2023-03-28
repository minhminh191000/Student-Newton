from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class Student(models.Model):
    _name = 'student_module.student' # ten bang hien thi trong db la student_module_student
    _description = 'Student Information'
    _inherit = ['mail.thread','mail.activity.mixin','avatar.mixin']

    # Student personal information
    name = fields.Char(string='Name')
    id_student = fields.Char(string='ID Student', required=True,unique=True)
    image = fields.Image(string='Avatar')
    image_url = fields.Char(compute='_compute_avatar_url')
    date_of_birth = fields.Date(string="Date of Birth")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string='Gender', required=True)
    # Guardian information
    guardian_name = fields.Char(string='Name of Guardian')
    guardian_phone = fields.Char(string='Phone of Guardian')
    guardian_email = fields.Char(string='Email of Guardian')
    guardian_relationship = fields.Selection([('parent', 'Parent'), ('sibling', 'Sibling'), ('relative', 'Relative')] , string='Guardian RelationShip', required=True)
    address = fields.Char(string='Home Address')
    # Student school information
    classroom_id = fields.Many2many('student_module.classroom', string='Class')
    exams = fields.One2many('student_module.exam', 'student_id', string='Exams')
    # Login Fields
    login = fields.Char(string='Login', readonly=True, copy=False)
    password = fields.Char(string='Password', readonly=True, copy=False)

    # Check if student id is unique
    _sql_constraints = [('id_student', 'unique(id_student)', 'This student id is already exist!!!')]
    
    # Check guardian phone valid
    @api.constrains('guardian_phone')
    def check_phonenumber(self):
        for rec in self:   
            if not re.match("^\\d{8,11}$", rec.guardian_phone):
                raise ValidationError("Enter valid 10 digits Mobile number")
        
    # Check guardian email valid
    @api.constrains('guardian_email')
    def _check_valid_email(self):
        for rec in self:
            if not re.match('(\w+[.|\w])*@(\w+[.])*\w+', rec.guardian_email):
                raise ValidationError("Wrong email format")
        
    # description = fields.(string='Description')
    @api.model
    def create(self, vals):
        # Generate a login based on the student's name
        login = vals.get('id_student').lower().replace(' ', '.')
        vals['login'] = login

        # Create the student record
        student = super().create(vals)

        # Create the user account
        user_vals = {
            'name': vals.get('name'),
            'login': login,
            'password': login,  # You can generate a more secure password here
            'email': vals.get('email'),
            # 'partner_id': student.partner_id.id,
        }
        try:
            self.env['res.users'].create(user_vals)
        except Exception as e:
            raise ValidationError("Error creating user account: %s" % str(e))

        return student