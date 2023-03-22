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
    class_location = fields.Many2one('res.partner', string='Class Location')
    documents = fields.Many2many('ir.attachment', string="Documents")
    # luu tru tai lieu cua lop


    # giai thich Many2many
    # 1 tai lieu co the co cho nhieu lop - 1 lop co the co nhieu tai lieu (nhieu - nhieu)

    @api.model
    def create(self, vals):
        # Tạo kênh mới trong discuss
        channel = self.env['mail.channel'].create({
            'name': vals['name'], # ten kenh = voi ten  vals['name'] = name cua class room
            'channel_partner_ids': [(4, self.env.user.partner_id.id)], # nhung nguoi duoc add vao kenh nay , no co day du cac quyeneeEE
            # 'public': 'private',
        })
        # tao moi 1 kenh bang cau lenh nay
        return super(Classroom, self).create(vals)