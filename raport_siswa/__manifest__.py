# -*- coding: utf-8 -*-
###############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
{
    'name': 'Raport Siswa',
    'version': '14.0.1.0',
    'license': 'LGPL-3',
    'category': 'Education',
    "sequence": 1,
    'summary': 'Manage Raport Students',
    'complexity': "easy",
    'author': 'AFajar',
    'website': '',
    'depends': ['openeducat_core'],
    'data': [
        'security/ir.model.access.csv',
        'views/raport_siswa_sts.xml',
        'views/student_inherit_raport_view.xml',
        'data/ir_sequence_data.xml',
        'report/print_raport_siswa_sts.xml',
        'report/print_raport_siswa_sas.xml',
        'report/print_raport_siswa_sat.xml'
    ],
    'demo': [

    ],
    'css': [

    ],
    'qweb': [

    ],
    'images': [

    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    #'post_init_hook': '_openeducat_post_init',
}
###############################################################################

