from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re
# goi cac libary python


class Teacher(models.Model):
    _name = 'student_module.teacher'
    _description = 'Teacher Information'
    _inherit = ['mail.thread','mail.activity.mixin','avatar.mixin']

    name = fields.Char(string='Name')
    id_teacher = fields.Char(string='ID Teacher',unique=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender', required=True)
    date_of_birth = fields.Date(string='Date of Birth')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    image = fields.Image(string='Avatar')
    classroom_ids = fields.Many2many('student_module.classroom', string='Class Taught')
    subject_ids = fields.Many2many('student_module.subject', string='Teaching Subjects')
    address = fields.Char(string='Home Address')
    partner_id = fields.Many2one(comodel_name='res.partner', string='Related Partner', required=True,
                                 ondelete='cascade')
    user_id = fields.Many2one(comodel_name='res.userss', string='User id')

    # Login Fields
    login = fields.Char(string='Login', readonly=True, copy=False)
    password = fields.Char(string='Password', readonly=True, copy=False)
    
    
    # description = fields.(string='Description')
    @api.constrains('phone')
    def check_phonenumber(self):
        for rec in self:
            if not re.match("^\\d{8,11}$", rec.phone):
                raise ValidationError("Enter valid 10 digits Mobile number")

    # Check guardian email valid
    @api.constrains('email')
    def _check_valid_email(self):
        for rec in self:
            if not re.match('(\w+[.|\w])*@(\w+[.])*\w+', rec.email):
                raise ValidationError("Wrong email format")


    @api.model 
    def create(self, vals):
        # Generate a login based on the student's name

        partner = self.env['res.partner'].create({
            'name': vals.get('name'),
            'email': vals.get('email'),
            'phone': vals.get('phone'),
        })
        vals['partner_id'] = partner.id
        vals['id_teacher'] = 'TEACHER{0}'.format(partner.id)
        login = vals.get('id_teacher').lower().replace(' ', '.')
        vals['login'] = login
        # Create the student record
        student = super().create(vals)

        # Create the user account
        user_vals = {
            'name': vals.get('name'),
            'login': login,
            'password': login,  # You can generate a more secure password here
            'email': vals.get('email'),
            'partner_id': partner.id,
            # 'partner_id': student.partner_id.id,
        }
        try:
            user = self.env['res.users'].create(user_vals)
            student.write({'user_id': [(4, user.id)]})
            group = self.env.ref('student_manager.group_teacher_manager')
            user.write({'groups_id': [(4, group.id)]})
        except Exception as e:
            raise ValidationError("Error creating user account: %s" % str(e))

        return student
