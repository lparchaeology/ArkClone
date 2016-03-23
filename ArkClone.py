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
"""

from PyQt4.QtGui import QAction, QMenu, QInputDialog

from qgis.core import QgsMapLayer

from .libarkqgis.plugin import Plugin
from .libarkqgis import layers

# Initialize Qt resources from file resources.py
import resources

class ArkClone(Plugin):
    """QGIS Plugin Implementation."""

    def __init__(self, iface, path):
        super(ArkClone, self).__init__(iface,
                                       pluginName = u'ArkClone',
                                       pluginIconPath = ':/images/themes/default/mActionCreateMemory.svg',
                                       pluginPath = path,
                                       menuGroup = Plugin.VectorGroup,
                                       toolbarGroup = Plugin.NoGroup,
                                       checkable = True,
                                       parent = iface.mainWindow())
        # Set display / menu name now we have tr() set up
        self.setDisplayName(self.tr(u'&Clone As Memory Layer'))

    def initGui(self):
        self._cloneAllAction = self.addNewAction('', 'All features', callback=self._cloneAll, parent=self)
        self._cloneSelectedAction = self.addNewAction('', 'Selected features', callback=self._cloneSelected, parent=self)
        self._cloneDefinitionAction = self.addNewAction('', 'Definition only', callback=self._cloneDefinition, parent=self)

        menu = QMenu(self.iface.mainWindow())
        menu.addAction(self._cloneAllAction)
        menu.addAction(self._cloneSelectedAction)
        menu.addAction(self._cloneDefinitionAction)
        self._cloneMenuAction = QAction(self.tr(u'&Clone As Memory Layer'), self)
        self._cloneMenuAction.setMenu(menu)

        self.iface.legendInterface().addLegendLayerAction(self._cloneMenuAction, '', 'arkclone', QgsMapLayer.VectorLayer, True)

    def unload(self):
        self.iface.legendInterface().removeLegendLayerAction(self._cloneMenuAction)

        # Removes the plugin menu item and icon from QGIS GUI.
        super(ArkClone, self).unload()

    def _cloneAll(self):
        self._clone(True, False)

    def _cloneSelected(self):
        self._clone(True, True)

    def _cloneDefinition(self):
        self._clone(False, False)

    def _clone(self, copyData, copySelected):
        layer = self.iface.mapCanvas().currentLayer()
        if not layers.isValid(layer):
            return
        name, ok = QInputDialog.getText(self.iface.mainWindow(), self.tr('Enter layer name'), self.tr('Enter memory layer name'), text=layer.name() + '_mem')
        if not ok or not name:
            return
        mem = None
        if copyData:
            mem = layers.duplicateAsMemoryLayer(layer, name, copySelected)
        else:
            mem = layers.cloneAsMemoryLayer(layer, name)
        if mem and mem.isValid():
            layers.addLayerToLegend(self.iface, mem)
