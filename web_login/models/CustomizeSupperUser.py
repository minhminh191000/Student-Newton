from odoo import models, api

class ResUsers(models.Model):
    _inherit = 'res.users'


    @api.model
    def _login(self, db, login, password):
        uid = super(ResUsers, self)._login(db, login, password)

        # Kiểm tra xem người dùng có cố gắng đăng nhập dưới tài khoản superuser hay không
        if uid == 1 and self.env['ir.config_parameter'].sudo().get_param('disable_superuser_login'):
            raise AccessDenied(_('Bạn không thể đăng nhập dưới tài khoản superuser.'))
        self.env['ir.config_parameter'].sudo().set_param('disable_superuser_login', True)
        return uid


