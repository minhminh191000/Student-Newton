from odoo import api, fields, models
#

class Classroom(models.Model): 
    _name = 'student_module.classroom'
    # khoi tao ten cua bang trong database
    _description = 'Classroom'
    # mo ta ve bang trong database
    _inherit = ['mail.thread','mail.activity.mixin','avatar.mixin']
    #ke thua lai bang trong database
    # li do ke thua tao ra cac truong 
    
    name = fields.Char(string='Class', required=True) # ten  cua lop hoc
    teacher = fields.Many2many('student_module.teacher', string='Teacher') # danh sach giao vien cua lop hoc 
    # lien ket nhieu du lieu giua 2 bang voi nhau
    id_classroom = fields.Char(string='ID Class', unique=True)
    students = fields.Many2many(comodel_name='student_module.student', string='Students')
    class_start_date = fields.Date(string='Class Start Date')
    class_end_date = fields.Date(string='Class End Date')
    class_schedule = fields.Char(string='Class Schedule')
    class_location_school = fields.Char(string='Class Location')
    documents = fields.Many2many('ir.attachment', string="Documents")

    message_channel_ids = fields.Many2one(comodel_name='mail.channel', string='Students')
    # luu tru tai lieu cua lop


    # giai thich Many2many
    # 1 tai lieu co the co cho nhieu lop - 1 lop co the co nhieu tai lieu (nhieu - nhieu)

    @api.model
    def create(self, vals):
        # Tạo kênh mới trong discuss
        channel = self.env['mail.channel'].create({
            'name': vals['name'],
            'channel_partner_ids': [(4, self.env.user.partner_id.id)],
        })
        vals['message_channel_ids'] = channel.id
        return super(Classroom, self).create(vals)

    def write(self, vals):
        res = super(Classroom, self).write(vals)
        if 'students' in vals:
            channel = self.message_channel_ids
            for student in vals['students'][0][2]:
                student_id = self.env['student_module.student'].browse(student)
                channel.write({'channel_partner_ids': [(4, student_id.partner_id.id)]})
        if 'teacher' in vals:
            channel = self.message_channel_ids
            for teacher in vals['teacher'][0][2]:
                teacher_id = self.env['student_module.teacher'].browse(teacher)
                channel.write({'channel_partner_ids': [(4, teacher_id.partner_id.id)]})
        return res