#Author-
#Description-

import adsk.core, adsk.cam, traceback
import adsk.fusion
import os

#Default values
ask_ss = False

def run(context):
           
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        def export_stl(component, output_path):
            output_path = os.path.join(path, filename)
            output_path = output_path + ".stl"
            export_mgr = design.exportManager
            stl_options = export_mgr.createSTLExportOptions(component, output_path)
            export_mgr.execute(stl_options)
            return
        
        def screenshot(file,name):
            #Isolate
            #file.rootComp.allOccurrences
            # parent = file.parentComponent
            # parent.activate()
            #file.isIsolated = True
            app.activeViewport.goHome()
            app.activeViewport.fit()
            out = os.path.join(name + "/"+ directory)
        
            app.activeViewport.saveAsImageFile(out, 400, 400);
            #file.isIsolated = False
            return
        
        #ask for folder
        dlg = ui.createFolderDialog()
        dlg.title = "Select a folder to export to"
        dialog_result = dlg.showDialog()
        if dialog_result == adsk.core.DialogResults.DialogOK:
            selected_folder = dlg.folder
            # Process the selected folder
            print("Selected folder:", selected_folder)
        else:
            # User canceled the dialog
            print("Folder selection canceled by user")
            return
        if ask_ss == True:
            ss_result = ui.messageBox(
              "Add screenshot?",
                "Export Objects",
                adsk.core.MessageBoxButtonTypes.YesNoCancelButtonType,
                adsk.core.MessageBoxIconTypes.QuestionIconType,
            )
        else:
            ss_result= False
        #try to create folder
        #parent_dir = "C:/Users/RishiKrishna/Desktop/anil/plugin/folder"
        design = adsk.fusion.Design.cast(app.activeProduct)
        Name = design.parentDocument.name 
        directory = Name
        path = os.path.join(selected_folder, directory) 
        if not os.path.exists(path):
            os.makedirs(path)
            #ui.messageBox("Directory '% s' created" % path) 
        
        # Get the active design
        product = app.activeProduct
        #design = adsk.fusion.FusionDocument.cast(product)
        design = adsk.fusion.Design.cast(app.activeProduct)
        if not design:
            ui.messageBox('No active Fusion 360 design', 'No Design')
        #getting all the components
#############################################################################

        design = adsk.fusion.Design.cast(product)
        rootComp = design.rootComponent
         
        for body in rootComp.bRepBodies:
            parentname = body.parentComponent
            parentname=parentname.name
            if rootComp.bRepBodies.count==1:
                filename = parentname
            else:
                filename = parentname+"_"+body.name
            export_stl(body, filename)
            if ss_result == adsk.core.DialogResults.DialogYes: 
                screenshot(body, filename) 

        for i in range(0, rootComp.allOccurrences.count):
            occ = rootComp.allOccurrences.item(i)
            bodies = occ.component.bRepBodies
            for body in bodies:
                parentname = body.parentComponent
                parentname=parentname.name
                if bodies.count==1:
                    filename = parentname
                else:
                    filename = parentname+"_"+body.name
                export_stl(body, filename)
                if ss_result == adsk.core.DialogResults.DialogYes: 
                    screenshot(occ, filename)

                # if not body.isVisible:
                #     continue
        screenshot(occ, path)
        ui.messageBox("STL files saved successfully.")
    except:
            if ui:
                ui.messageBox("Failed:\n{}".format(traceback.format_exc()))
