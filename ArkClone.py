# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                A QGIS plugin
                A legend context menu option to clone vector layers
        Part of the Archaeological Recording Kit by L - P : Archaeology
                        http://ark.lparchaeology.com
                              -------------------
        begin                : 2016-03-22
        git sha              : $Format:%H$
        copyright            : (C) 2016, 2017 by L - P : Archaeology
        email                : ark@lparchaeology.com
        copyright            : (C) 2016, 2017 by John Layt
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

from PyQt4.QtCore import QFileInfo
from PyQt4.QtGui import QAction, QMenu, QInputDialog, QFileDialog

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
                                       menuGroup = Plugin.NoGroup,
                                       toolbarGroup = Plugin.NoGroup,
                                       checkable = True,
                                       parent = iface.mainWindow())
        # Set display / menu name now we have tr() set up
        self.setDisplayName(self.tr(u'&Clone Layer'))

    def initGui(self):
        self._cloneMemoryAllAction = self.addNewAction('', 'All features', callback=self._cloneMemoryAll,  parent=self)
        self._cloneMemorySelectedAction = self.addNewAction('', 'Selected features', callback=self._cloneMemorySelected, parent=self)
        self._cloneMemoryDefinitionAction = self.addNewAction('', 'Definition only', callback=self._cloneMemoryDefinition, parent=self)
        self._cloneShapefileAllAction = self.addNewAction('', 'All features', callback=self._cloneShapefileAll, parent=self)
        self._cloneShapefileSelectedAction = self.addNewAction('', 'Selected features', callback=self._cloneShapefileSelected, parent=self)
        self._cloneShapefileDefinitionAction = self.addNewAction('', 'Definition only', callback=self._cloneShapefileDefinition, parent=self)

        menu = QMenu(self.iface.mainWindow())
        memoryMenu = menu.addMenu(self.tr(u'As Memory Layer'))
        shapefileMenu = menu.addMenu(self.tr(u'As Shapefile'))
        memoryMenu.addAction(self._cloneMemoryAllAction)
        memoryMenu.addAction(self._cloneMemorySelectedAction)
        memoryMenu.addAction(self._cloneMemoryDefinitionAction)
        shapefileMenu.addAction(self._cloneShapefileAllAction)
        shapefileMenu.addAction(self._cloneShapefileSelectedAction)
        shapefileMenu.addAction(self._cloneShapefileDefinitionAction)

        self._cloneMenuAction = QAction(self.tr(u'&Clone Layer'), self)
        self._cloneMenuAction.setMenu(menu)

        self.iface.legendInterface().addLegendLayerAction(self._cloneMenuAction, '', 'arkclone', QgsMapLayer.VectorLayer, True)

    def unload(self):
        self.iface.legendInterface().removeLegendLayerAction(self._cloneMenuAction)

        # Removes the plugin menu item and icon from QGIS GUI.
        super(ArkClone, self).unload()

    def _cloneMemoryAll(self):
        self._clone(True, False, 'mem')

    def _cloneMemorySelected(self):
        self._clone(True, True, 'mem')

    def _cloneMemoryDefinition(self):
        self._clone(False, False, 'mem')

    def _cloneShapefileAll(self):
        self._clone(True, False, 'shp')

    def _cloneShapefileSelected(self):
        self._clone(True, True, 'shp')

    def _cloneShapefileDefinition(self):
        self._clone(False, False, 'shp')

    def _clone(self, copyData, copySelected, dest = 'mem'):
        layer = self.iface.mapCanvas().currentLayer()
        if not layers.isValid(layer):
            return
        new = None
        name = layer.name() + '_' + dest
        if dest == 'shp':
            path = QFileDialog.getSaveFileName(self.iface.mainWindow(), self.tr("Save File"), name, self.tr("Shapefiles (*.shp)"));
            if not path:
                return
            name = QFileInfo(path).baseName()
            if copyData:
                new = layers.duplicateAsShapefile(layer, path, name, copySelected)
            else:
                new = layers.cloneAsShapefileLayer(layer, path, name)
        else:
            name, ok = QInputDialog.getText(self.iface.mainWindow(), self.tr('Enter layer name'), self.tr('Enter layer name'), text=name)
            if not ok or not name:
                return
            if copyData:
                new = layers.duplicateAsMemoryLayer(layer, name, copySelected)
            else:
                new = layers.cloneAsMemoryLayer(layer, name)
        if new and new.isValid():
            layers.addLayerToLegend(self.iface, new)
