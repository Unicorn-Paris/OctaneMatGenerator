# Create Octane Material from file folder by texture name
 
import c4d, os
from c4d import gui
 
# Unique id numbers for each of the GUI elements

# Labels 1
LBL_INFO1 = 1000
LBL_INFO2 = 1001
LBL_INFO3 = 1002
LBL_INFO4 = 1003
LBL_INFO5 = 1004
LBL_INFO6 = 1005
LBL_INFO7 = 1006
LBL_INFO8 = 1007

# Groups 2
GR_MAIN = 2001
GR_FOLDER_ADRESS = 2002

GR_FLUSH = 2003
GR_TEXDEF_L = 2004
GR_TEXDEF_R = 2005

GR_LOAD_BTN = 2006

GR_DDM = 2007

GR_IN_FLUSH = 2008

GR_TEXDEF = 2009

GR_TEXDEF_BTN = 2010

#Edit fields 3
FOLDER_ADRESS = 10001
INDEX = 10003

DIFFUSE_FIELD = 10010
SPECULAR_FIELD = 10011
ROUGHNESS_FIELD = 10012
BUMP_FIELD = 10013
NORMAL_FIELD = 10014

DSPLACEMENT_FIELD = 10020
OPACITY_FIELD = 10021
INDEX_FIELD = 10022
EMISSION_FIELD = 10023
MEDIUM_FIELD = 10024

# Buttons 4
BTN_LOAD_AND_CREATE = 4001
BTN_CANCEL = 4002
BTN_COMA = 4003
BTN_LOAD = 4004
BTN_CREATE_MAT = 4005
BTN_RELOAD = 4006

# Drop down menu 5
DDM_MATTYPE = 30040


# Octane Plugin ID
ID_OCTANE_DIFFUSE_MATERIAL = 1029501
ID_CREATE_GLOSSYMAT_PLUGIN = 1033893
ID_OCTANE_IMAGE_TEXTURE = 1029508
ID_OCTANE_DISPLACEMENT = 1031901
ID_OCTANE_TRANSFORM = 1030961
ID_OCTANE_PROJECTION = 1031460

diffuse = None
specular = None
roughness = None
normal = None
bump = None
opacity = None
displacement = None
index = None


class Shader():
  diffuse = None
  specular = None
  roughness = None
  normal = None
  bump = None
  opacity = None
  displacement = None
  index = None
    


def make_shader(shader, name,index,mat_type):
    print('shader name: {}'.format(name))
    doc = c4d.documents.GetActiveDocument()
    mat = c4d.BaseMaterial(ID_OCTANE_DIFFUSE_MATERIAL)

    #DEFINE MATERIAL TYPE

    mat[c4d.OCT_MATERIAL_TYPE] = mat_type
    mat[c4d.ID_BASELIST_NAME] = name 
    
    # TRANSFORM NODE
    TransN = c4d.BaseShader(ID_OCTANE_TRANSFORM)
    mat.InsertShader(TransN)
    
    # PROJECTION NODE
    ProjN = c4d.BaseShader(ID_OCTANE_PROJECTION)
    mat.InsertShader(ProjN)
    
    # DIFFUSE SETUP
    if shader.diffuse :
        IT = c4d.BaseShader(ID_OCTANE_IMAGE_TEXTURE)
        mat.InsertShader(IT)
        mat[c4d.OCT_MATERIAL_DIFFUSE_LINK] = IT
        # DIFFUSE IMAGE NAMES = Albedo/Col/Color
        IT[c4d.IMAGETEXTURE_FILE] = shader.diffuse
        IT[c4d.IMAGETEXTURE_MODE] = 0
        IT[c4d.IMAGETEXTURE_GAMMA] = 2.2
        IT[c4d.IMAGETEX_BORDER_MODE] = 0
        
        # TRANSFORM
        IT[c4d.IMAGETEXTURE_TRANSFORM_LINK] = TransN
        
        # TRANSFORM
        IT[c4d.IMAGETEXTURE_PROJECTION_LINK] = ProjN        

    # SPECULAR SETUP
    if shader.specular :
        IT = c4d.BaseShader(ID_OCTANE_IMAGE_TEXTURE)
        mat.InsertShader(IT)
        mat[c4d.OCT_MATERIAL_SPECULAR_LINK] = IT
        # SPECULAR IMAGE NAMES = Specular/Gloss
        IT[c4d.IMAGETEXTURE_FILE] = shader.specular
        IT[c4d.IMAGETEXTURE_MODE] = 1
        IT[c4d.IMAGETEXTURE_GAMMA] = 2.2
        IT[c4d.IMAGETEX_BORDER_MODE] = 0
        
        # TRANSFORM
        IT[c4d.IMAGETEXTURE_TRANSFORM_LINK] = TransN
        
        # TRANSFORM
        IT[c4d.IMAGETEXTURE_PROJECTION_LINK] = ProjN

    # ROUGHNESS SETUP
    if shader.roughness :
        IT = c4d.BaseShader(ID_OCTANE_IMAGE_TEXTURE)
        mat.InsertShader(IT)
        mat[c4d.OCT_MATERIAL_ROUGHNESS_LINK] = IT
        # ROUGHNESS IMAGE NAMES = Roughness/
        IT[c4d.IMAGETEXTURE_FILE] = shader.roughness
        IT[c4d.IMAGETEXTURE_MODE] = 1
        IT[c4d.IMAGETEXTURE_GAMMA] = 2.2
        IT[c4d.IMAGETEX_BORDER_MODE] = 0
        
        # TRANSFORM
        IT[c4d.IMAGETEXTURE_TRANSFORM_LINK] = TransN
        
        # TRANSFORM
        IT[c4d.IMAGETEXTURE_PROJECTION_LINK] = ProjN
    
    # NORMAL SETUP
    if shader.normal:
        IT = c4d.BaseShader(ID_OCTANE_IMAGE_TEXTURE)
        mat.InsertShader(IT)
        mat[c4d.OCT_MATERIAL_NORMAL_LINK] = IT
        # NORMAL IMAGE NAMES = Normal/NRM
        IT[c4d.IMAGETEXTURE_FILE] = shader.normal
        IT[c4d.IMAGETEXTURE_MODE] = 0
        IT[c4d.IMAGETEXTURE_GAMMA] = 2.2
        IT[c4d.IMAGETEX_BORDER_MODE] = 0
        
        # TRANSFORM
        IT[c4d.IMAGETEXTURE_TRANSFORM_LINK] = TransN
        
        # TRANSFORM
        IT[c4d.IMAGETEXTURE_PROJECTION_LINK] = ProjN
        
    else :
        if shader.bump:
            IT = c4d.BaseShader(ID_OCTANE_IMAGE_TEXTURE)
            mat.InsertShader(IT)
            mat[c4d.OCT_MATERIAL_BUMP_LINK] = IT
            # NORMAL IMAGE NAMES = BUMP
            IT[c4d.IMAGETEXTURE_FILE] = shader.bump
            IT[c4d.IMAGETEXTURE_MODE] = 1
            IT[c4d.IMAGETEXTURE_GAMMA] = 2.2
            IT[c4d.IMAGETEX_BORDER_MODE] = 0
            
            # TRANSFORM
            IT[c4d.IMAGETEXTURE_TRANSFORM_LINK] = TransN
        
            # TRANSFORM
            IT[c4d.IMAGETEXTURE_PROJECTION_LINK] = ProjN
    
    # OPACITY SETUP
    if shader.opacity:
        IT = c4d.BaseShader(ID_OCTANE_IMAGE_TEXTURE)
        mat.InsertShader(IT)
        mat[c4d.OCT_MATERIAL_OPACITY_LINK] = IT
        # OPACITY IMAGE NAMES = ALPHA/OPACITY/TRANSPARENCY
        IT[c4d.IMAGETEXTURE_FILE] = shader.opacity
        IT[c4d.IMAGETEXTURE_MODE] = 1
        IT[c4d.IMAGETEXTURE_GAMMA] = 2.2
        IT[c4d.IMAGETEX_BORDER_MODE] = 0
        
        # TRANSFORM
        IT[c4d.IMAGETEXTURE_TRANSFORM_LINK] = TransN
        
        # TRANSFORM
        IT[c4d.IMAGETEXTURE_PROJECTION_LINK] = ProjN

    # DISPLACEMENT SETUP
    if shader.displacement:
        IT = c4d.BaseShader(ID_OCTANE_IMAGE_TEXTURE)
        mat.InsertShader(IT)
        DISP = c4d.BaseShader(ID_OCTANE_DISPLACEMENT)
        mat.InsertShader(DISP)
        
        DISP[c4d.DISPLACEMENT_INPUT] = IT
        DISP[c4d.DISPLACEMENT_AMOUNT] = 5
        DISP[c4d.DISPLACEMENT_MID] = 0.5
        DISP[c4d.DISPLACEMENT_LEVELOFDETAIL] = c4d.DISPLACEMENT_RES_8192
        
        # DISPACEMENT IMAGE NAMES = DISPACEMENT/DEPTH/HEIGHT
        IT[c4d.IMAGETEXTURE_FILE] = shader.displacement
        IT[c4d.IMAGETEXTURE_MODE] = 1
        IT[c4d.IMAGETEXTURE_GAMMA] = 2.2
        IT[c4d.IMAGETEX_BORDER_MODE] = 0
        
        mat[c4d.OCT_MATERIAL_DISPLACEMENT_LINK] = DISP
        
        # TRANSFORM
        IT[c4d.IMAGETEXTURE_TRANSFORM_LINK] = TransN
        
        # TRANSFORM
        IT[c4d.IMAGETEXTURE_PROJECTION_LINK] = ProjN
    
    # INDEX SETUP    
    mat[c4d.OCT_MATERIAL_INDEX] = index    
    doc.InsertMaterial(mat)
    
def UpdateLayout (self, shader):

      #Texture Liste
      self.LayoutFlushGroup(id=GR_FLUSH)
      self.GroupBorder(c4d.BORDER_GROUP_IN)
      self.GroupBorderSpace(10, 0, 10, 0)

      self.GroupBegin(GR_IN_FLUSH, c4d.BFH_SCALEFIT,1,2)

      # DROP DOWN MATERIAL TYPE
        #STYLE    
      self.GroupBegin(GR_DDM, c4d.BFV_SCALEFIT|c4d.BFH_SCALEFIT, 2, 1,)
      self.GroupBorder(c4d.BORDER_NONE)
      self.GroupBorderSpace(10, 5, 10, 10)
    
      #CONTENT
      self.AddStaticText(LBL_INFO2, c4d.BFH_LEFT|c4d.BFV_TOP, name='Material Type')
      self.AddComboBox(DDM_MATTYPE, c4d.BFH_LEFT, initw = 80)
            #ComboBox CONTENT
      self.AddChild(DDM_MATTYPE, 0, 'Glossy')
      self.AddChild(DDM_MATTYPE, 1, 'Diffuse')
      self.AddChild(DDM_MATTYPE, 2, 'Specular')
    
      self.GroupEnd()

      self.GroupBegin(GR_TEXDEF, c4d.BFH_SCALEFIT)

    #GR_L
      self.GroupBegin(GR_TEXDEF_L, c4d.BFH_LEFT, 2,5)
      self.GroupBorderSpace(10, 5, 10, 5)

      self.AddStaticText(1006,c4d.BFH_LEFT, name='Diffuse :')
      self.editText = self.AddEditText(DIFFUSE_FIELD, c4d.BFH_SCALEFIT, initw = 300)
      if shader.diffuse:
        self.SetString(DIFFUSE_FIELD, shader.diffuse)

      self.AddStaticText(1006,c4d.BFH_LEFT, name='Specular :')
      self.editText = self.AddEditText(SPECULAR_FIELD, c4d.BFH_SCALEFIT, initw = 300)
      if shader.specular:
        self.SetString(SPECULAR_FIELD, shader.specular)

      self.AddStaticText(1006,c4d.BFH_LEFT, name='Roughness :')
      self.editText = self.AddEditText(ROUGHNESS_FIELD, c4d.BFH_SCALEFIT, initw = 300)
      if shader.roughness:
        self.SetString(ROUGHNESS_FIELD, shader.roughness)

      self.AddStaticText(1006,c4d.BFH_LEFT, name='Bump :')
      self.editText = self.AddEditText(BUMP_FIELD, c4d.BFH_SCALEFIT, initw = 300)
      if shader.bump:
        self.SetString(BUMP_FIELD, shader.bump)

      self.AddStaticText(1006,c4d.BFH_LEFT, name='Normal :')
      self.editText = self.AddEditText(NORMAL_FIELD, c4d.BFH_SCALEFIT, initw = 300)
      if shader.normal:
        self.SetString(NORMAL_FIELD, shader.normal)

      self.GroupEnd()

    #GR_R
      self.GroupBegin(GR_TEXDEF_R, c4d.BFH_RIGHT, 2,5)
      self.GroupBorderSpace(10, 5, 10, 5)


      self.AddStaticText(1006,c4d.BFH_LEFT, name='Displacement :')
      self.editText = self.AddEditText(DSPLACEMENT_FIELD, c4d.BFH_SCALEFIT, initw = 300)
      if shader.displacement:
        self.SetString(DSPLACEMENT_FIELD,shader.displacement)

      self.AddStaticText(1006,c4d.BFH_LEFT, name='Opacity :')
      self.editText = self.AddEditText(OPACITY_FIELD, c4d.BFH_SCALEFIT, initw = 300)
      if shader.opacity:
        self.SetString(OPACITY_FIELD,shader.opacity)

      
      self.AddStaticText(1006,c4d.BFH_LEFT, name='Index :')
      self.AddEditSlider(INDEX_FIELD,c4d.BFH_SCALEFIT,80,0)
      self.SetFloat(INDEX_FIELD, 1.33, min = 1, max = 8, step=0.001, format=c4d.FORMAT_FLOAT )

      self.AddStaticText(1006,c4d.BFH_LEFT, name='Emission :')
      self.editText = self.AddEditText(EMISSION_FIELD, c4d.BFH_SCALEFIT, initw = 300)
      # self.SetString(EMISSION_FIELD,emission)

      self.AddStaticText(1006,c4d.BFH_LEFT, name='Medium :')
      self.editText = self.AddEditText(MEDIUM_FIELD, c4d.BFH_SCALEFIT, initw = 300)
      # self.SetString(MEDIUM_FIELD,medium)

      self.GroupEnd()

      self.GroupEnd()

    # BTN GROUP
      self.GroupBegin(GR_TEXDEF_BTN,c4d.BFH_CENTER,2,1)
      self.GroupBorderSpace(5, 5, 5, 10)
      self.AddButton(BTN_CREATE_MAT,c4d.BFH_CENTER, name='Create Material')
      self.AddButton(BTN_RELOAD,c4d.BFH_CENTER, name='Reload')
      self.GroupEnd()

      self.LayoutChanged(id=GR_FLUSH)            
      return True
 
# Dialog
class OptionsDialog(gui.GeDialog):
      
  def CreateLayout(self):
    id == 0
    self.SetTitle('THE OCTANE MAT MAKER')
    
    # MEGA GROUP BEGIN------------------------------------------------------------------------------------------
    self.GroupBegin(GR_MAIN, c4d.BFH_SCALEFIT, 1,2)
    self.GroupBorderNoTitle(c4d.BORDER_NONE)
    self.GroupBorderSpace(10, 10, 10, 10)
    
    # TITLE
    
    self.AddSeparatorH(130 ,c4d.BFH_CENTER)
    self.AddStaticText(LBL_INFO3, c4d.BFH_CENTER, name='Material Type', borderstyle = c4d.BORDER_WITH_TITLE_BOLD)
    self.AddSeparatorH(130 ,c4d.BFH_CENTER,)
    
    # DROP DOWN MATERIAL TYPE
        #STYLE    
    #self.GroupBegin(GROUP_OPTIONS, c4d.BFV_SCALEFIT|c4d.BFH_SCALEFIT, 2, 2,title="Material Setup" ,)
    #self.GroupBorder(c4d.BORDER_GROUP_IN)
    #self.GroupBorderSpace(10, 10, 10, 10)
    #
        #CONTENT
    #self.AddStaticText(LBL_INFO2, c4d.BFH_LEFT|c4d.BFV_TOP, name='Material Type')
    #self.AddComboBox(DDM_MATTYPE, c4d.BFH_LEFT|c4d.BFV_TOP|c4d.BFH_SCALEFIT, initw = 80)
            #ComboBox CONTENT
    #self.AddChild(DDM_MATTYPE, 0, 'Diffuse')
    #self.AddChild(DDM_MATTYPE, 1, 'Glossy')
    #self.AddChild(DDM_MATTYPE, 2, 'Specular')
    
   
    #
    #self.GroupEnd()
    #
    
    
    # FOLDER SELECTION
    self.GroupBegin(GR_FOLDER_ADRESS, c4d.BFH_SCALEFIT|c4d.BFV_BOTTOM , 3, 1)
    self.GroupBorderSpace(0, 10, 0, 5)
    self.AddStaticText(LBL_INFO1, c4d.BFH_LEFT, name='Folder') 
    self.editText = self.AddEditText(FOLDER_ADRESS, c4d.BFH_SCALEFIT)
    self.AddButton(BTN_COMA, c4d.BFH_RIGHT, name='...')
    self.GroupEnd()
    
    #GroupVide
    self.GroupBegin(GR_FLUSH,c4d.BFH_SCALEFIT,2,1,title='Texture selection')
    #self.GroupBorder(c4d.BORDER_NONE)
    #self.GroupBorderSpace(10, 0, 10, 0)

    self.GroupEnd()
    #GroupeVide End
    
    self.GroupBegin(GR_LOAD_BTN, c4d.BFH_CENTER, 3, 1)
    self.GroupBorderSpace(0, 5, 0, 5)
    self.AddButton(BTN_LOAD, c4d.BFH_LEFT, name='Load')
    self.AddButton(BTN_LOAD_AND_CREATE, c4d.BFH_CENTER, name='Load & Creat Mat')
    self.AddButton(BTN_CANCEL, c4d.BFH_RIGHT, name='Cancel')
    self.GroupEnd()
    
    #MEGA GROUP END$------------------------------------------------------------------------------
    self.GroupEnd()

    self.images = None
    self.file_path = None
    
    self.ok = False
    return True
 
  # React to user's input:
  def Command(self, id, msg):
    if id == DDM_MATTYPE:
      self.GetLong(DDM_MATTYPE)
      if self.GetLong(30040) == 0:
        for id in [10010, 10012,10013,10014,10020,10021,10023,10024]:
          self.Enable(id, True)
        for id in [10011,10022]:
          self.Enable(id, True)

      if self.GetLong(30040) == 1:
        for id in [10010, 10012,10013,10014,10020,10021,10023,10024]:
          self.Enable(id, True)
        for id in [10011, 10022]:
          self.Enable(id, False)
      
      if self.GetLong(30040) == 2:
        gui.MessageDialog('OctaneMatGenerator doesn`t support specular material yet :)')
        self.SetLong(30040, 0)
        #self.UpdateLayout(0)
        for id in [10010, 10012,10013,10014,10020,10021,10023,10024]:
          self.Enable(id, True)
        for id in [10011,10022]:
          self.Enable(id, True)

      return True
            
    
    if id == BTN_CANCEL:
      print '{}'.format(self.file_path)
      self.Close()
      return True


    elif id == BTN_LOAD_AND_CREATE:
      index = self.GetFloat(INDEX_FIELD)
      
      if (self.file_path is None):
        self.file_path = self.GetString(FOLDER_ADRESS)
          
      if not os.path.exists(self.file_path):
        gui.MessageDialog('The system cannot find the path specified')
        return True
          
      self.images = os.listdir(self.file_path)

      shader = Shader()
      
      for filename in list(map(lambda j: j.lower(), self.images)):
        lowered_filename = filename.lower()
        absolute_filename = os.path.join(self.file_path, filename)
        if 'diffuse' in lowered_filename or 'color' in lowered_filename or 'col' in lowered_filename or 'albedo' in lowered_filename:
          shader.diffuse = absolute_filename
        if 'specular' in lowered_filename or 'gloss' in lowered_filename:
          shader.specular = absolute_filename
        if 'roughness' in lowered_filename:
          shader.roughness = absolute_filename
        if 'normal' in lowered_filename or 'nrm' in lowered_filename:
          shader.normal = absolute_filename
        if 'bump' in lowered_filename:
          shader.bump = absolute_filename
        if 'opacity' in lowered_filename or 'alpha' in lowered_filename:
          shader.opacity = absolute_filename
        if 'displacement' in lowered_filename or 'disp' in lowered_filename or 'depth' in lowered_filename:
          shader.displacement = absolute_filename

      make_shader(shader, os.path.basename(self.file_path) ,index,2511)    
      c4d.EventAdd()    
      self.Close()
      return True
    

    elif id == BTN_LOAD or id == BTN_RELOAD:
      self.file_path = self.GetString(FOLDER_ADRESS)
        
      if not os.path.exists(self.file_path):
        gui.MessageDialog('The system cannot find the path specified')
        return True
        
      self.images = os.listdir(self.file_path)
      
      shader = Shader()

      for filename in self.images:
        lowered_filename = filename.lower()
        if 'diffuse' in lowered_filename or 'color' in lowered_filename or 'col' in lowered_filename or 'albedo' in lowered_filename:
          shader.diffuse = filename
        if 'specular' in lowered_filename or 'gloss' in lowered_filename:
          shader.specular = filename
        if 'roughness' in lowered_filename:
          shader.roughness = filename
        if 'normal' in lowered_filename or 'nrm' in lowered_filename:
          shader.normal = filename
        if 'bump' in lowered_filename:
          shader.bump = filename
        if 'opacity' in lowered_filename or 'alpha' in lowered_filename:
          shader.opacity = filename
        if 'displacement' in lowered_filename or 'disp' in lowered_filename or 'depth' in lowered_filename:
          shader.displacement = filename
  
      
      UpdateLayout (self, shader)
      return True


    elif id == BTN_COMA:
      self.ok = True
      self.file_path = c4d.storage.LoadDialog(flags=c4d.FILESELECT_DIRECTORY) and c4d.storage.LoadDialog(flags=c4d.FILESELECT_DIRECTORY) or ''
      self.SetString(FOLDER_ADRESS,self.file_path)
      return True


    elif id == BTN_CREATE_MAT:
      self.ok = True


      if self.GetLong(30040) == 0:
        mat_type = 2511
      if self.GetLong(30040) == 1:
        mat_type = 2510

      shader = Shader()

      if not self.GetString(DIFFUSE_FIELD) == '':
        shader.diffuse = os.path.join(self.file_path,self.GetString(DIFFUSE_FIELD))
      if not self.GetString(SPECULAR_FIELD) == '':
        shader.specular = os.path.join(self.file_path,self.GetString(SPECULAR_FIELD))
      if not self.GetString(ROUGHNESS_FIELD) == '':
        shader.roughness = os.path.join(self.file_path,self.GetString(ROUGHNESS_FIELD))
      if not self.GetString(NORMAL_FIELD) == '':
        shader.normal = os.path.join(self.file_path,self.GetString(NORMAL_FIELD))
      if not self.GetString(BUMP_FIELD) == '':
        shader.bump = os.path.join(self.file_path,self.GetString(BUMP_FIELD))
      if not self.GetString(OPACITY_FIELD) == '':
        shader.opacity = os.path.join(self.file_path,self.GetString(OPACITY_FIELD))
      if not self.GetString(DSPLACEMENT_FIELD) == '':
        shader.displacement = os.path.join(self.file_path,self.GetString(DSPLACEMENT_FIELD))
      index = self.GetFloat(INDEX_FIELD)

      make_shader(shader, os.path.basename(self.file_path) ,index,mat_type) 
      self.Close()

      return True

    else:
      return True

#This is where the action happens
def main():

  dlg = OptionsDialog()
  
 
  # Open the options dialogue to let users choose their options.  
  dlg.Open(c4d.DLG_TYPE_MODAL, defaultw=400, defaulth=10)
  if not dlg.ok:
    return
 
  c4d.EventAdd()  # Update C4D to see changes.
 
if __name__=='__main__':
  main()