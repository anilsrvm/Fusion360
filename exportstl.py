#Author-
#Description-

import adsk.core, adsk.cam, traceback
import adsk.fusion
import os

    


def run(context):
    
        
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
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
        ss_result = ui.messageBox(
            "Add screenshot?",
            "Export Objects",
            adsk.core.MessageBoxButtonTypes.YesNoCancelButtonType,
            adsk.core.MessageBoxIconTypes.QuestionIconType,
        )
        if ss_result == adsk.core.DialogResults.DialogCancel:
             return 
        #try to create folder
        #parent_dir = "C:/Users/RishiKrishna/Desktop/anil/plugin/folder"
        directory = "assembly"
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
        components = design.allComponents
        
        i=0
        for component in components:
                # Activate the component
                design.activateRootComponent
                # Generate a unique filename for the component
                filename = component.name + ".stl"
                #filename = product.name+component.name + ".stl"
                output_path = os.path.join(path, filename)
                # Save the component as an STL file
                export_mgr = design.exportManager
                stl_options = export_mgr.createSTLExportOptions(component, output_path)
                export_mgr.execute(stl_options)
                if ss_result == adsk.core.DialogResults.DialogYes: 
                    #Isolate
                    rootComp = design.activeComponent
                    occ1 = rootComp.allOccurrences.item(i)
                    occ1.isIsolated = True
component.isIsolated = True
                    app.activeViewport.saveAsImageFile(output_path, 400, 400);
                    #ui.messageBox('Component 1 isloated. It will be unisolated on OK')
                    occ1.isIsolated = False
                i=i+1
        ui.messageBox("STL files saved successfully.")
    except:
            if ui:
                ui.messageBox("Failed:\n{}".format(traceback.format_exc()))
