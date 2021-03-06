# Simple script for doing a Find/Replace over all selected object names.
 
import c4d
from c4d import bitmaps, gui, plugins, utils
import collections, os

### Dialoog test ###
# Add / remove GUI fields.
# Enable / disable GUI fields
#
PLUGIN_ID = 1041301 #TestID only!!!!!!!!!!!!
 
# Unique id numbers for each of the GUI elements
LBL_INFO1 = 1000
LBL_INFO2 = 1001
LBL_INFO3 = 1002
LBL_INFO4 = 1003
LBL_INFO5 = 1004
LBL_INFO6 = 1005
LBL_INFO7 = 1006
LBL_INFO8 = 1007
FOLDER_ADRESS = 10001
TXT_REPLACE = 10002
GROUP_OPTIONS = 20000
BTN_OK = 20001
BTN_CANCEL = 20002
BTN_COMA = 20003
DDM_MATTYPE = 20005
POPO = 20004


ID_OCTANE_DIFFUSE_MATERIAL = 1029501
ID_CREATE_GLOSSYMAT_PLUGIN = 1033893
ID_OCTANE_IMAGE_TEXTURE = 1029508
ID_OCTANE_DISPLACEMENT = 1031901
ID_OCTANE_TRANSFORM = 1030961
ID_OCTANE_PROJECTION = 1031460

def make_shader(diffuse, specular, roughness, normal, bump, opacity, displacement):
    doc = c4d.documents.GetActiveDocument()
    mat = c4d.BaseMaterial(ID_OCTANE_DIFFUSE_MATERIAL)

#DEFINE MATERIAL TYPE
    mat()[c4d.OCT_MATERIAL_TYPE]=2511
    
# TRANSFORM NODE
    TransN = c4d.BaseShader(ID_OCTANE_TRANSFORM)
    mat.InsertShader(TransN)
    
# PROJECTION NODE
    ProjN = c4d.BaseShader(ID_OCTANE_PROJECTION)
    mat.InsertShader(ProjN)
    
# DIFFUSE SETUP
    if diffuse :
        IT = c4d.BaseShader(ID_OCTANE_IMAGE_TEXTURE)
        mat.InsertShader(IT)
        mat[c4d.OCT_MATERIAL_DIFFUSE_LINK] = IT
        # DIFFUSE IMAGE NAMES = Albedo/Col/Color
        IT[c4d.IMAGETEXTURE_FILE] = diffuse
        IT[c4d.IMAGETEXTURE_MODE] = 0
        IT[c4d.IMAGETEXTURE_GAMMA] = 2.2
        IT[c4d.IMAGETEX_BORDER_MODE] = 0
        
        # TRANSFORM
        IT[c4d.IMAGETEXTURE_TRANSFORM_LINK] = TransN
        
        # TRANSFORM
        IT[c4d.IMAGETEXTURE_PROJECTION_LINK] = ProjN

# SPECULAR SETUP
    if specular :
        IT = c4d.BaseShader(ID_OCTANE_IMAGE_TEXTURE)
        mat.InsertShader(IT)
        mat[c4d.OCT_MATERIAL_SPECULAR_LINK] = IT
        # SPECULAR IMAGE NAMES = Specular/Gloss
        IT[c4d.IMAGETEXTURE_FILE] = specular
        IT[c4d.IMAGETEXTURE_MODE] = 1
        IT[c4d.IMAGETEXTURE_GAMMA] = 2.2
        IT[c4d.IMAGETEX_BORDER_MODE] = 0
        
        # TRANSFORM
        IT[c4d.IMAGETEXTURE_TRANSFORM_LINK] = TransN
        
        # TRANSFORM
        IT[c4d.IMAGETEXTURE_PROJECTION_LINK] = ProjN

# ROUGHNESS SETUP
    if roughness :
        IT = c4d.BaseShader(ID_OCTANE_IMAGE_TEXTURE)
        mat.InsertShader(IT)
        mat[c4d.OCT_MATERIAL_ROUGHNESS_LINK] = IT
        # ROUGHNESS IMAGE NAMES = Roughness/
        IT[c4d.IMAGETEXTURE_FILE] = roughness
        IT[c4d.IMAGETEXTURE_MODE] = 1
        IT[c4d.IMAGETEXTURE_GAMMA] = 2.2
        IT[c4d.IMAGETEX_BORDER_MODE] = 0
        
        # TRANSFORM
        IT[c4d.IMAGETEXTURE_TRANSFORM_LINK] = TransN
        
        # TRANSFORM
        IT[c4d.IMAGETEXTURE_PROJECTION_LINK] = ProjN
    
# NORMAL SETUP
    if normal:
        IT = c4d.BaseShader(ID_OCTANE_IMAGE_TEXTURE)
        mat.InsertShader(IT)
        mat[c4d.OCT_MATERIAL_NORMAL_LINK] = IT
        # NORMAL IMAGE NAMES = Normal/NRM
        IT[c4d.IMAGETEXTURE_FILE] = normal
        IT[c4d.IMAGETEXTURE_MODE] = 0
        IT[c4d.IMAGETEXTURE_GAMMA] = 2.2
        IT[c4d.IMAGETEX_BORDER_MODE] = 0
        
        # TRANSFORM
        IT[c4d.IMAGETEXTURE_TRANSFORM_LINK] = TransN
        
        # TRANSFORM
        IT[c4d.IMAGETEXTURE_PROJECTION_LINK] = ProjN
    else :
        if bump:
            IT = c4d.BaseShader(ID_OCTANE_IMAGE_TEXTURE)
            mat.InsertShader(IT)
            mat[c4d.OCT_MATERIAL_BUMP_LINK] = IT
            # NORMAL IMAGE NAMES = BUMP
            IT[c4d.IMAGETEXTURE_FILE] = bump
            IT[c4d.IMAGETEXTURE_MODE] = 1
            IT[c4d.IMAGETEXTURE_GAMMA] = 2.2
            IT[c4d.IMAGETEX_BORDER_MODE] = 0
            
            # TRANSFORM
            IT[c4d.IMAGETEXTURE_TRANSFORM_LINK] = TransN
            
            # TRANSFORM
            IT[c4d.IMAGETEXTURE_PROJECTION_LINK] = ProjN
            
            
            
            
    
# OPACITY SETUP
    if opacity:
        IT = c4d.BaseShader(ID_OCTANE_IMAGE_TEXTURE)
        mat.InsertShader(IT)
        mat[c4d.OCT_MATERIAL_OPACITY_LINK] = IT
        # OPACITY IMAGE NAMES = ALPHA/OPACITY/TRANSPARENCY
        IT[c4d.IMAGETEXTURE_FILE] = opacity
        IT[c4d.IMAGETEXTURE_MODE] = 1
        IT[c4d.IMAGETEXTURE_GAMMA] = 2.2
        IT[c4d.IMAGETEX_BORDER_MODE] = 0
        
        # TRANSFORM
        IT[c4d.IMAGETEXTURE_TRANSFORM_LINK] = TransN
        
        # TRANSFORM
        IT[c4d.IMAGETEXTURE_PROJECTION_LINK] = ProjN

# DISPLACEMENT SETUP
    if displacement:
        IT = c4d.BaseShader(ID_OCTANE_IMAGE_TEXTURE)
        mat.InsertShader(IT)
        DISP = c4d.BaseShader(ID_OCTANE_DISPLACEMENT)
        mat.InsertShader(DISP)
        
        DISP[c4d.DISPLACEMENT_INPUT] = IT
        DISP[c4d.DISPLACEMENT_AMOUNT] = 5
        DISP[c4d.DISPLACEMENT_MID] = 0.5
        DISP[c4d.DISPLACEMENT_LEVELOFDETAIL] = c4d.DISPLACEMENT_RES_8192
        
        # DISPACEMENT IMAGE NAMES = DISPACEMENT/DEPTH/HEIGHT
        IT[c4d.IMAGETEXTURE_FILE] = displacement
        IT[c4d.IMAGETEXTURE_MODE] = 1
        IT[c4d.IMAGETEXTURE_GAMMA] = 2.2
        IT[c4d.IMAGETEX_BORDER_MODE] = 0
        
        # TRANSFORM
        IT[c4d.IMAGETEXTURE_TRANSFORM_LINK] = TransN
        
        # TRANSFORM
        IT[c4d.IMAGETEXTURE_PROJECTION_LINK] = ProjN
        
        mat[c4d.OCT_MATERIAL_DISPLACEMENT_LINK] = DISP
    
# INDEX SETUP    
    mat[c4d.OCT_MATERIAL_INDEX] = 1.33    
    doc.InsertMaterial(mat)
    
    
 
# Dialog Setup
class OptionsDialog(gui.GeDialog):
  def CreateLayout(self):
    self.SetTitle('THE OCTANE MAT MAKER')
    
    # TITLE
    
    self.AddStaticText(LBL_INFO4, c4d.BFH_CENTER, name='')

    self.AddSeparatorH(130 ,c4d.BFH_CENTER)
    self.AddStaticText(LBL_INFO3, c4d.BFH_CENTER, name='Material Type', borderstyle = c4d.BORDER_WITH_TITLE_BOLD)
    self.AddSeparatorH(130 ,c4d.BFH_CENTER,)
    self.AddStaticText(LBL_INFO4, c4d.BFH_CENTER, name='')
    
    # DROP DOWN MATERIAL TYPE
    
    self.GroupBegin(GROUP_OPTIONS, c4d.BFH_CENTER, 2, 1)
    self.AddStaticText(LBL_INFO2, c4d.BFH_LEFT, name='Material Type')
    self.AddComboBox(DDM_MATTYPE, c4d.BFH_RIGHT, initw = 30)
    self.GroupEnd()
    
    # FOLDER SELECTION
    self.GroupBegin(GROUP_OPTIONS, c4d.BFH_SCALEFIT, 3, 1)
    self.AddStaticText(LBL_INFO1, c4d.BFH_LEFT, name='Folder') 
    self.editText = self.AddEditText(FOLDER_ADRESS, c4d.BFH_SCALEFIT)
    self.AddButton(BTN_COMA, c4d.BFH_RIGHT, name='...')
    self.GroupEnd()
    
    
    
    self.GroupBegin(GROUP_OPTIONS, c4d.BFH_CENTER, 3, 1)
    self.AddButton(BTN_OK, c4d.BFH_LEFT, name='OK')
    self.AddButton(BTN_CANCEL, c4d.BFH_CENTER, name='Cancel')
    self.GroupEnd()

    self.images = None
    self.file_path = None
    
    self.ok = False
    return True
 
  # React to user's input:
  def Command(self, id, msg):
    if id==BTN_CANCEL:
      self.Close()
    elif id ==BTN_OK:
    
      diffuse = None
      specular = None
      roughness = None
      normal = None
      bump = None
      opacity = None
      displacement = None
      
      if (self.file_path is None):
        self.file_path = self.GetString(FOLDER_ADRESS)
          
      self.images = os.listdir(self.file_path)
      
      for i in self.images:
        print i
        if 'diffuse' in i.lower() or 'color' in i.lower() or 'col' in i.lower() or 'albedo' in i.lower():
          diffuse = '{}\{}'.format(self.file_path, i)
        if 'specular' in i.lower() or 'gloss' in i.lower():
          specular = '{}\{}'.format(self.file_path, i)
        if 'roughness' in i.lower():
          roughness = '{}\{}'.format(self.file_path, i)
        if 'normal' in i.lower() or 'nrm' in i.lower():
          normal = '{}\{}'.format(self.file_path, i)
        if 'bump' in i.lower():
          bump = '{}\{}'.format(self.file_path, i)
        if 'opacity' in i.lower() or 'alpha' in i.lower():
          opacity = '{}\{}'.format(self.file_path, i)
        if 'displacement' in i.lower() or 'disp' in i.lower() or 'depth' in i.lower():
          displacement = '{}\{}'.format(self.file_path, i)

      
      make_shader(diffuse, specular, roughness, normal, bump, opacity, displacement)    
      c4d.EventAdd()    
      
      self.Close()
      
    elif id==BTN_COMA:
      self.ok = True
      self.file_path = c4d.storage.LoadDialog(flags=c4d.FILESELECT_DIRECTORY) and c4d.storage.LoadDialog(flags=c4d.FILESELECT_DIRECTORY) or ''
      print self.file_path
      self.SetString(FOLDER_ADRESS,self.file_path)

     
    return True

class CommandDataDialog(plugins.CommandData):

    dialog = None

    def Execute(self, doc):
        if self.dialog is None: self.dialog = OptionsDialog()
        return self.dialog.Open(dlgtype=c4d.DLG_TYPE_ASYNC, pluginid=PLUGIN_ID, defaultw=400, defaulth=100)
    def RestoreLayout(self, sec_ref):
        if self.dialog is None: self.dialog = OptionsDialog()
        return self.dialog.Restore(pluginid=PLUGIN_ID, secret=sec_ref)

#This is where the magic happens
def main():

  # Open the options dialogue to let users choose their options.
  # dlg = OptionsDialog()
  # dlg.Open(c4d.DLG_TYPE_ASYNC, defaultw=400, defaulth=100)
  # if not dlg.ok:
  #   return
 
  # c4d.EventAdd()  # Update C4D to see changes.
    bmp = bitmaps.BaseBitmap()
    dir, f = os.path.split(__file__)
    fn = os.path.join(dir, "OctaneMAT_Genrator.tif")
    bmp.InitWith(fn)
    plugins.RegisterCommandPlugin(id=PLUGIN_ID, 
                                  str="OMG",
                                  info=0,
                                  help="Octane mat Generator", 
                                  dat=CommandDataDialog(),
                                  icon=bmp)
 
if __name__=='__main__':
  main()