{
    'name': 'Web Login',
    'category': 'NEWTON/Apps',
    'version': '1.0',
    'depends': ['base','web'],
    'data': [
        'views/login_layout.xml',
    ],
    'qweb': [
        'static/src/xml/login.xml',
        'web_login/static/src/css/web_login_style.css'
    ],
    "assets": {
        "web.assets_frontend": [
            "web_login/static/src/css/web_login_style.css"
        ],
    },
    'installable': True,
    'auto_install': False,
}