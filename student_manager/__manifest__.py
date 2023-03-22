{
    'name': 'Student Management',
    'category': 'NEWTON/Apps',
    'version': '1.0',
    'depends': ['base','web','mail',],
    # gọi các hàm bên trong folder views
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/student_info.xml',
        'views/class_room.xml',
        'views/exam.xml',
        'views/menu.xml',
    ],
    'qweb': [
    ],
    'images':[
        'static/img/icon.png',
    ],
    "assets": {
        "web.assets_frontend": [
        ],
        'web.assets_backend': [
            'student_manager/static/src/css/student_info.css', # định nghĩa css cho view , css la gi ?
        ],
    },
    'installable': True,
    'auto_install': False, # tự động tải module
}
# hàm manifet dùng để định nghĩa các view hiển thị lên trên màn hình 