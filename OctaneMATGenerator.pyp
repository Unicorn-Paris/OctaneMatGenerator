"""
OctaneMATGenerator.

Given a chosen path/folder, attempts to compose an Octane material
using found files (uses file names to compose material like the user would manually do).

First, user sets the path to the directory containing the files.
Then files are loaded and user can optionally fine-tune some presets,
or choose between several files of the same type.
Finally, user submits the setup to automatically compose an Octane material
in her current C4D document.
"""


import os
import sys

"""Add plugin to the python search path."""
folder = os.path.dirname(__file__)
if folder not in sys.path:
    sys.path.insert(0, folder)

import c4d
from unicorn_paris.plugin import ids, shaders


class OptionsDialog(c4d.gui.GeDialog):

    def CreateLayout(self):
        self.SetTitle(ids.PLUGIN_NAME_STR)
        self._create_path_field()
        self._create_command_buttons()

        self.files_in_dir = None
        self.filepath = None
        return True

    def Command(self, id, msg):
        if id == BTN_CANCEL:
            self.Close()

        # When "files" dialog is used, display in the textfield the content it yields.
        # If it doesn't yield any, ensure the resulting value is set to empty string
        # (it display the string "None" otherwise).
        if id == BTN_SEARCH_FILE:
            self.filepath = (
                c4d.storage.LoadDialog(flags=c4d.FILESELECT_DIRECTORY) and
                c4d.storage.LoadDialog(flags=c4d.FILESELECT_DIRECTORY) or ''
            )
            self.SetString(FOLDER_PATH, self.filepath)

        if id == BTN_READ_FILES:
            s = shaders.OctaneShader()

            # Update filepath using value set in the textfield, in case it was
            # set manually by user and not using the "files" dialog.
            if self.filepath is None:
                self.filepath = self.GetString(FOLDER_PATH)

            self.files_in_dir = os.listdir(self.filepath)

            if len(self.files_in_dir) > 0:
                for f in self.files_in_dir:
                    if f.lower() in ['diffuse', 'color', 'col', 'albedo', 'alb']:
                        s.diffuse = os.path.join(self.filepath, f)
                    if f.lower() in ['specular', 'gloss']:
                        s.specular = os.path.join(self.filepath, f)
                    if f.lower() in ['roughness']:
                        s.roughness = os.path.join(self.filepath, f)
                    if f.lower() in ['normal']:
                        s.normal = os.path.join(self.filepath, f)
                    if f.lower() in ['bump']:
                        s.bump = os.path.join(self.filepath, f)
                    if f.lower() in ['opacity', 'alpha']:
                        s.opacity = os.path.join(self.filepath, f)
                    if f.lower() in ['displacement', 'disp', 'depth']:
                        s.displacement = os.path.join(self.filepath, f)

                s.generate()
                c4d.EventAdd()

                self.Close()
            else:
                print "Error while composing material..."

    def _create_path_field(self):
        self.GroupBegin(GRP_SEARCHFILE, c4d.BFH_CENTER, CNF_COLS, CNF_ROWS)
        self.AddStaticText(LBL_FOLDER, c4d.BFH_LEFT, name='Folder path')
        self.AddStaticText(FOLDER_PATH, c4D.BFH_SCALEFIT)
        self.AddButton(BTN_SEARCH_FILE, c4d.BFH_RIGHT, name='...')
        self.GroupEnd()

    def _create_command_buttons(self):
        self.GroupBegin(GRP_COMMANDS, c4d.BFH_CENTER, CNF_COLS, CNF_ROWS)
        self.AddButton(BTN_READ_FILES, c4d.BFH_LEFT, name='Read texture files')
        self.AddButton(BTN_CANCEL, c4d.BFH_RIGHT, name='Cancel')
        self.GroupEnd()


class CommandDataDialog(c4d.plugins.CommandData):

    dialog = None

    def Execute(self, doc):
        if self.dialog is None:
            self.dialog = OptionsDialog()
        return self.dialog.Open(dlgtype=c4d.DLG_TYPE_ASYNC, pluginid=ids.PLUGIN_ID, defaultw=400, defaulth=100)

    def RestoreLayout(self, sec_ref):
        if self.dialog is None:
            self.dialog = OptionsDialog()
        return self.dialog.Restore(pluginid=ids.PLUGIN_ID, secret=sec_ref)


if __name__=='__main__':
    icon = c4d.bitmaps.BaseBitmap()
    icon.InitWith(os.path.join(os.path.dirname(__file__), 'res', 'icon.tif'))
    c4d.plugins.RegisterCommandPlugin(
        info=0,
        icon=icon,
        id=ids.PLUGIN_ID,
        str=ids.PLUGIN_NAME_STR_LONG,
        help=ids.PLUGIN_NAME_STR_LONG,
        dat=CommandDataDialog()
    )
