# ARK Clone

A QGIS Plugin to clone existing vector layers as temporary memory layers.

This plugin adds an option to the legend context menu to clone the current layer. Users can choose to clone just the layer structure, just the selected features, or all the features.

ARK Clone is hosted on GitHub at https://github.com/lparchaeology/ArkClone.

ARK Clone was developed as part of ARK, the Archaeological Recording Kit, by L - P : Archaeology (http://ark.lparchaeology.com).

## Development

This plugin uses a library of common utilities shared between several QGIS plugins developed for ARK. This library is imported as a Git submodule and must be initialised.

1. Clone the ArkClone repository from GitHub: 'git clone https://github.com/lparchaeology/ArkClone.git'
2. Initialise the Git submodules: 'cd ArkClone && git submodule init && git submodule update'
