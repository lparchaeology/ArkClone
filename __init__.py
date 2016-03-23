# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                    ArkClone
                                 A QGIS plugin
    A legend context menu option to clone vector layers as memory layers
       Part of the Archaeological Recording Kit by L - P : Archaeology
                        http://ark.lparchaeology.com
                              -------------------
        begin                : 2016-03-22
        git sha              : $Format:%H$
        copyright            : (C) 2016 by L - P : Archaeology
        email                : ark@lparchaeology.com
        copyright            : (C) 2016 by John Layt / L - P : Archaeology
        email                : j.layt@kde.org
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""

import os.path

# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load ArkClone class from file ArkClone.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .ArkClone import ArkClone
    return ArkClone(iface, os.path.dirname(__file__))
