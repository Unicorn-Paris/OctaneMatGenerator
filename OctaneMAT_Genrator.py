# Simple script for doing a Find/Replace over all selected object names.
 
import c4d, os
from c4d import gui
 
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
INDEX = 10003
GROUP_OPTIONS = 20000
GROUP_TEST = 20001

BTN_OK = 20001
BTN_CANCEL = 20002
BTN_COMA = 20003

DDM_MATTYPE = 30040



ID_OCTANE_DIFFUSE_MATERIAL = 1029501
ID_CREATE_GLOSSYMAT_PLUGIN = 1033893
ID_OCTANE_IMAGE_TEXTURE = 1029508
ID_OCTANE_DISPLACEMENT = 1031901

def make_shader(diffuse, specular, roughness, normal, bump, opacity, displacement):
    doc = c4d.documents.GetActiveDocument()
    mat = c4d.BaseMaterial(ID_OCTANE_DIFFUSE_MATERIAL)

#DEFINE MATERIAL TYPE
    mat()[c4d.OCT_MATERIAL_TYPE]=2511
    
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
        
        mat[c4d.OCT_MATERIAL_DISPLACEMENT_LINK] = DISP
    
# INDEX SETUP    
    mat[c4d.OCT_MATERIAL_INDEX] = 1.33    
    doc.InsertMaterial(mat)
    
 
# Dialog for renaming objects
class OptionsDialog(gui.GeDialog):
    
  
  def UpdateLayout (self, id,):
      if id==0:
          self.LayoutFlushGroup(id=20001)
          self.AddStaticText(1006,c4d.BFH_LEFT, name='Diffuse')
      if id==1:
          self.LayoutFlushGroup(id=20001)
          self.AddStaticText(1006,c4d.BFH_LEFT, name='Index')
          self.AddEditSlider(INDEX,c4d.BFH_SCALEFIT,80,0)
          self.SetFloat(INDEX, 1.33, min = 1, max = 8, step=0.001, format=c4d.FORMAT_FLOAT )
      if id==2:
          self.LayoutFlushGroup(id=20001)
          self.AddStaticText(1006,c4d.BFH_LEFT, name='Diffuse')
      #
      self.LayoutChanged(id=GROUP_TEST)            
      return True
    
    
  def CreateLayout(self):
    id == 0
    self.SetTitle('THE OCTANE MAT MAKER')
    
# MEGA GROUP BEGIN------------------------------------------------------------------------------------------
    self.GroupBegin(GROUP_OPTIONS, c4d.BFH_SCALEFIT, 1,2)
    self.GroupBorderNoTitle(c4d.BORDER_NONE)
    self.GroupBorderSpace(10, 10, 10, 10)
    
    # TITLE
    
    self.AddSeparatorH(130 ,c4d.BFH_CENTER)
    self.AddStaticText(LBL_INFO3, c4d.BFH_CENTER, name='Material Type', borderstyle = c4d.BORDER_WITH_TITLE_BOLD)
    self.AddSeparatorH(130 ,c4d.BFH_CENTER,)
    self.AddStaticText(LBL_INFO4, c4d.BFH_CENTER, name='')
    
    # DROP DOWN MATERIAL TYPE
        #STYLE    
    self.GroupBegin(GROUP_OPTIONS, c4d.BFV_SCALEFIT|c4d.BFH_SCALEFIT, 2, 2,title="Material Setup" ,)
    self.GroupBorder(c4d.BORDER_GROUP_IN)
    self.GroupBorderSpace(10, 10, 10, 10)
    
        #CONTENT
    self.AddStaticText(LBL_INFO2, c4d.BFH_LEFT|c4d.BFV_TOP, name='Material Type')
    self.AddComboBox(DDM_MATTYPE, c4d.BFH_LEFT|c4d.BFV_TOP|c4d.BFH_SCALEFIT, initw = 80)
            #ComboBox CONTENT
    self.AddChild(DDM_MATTYPE, 0, 'Diffuse')
    self.AddChild(DDM_MATTYPE, 1, 'Glossy')
    self.AddChild(DDM_MATTYPE, 2, 'Specular')
    
    self.GroupBegin(GROUP_TEST,c4d.BFH_LEFT,2)
    self.GroupBorder(c4d.BORDER_NONE)
    self.GroupBorderSpace(10, 0, 10, 0)
    #GroupVide
    self.GroupEnd()
    
    
    self.GroupEnd()
    
    
    
    # FOLDER SELECTION
    self.GroupBegin(GROUP_OPTIONS, c4d.BFH_SCALEFIT|c4d.BFV_BOTTOM , 3, 1)
    self.AddStaticText(LBL_INFO1, c4d.BFH_LEFT, name='Folder') 
    self.editText = self.AddEditText(FOLDER_ADRESS, c4d.BFH_SCALEFIT)
    self.AddButton(BTN_COMA, c4d.BFH_RIGHT, name='...')
    self.GroupEnd()
    
    
    
    self.GroupBegin(GROUP_OPTIONS, c4d.BFH_CENTER, 3, 1)
    self.AddButton(BTN_OK, c4d.BFH_LEFT, name='OK')
    self.AddButton(BTN_CANCEL, c4d.BFH_CENTER, name='Cancel')
    self.GroupEnd()
    
#MEGA GROUP END$------------------------------------------------------------------------------
    self.GroupEnd()

    self.images = None
    self.file_path = None
    
    self.ok = False
    return True
 
  # React to user's input:
  def Command(self, id, msg):
    #print id 
    #print msg
    
    if id == DDM_MATTYPE:
        self.UpdateLayout(self.GetLong(DDM_MATTYPE))
        #print dir(msg)
        #print msg.GetData()
        self.GetLong(DDM_MATTYPE)
        if self.GetLong(30040) == 0:
            print 'Diffuse'
        if self.GetLong(30040) == 1:
            print 'Glossy'
        if self.GetLong(30040) == 2:
            gui.MessageDialog('OctaneMatGenerator doesn`t support specular material yet :)')
            self.SetLong(30040, 0)
            self.UpdateLayout(0)
            print 'Specular'
        
            
    
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
 
#This is where the action happens
def main():

  dlg = OptionsDialog()
  
 
  # Open the options dialogue to let users choose their options.  
  dlg.Open(c4d.DLG_TYPE_MODAL, defaultw=400, defaulth=300)
  if not dlg.ok:
    return
 
  c4d.EventAdd()  # Update C4D to see changes.
 
if __name__=='__main__':
  main()